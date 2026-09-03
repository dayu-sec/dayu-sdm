#!/usr/bin/env python3
"""Build the Dayu-SDM GitHub Pages set.

Generates from authoritative sources under log-model/ and alert-model/:
  - pages/index.html          (landing, from templates/index.html)
  - pages/log-standard.html   (log standard, from templates/log-standard.html)
  - pages/alert-standard.html (from templates/alert-standard.html)

Re-run after the source catalogs, examples, or the review page change:
  python3 pages/build/build_pages.py
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]

DELIV = ROOT / "log-model"
ALERT_TEMPLATE = Path(__file__).resolve().parent / "templates" / "alert-standard.html"
BUILD = ROOT / "pages"
TEMPLATES = Path(__file__).resolve().parent / "templates"

DOC_MAIN = DELIV / "docs" / "main"
PROJECTION_REGISTRY = DELIV / "contracts" / "hybrid-event" / "projection-registry.v1.json"
RAW_LOG_SQL = DELIV / "schema" / "006_raw_log.sql"
CHANGES_FILE = Path(__file__).resolve().parent / "changes.json"
EXAMPLES = DELIV / "examples"

# ─────────────────────────── markdown table parsing ───────────────────────────

def split_row(line: str) -> list[str]:
    parts = line.strip().strip("|").split("|")
    return [p.strip() for p in parts]


def is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c) and any(cells)


def strip_ticks(s: str) -> str:
    return s.replace("`", "").strip()


def parse_numbered_table(text: str, ncols: int, merge_into: int) -> list[list[str]]:
    """Parse markdown rows like `| 1 | a | b |`. Extra cells merged into column `merge_into`."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if not cells or is_sep_row(cells):
            continue
        if not cells[0].isdigit():
            continue
        if len(cells) > ncols:
            extra = cells[ncols - 1:merge_into + 1] if merge_into >= ncols else []
            # merge overflow into the designated column
            keep = cells[:ncols]
            over = cells[ncols:]
            keep[merge_into] = " | ".join([keep[merge_into]] + over)
            cells = keep
        if len(cells) != ncols:
            continue
        rows.append(cells)
    return rows


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    parts = re.split(r"^## ", text, flags=re.M)
    for part in parts[1:]:
        title, _, body = part.partition("\n")
        out[title.strip()] = body
    return out


# ─────────────────────────── source parsers ───────────────────────────

def parse_physical() -> list[dict]:
    """Physical columns from the retired-era 04 catalog, kept only when the
    current projection-registry still carries the column (the 04 doc itself is
    frozen history; the registry decides what is live)."""
    text = (DOC_MAIN / "04-sdm-event-doris-field-catalog.md").read_text(encoding="utf-8")
    registry = json.loads(PROJECTION_REGISTRY.read_text(encoding="utf-8"))
    live_paths = {item["path"] for item in registry["columns"]}
    variant_columns = {meta["physical_column"] for meta in registry["variant_objects"].values()}
    rows = parse_numbered_table(text, ncols=6, merge_into=4)
    out = []
    for n, name, typ, path, sample, desc in rows:
        if strip_ticks(path) not in live_paths and strip_ticks(name) not in variant_columns:
            continue
        out.append(dict(
            n=len(out) + 1, name=strip_ticks(name), type=strip_ticks(typ),
            path=strip_ticks(path), sample=strip_ticks(sample), desc=desc.strip(),
        ))
    return out


