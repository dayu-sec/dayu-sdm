#!/usr/bin/env python3
"""Generate the standalone Chinese enum catalog for SDM2.0 logical events."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DICTIONARY = REPO / "log-model/contracts/event_operation_dictionary.json"
OUTPUT = ROOT / "docs/main/06-sdm-event-enum-catalog.md"

RECORD_KINDS = {
    "activity": "行为活动记录，表示已经发生或被观察到的操作。",
    "finding": "来源设备的检测或安全发现记录。",
    "inventory": "资产、软件、账号或配置清单记录。",
    "state": "对象在某个时点的状态记录。",
    "remediation": "隔离、阻断、删除等处置行为记录。",
}
OUTCOMES = {
    "success": "操作成功完成。", "failed": "操作执行失败。", "observed": "仅确认观察到该操作，结果不适用。",
    "denied": "操作请求被拒绝或阻止。", "allowed": "操作请求被允许通过。", "unknown": "已知发生操作，但无法判断结果。",
}
SEVERITIES = {
    "emerg": "系统不可用的紧急情况。", "alert": "必须立即处理的警报。", "crit": "严重错误或严重故障。",
    "error": "一般错误。", "warning": "可能导致问题的警告。", "notice": "正常但值得注意的情况。",
    "info": "一般信息。", "debug": "调试信息。",
}
ENTITY_TYPES = {
    "user": "人员或用户主体。", "account": "用于登录或授权的账号。", "host": "主机或终端实体。",
    "endpoint": "网络通信端点。", "process": "操作系统进程。", "file": "文件对象。",
    "service": "系统或网络服务。", "domain": "域名对象。", "url": "URL 对象。",
    "device": "采集设备或关联外设。", "resource": "统一资源对象。", "application": "应用程序或业务应用。",
    "cloud": "云资源对象。", "container": "容器对象。", "certificate": "数字证书对象。",
}
DOMAIN_VALUES = {
    "identity": "身份、登录和认证活动。", "network": "网络连接、流量和协议活动。",
    "endpoint": "终端、主机、进程和文件活动。", "threat": "威胁检测和安全发现。",
    "asset": "资产、配置和清单信息。", "system": "操作系统和系统审计活动。",
    "application": "应用程序和业务应用活动。", "discovery": "扫描、发现和探测活动。",
}
ATTACK_DIRECTIONS = {
    "L2L": "攻击方和受害方均位于受治理的内部网络。",
    "L2W": "攻击方位于内部网络，受害方位于外部网络。",
    "W2L": "攻击方位于外部网络，受害方位于内部网络。",
    "W2W": "攻击方和受害方均位于外部网络。",
    "unknown": "缺少边界信息，无法可靠判断攻击方向。",
}
REGISTRY_VALUE_TYPES = {
    "reg_none": "未定义具体数据类型（Windows 类型代码 0）。",
    "reg_sz": "以空字符结尾的字符串（代码 1）。",
    "reg_expand_sz": "可展开环境变量的字符串（代码 2）。",
    "reg_binary": "任意二进制数据（代码 3）。",
    "reg_dword": "32 位小端整数（代码 4）。",
    "reg_dword_big_endian": "32 位大端整数（代码 5）。",
    "reg_link": "注册表符号链接（代码 6）。",
    "reg_multi_sz": "字符串数组（代码 7）。",
    "reg_resource_list": "设备驱动程序资源列表（代码 8）。",
    "reg_full_resource_descriptor": "完整资源描述符（代码 9）。",
    "reg_resource_requirements_list": "资源需求列表（代码 10）。",
    "reg_qword": "64 位小端整数（代码 11）。",
}

TOKEN_LABELS = {
    "analyst": "分析人员", "add": "添加", "comment": "评论", "update": "更新", "priority": "优先级",
    "reason": "原因", "reputation": "信誉", "risk": "风险", "score": "评分", "root": "根本",
    "cause": "原因", "severity": "严重度", "status": "状态", "verdict": "研判结论",
    "device": "设备", "config": "配置", "firmware": "固件", "program": "程序", "download": "下载",
    "upload": "上传", "email": "邮件", "transaction": "事务", "uncategorized": "未分类", "url": "URL",
    "click": "点击", "entity": "实体", "change": "变更", "eventtype": "事件类型", "unspecified": "未指定",
    "file": "文件", "copy": "复制", "creation": "创建", "deletion": "删除", "modification": "修改",
    "move": "移动", "open": "打开", "read": "读取", "sync": "同步", "generic": "通用",
    "event": "事件", "group": "用户组", "mutex": "互斥体", "network": "网络", "connection": "连接",
    "dhcp": "DHCP", "dns": "DNS", "flow": "流量", "ftp": "FTP", "http": "HTTP", "smtp": "SMTP",
    "process": "进程", "injection": "注入", "launch": "启动", "module": "模块", "load": "加载",
    "privilege": "权限", "escalation": "提升", "termination": "终止", "registry": "注册表",
    "resource": "资源", "permissions": "权限", "written": "写入", "scan": "扫描", "host": "主机",
    "vuln": "漏洞", "scheduled": "计划", "task": "任务", "disable": "禁用", "enable": "启用",
    "service": "服务", "start": "启动", "stop": "停止", "setting": "设置", "heartbeat": "心跳",
    "shutdown": "关闭", "startup": "启动", "system": "系统", "audit": "审计", "log": "日志",
    "wipe": "清除", "triage": "研判", "agent": "Agent", "investigation": "调查", "user": "用户",
    "badge": "门禁卡", "in": "进入", "password": "REDACTED", "communication": "通信", "login": "登录",
    "logout": "登出", "content": "内容", "stats": "统计", "behaviors": "行为",
    "spawn": "创建进程", "fork": "派生进程", "exec": "执行程序", "remote": "远程", "thread": "线程",
    "library": "库", "queue": "排队", "apc": "APC", "set": "设置", "id": "标识", "assume": "承担",
    "role": "角色", "checkin": "签入", "checkout": "签出", "rename": "重命名", "query": "查询",    "response": "响应", "reset": "重置", "close": "关闭", "connect": "连接", "disconnect": "断开",
}

STATUS_LABELS = {
    "FULL": "完整映射", "PARTIAL": "部分映射", "NOT_APPLICABLE": "无需动作细分",
    "UNMAPPED": "无可靠动作映射", "DEPRECATED": "已废弃，只读兼容",
}

OPERATION_LABELS = {
    "access_check": "访问检查", "account_switch": "切换账号", "ack": "确认应答", "add_subgroup": "添加子组",
    "add_user": "添加用户", "assign": "分配", "assign_privileges": "授予权限", "assume_role": "承担角色",
    "authentication_ticket": "获取认证票据", "cancelled": "已取消", "checkin": "签入", "checkout": "签出",
    "clear": "清除", "close": "关闭", "completed": "已完成", "copy": "复制", "decline": "拒绝租约",
    "delayed": "已延迟", "delete": "删除", "disable": "禁用", "discover": "发现", "dns_update": "更新 DNS",
    "download": "下载", "duration_violation": "持续时间超限", "enable": "启用", "error": "执行错误",
    "exec": "执行程序", "expire": "租约过期", "extended": "扩展读取", "fail": "失败", "fork": "派生进程",
    "get": "获取", "inform": "通知配置", "install": "安装", "interactive": "交互式登录", "list": "列出",
    "listen": "监听", "load_library": "加载动态库", "lock": "锁定", "move": "移动", "mta_relay": "邮件中继",
    "nak": "否定应答", "offer": "提供租约", "open": "打开", "pause_violation": "暂停时间超限",
    "paused": "已暂停", "poll": "轮询", "preauth": "预认证", "preview": "预览", "put": "上传写入",
    "write": "写入",
    "query": "查询", "queue_apc": "排队 APC", "receive": "接收", "recycled": "移入回收站",
    "refuse": "拒绝连接", "release": "释放租约", "remote": "远程登录", "remote_interactive": "远程交互式登录",
    "remote_service": "远程服务登录", "remote_thread": "创建远程线程", "remove": "移除",
    "remove_subgroup": "移除子组", "remove_user": "移除用户", "rename": "重命名", "renew": "续租",
    "request": "请求租约", "reset": "重置连接", "response": "响应", "restart": "重新启动",
    "restarted": "已重新启动", "restore": "恢复", "resumed": "已恢复", "revoke_privileges": "撤销权限",
    "scan": "扫描", "send": "发送", "service": "服务登录", "service_ticket_renew": "续订服务票据",
    "service_ticket_request": "请求服务票据", "set_user_id": "设置用户标识", "share": "共享",
    "site": "站点操作", "spawn": "创建进程", "start": "开始", "started": "已开始", "sync": "同步",
    "system": "系统登录", "trace": "邮件跟踪", "traffic": "传输流量", "unlock": "解锁",
    "unshare": "取消共享", "unsync": "取消同步", "update": "更新", "upload": "上传", "versions": "版本操作",
}


def chinese_code(code):
    return "".join(TOKEN_LABELS.get(token, token.upper() if len(token) <= 4 else token) for token in code.split("_"))


def render_simple_enum(lines, title, path, values, closed=True):
    lines.extend([
        f"## {title}", "", f"逻辑路径：`{path}`。" + ("这是闭合枚举，新数据只能写入下列值。" if closed else "这是开放字段，下列值是当前中间版本推荐集合，不是强制全集。"), "",
        "| 枚举值 | 中文含义 |", "|---|---|",
    ])
    for value, description in values.items():
        lines.append(f"| `{value}` | {description} |")
    lines.append("")


def main():
    dictionary = json.loads(DICTIONARY.read_text(encoding="utf-8"))
    event_types = {}
    for rule in dictionary["mapping_rules"]:
        for event_type in rule["event_types"]:
            if event_type in event_types:
                raise ValueError(f"Duplicate event type: {event_type}")
            event_types[event_type] = {
                "status": rule["status"], "operations": rule["operations"], "sources": rule["sources"],
            }
    if len(event_types) != 105:
        raise ValueError(f"Expected 105 event types, found {len(event_types)}")
    operation_values = {operation for item in event_types.values() for operation in item["operations"]}
    if operation_values != OPERATION_LABELS.keys():
        missing = sorted(operation_values - OPERATION_LABELS.keys())
        stale = sorted(OPERATION_LABELS.keys() - operation_values)
        raise ValueError(f"Operation labels mismatch: missing={missing}, stale={stale}")

    lines = [
        "# SDM2.0 事件逻辑字段枚举说明", "",
        "> 本文档独立于逻辑字段清单，集中说明当前中间版本使用的枚举和受控字典。",
        "> 闭合枚举只能写入本文列出的值；开放字段的推荐值允许经评审扩展。",
        f"> `event.type + event.operation` 机器字典版本：`{dictionary['dictionary_version']}`。", "",
    ]
    render_simple_enum(lines, "记录种类", "event.record_kind", RECORD_KINDS)
    render_simple_enum(lines, "事件结果", "event.outcome", OUTCOMES)
    render_simple_enum(lines, "事件严重级别", "event.severity", SEVERITIES)
    render_simple_enum(lines, "关联对象实体类型", "roles.related[].entity_type、source_finding.entities.*[].entity_type", ENTITY_TYPES)
    render_simple_enum(lines, "事件领域推荐值", "event.domain", DOMAIN_VALUES, closed=False)
    render_simple_enum(lines, "攻击方向", "source_finding.attack_direction", ATTACK_DIRECTIONS)
    render_simple_enum(lines, "Windows 注册表值类型", "facets.registry.value.type", REGISTRY_VALUE_TYPES)

    lines.extend([
        "## 事件类型与操作", "",
        "`event.type` 是 105 项受控字典；`event.operation` 必须与当前事件类型组合解释。",
        "“—”表示该事件类型不允许填写 `event.operation`。已废弃类型只用于读取存量数据，新数据禁止写入。", "",
        "| 序号 | `event.type` | 中文含义 | 合法 `event.operation` | 动作中文说明 | 状态 |", "|---:|---|---|---|---|---|",
    ])
    for index, event_type in enumerate(sorted(event_types), 1):
        item = event_types[event_type]
        operations = item["operations"]
        operation_codes = "、".join(f"`{value}`" for value in operations) or "—"
        operation_labels = "；".join(f"`{value}`：{OPERATION_LABELS[value]}" for value in operations) or "—"
        lines.append(
            f"| {index} | `{event_type}` | {chinese_code(event_type)} | {operation_codes} | "
            f"{operation_labels} | {STATUS_LABELS[item['status']]} |"
        )

    lines.extend([
        "", "## 非枚举字段", "",
        "下列字段容易被误认为枚举，但当前没有可执行的闭合集合：", "",
        "| 逻辑路径 | 当前约束 |", "|---|---|",
        "| `event.domain` | 开放字段，本文仅给出当前推荐值。 |",
        "| `source_finding.severity` | 保存来源设备检测严重度，当前按来源契约映射，不与 `event.severity` 共用枚举。 |",
        "| `facets.authentication.auth_type` | 认证方式，当前未形成闭合枚举。 |",
        "| `facets.authentication.auth_result` | 认证专属结果，当前未形成闭合枚举，不等同于 `event.outcome`。 |",
        "| `facets.authentication.auth_failure_reason` | 认证失败原因，当前未形成闭合枚举。 |",
        "| `facets.network.direction` | 网络方向，当前未形成 SDM2.0 闭合枚举。 |",
        "| `facets.network.connection_state` | 网络连接状态，当前未形成 SDM2.0 闭合枚举。 |", "",
        "## 写入规则", "",
        "- 所有标准枚举值统一使用小写形式。",
        "- `event.outcome` 不保存阻断动作或检测结论；来源 `blocked` 应根据语义映射为 `denied`。",
        "- `event.severity` 使用 syslog 八级；来源告警的高、中、低危写入 `source_finding.severity`。",
        "- 未在字典中的 `(event.type, event.operation)` 组合必须将 `event.operation` 留空。",
        "- 开放字段新增推荐值时，需要更新契约和本文档，不应由单个接入规则自由造词。", "",
    ])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(event_types)} event types")


if __name__ == "__main__":
    main()
