#!/usr/bin/env python3
"""primary_entity_* 统一派生参考实现（alert-model/docs/02-alert-fields.md §3）。

规则与接入映射不填写 primary_entity_* 四列，也不重复实现本算法；
告警写入服务照此实现，从触发事件的 roles / source_finding 派生。

输入：触发事件的五层逻辑对象（dict，键 roles / source_finding，物理表为
roles_obj / source_finding_obj）。输出：主表四列 + is_primary 实体行，
无合格候选时返回 None（合法兜底）。

纯函数、无副作用、无第三方依赖。`python3 project_primary_entity.py` 跑内置用例。
"""
from __future__ import annotations

import ipaddress
import re
import sys
from typing import Any, Optional

# ── §3.3 排序表 ──────────────────────────────────────────────────────────────
ROLE_RANK = {"victim": 0, "affected": 1, "attacker": 2, "indicator": 3, "related": 4}
TYPE_RANK = {"host": 0, "user": 1, "account": 2, "service": 3, "ip": 4, "domain": 5}
HINT_RANK = {"target": 0, "source": 1, "related": 2}
# ip/domain 为全局域，其余（含未列类型）为租户域（§3.4）
GLOBAL_PREFIX_TYPES = {"ip", "domain"}

# §3.2 占位值：去首尾空白、去值内空白、小写后比较
PLACEHOLDER_VALUES = {"", "0.0.0.0", "内网ip范围", "unknown", "-", "::", "0:0:0:0:0:0:0:0"}

IP_PORT_RE = re.compile(r"^(.+):\d{1,5}$")


def _norm(v: Any) -> str:
    return re.sub(r"\s+", "", str(v or "")).lower()


def is_placeholder(v: Any) -> bool:
    return _norm(v) in PLACEHOLDER_VALUES


def parse_ip(value: str) -> Optional[str]:
    """合法 IP 返回规范值（去端口）；不是 IP 返回 None。"""
    raw = str(value or "").strip()
    if not raw:
        return None
    m = IP_PORT_RE.match(raw)
    candidate = m.group(1) if m else raw
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None


# ── §3.1 候选收集 ────────────────────────────────────────────────────────────

def _cand(role: str, etype: str, value: str, hint: str = "") -> dict:
    return {"alert_entity_role": role, "entity_type": etype,
            "entity_value": str(value).strip(), "event_role_hint": hint}


def _endpoint_candidates(node: dict, role: str, hint: str) -> list[dict]:
    out = []
    ep = (node or {}).get("endpoint") or {}
    for key in ("ip", "ipv4", "ipv6"):
        ip = parse_ip(ep.get(key, ""))
        if ip:
            out.append(_cand(role, "ip", ip, hint))
    host = ((node or {}).get("host") or {}).get("name")
    if host and not is_placeholder(host):
        out.append(_cand(role, "host", str(host).strip(), hint))
    user = (node or {}).get("user") or {}
    for key in ("uid", "name"):
        v = user.get(key)
        if v and not is_placeholder(v):
            out.append(_cand(role, "user", str(v).strip(), hint))
            break
    acct = ((node or {}).get("account") or {}).get("name")
    if acct and not is_placeholder(acct):
        out.append(_cand(role, "account", str(acct).strip(), hint))
    return out


def _indicator_candidates(finding: dict) -> list[dict]:
    out = []
    ioc = finding.get("ioc") or finding.get("indicators") or []
    if isinstance(ioc, str):
        ioc = [ioc]
    for item in ioc:
        value = item if isinstance(item, str) else (item or {}).get("value") or (item or {}).get("id")
        if not value or is_placeholder(value):
            continue
        value = str(value).strip()
        ip = parse_ip(value)
        if ip:
            out.append(_cand("indicator", "ip", ip))
        elif "." in value:
            out.append(_cand("indicator", "domain", value))
    return out


def collect_candidates(event: dict) -> list[dict]:
    """按 §3.1 候选链收集（C1→C5）；observer 不参与。"""
    roles = event.get("roles") or {}
    finding = event.get("source_finding") or {}
    out: list[dict] = []

    # C1 设备明确声明的受害方
    victim = finding.get("victim") or {}
    out += _endpoint_candidates({"endpoint": victim.get("endpoint")}, "victim", "")
    res_name = (victim.get("resource") or {}).get("name")
    if res_name and not is_placeholder(res_name):
        out.append(_cand("victim", "host", str(res_name).strip()))

    # C2 声明的关联实体
    entities = finding.get("entities") or {}
    for key, role in (("victims", "victim"), ("affected", "affected")):
        for row in entities.get(key) or []:
            ref = (row or {}).get("ref_id")
            etype = (row or {}).get("entity_type")
            if not ref or is_placeholder(ref):
                continue
            if etype == "endpoint":
                ip = parse_ip(ref.split("::")[-1])
                out.append(_cand(role, "ip" if ip else "related", ip or ref))
            else:
                out.append(_cand(role, str(etype or "related"), ref))

    # C3 观测受影响方（观测角色不得自动升格 victim）
    out += _endpoint_candidates(roles.get("target"), "affected", "target")

    # C4 攻击方（仅当 C1–C3 无候选时才可能成为主对象，由排序自然保证）
    attacker = finding.get("attacker") or {}
    out += _endpoint_candidates({"endpoint": attacker.get("endpoint")}, "attacker", "")
    out += _endpoint_candidates(roles.get("source"), "attacker", "source")

    # C5 指标兜底
    out += _indicator_candidates(finding)

    return [c for c in out
            if c["alert_entity_role"] != "observer"
            and c["entity_type"] not in ("", "product")
            and not is_placeholder(c["entity_value"])]