def parse_logical() -> tuple[list[dict], dict[str, int]]:
    """Flatten the M1 behavior-contract schema (07) into logical field rows.

    Rows are (layer, path, type, cardinality, required, sample, meaning); the
    layer is the top-level segment (meta / behavior / subject / ...)."""
    schema = json.loads((DOC_MAIN / "07-sdm-event-behavior.schema.json").read_text(encoding="utf-8"))
    out: list[dict] = []

    def resolve(node: dict) -> dict:
        while "$ref" in node:
            name = node["$ref"].split("/")[-1]
            merged = dict(schema["$defs"][name])
            merged.update({k: v for k, v in node.items() if k != "$ref"})
            node = merged
        return node

    def type_label(node: dict) -> str:
        if "enum" in node:
            vals = node["enum"]
            return "enum(" + "、".join(map(str, vals[:3])) + ("…" if len(vals) > 3 else "") + ")"
        if "const" in node:
            return f"const({node['const']})"
        t = node.get("type")
        if isinstance(t, list):
            return "/".join("null" if x is None else str(x) for x in t)
        if t == "object":
            return "object" if node.get("properties") else "开放对象"
        return str(t or "any")


    def _sample_of(node: dict) -> str:
        if "const" in node:
            return str(node["const"])
        if "enum" in node:
            vals = [v for v in node["enum"] if v is not None]
            return str(vals[0]) if vals else "—"
        if node.get("type") == ["string", "null"] or node.get("type") == "string":
            return "文本"
        return "—"

    # required marking: re-walk with parent-required context
    def walk2(props: dict, required: list, prefix: str, layer: str) -> None:
        for key, raw in props.items():
            node = resolve(raw)
            path = f"{prefix}{key}"
            is_req = key in required
            if node.get("type") == "array":
                item = resolve(node.get("items", {}))
                if item.get("properties"):
                    walk2(item["properties"], item.get("required", []), f"{path}[].", layer)
                else:
                    append_row(node, path + "[]", "多值", layer, is_req)
                continue
            if node.get("properties"):
                walk2(node["properties"], node.get("required", []), path + ".", layer)
                continue
            append_row(node, path, "单值", layer, is_req)

    def append_row(node: dict, path: str, card: str, layer: str, is_req: bool) -> None:
        out.append(dict(
            n=len(out) + 1, layer=layer, path=path,
            type=type_label(node), card=card, req="Y" if is_req else "N",
            sample=_sample_of(node), meaning=(node.get("description") or "—").strip(),
        ))


    def emit_role_slot(raw_node: dict, prefix: str, layer: str, extra_keys: tuple[str, ...] = ()) -> None:
        node = resolve(raw_node)
        props = node.get("properties", {})
        keys = ("ref_id", "entity_type") + extra_keys
        identity = {k: props[k] for k in keys if k in props}
        req = [k for k in node.get("required", []) if k in identity]
        walk2(identity, req, prefix, layer)
        n_types = {"subject": 16, "object": 16, "carriers": 8, "observation": 9}[layer]
        append_row(
            {"type": "object",
             "description": f"与 entity_type 同名的属性对象，{n_types} 选 1；内部字段见「对象类型」视图（object-fields.v1）"},
            f"{prefix}<type>", "单值", layer, False,
        )

    walk2(schema["properties"]["meta"]["properties"],
          schema["properties"]["meta"].get("required", []), "meta.", "meta")
    append_row(schema["properties"]["event_kind"], "event_kind", "单值", "event_kind", True)
    walk2(schema["properties"]["behavior"]["properties"],
          schema["properties"]["behavior"].get("required", []), "behavior.", "behavior")
    emit_role_slot(schema["properties"]["subject"], "subject.", "subject")
    emit_role_slot(schema["properties"]["object"], "object.", "object")
    emit_role_slot(schema["properties"]["carriers"]["items"], "carriers[].", "carriers",
                   extra_keys=("carrier_role",))
    for dom, dom_node in schema["properties"]["facets"]["properties"].items():
        out.append(dict(n=len(out) + 1, layer="facets", path=f"facets.{dom}",
                        type="开放对象", card="单值", req="N",
                        sample="—", meaning=(dom_node.get("description") or "领域行为上下文；字段经注册表治理（M2）").strip()))
    obs = schema["properties"]["observation"]
    obs_props = {k: v for k, v in obs["properties"].items() if k != "observer"}
    walk2(obs_props, [k for k in obs.get("required", []) if k != "observer"],
          "observation.", "observation")
    emit_role_slot(obs["properties"]["observer"], "observation.observer.", "observation")
    walk2(schema["properties"]["extensions"]["properties"],
          schema["properties"]["extensions"].get("required", []), "extensions.", "extensions")

    counts: dict[str, int] = {}
    for row in out:
        counts[row["layer"]] = counts.get(row["layer"], 0) + 1
    return out, counts


OBJECT_FIELDS = DELIV / "contracts" / "hybrid-event" / "object-fields.v1.json"


