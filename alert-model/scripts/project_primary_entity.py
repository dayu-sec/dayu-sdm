#!/usr/bin/env python3
"""primary_entity_* 统一派生参考实现（alert-model/docs/02-alert-fields.md §3）。

从 observation.assertion.victim[]/affected[]/attacker[] 与 subject/object 收集候选，
`python3 project_primary_entity.py` 跑内置用例。
"""
from __future__ import annotations

import re
import sys
from typing import Any, Optional

# ── §3.3 排序表 ──────────────────────────────────────────────────────────────
ROLE_RANK = {"victim": 0, "affected": 1, "attacker": 2, "related": 3}
TYPE_RANK = {"host": 0, "user": 1, "account": 2, "service": 3, "ip": 4, "domain": 5}
HINT_RANK = {"assertion": 0, "object": 1, "subject": 2}
# ip/domain 为全局域，其余（含未列类型）为租户域（§3.4）
GLOBAL_PREFIX_TYPES = {"ip", "domain"}

# §3.2 占位值：去首尾空白、去值内空白、小写后比较
PLACEHOLDER_VALUES = {"", "0.0.0.0", "内网ip范围", "unknown", "-", "::", "0:0:0:0:0:0:0:0"}

IP_PORT_RE = re.compile(r"^(.+):\d{1,5}$")

# 事件 16 值 entity_type 中参与映射的 9 值；其余（device/resource/application/
# cloud/container/certificate/script）不映射，跳过（§3.1 映射表）
SUPPORTED_EVENT_TYPES = {
    "endpoint", "host", "user", "account", "process",
    "file", "domain", "url", "service",
}


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
    if m:
        raw = m.group(1)
    try:
        import ipaddress
        return str(ipaddress.ip_address(raw))
    except ValueError:
        return None


# ── §3.1 候选收集 ────────────────────────────────────────────────────────────

def _cand(role: str, etype: str, value: str, hint: str = "") -> dict:
    return {"alert_entity_role": role, "entity_type": etype,
            "entity_value": str(value).strip(), "event_role_hint": hint}


def _typed_value(node: dict) -> Optional[tuple[str, str]]:
    """typed entity → (告警 entity_type, 值)；不支持/无值返回 None（§3.1 映射表）。"""
    node = node or {}
    etype = node.get("entity_type")
    if etype not in SUPPORTED_EVENT_TYPES:
        return None

    def val(*path: str) -> Optional[str]:
        cur: Any = node
        for p in path:
            cur = (cur or {}).get(p) if isinstance(cur, dict) else None
        v = str(cur).strip() if cur is not None else ""
        return v if v and not is_placeholder(v) else None

    if etype == "endpoint":
        ip = parse_ip(val("endpoint", "ip") or "")
        if not ip:  # 兜底：typed object 缺失时从 ref_id 尾段取
            ip = parse_ip(str(node.get("ref_id") or "").split("::")[-1])
        return ("ip", ip) if ip else None
    if etype == "host":
        name = val("host", "name")
        if name:
            return ("host", name)
        ip = parse_ip(val("host", "ip") or "")
        return ("ip", ip) if ip else None  # §3.2：host 仅 IP 值降级 ip
    if etype == "user":
        v = val("user", "name")
        return ("user", v) if v else None
    if etype == "account":
        v = val("account", "name")
        return ("account", v) if v else None
    if etype == "process":
        v = val("process", "name")
        return ("process", v) if v else None
    if etype == "service":
        v = val("service", "name")
        return ("service", v) if v else None
    if etype == "domain":
        v = val("domain", "name")
        return ("domain", v.lower()) if v else None
    if etype == "file":
        v = val("file", "path") or val("file", "name")
        return ("file", v) if v else None
    if etype == "url":
        v = val("url", "full")
        return ("url", v) if v else None
    return None


def collect_candidates(event: dict) -> list[dict]:
    """按 §3.1 候选链收集（C1→C4）；observation.observer 不参与。"""
    assertion = ((event.get("observation") or {}).get("assertion")) or {}
    out: list[dict] = []

    # C1 设备明确声明的受害方
    for row in assertion.get("victim") or []:
        tv = _typed_value(row)
        if tv:
            out.append(_cand("victim", tv[0], tv[1], "assertion"))

    # C2 声明的受影响实体
    for row in assertion.get("affected") or []:
        tv = _typed_value(row)
        if tv:
            out.append(_cand("affected", tv[0], tv[1], "assertion"))

    # C3 观测受影响方（观测角色不得自动升格 victim）
    tv = _typed_value(event.get("object"))
    if tv:
        out.append(_cand("affected", tv[0], tv[1], "object"))

    # C4 攻击方：声明优先，subject 兜底
    for row in assertion.get("attacker") or []:
        tv = _typed_value(row)
        if tv:
            out.append(_cand("attacker", tv[0], tv[1], "assertion"))
    tv = _typed_value(event.get("subject"))
    if tv:
        out.append(_cand("attacker", tv[0], tv[1], "subject"))

    return [c for c in out
            if c["entity_type"] not in ("", "product")
            and not is_placeholder(c["entity_value"])]



# ── §3.2 过滤纠正 + §3.3 排序 + §3.4 输出 ──────────────────────────────────