# ── §3.2 过滤纠正 + §3.3 排序 + §3.4 输出 ──────────────────────────────────

def _fix_type(c: dict) -> dict:
    """host 仅存 IP 值、无主机名凭证时降级 ip。"""
    if c["entity_type"] == "host" and parse_ip(c["entity_value"]):
        c = dict(c, entity_type="ip")
    return c


def _sort_key(c: dict) -> tuple:
    return (
        ROLE_RANK.get(c["alert_entity_role"], 9),
        TYPE_RANK.get(c["entity_type"], 9),
        HINT_RANK.get(c.get("event_role_hint") or "", 9),
        c["entity_value"],
    )


def entity_id(entity_type: str, tenant_id: str, value: str) -> str:
    """§3.4 前缀：ip/domain 全局域 {type}:{value}；其余租户域 {type}:{tenant}:{value}。"""
    if entity_type in GLOBAL_PREFIX_TYPES:
        return f"{entity_type}:{value}"
    return f"{entity_type}:{tenant_id}:{value}"


def project_primary_entity(event: dict, tenant_id: str) -> Optional[dict]:
    """返回主表四列 + is_primary 实体行；无合格候选返回 None。"""
    cands = [_fix_type(c) for c in collect_candidates(event)]
    if not cands:
        return None
    best = min(_sort_key(c) for c in cands)
    chosen = sorted(cands, key=_sort_key)[0]
    return {
        "primary_entity_id": entity_id(chosen["entity_type"], tenant_id, chosen["entity_value"]),
        "primary_entity_type": chosen["entity_type"],
        "primary_entity_value": chosen["entity_value"],
        "primary_entity_role": chosen["alert_entity_role"],
        "_primary_row": dict(chosen, is_primary=True),
        "_sort_key": list(best),
    }


# ── 内置用例（真实穿透告警形态；python3 直接运行即自检） ─────────────────────

def _selftest() -> int:
    tenant = "t01"
    cases = []

    # 1. WAF 穿透告警：只有观测方向，dst 是受影响资产——不得选攻击者
    waf = {"roles": {
        "source": {"entity_type": "endpoint", "endpoint": {"ip": "198.51.100.19"}},
        "target": {"entity_type": "endpoint", "endpoint": {"ip": "198.51.100.240"}},
    }}
    r = project_primary_entity(waf, tenant)
    cases.append(("waf dst 优先于攻击者", r and r["primary_entity_value"] == "198.51.100.240"
                  and r["primary_entity_role"] == "affected"
                  and r["primary_entity_id"] == "ip:198.51.100.240", r))

    # 2. 设备声明受害方：source_finding.victim 压过 roles.target
    declared = {"roles": {"target": {"endpoint": {"ip": "198.51.100.91"}}},
                "source_finding": {"victim": {"resource": {"name": "portal-web-01"}}}}
    r = project_primary_entity(declared, tenant)
    cases.append(("声明受害方 host 优先", r and r["primary_entity_type"] == "host"
                  and r["primary_entity_role"] == "victim"
                  and r["primary_entity_id"] == f"host:{tenant}:portal-web-01", r))

    # 3. 占位值全被剔除 → 四列 NULL
    ph = {"roles": {"target": {"endpoint": {"ip": "0.0.0.0"}},
                    "source": {"endpoint": {"ip": "内网IP范围"}}}}
    r = project_primary_entity(ph, tenant)
    cases.append(("占位值 → NULL 兜底", r is None, r))

    # 4. host 挂 IP 值 → 降级 ip
    host_ip = {"roles": {"target": {"host": {"name": "198.51.100.93"},
                                    "endpoint": {"ip": "0.0.0.0"}}}}
    r = project_primary_entity(host_ip, tenant)
    cases.append(("host 字段挂 IP 值降级 ip", r and r["primary_entity_type"] == "ip"
                  and r["primary_entity_value"] == "198.51.100.93"
                  and r["primary_entity_role"] == "affected", r))
    mis_ref = {"source_finding": {"entities": {"victims": [
        {"ref_id": "host_target_01", "entity_type": "host"}]}}}
    r = project_primary_entity(mis_ref, tenant)
    cases.append(("声明实体 ref_id 非裸 IP 按声明类型保留", r and r["primary_entity_type"] == "host", r))


    # 5. 只有攻击方 → attacker 兜底（合法，但排序最后）
    only_src = {"roles": {"source": {"endpoint": {"ip": "203.0.113.30"}}}}
    r = project_primary_entity(only_src, tenant)
    cases.append(("仅攻击方 → attacker 兜底", r and r["primary_entity_role"] == "attacker", r))

    # 6. ioc 带端口 IP → 去端口归 ip
    ioc = {"source_finding": {"ioc": ["192.0.2.213:443", "evil.example.com"]}}
    r = project_primary_entity(ioc, tenant)
    cases.append(("ioc 指标兜底", r and r["primary_entity_type"] == "ip"
                  and r["primary_entity_value"] == "192.0.2.213", r))

    failed = 0
    for name, ok, detail in cases:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            failed += 1
            print(f"      got: {detail}")
    print(f"\n{len(cases) - failed}/{len(cases)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_selftest())