def object_types() -> list[dict]:
    """16 entity_type cards from the registered object-fields contract (M2)."""
    data = json.loads(OBJECT_FIELDS.read_text(encoding="utf-8"))
    out = []
    for t in data["entity_types"]:
        roles = ["subject", "object"]
        if t["carrier"]:
            roles.append("carriers[]")
        if t["observer"]:
            roles.append("observer")
        out.append(dict(
            type=t["type"], title=t["title"], roles=roles, status="registered",
            fields=[dict(name=f["name"], meaning=f["meaning"]) for f in t["fields"]],
            notes=t["notes"],
        ))
    return out


def assertion_fields() -> dict:
    data = json.loads(OBJECT_FIELDS.read_text(encoding="utf-8"))
    return dict(fields=[dict(name=f["name"], meaning=f["meaning"], **{"from": f["from"]})
                        for f in data["assertion"]["fields"]])



BEHAVIOR_SCHEMA = DOC_MAIN / "07-sdm-event-behavior.schema.json"
CONTRACT_CATALOG = ROOT / "docs" / "SDM事件模型逻辑契约字段目录.md"

# facets 页面主题组：(domains, 组名, 标题, 一句判别)
FACET_THEMES = [
    (("network",), "network", "连接与流量",
     "direction、session_id、packet_metadata；协议与会话不进 carriers，地址属于主体/客体对象。"),
    (("http", "dns"), "http · dns", "Web 与解析",
     "HTTP 请求 / 响应与域名解析应答；按行为上下文归组，不按设备类型。"),
    (("email",), "email", "邮件",
     "from、recipients[]、attachments[]、subject；收发双方身份在 subject / object。"),
    (("process",), "process", "进程与注入",
     "ancestry[] 创建链、注入细节等；进程身份在 subject / carriers 的 process 对象，此处只放行为细节。"),
    (("authentication",), "authentication", "认证与会话",
     "auth_type、auth_result、session_id；与 behavior.outcome 联动判别。"),
    (("registry",), "registry", "注册表",
     "key、value 与闭合枚举；文件实体经 subject / object 的 file 对象表达。"),
    (("application", "container"), "application · container", "应用与容器",
     "application.name 与 container / kubernetes 上下文；容器身份是 entity_type=container。"),
]


