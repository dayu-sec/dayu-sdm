#!/usr/bin/env python3
"""Build the SDM2.0 presentation page set.

Generates from authoritative sources under log-model/ and alert-model/:
  - presentation/index.html          (landing, from templates/index.html)
  - presentation/log-standard.html   (log standard, from templates/log-standard.html)
  - presentation/alert-standard.html (from templates/alert-standard.html)

Re-run after the source catalogs, examples, or the review page change:
  python3 presentation/build/build_pages.py
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
BUILD = ROOT / "presentation"
TEMPLATES = Path(__file__).resolve().parent / "templates"

DOC_MAIN = DELIV / "docs" / "main"
PROJECTION_REGISTRY = DELIV / "contracts" / "hybrid-event" / "projection-registry.v1.json"
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
    text = (DOC_MAIN / "05-sdm-event-logical-field-catalog.md").read_text(encoding="utf-8")
    sec = sections(text)
    stats: dict[str, int] = {}
    for line in sec.get("分层统计", "").splitlines():
        if line.startswith("|"):
            cells = split_row(line)
            if is_sep_row(cells) or cells[0].strip() == "层":
                continue
            stats[strip_ticks(cells[0])] = int(cells[1])
    rows = parse_numbered_table(sec.get("核心逻辑字段", ""), ncols=8, merge_into=6)
    out = []
    for n, layer, path, typ, card, req, sample, meaning in rows:
        out.append(dict(
            n=int(n), layer=strip_ticks(layer), path=strip_ticks(path),
            type=strip_ticks(typ), card=strip_ticks(card), req=strip_ticks(req),
            sample=strip_ticks(sample), meaning=meaning.strip(),
        ))
    return out, stats


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
                    if is_sep_row(cells) or cells[0].strip() == "逻辑路径":
                        continue
                    non_enums.append([strip_ticks(cells[0]), cells[1].strip()])
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


def rel_from_presentation(p: Path) -> str:
    """Repo file path as referenced from pages inside presentation/."""
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
                href=rel_from_presentation(t),
            ) for t in types],
        ))
    n_types = sum(len(v["types"]) for v in vendors)
    return dict(vendors=vendors, nVendors=len(vendors), nTypes=n_types)


# ─────────────────────────── showcase examples ───────────────────────────

SHOWCASE = [
    dict(
        dir="examples/topas_waf/topas_waf_attack", prefix="runtime_observed",
        title="天融信 WAF · SQL 注入检测", tag="finding", tagClass="cyan",
        column="告警列（alert / finding）",
        steps=[
            ("1 定性", "record_kind / data_src_category", "finding / alert*", "有攻击名、规则命中与处置判定 → 告警列。*样例仍存废弃值 security_log，见第 8 步"),
            ("2 身份", "event_id / log_id / occur_time", "evt-dee1e370… / log-dee1e370… / 2026-01-23 11:00:00", "来源无独立 ID，log_id 与 event_id 同源；设备时间已转 UTC"),
            ("3 定型", "event_type / operation / domain", "network_http / 留空 / threat*", "按行为查 105 字典（HTTP 访问）；*样例 domain 未落，见第 8 步"),
            ("4 结果", "outcome / severity", "unknown / 留空", "样例未从动作推导；新口径应为 action=block → denied，severity 走统一换算"),
            ("5 角色", "source / target", "198.51.100.54 → 203.0.113.115", "观测方向：客户端 → 受保护服务器；不是 attacker/victim"),
            ("6 检测", "source_finding", "title=SQL SELECT 注入 · severity=High · status=deny", "检测声明与行为事实分离；*status 应记 action=block，见第 8 步"),
            ("7 扩展", "source_private", "保留设备未映射字段", "装不下的原样保留，不丢数据"),
            ("8 自查", "清单 #1–#10", "3 处旧样例差异", "category=security_log（废弃）、domain 未落、status 代替 action——均为新契约前产出，重映射时按指南修正"),
        ],
    ),
    dict(
        dir="examples/sxf_probe/flow_dns", prefix="runtime_observed",
        title="深信服探针 · DNS 查询", tag="activity", tagClass="green",
        column="流量列（network / activity）",
        steps=[
            ("1 定性", "record_kind / data_src_category", "activity / network*", "纯行为记录，无检测判定 → 流量列。*样例仍存 security_log，见第 8 步"),
            ("2 身份", "event_id / log_id / occur_time", "evt-f2ebaf11… / log-f2ebaf11… / 2025-05-22 12:30:11", "来源无独立 ID，log_id 派生同源；探针时间已转 UTC"),
            ("3 定型", "event_type / operation / domain", "network_dns / query / network", "行为动词=查询 → 字典登记组合，不是一律 network_connection"),
            ("4 结果", "outcome / severity", "success / 留空", "无守门人、行为完成 → success；activity 无独立证据 severity 留空"),
            ("5 角色", "source / target", "192.0.2.199 → 192.0.2.123", "观测方向：客户端 → DNS 服务器"),
            ("6 检测", "source_finding", "跳过", "activity 不建 source_finding，outcome 只走判定树"),
            ("7 扩展", "source_private", "未确认的协议/命令字典原值", "保留原值待评审，不造词"),
            ("8 自查", "清单 #1–#10", "1 处旧样例差异", "category=security_log（废弃，应 network）——新契约前产出"),
        ],
    ),
    dict(
        dir="examples/tianqing/edr_process_event", prefix="process_creation",
        title="天擎 · 进程创建", tag="activity", tagClass="green",
        column="终端审计列（audit / activity）",
        steps=[
            ("1 定性", "record_kind / data_src_category", "activity / audit*", "按 log_type 走终端列：同一 EDR 的告警日志走告警列。*样例仍存 endpoint_security，见第 8 步"),
            ("2 身份", "event_id / log_id / occur_time", "evt-2555c859… / log-tianqing-process-creation-0001 / 1734489737220", "来源有稳定 ID → log_id 用来源 ID，不改写成 event_id"),
            ("3 定型", "event_type / operation / domain", "process_launch / spawn / endpoint", "行为动词=创建进程 → 字典登记组合 spawn"),
            ("4 结果", "outcome / severity", "observed / 留空*", "行为无成败语义 → observed；*样例 severity=info 属旧样例差异，新口径无独立证据应留空"),
            ("5 角色", "source / carrier", "source_host=DESKTOP-NU779RJ，载体为进程链", "终端审计特有：carrier 记录行为链主载体（哪个进程干的），与 source（哪个端点）区分"),
            ("6 检测", "source_finding", "跳过", "activity 不建 source_finding"),
            ("7 扩展", "source_private", "父进程、命令行等未投影字段", "原样保留"),
            ("8 自查", "清单 #1–#10", "2 处旧样例差异", "category=endpoint_security（应 audit）、severity=info——新契约前产出"),
        ],
    ),
]

SHOWCASE_FOOTNOTE = (
    "例外样例：<a href='../log-model/examples/tianqing/edr_powershell_cmd_exec/' "
    "style='color:var(--acc)'>天擎 PowerShell 执行</a>——受控字典暂无脚本执行类型，暂用 generic_event；"
 "登记组合落地前不改判。"
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
            files[f"{key}Url"] = rel_from_presentation(p)
            files[key] = p.read_text(encoding="utf-8")
        out.append(dict(
            title=cfg["title"], tag=cfg["tag"], tagClass=cfg["tagClass"],
            column=cfg["column"], steps=cfg["steps"],
            href=rel_from_presentation(exdir / "README.md"),
            files=files,
        ))
    return out


# ─────────────────────────── page assembly ───────────────────────────

def extract_base_css() -> str:
    html = ALERT_TEMPLATE.read_text(encoding="utf-8")
    m = re.search(r"<style>\n(.*?)</style>", html, flags=re.S)
    if not m:
        sys.exit("cannot extract base CSS from presentation/build/templates/alert-standard.html")
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

    # 数量断言：与文档头声明一致
    assert len(physical) == 53, f"physical columns = {len(physical)}, expected 53"
    assert len(logical) == 504, f"logical fields = {len(logical)}, expected 504"
    assert len(event_dict) == 105, f"event.type entries = {len(event_dict)}, expected 105"
    assert layer_stats == dict(metadata=15, event=7, roles=253, facets=89, source_finding=140), layer_stats

    stats = dict(
        physical=len(physical), logical=len(logical),
        vendors=coverage["nVendors"], types=coverage["nTypes"],
        layerCounts=layer_stats,
    )
    data = dict(
        stats=stats, physical=physical, logical=logical,
        enums=enums, eventDict=event_dict, nonEnums=non_enums,
        coverage=dict(vendors=coverage["vendors"]),
        examples=showcase, examplesFootnote=SHOWCASE_FOOTNOTE, ddl=ddl,
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

    print(f"ok: 53 cols / 504 fields / 105 dict entries / "
          f"{coverage['nVendors']} vendors / {coverage['nTypes']} example types; links validated")


if __name__ == "__main__":
    main()
