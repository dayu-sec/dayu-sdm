# 样例：反弹 Shell

展示 v0.2 写入形状：瘦主表 + 主体证据 + 实体 + 闸门分析 + 告警轮 / 案件轮 AI。`verdict` 仍为 UNKNOWN，直到策略或人接受。

触发日志挂在 Alert 下。调查中补充的登录日志挂在 Case 下。案件轮同时 cite 两类证据。

## 告警

```json
{
  "tenant_id": "tenant01",
  "alert_id": "alert_a1b2c3d4e5f6",
  "alert_display_id": "ALT-20260708-2D749209",
  "source_product": "sdm-rule-engine",
  "alert_name": "反弹 Shell",
  "description": "检测主机进程执行交互式 Shell 并主动连接远端地址的行为。",
  "alert_type": "DETECTION",
  "category_code": "NETWORK_COMMAND_AND_CONTROL",
  "event_count": 2,
  "severity": "HIGH",
  "detection_confidence": 80,
  "detection_risk_score": 85,
  "workflow_status": "NEW",
  "verdict": "UNKNOWN",
  "case_id": "case_9f8e7d6c5b4a",
  "created_time": 1783504800000,
  "updated_time": 1783504808000,
  "first_seen": 1783504500000,
  "last_seen": 1783504680000,
  "rule_id": "rule_revshell_001",
  "rule_version": "1.2.0",
  "rule_type": "SINGLE_CONDITION",
  "detection_engine": "sdm-rule-engine",
  "dedup_key": "tenant01|rule_revshell_001|host_a1b2c3|execution|2026070809",
  "merge_id": "merge_1b7fd783983a2cf7",
  "primary_entity_id": "host:tenant01:k3s-master-1",
  "primary_entity_type": "host",
  "primary_entity_role": "victim",
  "primary_entity_value": "k3s-master-1",
  "primary_tactic_id": "TA0011",
  "primary_technique_id": "T1059",
  "latest_analysis_id": "an_ai_001",
  "latest_analysis_conclusion": "SUSPICIOUS",
  "latest_analysis_confidence": 72,
  "latest_analysis_summary": "主机执行交互式 bash 并外连 203.0.113.218:9990，未见工单或变更解释。",
  "latest_analysis_time": 1783504808000
}
```

## 实体（节选）

```json
[
  {
    "entity_id": "host:tenant01:k3s-master-1",
    "entity_type": "host",
    "alert_entity_role": "victim",
    "entity_value": "k3s-master-1",
    "is_primary": true
  },
  {
    "entity_id": "ip:203.0.113.218",
    "entity_type": "ip",
    "alert_entity_role": "attacker",
    "entity_value": "203.0.113.218",
    "is_primary": false,
    "used_for_grouping": false
  }
]
```

## 证据

Alert 证据是检出触发与上下文。Case 证据是调查新增，不把 TRIGGER 再挂一遍。

```json
[
  {
    "evidence_id": "ev_3c8a1f0b9d2e4a7c6b15d8e1",
    "subject_type": "ALERT",
    "alert_id": "alert_a1b2c3d4e5f6",
    "evidence_type": "EVENT",
    "event_id": "evt_proc_bash_revshell",
    "evidence_role": "TRIGGER",
    "evidence_summary": "k3s-master-1 执行交互式 bash 并连接 203.0.113.218:9990。"
  },
  {
    "evidence_id": "ev_71aa0c2d4e8f901234567890",
    "subject_type": "ALERT",
    "alert_id": "alert_a1b2c3d4e5f6",
    "evidence_type": "EVENT",
    "event_id": "evt_net_c2_9990",
    "evidence_role": "CONTEXT",
    "evidence_summary": "同主机随后对 203.0.113.218:9990 建立出站连接。"
  },
  {
    "evidence_id": "ev_9b2c4d6e8f0a1b3c5d7e9f01",
    "subject_type": "CASE",
    "case_id": "case_9f8e7d6c5b4a",
    "evidence_type": "EVENT",
    "event_id": "evt_auth_root_login",
    "evidence_role": "CORROBORATION",
    "evidence_summary": "调查补充：同一主机在检出前 4 分钟出现 root 异地登录，不是检出 TRIGGER。"
  }
]
```

## 闸门 + AI 分析行

告警轮只 cite Alert 证据。案件轮同时 cite Alert TRIGGER 和 Case 补充日志。

```json
[
  {
    "analysis_id": "an_gate_001",
    "subject_type": "ALERT",
    "analysis_type": "GATE",
    "trigger_mode": "ALERT",
    "next_hop": "FULL_AGENT",
    "noise_reason": "NONE",
    "conclusion": "UNKNOWN",
    "accepted_status": "SUPERSEDED"
  },
  {
    "analysis_id": "an_ai_001",
    "subject_type": "ALERT",
    "analysis_type": "AI",
    "trigger_mode": "ALERT",
    "conclusion": "SUSPICIOUS",
    "analysis_confidence": 72,
    "reasoning_summary": "主机执行交互式 bash 并外连 203.0.113.218:9990，未见工单或变更解释。",
    "cited_evidence": [
      {
        "evidence_id": "ev_3c8a1f0b9d2e4a7c6b15d8e1",
        "evidence_subject_type": "ALERT",
        "alert_id": "alert_a1b2c3d4e5f6"
      }
    ],
    "accepted_status": "PENDING",
    "model_name": "triage-agent",
    "token_out": 280
  },
  {
    "analysis_id": "an_case_001",
    "subject_type": "CASE",
    "case_id": "case_9f8e7d6c5b4a",
    "analysis_type": "AI",
    "trigger_mode": "CASE",
    "conclusion": "SUSPICIOUS",
    "analysis_confidence": 78,
    "reasoning_summary": "反弹 Shell 检出前后出现 root 异地登录，仍缺变更单。正式 verdict 保持 UNKNOWN。",
    "cited_evidence": [
      {
        "evidence_id": "ev_3c8a1f0b9d2e4a7c6b15d8e1",
        "evidence_subject_type": "ALERT",
        "alert_id": "alert_a1b2c3d4e5f6"
      },
      {
        "evidence_id": "ev_9b2c4d6e8f0a1b3c5d7e9f01",
        "evidence_subject_type": "CASE",
        "case_id": "case_9f8e7d6c5b4a"
      }
    ],
    "accepted_status": "PENDING"
  }
]
```

Agent 输出仍是短 JSON。写入服务按 `evidence_id` 展开为 `sdm_analysis_citation` 行，带当时的主体快照。