def facet_stats() -> dict:
    """Group the contract catalog's典型 facet paths (§2.8) into page theme
    groups; domains present in the schema but without登记 paths surface as
    reserved (M2 注册表登记后启用)."""
    schema = json.loads(BEHAVIOR_SCHEMA.read_text(encoding="utf-8"))
    registered = list(schema["properties"]["facets"]["properties"])

    text = CONTRACT_CATALOG.read_text(encoding="utf-8")
    leaves: dict[str, list[str]] = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*`(?P<path>facets\.[^`]+)`\s*\|", line)
        if not m:
            continue
        parts = m.group("path").split(".")
        dom = parts[1]
        leaf = parts[-1].replace("[]", "")
        if leaf not in leaves.setdefault(dom, []):
            leaves[dom].append(leaf)

    groups = []
    for domains, name, title, note in FACET_THEMES:
        group_leaves: list[str] = []
        for d in domains:
            for leaf in leaves.get(d, []):
                if leaf not in group_leaves:
                    group_leaves.append(leaf)
        groups.append(dict(
            name=name, title=title, note=note,
            count=sum(len(leaves.get(d, [])) for d in domains),
            fields=group_leaves[:6],
        ))
    themed = {d for domains, *_ in FACET_THEMES for d in domains}
    reserved = [dict(name=d, title=FACET_RESERVED.get(d, (d, "候选域；字段经注册表登记后启用"))[0],
                     note=FACET_RESERVED.get(d, (d, "候选域；字段经注册表登记后启用"))[1])
                for d in registered if d not in leaves and d not in themed]
    return dict(total=len(registered), active=len(leaves),
                groups=groups, reserved=reserved)

# facets 注册预留 domain 的页面卡片文案
FACET_RESERVED = {
    "database": ("数据库操作", "查询语句、库表与行数等数据库操作细节；启用前经映射评审。"),
    "tls": ("TLS 与证书", "协议版本、密码套件、证书与指纹（如 JA3）等握手细节。"),
    "file": ("文件行为", "文件操作细节；文件实体与身份经 subject / object 的 file 对象表达。"),
    "peripheral": ("外设接入", "USB、网卡等接入外设；来自 related 迁移字典 facets.peripheral.device。"),
    "cloud": ("云控制面", "云账号、区域与 API 动作等云上操作细节。"),
}




def parse_enums() -> tuple[list[dict], list[dict], list[list[str]]]:
    text = (DOC_MAIN / "06-sdm-event-enum-catalog.md").read_text(encoding="utf-8")
    sec = sections(text)
    simple: list[dict] = []
    event_dict: list[dict] = []
    non_enums: list[list[str]] = []
    for title, body in sec.items():
        lines = body.splitlines()
        intro = next((l for l in lines if l.strip()), "")
        if title == "事件类型与操作":
            rows = parse_numbered_table(body, ncols=6, merge_into=4)
            for n, typ, meaning, ops, op_meaning, status in rows:
                event_dict.append(dict(
                    n=int(n), type=strip_ticks(typ), meaning=meaning.strip(),
                    ops=ops.strip(), opMeaning=op_meaning.strip(), status=status.strip(),
                ))
            continue
        if title == "非枚举字段":
            for line in body.splitlines():
                if line.startswith("|"):
                    cells = split_row(line)
                    if is_sep_row(cells):
                        continue
                    if len(cells) >= 3:
                        non_enums.append([strip_ticks(cells[0]), cells[1].strip(), cells[2].strip()])
            continue
        if title == "写入规则":
            continue
        m = re.search(r"逻辑路径：(.+?)。(.*)", intro)
        path = strip_ticks(m.group(1)) if m else ""
        note = (m.group(2) if m else intro).strip()
        closed = "闭合枚举" in intro
        values: list[list[str]] = []
        for line in body.splitlines():
            if line.startswith("|"):
                cells = split_row(line)
                if is_sep_row(cells):
                    continue
                head = cells[0].strip()
                if head == "枚举值":
                    continue
                if head == "废弃值":  # 废弃值迁移映射表不是枚举值，到此为止
                    break
                if len(cells) >= 2:
                    values.append([strip_ticks(cells[0]), cells[1].strip()])
        if values:
            simple.append(dict(title=title, path=path, closed=closed, note=note, values=values))
    return simple, event_dict, non_enums


def rel_from_pages(p: Path) -> str:
    """Repo file path as referenced from HTML under pages/."""
    return "../" + p.relative_to(ROOT).as_posix()


def parse_coverage() -> dict:
    vendors = []
    for vdir in sorted(EXAMPLES.iterdir()):
        if not vdir.is_dir():
            continue
        types = [d for d in sorted(vdir.iterdir()) if d.is_dir()]
        if not types:
            continue
        vendors.append(dict(
            name=vdir.name,
            types=[dict(
                name=t.name,
                href=rel_from_pages(t),
            ) for t in types],
        ))
    n_types = sum(len(v["types"]) for v in vendors)
    return dict(vendors=vendors, nVendors=len(vendors), nTypes=n_types)


# ─────────────────────────── showcase examples ───────────────────────────

SHOWCASE = [
    dict(
        dir="examples/topas_waf/topas_waf_attack", prefix="runtime_observed",
        title="天融信 WAF · SQL 注入检测", tag="behavior+detect", tagClass="cyan",
        column="检出告警（behavior + detect）",
        steps=[
            ("1 定性", "event_kind / record_kind", "behavior / finding", "全部事件先判 event_kind=behavior；record_kind 降为 meta.source_record 兼容路由值"),
            ("2 身份", "meta.event_id / log_id / occur_time", "evt-dee1e370… / log-dee1e370… / 2026-01-23T11:00:00Z", "来源无独立 ID，log_id 与 event_id 同源；设备时间已转 UTC"),
            ("3 定型", "behavior.layer / type / operation", "network / read / http_request", "层次决定实体域：网络层 → 实体是 endpoint/domain；read 由取与移判据判定"),
            ("4 结果", "behavior.outcome", "denied", "WAF 是策略判定点 → 处置结果 denied；不与 success/failed 混用"),
            ("5 主体/客体", "subject / object", "客户端 endpoint → 受保护服务器", "subject=行为发起者，object=直接作用客体；不自动等于攻击者/受害者"),
            ("6 观察", "observation", "action=detect · assertion.title/severity · observer", "断言与 observer、evidence_refs 绑定，不反写事实层主体客体"),
            ("7 扩展", "extensions.source_private", "保留设备未映射字段", "装不下的原样保留，不丢数据"),
            ("8 自查", "迁移清单 §四/§六", "行为信封已重生成", "runtime_observed.expected-sdm-event.behavior.json 对齐 07 Schema；interim 物理 JSON 保留到 M4"),
        ],
    ),
    dict(
        dir="examples/sxf_probe/flow_dns", prefix="runtime_observed",
        title="深信服探针 · DNS 查询", tag="behavior", tagClass="green",
        column="网络流量（behavior）",
        steps=[
            ("1 定性", "event_kind / record_kind", "behavior / activity", "纯行为记录，无检测判定；observation 可省或 action=record"),
            ("2 身份", "meta.event_id / log_id / occur_time", "evt-f2ebaf11… / log-f2ebaf11… / 2025-05-22T12:30:11Z", "来源无独立 ID，log_id 与 event_id 同源；探针时间已转 UTC"),
            ("3 定型", "behavior.layer / type / operation", "network / flow / dns_query", "层次决定实体域：网络层 → 实体是 endpoint；查询名进 facets.dns.question，应答为空"),
            ("4 结果", "behavior.outcome", "observed", "qr=0 是请求、ancnt=0；rcode=0 不是执行成功"),
            ("5 主体/客体", "subject / object", "192.0.2.199:52040 → 192.0.2.123:53", "观测方向：客户端 → DNS 服务器；查询名不升第二类型"),
            ("6 观察", "observation", "action=record · observer=device", "样例无观察者 IP，不发明 device.ip；产品名留 data_source"),
            ("7 扩展", "extensions.source_private", "DNS 标志与未确认数字字典", "src/dst 不复写；丢弃 Questions FieldStorage 垃圾串"),
            ("8 自查", "迁移清单 §四/§六", "行为信封已重生成", "runtime_observed.expected-sdm-event.behavior.json 对齐 07 Schema；interim 物理 JSON 保留到 M4"),
        ],
    ),
    dict(
        dir="examples/tianqing/edr_process_event", prefix="process_creation",
        title="天擎 · 进程创建", tag="behavior", tagClass="green",
        column="终端审计（behavior）",
        steps=[
            ("1 定性", "event_kind / record_kind", "behavior / activity", "终端审计行为记录；同一 EDR 的告警日志走 detect 观察"),
            ("2 身份", "meta.event_id / log_id / occur_time", "evt-2555c859… / log-tianqing-process-creation-0001 / 2024-12-18T02:42:17.220Z", "来源有稳定 ID → log_id 用来源测试值，不改写成 event_id；毫秒时间已转 UTC"),
            ("3 定型", "behavior.layer / type / operation", "system / appear / spawn", "层次决定实体域：系统层 → 实体是 process/file；新进程出现 → appear；祖父进 facets.process.ancestry[]"),
            ("4 结果", "behavior.outcome", "observed", "行为无成败语义 → observed（事实记录）"),
            ("5 主体/客体", "subject / object / carriers[]", "svchost.exe → WmiPrvSE.exe；carriers=[]", "subject=创建者进程，object=新进程；父进程不重复进载体；execution_host 未决，终端进 profiles"),
            ("6 观察", "observation", "action=record", "EDR 只记录，无断言；assertion 不设置"),
            ("7 扩展", "extensions.source_private", "SID/完整性等未登记字段", "原样保留；不复写标准字段"),
            ("8 自查", "迁移清单 §四/§六", "行为信封已重生成", "process_creation.expected-sdm-event.behavior.json 对齐 07 Schema；interim 物理 JSON 保留到 M4"),
        ],
    ),
]

SHOWCASE_FOOTNOTE = (
    "例外样例：<a href='../log-model/examples/tianqing/edr_powershell_cmd_exec/' "
    "style='color:var(--acc)'>天擎 PowerShell 执行</a>——受控字典暂无脚本执行类型，暂用 generic_event；"
    "登记组合落地前不改判。三张展示卡均为行为信封；interim 物理 JSON 保留到 M4。"
)

STAGE_FILES = [
    ("raw", "raw-log.json", "raw-log"),
    ("wpl", "wpl-output.json", "wpl-output"),
    ("ctx", "platform-context.json", "platform-context"),
    ("event", "expected-sdm-event.json", "expected-sdm-event"),
]


def parse_showcase() -> list[dict]:
    out = []
    for cfg in SHOWCASE:
        exdir = DELIV / cfg["dir"]
        files = {}
        for key, suffix, _label in STAGE_FILES:
            p = exdir / f"{cfg['prefix']}.{suffix}"
            files[f"{key}Url"] = rel_from_pages(p)
            files[key] = p.read_text(encoding="utf-8")
        behavior = exdir / f"{cfg['prefix']}.expected-sdm-event.behavior.json"
        if behavior.exists():
            files["eventUrl"] = rel_from_pages(behavior)
            files["event"] = behavior.read_text(encoding="utf-8")
        out.append(dict(
            title=cfg["title"], tag=cfg["tag"], tagClass=cfg["tagClass"],
            column=cfg["column"], steps=cfg["steps"],
            href=rel_from_pages(exdir / "README.md"),
            files=files,
        ))
    return out


# ─────────────────────────── page assembly ───────────────────────────

def extract_base_css() -> str:
    html = ALERT_TEMPLATE.read_text(encoding="utf-8")
    m = re.search(r"<style>\n(.*?)</style>", html, flags=re.S)
    if not m:
        sys.exit("cannot extract base CSS from pages/build/templates/alert-standard.html")
    return m.group(1).rstrip() + "\n"




def build_log_page(base_css: str, data: dict, changes_html: str) -> str:
    tpl = (TEMPLATES / "log-standard.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = (tpl
           .replace("/*__BASE_CSS__*/", base_css)
           .replace("/*__DATA__*/", payload)
           .replace("__BUILD_DATE__", str(datetime.date.today()))
           .replace("<!--__CHANGES__-->", changes_html))
    return out


def build_landing(base_css: str, stats: dict) -> str:
    tpl = (TEMPLATES / "index.html").read_text(encoding="utf-8")
    out = (tpl
           .replace("/*__BASE_CSS__*/", base_css)
           .replace("__STAT_PHYSICAL__", str(stats["physical"]))
           .replace("__STAT_LOGICAL__", str(stats["logical"]))
           .replace("__STAT_VENDORS__", str(stats["vendors"]))
           .replace("__STAT_TYPES__", str(stats["types"]) + "+")
           .replace("__BUILD_DATE__", str(datetime.date.today())))
    return out


def render_changes(domain: str) -> str:
    data = json.loads(CHANGES_FILE.read_text(encoding="utf-8"))
    entries = sorted(data["entries"], key=lambda e: e["date"], reverse=True)
    entries = [e for e in entries if e["domain"] == domain]

    def item_html(e: dict) -> str:
        links = " · ".join(
            f'<a href="../{href}" style="color:var(--acc)">{label}</a>'
            for href, label in e.get("links", [])
        )
        return (
            '<div class="card reveal chg-item" style="margin-bottom:14px">'
            + f'<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px">'
            + f'<span class="tag cyan" style="margin:0">{e["date"]}</span>'
            + f'<span class="tag gray" style="margin:0">{e["type"]}</span></div>'
            + f'<h3 style="margin:0 0 6px">{e["title"]}</h3>'
            + f'<p style="margin:0 0 6px;color:var(--t2);font-size:14px">{e["desc"]}</p>'
            + f'<p style="margin:0 0 6px;color:var(--t3);font-size:13px"><b style="color:var(--t2)">影响：</b>{e["impact"]}</p>'
            + (f'<p style="margin:0;font-size:13px">{links}</p>' if links else "")
            + "</div>"
        )

    # group by version label, latest group first (by newest entry date)
    groups: dict[str, list] = {}
    for e in entries:
        groups.setdefault(e.get("version", "未版本化"), []).append(e)
    ordered = sorted(groups.items(), key=lambda kv: max(x["date"] for x in kv[1]), reverse=True)

    parts = []
    for version, items in ordered:
        count = len(items)
        parts.append(
            '<div class="card reveal" style="margin:26px 0 14px;padding:10px 16px;background:var(--acc-dim,#eef);border:1px solid var(--acc-line,#ccd)">'
            + f'<b style="color:var(--acc)">{version}</b>'
            + f'<span style="margin-left:10px;color:var(--t3);font-size:13px">{count} 项修订</span></div>'
        )
        parts.extend(item_html(e) for e in items)
    return "\n".join(parts) or '<div class="card reveal"><p>该域暂无修订记录。</p></div>'


def build_alert_page(changes_html: str) -> str:
    return ALERT_TEMPLATE.read_text(encoding="utf-8").replace("<!--__CHANGES__-->", changes_html)


# ─────────────────────────── validation ───────────────────────────

HREF_RE = re.compile(r'(?:href|src)="([^"#]+?)"')


def validate_links(page: Path) -> list[str]:
    text = page.read_text(encoding="utf-8")
    missing = []
    for target in HREF_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "data:", "overflow:")):
            continue
        if "'" in target or "+" in target:  # JS 模板拼接片段，非静态链接
            continue
        p = (page.parent / unquote(target).split("#")[0]).resolve()
        if not p.exists():
            missing.append(target)
    return missing


def main() -> None:
    physical = parse_physical()
    logical, layer_stats = parse_logical()
    enums, event_dict, non_enums = parse_enums()
    coverage = parse_coverage()
    showcase = parse_showcase()
    registry = json.loads(PROJECTION_REGISTRY.read_text(encoding="utf-8"))
    ddl = json.dumps(registry, ensure_ascii=False, indent=2)
    raw_ddl = RAW_LOG_SQL.read_text(encoding="utf-8")

    otypes = object_types()
    facets = facet_stats()
    assert len(physical) == 53, f"physical columns = {len(physical)}, expected 53"
    assert len(logical) >= 50, f"logical fields = {len(logical)}, expected >= 50 (07 envelope)"
    assert len(event_dict) == 105, f"event.type entries = {len(event_dict)}, expected 105"
    expected_layers = {"meta", "event_kind", "behavior", "subject", "object",
                       "carriers", "facets", "observation", "extensions"}
    assert set(layer_stats) == expected_layers, layer_stats
    assert len(otypes) == 16, len(otypes)
    assert facets["total"] == 15 and facets["active"] == 5, facets

    stats = dict(
        physical=len(physical), logical=len(logical),
        vendors=coverage["nVendors"], types=coverage["nTypes"],
        layerCounts=layer_stats, facets=facets,
        dictEntries=len(event_dict), objectTypes=len(otypes),
    )
    data = dict(
        stats=stats, physical=physical, logical=logical,
        enums=enums, eventDict=event_dict, nonEnums=non_enums,
        coverage=dict(vendors=coverage["vendors"]),
        examples=showcase, objectTypes=otypes, assertion=assertion_fields(),
        examplesFootnote=SHOWCASE_FOOTNOTE, ddl=ddl, rawDdl=raw_ddl,
    )
    base_css = extract_base_css()

    pages = {
        BUILD / "log-standard.html": build_log_page(base_css, data, render_changes("日志")),
        BUILD / "index.html": build_landing(base_css, stats),
        BUILD / "alert-standard.html": build_alert_page(render_changes("告警")),
    }
    for path, content in pages.items():
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1024:.1f} KB)")

    # 校验：残留标记 & 相对链接可达
    problems = []
    for path in pages:
        text = path.read_text(encoding="utf-8")
        for marker in ("__BASE_CSS__", "__DATA__", "__BUILD_DATE__",
                       "__STAT_PHYSICAL__", "__STAT_LOGICAL__", "__STAT_VENDORS__", "__STAT_TYPES__",
                       "__CHANGES__"):
            if marker in text:
                problems.append(f"{path.name}: marker {marker} not replaced")
        for miss in validate_links(path):
            problems.append(f"{path.name}: broken link {miss}")
    if problems:
        print("\n".join("PROBLEM " + p for p in problems))
        sys.exit(1)

    print(f"ok: 53 cols / {len(logical)} behavior fields / 105 dict entries / "
          f"{coverage['nVendors']} vendors / {coverage['nTypes']} example types; links validated")


if __name__ == "__main__":
    main()