def _fix_type(c: dict) -> dict:
    """host 仅存 IP 值、无主机名凭证时降级 ip。（_typed_value 已内联处理，保留钩子。）"""
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


# ── 内置用例（行为信封形态；python3 直接运行即自检） ─────────────────────────

def _selftest() -> int:
    tenant = "t01"
    cases = []

    # 1. WAF 穿透（action=detect、无声明）：object 是受影响资产——不得选攻击者
    waf = {
        "subject": {"ref_id": "endpoint::198.51.100.19", "entity_type": "endpoint",
                    "endpoint": {"ip": "198.51.100.19"}},
        "object": {"ref_id": "endpoint::198.51.100.240", "entity_type": "endpoint",
                   "endpoint": {"ip": "198.51.100.240"}},
        "observation": {"action": "detect",
                        "assertion": {"title": "SQLi attempt", "conclusion": "deny"}},
    }
    r = project_primary_entity(waf, tenant)
    cases.append(("waf object 优先于攻击者", r and r["primary_entity_value"] == "198.51.100.240"
                  and r["primary_entity_role"] == "affected"
                  and r["primary_entity_id"] == "ip:198.51.100.240", r))

    # 2. 设备声明受害方：assertion.victim[] 压过 object
    declared = {
        "object": {"entity_type": "endpoint", "endpoint": {"ip": "198.51.100.91"}},
        "observation": {"action": "detect", "assertion": {"victim": [
            {"ref_id": "host::portal-web-01", "entity_type": "host",
             "host": {"name": "portal-web-01"}}]}},
    }
    r = project_primary_entity(declared, tenant)
    cases.append(("声明受害方 host 优先", r and r["primary_entity_type"] == "host"
                  and r["primary_entity_role"] == "victim"
                  and r["primary_entity_id"] == f"host:{tenant}:portal-web-01", r))

    # 7. object ref_id 带端口 → 去端口归 ip（同分 affected 下 type_rank ip<domain）
    ported = {
        "object": {"ref_id": "endpoint::203.0.113.9:8443", "entity_type": "endpoint"},
        "observation": {"action": "assess", "assertion": {"affected": [
            {"ref_id": "domain::Evil.Example.COM", "entity_type": "domain",
             "domain": {"name": "Evil.Example.COM"}}]}},
    }
    r = project_primary_entity(ported, tenant)
    cases.append(("object ref_id 去端口归 ip（type_rank 压过声明 domain）",
                  r and r["primary_entity_type"] == "ip"
                  and r["primary_entity_value"] == "203.0.113.9", r))

    # 7b. domain 唯一候选 → 小写 + 全局域 id
    dom_only = {
        "observation": {"action": "detect", "assertion": {"affected": [
            {"entity_type": "domain", "domain": {"name": "Evil.Example.COM"}}]}},
    }
    r = project_primary_entity(dom_only, tenant)
    cases.append(("声明 affected domain 小写",
                  r and r["primary_entity_value"] == "evil.example.com"
                  and r["primary_entity_id"] == "domain:evil.example.com", r))
    ph = {
        "object": {"entity_type": "endpoint", "endpoint": {"ip": "0.0.0.0"}},
        "subject": {"entity_type": "endpoint", "endpoint": {"ip": "内网IP范围"}},
    }
    r = project_primary_entity(ph, tenant)
    cases.append(("占位值 → NULL 兜底", r is None, r))

    # 4. host 仅 IP 值（无主机名凭证）→ 降级 ip
    host_ip = {"object": {"entity_type": "host", "host": {"ip": "198.51.100.93"}}}
    r = project_primary_entity(host_ip, tenant)
    cases.append(("host 仅 IP 值降级 ip", r and r["primary_entity_type"] == "ip"
                  and r["primary_entity_value"] == "198.51.100.93"
                  and r["primary_entity_role"] == "affected", r))

    # 5. 无声明、无 object，只有 subject → attacker 兜底（排序最后，合法）
    only_src = {"subject": {"entity_type": "endpoint", "endpoint": {"ip": "203.0.113.30"}}}
    r = project_primary_entity(only_src, tenant)
    cases.append(("仅 subject → attacker 兜底", r and r["primary_entity_role"] == "attacker", r))

    # 6. agency 保护：有 attacker[] 声明时，声明的攻击方压过 subject 兜底
    agency = {
        "subject": {"entity_type": "endpoint", "endpoint": {"ip": "203.0.113.162"}},
        "observation": {"action": "detect", "assertion": {"attacker": [
            {"entity_type": "endpoint", "endpoint": {"ip": "192.0.2.213:443"}}]}},
    }
    r = project_primary_entity(agency, tenant)
    cases.append(("声明攻击方压过 subject（且去端口）",
                  r and r["primary_entity_role"] == "attacker"
                  and r["primary_entity_value"] == "192.0.2.213", r))


    # 8. 未映射类型（resource/script 等）不产生候选
    unmapped = {"object": {"entity_type": "resource", "resource": {"name": "db-01"}}}
    r = project_primary_entity(unmapped, tenant)
    cases.append(("未映射 entity_type 跳过 → NULL", r is None, r))

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
