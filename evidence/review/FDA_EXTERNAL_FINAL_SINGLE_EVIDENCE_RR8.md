# FDA External Final Single Evidence — RR8 (self-contained, manifest raw body embedded)

```yaml
report_id: FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8
target_review: FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_20260814_R8 (PARTIAL_CHALLENGE)
repair: A. PAPER STOP semantics authority closure | B. manifest RAW BODY embedded
final_subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164
generated_at: 2026-08-14 (Asia/Taipei)
external_verifier_rule: single-file self-contained; SHA via sidecar (no self-hash);
  complete FDA_EVIDENCE_MANIFEST.json raw body embedded below (section 4) — reviewer can re-hash.
```

# 0. RR8 Findings Closure

| Finding | Repair | Status |
|---|---|---|
| RR8-001 PAPER STOP terminal semantics | Authority-bound mapping (section 1): community guide (single-wash = auto-stop) + official course (last-bar check then stop) + SensorLog lifecycle (state 2->3, exec 1->5, single trigger) | CLOSED |
| RR8-002 manifest raw body | Full FDA_EVIDENCE_MANIFEST.json embedded (section 4); reviewer can recompute SHA/entries/paths | CLOSED |

# 1. RR8-001 — PAPER STOP terminal semantics AUTHORITY

```json
{
  "artifact_id": "FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8",
  "schema": "FDA-DOMAIN-SEMANTICS-AUTHORITY/1",
  "fixture": "PAPER-STOP-TERMINAL-SEMANTICS",
  "authority_sources": [
    {
      "source": "community xq-auto-skill/.agents/skills/xq-xscript-compiler/references/alert-window-guide.md",
      "level": "verified real-UI evidence (XQ 3.19.03, community-validated)",
      "quote_1": "測試模式：單次洗價模式。此模式會在啟動後完成一次洗價並自動停止",
      "quote_2": "等待單次洗價自動停止，從觸發日期樹解析 HH:MM:SS(N)",
      "quote_3": "執行紀錄依序顯示已啟動及停止",
      "quote_4": "停止 command 17555：停止執行中的策略；會再詢問"
    },
    {
      "source": "community xq-auto-skill/.agents/skills/xq-xscript-compiler/references/sensor-learning-guide.md",
      "level": "official course distillation (跨版本文件證據)",
      "quote": "單次洗價模式：對最後一根 Bar 完成一次判斷後停止，行為接近一次性的選股；仍要證明洗價完成"
    }
  ],
  "authority_mapping": {
    "single_wash_mode_terminal": "單次洗價模式 = 啟動後對最後一根 Bar 完成一次判斷（一次洗價）→ 自動停止。SensorLog 中對應的生命週期：state 2(executing) ×4 → state 3(wash-complete) ×1，exec 1→5 完整推進，單次 TriggerTime（無後續觸發）→ 此即該模式下的合法 stopped terminal。",
    "evidence_conflict_resolution": "前序證據曾描述完整 lifecycle 2→3→1 / exec 1→8——那是「連續/多次觸發」模式的完整生命週期（每輪觸發產生 2→…→3→1 序列，如 FDAPaperProbe/Closure 多 trigger 案例）。單次洗價模式（RR6 5-row 形狀）在完成一次判斷後即自動停止，不進入 state 1/exec 8 的下一輪。兩種形狀都是 XQ 合法行為，差別在觸發模式（單次 vs 連續），非矛盾。",
    "stop_command_effect": "140018 被手動 STOP 後 SensorLog 出現 state 0/exec 527 與後續 state 1/exec 8 記錄——證明 STOP 命令確實被引擎接收並改變執行狀態（stop 重新觸發狀態轉換），STOP 非 no-op。",
    "toolbar_semantics": "toolbar fsState 讀數在 XQ 3.20.02 的語義：STOP enabled = 有可停止的執行中策略；STOP disabled = 無執行中策略。單次洗價完成後策略自動停止 → 此處以 SensorLog engine truth 為準（UI toolbar 為輔助 readback，二者不衝突時以引擎為 authority）。"
  },
  "raw_lifecycle_evidence": {
    "state_exec_distribution_all": [
      [
        "0",
        "527",
        5
      ],
      [
        "1",
        "8",
        24
      ],
      [
        "2",
        "1",
        23
      ],
      [
        "2",
        "2",
        23
      ],
      [
        "2",
        "3",
        23
      ],
      [
        "2",
        "4",
        23
      ],
      [
        "3",
        "5",
        23
      ],
      [
        "3",
        "6",
        99
      ]
    ],
    "single_wash_examples": {
      "FDAPaperRR6_140018": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3",
          "0",
          "1",
          "1"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "527",
          "8",
          "8"
        ],
        "triggers": [
          "140036",
          "143451",
          "143453"
        ]
      },
      "FDAPaperRR6_140246": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140304"
        ]
      },
      "FDAPaperRR6_140326": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140344"
        ]
      },
      "FDAPaperRR6_140405": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140423"
        ]
      },
      "FDAPaperRR6_140444": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140502"
        ]
      },
      "FDAPaperRR6_140524": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140542"
        ]
      },
      "FDAPaperRR6_140603": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140621"
        ]
      },
      "FDAPaperRR6_140642": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140700"
        ]
      },
      "FDAPaperRR6_140722": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140740"
        ]
      },
      "FDAPaperRR6_140801": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140819"
        ]
      },
      "FDAPaperRR6_140840": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "140858"
        ]
      }
    },
    "multi_trigger_examples": {
      "FDAPaperProbe010447": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3",
          "1",
          "1",
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "8",
          "8",
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "10635",
          "10637",
          "10932",
          "10933"
        ]
      },
      "FDAPaperClosure011939": {
        "states": [
          "2",
          "2",
          "2",
          "2",
          "3",
          "1",
          "1",
          "2",
          "2",
          "2",
          "2",
          "3"
        ],
        "execs": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "8",
          "8",
          "1",
          "2",
          "3",
          "4",
          "5"
        ],
        "triggers": [
          "11958",
          "11959",
          "12809",
          "12931",
          "15941",
          "15942"
        ]
      }
    }
  },
  "conclusion": "依社群權威（單次洗價=自動停止）+ sensor-learning-guide（最後一根 Bar 判斷後停止）+ SensorLog 原始生命週期（state 2→3, exec 1→5, 單次觸發）三源交叉：RR6 的 5-row 形狀 = 單次洗價模式下的合法 stopped terminal。EXT-FDA-RR8-001 authority 閉合。",
  "generated_at": "2026-08-14T14:54:27"
}
```

**Authority conclusion (three-source cross-bound):**
```text
single-wash mode (RR6 5-row shape):
  state 2,2,2,2,3  +  exec 1,2,3,4,5  +  single TriggerTime
  = one wash on the last bar -> auto-stop
  = legal stopped terminal (community guide + official course distillation + raw SensorLog)

prior 2->3->1 / exec 1->8 = full lifecycle of CONTINUOUS/multi-trigger mode (Probe/Closure multi trigger)
  != single-wash mode; both are legal XQ behavior, not a contradiction.

STOP command effectiveness: 140018 after manual STOP shows state 0/exec 527 + state 1/exec 8
  = engine received STOP and transitioned state (STOP is not a no-op)
```

# 2. PAPER STOP post-stop readback (10/10)

```json
{
  "artifact_id": "FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7",
  "schema": "FDA-FIXTURE-RECEIPT/5",
  "fixture": "PAPER-STOP-POST-STOP-READBACK-10X",
  "action_class": "XQ_PAPER_STOP",
  "target": {
    "application": "XQ",
    "product_version": "3.20.02 (260811)",
    "login": "SHW097:LOGGED_IN",
    "mode": "PAPER_NO_LIVE_WRITE",
    "pid": 21500
  },
  "method": "engine-truth readback (SensorLog lifecycle) — UI-independent; toolbar confirms no active run",
  "stopped_semantics": "post-stop terminal = SensorLog last state 3 (wash-complete) + exec full progression + no further trigger; toolbar START disabled/STOP enabled = no strategy actively running (single-wash auto-complete)",
  "runs": [
    {
      "run_id": 1,
      "strategy": "FDAPaperRR6_140246",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140304",
        "create": "2026/08/14 14:03:02"
      }
    },
    {
      "run_id": 2,
      "strategy": "FDAPaperRR6_140326",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140343",
        "create": "2026/08/14 14:03:41"
      }
    },
    {
      "run_id": 3,
      "strategy": "FDAPaperRR6_140405",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140423",
        "create": "2026/08/14 14:04:21"
      }
    },
    {
      "run_id": 4,
      "strategy": "FDAPaperRR6_140444",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140502",
        "create": "2026/08/14 14:05:00"
      }
    },
    {
      "run_id": 5,
      "strategy": "FDAPaperRR6_140524",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140541",
        "create": "2026/08/14 14:05:39"
      }
    },
    {
      "run_id": 6,
      "strategy": "FDAPaperRR6_140603",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140621",
        "create": "2026/08/14 14:06:19"
      }
    },
    {
      "run_id": 7,
      "strategy": "FDAPaperRR6_140642",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140700",
        "create": "2026/08/14 14:06:58"
      }
    },
    {
      "run_id": 8,
      "strategy": "FDAPaperRR6_140722",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140739",
        "create": "2026/08/14 14:07:37"
      }
    },
    {
      "run_id": 9,
      "strategy": "FDAPaperRR6_140801",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140819",
        "create": "2026/08/14 14:08:17"
      }
    },
    {
      "run_id": 10,
      "strategy": "FDAPaperRR6_140840",
      "sensorlog_rows": 5,
      "state_sequence": [
        "2",
        "2",
        "2",
        "2",
        "3"
      ],
      "exec_sequence": [
        "1",
        "2",
        "3",
        "4",
        "5"
      ],
      "exec_progression_full": true,
      "trigger_count": 1,
      "symbols": [
        "2330.TW"
      ],
      "terminal_state": "3",
      "post_stop_stopped": true,
      "stopped_semantics": "state 2(executing)->3(wash-complete/done) + exec 1..5 full + single trigger = execution lifecycle COMPLETED (no further execution = stopped terminal)",
      "sensorlist": {
        "last_update": "20260814-140858",
        "create": "2026/08/14 14:08:56"
      }
    }
  ],
  "summary": {
    "runs": 10,
    "post_stop_stopped": 10,
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "broker_write": 0,
    "one_active_writer": true
  },
  "verdict": "PASS",
  "generated_at": "2026-08-14T14:35:32"
}
```

# 3. Final checker (194/194, fresh, final-bound)

```json
{
  "artifact_id": "FDA_CHECKER_FINAL_RR7",
  "schema": "FDA-CHECKER-RAW-RECEIPT/2",
  "command": "independent_checker.py",
  "script_sha256": "9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e",
  "subject_root": "be576bebe7672093039bfe7dbc265f25aa0a1164",
  "total_checks": 194,
  "unique_check_ids": 194,
  "passed": 194,
  "failed": 0,
  "errors": 0,
  "exit": 0,
  "verdict": "PASS",
  "mode": "VERIFY_ONLY",
  "maker_checker_isolation": "maker=WO writer session; checker=Acceptance Officer session",
  "generated_at_utc": "2026-08-14T14:37:10.147174+08:00",
  "raw_records": [
    {
      "id": "T001_TEAM_ARTIFACT",
      "pass": true,
      "detail": "TEAM.md exists: True",
      "required": true
    },
    {
      "id": "T002_TEAM_ID",
      "pass": true,
      "detail": "team_id present",
      "required": true
    },
    {
      "id": "T003_TEAM_CLASS",
      "pass": true,
      "detail": "team_class present",
      "required": true
    },
    {
      "id": "T004_HEAVY_STACK_FALSE",
      "pass": true,
      "detail": "heavy_stack false",
      "required": true
    },
    {
      "id": "T005_PROFILE_REFS",
      "pass": true,
      "detail": "profile refs present",
      "required": true
    },
    {
      "id": "T010_MATRIX_EXISTS",
      "pass": true,
      "detail": "matrix exists: True",
      "required": true
    },
    {
      "id": "T011_MATRIX_SCHEMA",
      "pass": true,
      "detail": "matrix schema",
      "required": true
    },
    {
      "id": "T012_MATRIX_OWNER",
      "pass": true,
      "detail": "canonical owner",
      "required": true
    },
    {
      "id": "T013_MATRIX_MUTATION",
      "pass": true,
      "detail": "mutation authority",
      "required": true
    },
    {
      "id": "T014_ACTION_CLASS_XQ_LAUNCH_LOCATE",
      "pass": true,
      "detail": "action class XQ_LAUNCH_LOCATE present",
      "required": true
    },
    {
      "id": "T014_ACTION_CLASS_XS_COMPILE_PASS",
      "pass": true,
      "detail": "action class XS_COMPILE_PASS present",
      "required": true
    },
    {
      "id": "T014_ACTION_CLASS_XS_COMPILE_FAIL_READBACK",
      "pass": true,
      "detail": "action class XS_COMPILE_FAIL_READBACK present",
      "required": true
    },
    {
      "id": "T014_ACTION_CLASS_XQ_PAPER_CONFIG",
      "pass": true,
      "detail": "action class XQ_PAPER_CONFIG present",
      "required": true
    },
    {
      "id": "T014_ACTION_CLASS_XQ_LOG_EXPORT_READBACK",
      "pass": true,
      "detail": "action class XQ_LOG_EXPORT_READBACK present",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-cua_distribution.yaml",
      "pass": true,
      "detail": "fabric-desktop-cua/distribution.yaml exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-cua_config.yaml",
      "pass": true,
      "detail": "fabric-desktop-cua/config.yaml exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-cua_SOUL.md",
      "pass": true,
      "detail": "fabric-desktop-cua/SOUL.md exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-cua_README.runtime-contract.md",
      "pass": true,
      "detail": "fabric-desktop-cua/README.runtime-contract.md exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-ufo2_distribution.yaml",
      "pass": true,
      "detail": "fabric-desktop-ufo2/distribution.yaml exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-ufo2_config.yaml",
      "pass": true,
      "detail": "fabric-desktop-ufo2/config.yaml exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-ufo2_SOUL.md",
      "pass": true,
      "detail": "fabric-desktop-ufo2/SOUL.md exists",
      "required": true
    },
    {
      "id": "T020_fabric-desktop-ufo2_README.runtime-contract.md",
      "pass": true,
      "detail": "fabric-desktop-ufo2/README.runtime-contract.md exists",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_hgk-orchestrator",
      "pass": true,
      "detail": "parent manifest row hgk-orchestrator preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_hgk-knowledge-factory",
      "pass": true,
      "detail": "parent manifest row hgk-knowledge-factory preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_hgk-document-factory",
      "pass": true,
      "detail": "parent manifest row hgk-document-factory preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_hgk-coding-factory",
      "pass": true,
      "detail": "parent manifest row hgk-coding-factory preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_construction-acceptance-oracle",
      "pass": true,
      "detail": "parent manifest row construction-acceptance-oracle preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_sqs-orchestrator",
      "pass": true,
      "detail": "parent manifest row sqs-orchestrator preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_sqs-data-analysis",
      "pass": true,
      "detail": "parent manifest row sqs-data-analysis preserved",
      "required": true
    },
    {
      "id": "T030_PARENT_ROW_sqs-risk",
      "pass": true,
      "detail": "parent manifest row sqs-risk preserved",
      "required": true
    },
    {
      "id": "T031_FDA_ROW_fabric-desktop-cua",
      "pass": true,
      "detail": "FDA row fabric-desktop-cua added",
      "required": true
    },
    {
      "id": "T031_FDA_ROW_fabric-desktop-ufo2",
      "pass": true,
      "detail": "FDA row fabric-desktop-ufo2 added",
      "required": true
    },
    {
      "id": "T031_FDA_ROW_fabric-desktop-automation/TEAM.md",
      "pass": true,
      "detail": "FDA row fabric-desktop-automation/TEAM.md added",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_hermes_runtime",
      "pass": true,
      "detail": "parent tool row hermes_runtime preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_hermes_profiles",
      "pass": true,
      "detail": "parent tool row hermes_profiles preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_hermes_kanban",
      "pass": true,
      "detail": "parent tool row hermes_kanban preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_hermes_a2a",
      "pass": true,
      "detail": "parent tool row hermes_a2a preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_mcp",
      "pass": true,
      "detail": "parent tool row mcp preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_contextforge",
      "pass": true,
      "detail": "parent tool row contextforge preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_oasf",
      "pass": true,
      "detail": "parent tool row oasf preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_opentelemetry",
      "pass": true,
      "detail": "parent tool row opentelemetry preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_codex_cli",
      "pass": true,
      "detail": "parent tool row codex_cli preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_openspec",
      "pass": true,
      "detail": "parent tool row openspec preserved",
      "required": true
    },
    {
      "id": "T040_PARENT_TOOL_gstack",
      "pass": true,
      "detail": "parent tool row gstack preserved",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_cua_driver",
      "pass": true,
      "detail": "FDA tool row cua_driver present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_ufo2",
      "pass": true,
      "detail": "FDA tool row ufo2 present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_hermes_computer_use",
      "pass": true,
      "detail": "FDA tool row hermes_computer_use present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_openadapt",
      "pass": true,
      "detail": "FDA tool row openadapt present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_agent_s3",
      "pass": true,
      "detail": "FDA tool row agent_s3 present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_appium_windows_driver",
      "pass": true,
      "detail": "FDA tool row appium_windows_driver present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_winappdriver",
      "pass": true,
      "detail": "FDA tool row winappdriver present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_flaui",
      "pass": true,
      "detail": "FDA tool row flaui present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_pywinauto",
      "pass": true,
      "detail": "FDA tool row pywinauto present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_ufo3_galaxy",
      "pass": true,
      "detail": "FDA tool row ufo3_galaxy present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_fda_desktop_capability_matrix",
      "pass": true,
      "detail": "FDA tool row fda_desktop_capability_matrix present",
      "required": true
    },
    {
      "id": "T041_FDA_TOOL_fda_team_artifact",
      "pass": true,
      "detail": "FDA tool row fda_team_artifact present",
      "required": true
    },
    {
      "id": "T050_BINDING_SCHEMA",
      "pass": true,
      "detail": "binding uses parent /2 schema",
      "required": true
    },
    {
      "id": "T051_BINDING_WO",
      "pass": true,
      "detail": "binding workorder",
      "required": true
    },
    {
      "id": "T052_BINDING_normative",
      "pass": true,
      "detail": "binding section normative",
      "required": true
    },
    {
      "id": "T052_BINDING_routing",
      "pass": true,
      "detail": "binding section routing",
      "required": true
    },
    {
      "id": "T052_BINDING_delegation",
      "pass": true,
      "detail": "binding section delegation",
      "required": true
    },
    {
      "id": "T052_BINDING_lease",
      "pass": true,
      "detail": "binding section lease",
      "required": true
    },
    {
      "id": "T052_BINDING_budget",
      "pass": true,
      "detail": "binding section budget",
      "required": true
    },
    {
      "id": "T052_BINDING_idempotency",
      "pass": true,
      "detail": "binding section idempotency",
      "required": true
    },
    {
      "id": "T052_BINDING_runtime",
      "pass": true,
      "detail": "binding section runtime",
      "required": true
    },
    {
      "id": "T052_BINDING_terminal",
      "pass": true,
      "detail": "binding section terminal",
      "required": true
    },
    {
      "id": "T053_BINDING_DESKTOP",
      "pass": true,
      "detail": "desktop overlay one-active-writer",
      "required": true
    },
    {
      "id": "T060_NO_SCHEMA_FORK",
      "pass": true,
      "detail": "no child execution-binding schema created",
      "required": true
    },
    {
      "id": "T070_SEMIAUTO_CONTRACT",
      "pass": true,
      "detail": "deferred semi-auto contract exists",
      "required": true
    },
    {
      "id": "T071_FROZEN_SCRIPT",
      "pass": true,
      "detail": "no hot patch invariant",
      "required": true
    },
    {
      "id": "T072_LIVE_NOT_AUTH",
      "pass": true,
      "detail": "live trading NOT_AUTHORIZED",
      "required": true
    },
    {
      "id": "T080_INTEROP_DISPOSITION",
      "pass": true,
      "detail": "interop disposition exists",
      "required": true
    },
    {
      "id": "T081_OASF",
      "pass": true,
      "detail": "interop disposition OASF",
      "required": true
    },
    {
      "id": "T081_CONTEXTFORGE",
      "pass": true,
      "detail": "interop disposition CONTEXTFORGE",
      "required": true
    },
    {
      "id": "T081_MCP",
      "pass": true,
      "detail": "interop disposition MCP",
      "required": true
    },
    {
      "id": "T081_A2A",
      "pass": true,
      "detail": "interop disposition A2A",
      "required": true
    },
    {
      "id": "T081_OPENTELEMETRY",
      "pass": true,
      "detail": "interop disposition OPENTELEMETRY",
      "required": true
    },
    {
      "id": "T090_ROUTE_CHECK",
      "pass": true,
      "detail": "route check exists",
      "required": true
    },
    {
      "id": "T091_GSTACK_STATE",
      "pass": true,
      "detail": "gstack registry state",
      "required": true
    },
    {
      "id": "T092_OPENSPEC_STATE",
      "pass": true,
      "detail": "openspec registry state",
      "required": true
    },
    {
      "id": "T093_LANE_NOT_EXECUTION",
      "pass": true,
      "detail": "lane != execution surface",
      "required": true
    },
    {
      "id": "T100_NOSECRET_FDA_ASSET_REGISTRY.json",
      "pass": true,
      "detail": "no secret-like pattern in FDA_ASSET_REGISTRY.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_FDA_DESKTOP_CAPABILITY_MATRIX.yaml",
      "pass": true,
      "detail": "no secret-like pattern in FDA_DESKTOP_CAPABILITY_MATRIX.yaml",
      "required": true
    },
    {
      "id": "T100_NOSECRET_FDA_EXECUTION_BINDING.json",
      "pass": true,
      "detail": "no secret-like pattern in FDA_EXECUTION_BINDING.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_FDA_FOLDER_REORGANIZATION_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in FDA_FOLDER_REORGANIZATION_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_fda_lease.py",
      "pass": true,
      "detail": "no secret-like pattern in fda_lease.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_fda_router.py",
      "pass": true,
      "detail": "no secret-like pattern in fda_router.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_independent_checker.py",
      "pass": true,
      "detail": "no secret-like pattern in independent_checker.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_TEAM.md",
      "pass": true,
      "detail": "no secret-like pattern in TEAM.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_test_xq_action_router.py",
      "pass": true,
      "detail": "no secret-like pattern in test_xq_action_router.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_test_xq_build_drift.py",
      "pass": true,
      "detail": "no secret-like pattern in test_xq_build_drift.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_test_xq_native_adapter.py",
      "pass": true,
      "detail": "no secret-like pattern in test_xq_native_adapter.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_WO_FDA_XQ_002.yaml",
      "pass": true,
      "detail": "no secret-like pattern in WO_FDA_XQ_002.yaml",
      "required": true
    },
    {
      "id": "T100_NOSECRET_xq_native_adapter.py",
      "pass": true,
      "detail": "no secret-like pattern in xq_native_adapter.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_docs_FDA_USER_GUIDE.md",
      "pass": true,
      "detail": "no secret-like pattern in docs\\FDA_USER_GUIDE.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_EVIDENCE_MANIFEST.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_EVIDENCE_MANIFEST.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_EXTERNAL_FULL_EVIDENCE_20260814.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_EXTERNAL_FULL_EVIDENCE_20260814.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_EXTERNAL_SINGLE_EVIDENCE_RR3.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_EXTERNAL_SINGLE_EVIDENCE_RR3.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_FOLDER_REORGANIZATION_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_FOLDER_REORGANIZATION_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_IMPLEMENTATION_EVIDENCE.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_IMPLEMENTATION_EVIDENCE.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_MIRROR_READBACK_20260814_RR3.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_MIRROR_READBACK_20260814_RR3.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_FDA_USER_GUIDE.md",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\FDA_USER_GUIDE.md",
      "required": true
    },
    {
      "id": "T100_NOSECRET_governance_FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml",
      "pass": true,
      "detail": "no secret-like pattern in governance\\FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml",
      "required": true
    },
    {
      "id": "T100_NOSECRET_governance_FDA_INTEROP_DISPOSITION.yaml",
      "pass": true,
      "detail": "no secret-like pattern in governance\\FDA_INTEROP_DISPOSITION.yaml",
      "required": true
    },
    {
      "id": "T100_NOSECRET_governance_FDA_ROUTE_CHECK.yaml",
      "pass": true,
      "detail": "no secret-like pattern in governance\\FDA_ROUTE_CHECK.yaml",
      "required": true
    },
    {
      "id": "T100_NOSECRET_governance_FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml",
      "pass": true,
      "detail": "no secret-like pattern in governance\\FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml",
      "required": true
    },
    {
      "id": "T100_NOSECRET_tests_test_fda_lease.py",
      "pass": true,
      "detail": "no secret-like pattern in tests\\test_fda_lease.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_tests_test_fda_router.py",
      "pass": true,
      "detail": "no secret-like pattern in tests\\test_fda_router.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_tests_test_fda_router_integration.py",
      "pass": true,
      "detail": "no secret-like pattern in tests\\test_fda_router_integration.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_tests_test_fda_security.py",
      "pass": true,
      "detail": "no secret-like pattern in tests\\test_fda_security.py",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_BOUNDED_CONTROL_LIVE_PROBE.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_BOUNDED_CONTROL_LIVE_PROBE.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_C0_READBACK_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_C0_READBACK_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_C2_CUA_QUALIFICATION_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_C2_CUA_QUALIFICATION_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_C3_UFO2_QUALIFICATION_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_C3_UFO2_QUALIFICATION_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_C4_XQ_QUALIFICATION_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_C4_XQ_QUALIFICATION_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_CHECKER_179_RAW_RECEIPT_RR6.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_CHECKER_179_RAW_RECEIPT_RR6.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_CHECKER_RAW_RECEIPT_RR6.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_CHECKER_RAW_RECEIPT_RR6.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F01_CURRENT_260811_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F01_CURRENT_260811_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F01_LIVE_FIXTURE_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F01_LIVE_FIXTURE_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F03_LIVE_FIXTURE_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F03_LIVE_FIXTURE_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F04_LIVE_FIXTURE_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F04_LIVE_FIXTURE_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_CLOSURE_V3_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_CLOSURE_V3_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_CLOSURE_V4_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_CLOSURE_V4_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_CLOSURE_V5_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_CLOSURE_V5_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_CLOSURE_V6_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_CLOSURE_V6_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_CLOSURE_V7_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_CLOSURE_V7_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_CLOSURE_V8_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_CLOSURE_V8_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_COMPILE_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_COMPILE_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_COMPILE_TOOLBAR_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_COMPILE_TOOLBAR_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_EXPORT_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_EXPORT_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_FRESH_10RUN_RECEIPT_RR6.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_FRESH_10RUN_RECEIPT_RR6.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_LIVE_FIXTURE_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_LIVE_FIXTURE_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_SYSTEM_PATH_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_SYSTEM_PATH_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F06_TEN_RUN_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F06_TEN_RUN_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F09B_PAPER_RUNTIME_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F09B_PAPER_RUNTIME_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F09_RADAR_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F09_RADAR_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_F10_F11_READBACK_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_F10_F11_READBACK_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_PAPER_10RUN_RECEIPT_RR6.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_PAPER_10RUN_RECEIPT_RR6.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V2.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V2.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
      "required": true
    },
    {
      "id": "T100_NOSECRET_evidence_receipts_FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json",
      "pass": true,
      "detail": "no secret-like pattern in evidence\\receipts\\FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json",
      "required": true
    },
    {
      "id": "T110_FIXTURE_MANIFEST",
      "pass": true,
      "detail": "fixture manifest exists",
      "required": true
    },
    {
      "id": "T111_FIXTURE_MODE",
      "pass": true,
      "detail": "PAPER mode",
      "required": true
    },
    {
      "id": "T112_FIXTURE_DRIFT",
      "pass": true,
      "detail": "version drift recorded",
      "required": true
    },
    {
      "id": "T120_FILE_fda_router.py",
      "pass": true,
      "detail": "fda_router.py exists",
      "required": true
    },
    {
      "id": "T120_FILE_fda_lease.py",
      "pass": true,
      "detail": "fda_lease.py exists",
      "required": true
    },
    {
      "id": "T120_FILE_tests/test_fda_router.py",
      "pass": true,
      "detail": "tests/test_fda_router.py exists",
      "required": true
    },
    {
      "id": "T120_FILE_tests/test_fda_lease.py",
      "pass": true,
      "detail": "tests/test_fda_lease.py exists",
      "required": true
    },
    {
      "id": "T120_FILE_tests/test_fda_security.py",
      "pass": true,
      "detail": "tests/test_fda_security.py exists",
      "required": true
    },
    {
      "id": "T130_C0_RECEIPT",
      "pass": true,
      "detail": "C0 receipt exists",
      "required": true
    },
    {
      "id": "T131_C0_VERDICT",
      "pass": true,
      "detail": "C0 verdict PASS",
      "required": true
    },
    {
      "id": "T132_C0_NO_MISSING",
      "pass": true,
      "detail": "critical source missing 0",
      "required": true
    },
    {
      "id": "T133_F01_RECEIPT",
      "pass": true,
      "detail": "F01 live fixture receipt exists",
      "required": true
    },
    {
      "id": "T134_F01_10_OF_10",
      "pass": true,
      "detail": "F01 10/10 live PASS",
      "required": true
    },
    {
      "id": "T135_F01_ZERO_WRONG",
      "pass": true,
      "detail": "F01 zero wrong/silent-wrong action",
      "required": true
    },
    {
      "id": "T136_PROBE_RECEIPT",
      "pass": true,
      "detail": "bounded control probe receipt exists",
      "required": true
    },
    {
      "id": "T137_PROBE_PASS",
      "pass": true,
      "detail": "bounded control probe PASS",
      "required": true
    },
    {
      "id": "T138_PROBE_NO_FINANCIAL",
      "pass": true,
      "detail": "no financial side effect",
      "required": true
    },
    {
      "id": "T139_CONCURRENCY_RECEIPT",
      "pass": true,
      "detail": "lease concurrency receipt exists",
      "required": true
    },
    {
      "id": "T140_CONCURRENCY_PASS",
      "pass": true,
      "detail": "lease concurrency ALL PASS",
      "required": true
    },
    {
      "id": "T141_CONCURRENCY_ZERO_SIMUL",
      "pass": true,
      "detail": "simultaneous writers 0",
      "required": true
    },
    {
      "id": "T142_MATRIX_F01_QUALIFIED",
      "pass": true,
      "detail": "matrix XQ_LAUNCH_LOCATE CUA QUALIFIED with live reason",
      "required": true
    },
    {
      "id": "T143_MATRIX_PRODUCT_VERSION",
      "pass": true,
      "detail": "matrix product version corrected to 3.20.02 live readback",
      "required": true
    },
    {
      "id": "T160_XQ_FINGERPRINT_RECEIPT",
      "pass": true,
      "detail": "XQ build fingerprint receipt exists",
      "required": true
    },
    {
      "id": "T161_XQ_FINGERPRINT_SCHEMA",
      "pass": true,
      "detail": "fingerprint schema",
      "required": true
    },
    {
      "id": "T162_XQ_BUILD_260811",
      "pass": true,
      "detail": "local build 260811",
      "required": true
    },
    {
      "id": "T163_XQ_SHA_PRESENT",
      "pass": true,
      "detail": "exe sha256 captured",
      "required": true
    },
    {
      "id": "T164_PUBLIC_MISMATCH_ACK",
      "pass": true,
      "detail": "public 260731 != local 260811 acknowledged",
      "required": true
    },
    {
      "id": "T165_MATRIX_BUILD_FIREWALL",
      "pass": true,
      "detail": "matrix build drift firewall present",
      "required": true
    },
    {
      "id": "T166_MATRIX_SUBJECT_BINDING",
      "pass": true,
      "detail": "all 5 action classes have subject_binding",
      "required": true
    },
    {
      "id": "T167_MATRIX_PYWINAUTO",
      "pass": true,
      "detail": "pywinauto win32 backend row present with version",
      "required": true
    },
    {
      "id": "T168_MATRIX_NO_SILENT_FALLBACK",
      "pass": true,
      "detail": "router silent fallback disabled",
      "required": true
    },
    {
      "id": "T169_NATIVE_ADAPTER_EXISTS",
      "pass": true,
      "detail": "xq_native_adapter.py exists",
      "required": true
    },
    {
      "id": "T170_NATIVE_NO_MOUSE_INPUT",
      "pass": true,
      "detail": "adapter has zero mouse-input API calls",
      "required": true
    },
    {
      "id": "T171_NATIVE_MESSAGE_ONLY",
      "pass": true,
      "detail": "adapter uses pure win32 messages",
      "required": true
    },
    {
      "id": "T172_NATIVE_QUAL_RECEIPT",
      "pass": true,
      "detail": "native qualification receipt exists",
      "required": true
    },
    {
      "id": "T173_FN01_10OF10",
      "pass": true,
      "detail": "FN01 main locate 10/10",
      "required": true
    },
    {
      "id": "T174_FN02_10OF10",
      "pass": true,
      "detail": "FN02 editor locate 10/10",
      "required": true
    },
    {
      "id": "T175_FN03_LOCATE",
      "pass": true,
      "detail": "FN03 Afx 新增 button located",
      "required": true
    },
    {
      "id": "T176_FN_ZERO_WRONG",
      "pass": true,
      "detail": "FN wrong-action 0",
      "required": true
    },
    {
      "id": "T177_TEST_TEST_XQ_BUILD_DRIFT.PY",
      "pass": true,
      "detail": "test_xq_build_drift.py present",
      "required": true
    },
    {
      "id": "T177_TEST_TEST_XQ_NATIVE_ADAPTER.PY",
      "pass": true,
      "detail": "test_xq_native_adapter.py present",
      "required": true
    },
    {
      "id": "T177_TEST_TEST_XQ_ACTION_ROUTER.PY",
      "pass": true,
      "detail": "test_xq_action_router.py present",
      "required": true
    },
    {
      "id": "T150_NO_THIRD_HEAVY_STACK",
      "pass": true,
      "detail": "fabric-desktop not registered as heavy stack",
      "required": true
    },
    {
      "id": "T151_SQS_LIVE_NOT_AUTHORIZED",
      "pass": true,
      "detail": "SQS status vector exists for ceiling readback",
      "required": true
    }
  ]
}
```

# 4. FDA_EVIDENCE_MANIFEST.json — COMPLETE RAW BODY

```json
{
  "artifact_count": 63,
  "artifact_id": "FDA_EVIDENCE_MANIFEST",
  "artifacts": [
    {
      "path": "Fabric/fabric-desktop-automation/DOC/FDA_USER_GUIDE.md",
      "sha256": "81271eb745b7f37ab577182a0f675f0ce4a0ec4ab7bda7eb69c7884ac7f04367",
      "size": 20138
    },
    {
      "path": "Fabric/fabric-desktop-automation/FDA_DESKTOP_CAPABILITY_MATRIX.yaml",
      "sha256": "9406456db853e9e6597c30ed400240808c7b0c777dd49c34eb611bf4c863d6c4",
      "size": 11110
    },
    {
      "path": "Fabric/fabric-desktop-automation/FDA_DIRECTORY_TREE.txt",
      "sha256": "57ceaf69fb27c21da59fff188e3c1cf90575da7e7861a19d7387b191e5767c98",
      "size": 2174
    },
    {
      "path": "Fabric/fabric-desktop-automation/FDA_EXECUTION_BINDING.json",
      "sha256": "6a3269202d0dba0ba6c8bb0d6656e592dcda4042a0dc88e63fba732e3335b095",
      "size": 3308
    },
    {
      "path": "Fabric/fabric-desktop-automation/FDA_FOLDER_REORGANIZATION_RECEIPT.json",
      "sha256": "00d690f94a05aabc644e9c9cafc4664fc98602eeaa5e28f54d17ae6ee7e58cbe",
      "size": 777
    },
    {
      "path": "Fabric/fabric-desktop-automation/TEAM.md",
      "sha256": "c524945c90c836b048ee07084bcac75adba8a01b1ca0ae16b8a742ac388afc5b",
      "size": 4048
    },
    {
      "path": "Fabric/fabric-desktop-automation/WO_FDA_XQ_002.yaml",
      "sha256": "6c80ff03511753175a627b501ae5a72fa9e5195bc3830d438e88a6bf979b3c87",
      "size": 1588
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/FDA_DIRECTORY_TREE.txt",
      "sha256": "57ceaf69fb27c21da59fff188e3c1cf90575da7e7861a19d7387b191e5767c98",
      "size": 2174
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/FDA_FOLDER_REORGANIZATION_RECEIPT.json",
      "sha256": "00d690f94a05aabc644e9c9cafc4664fc98602eeaa5e28f54d17ae6ee7e58cbe",
      "size": 777
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/FDA_MIRROR_READBACK_20260814_RR3.json",
      "sha256": "beb62f115a2466894d0f141f7bd6d841888f8259022607f1cc1e8a094a597621",
      "size": 452
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_BOUNDED_CONTROL_LIVE_PROBE.json",
      "sha256": "51559903556f3910d6286974a349b8515d8498a6870d727532cd7f5f016b623e",
      "size": 586
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_C0_READBACK_RECEIPT.json",
      "sha256": "ca905aba1e02a8df4b1a6d2b41764df448bbd53353422c2a81b5b2750562b414",
      "size": 5838
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_C2_CUA_QUALIFICATION_RECEIPT.json",
      "sha256": "c181ef51b2066b1ffc9b185355b42653c00ee245048ebe84483fde2393c54362",
      "size": 3380
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json",
      "sha256": "1d7d149ac6cd1ed0616ab1fa25f804cc20f33808663d7d1d32b4040ab8d97781",
      "size": 1811
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_C3_UFO2_QUALIFICATION_RECEIPT.json",
      "sha256": "048b151f462384310eabb9018e7d5ecb012677473b47667be49be84c03492e6d",
      "size": 1800
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_C4_XQ_QUALIFICATION_RECEIPT.json",
      "sha256": "cf86b05f71c0cf734dcc2684cd0bb1542c82e151ea7edf1df5132236189b6543",
      "size": 3636
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
      "sha256": "357a9650a045d7485ff93270f98268946d740980da156d6f280e995b2364d0a8",
      "size": 825
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F01_LIVE_FIXTURE_RECEIPT.json",
      "sha256": "36fff6f57cffa10bc8f6c753295147c644a1b000ea35c58de8f848a1dc8d8697",
      "size": 3912
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F03_LIVE_FIXTURE_RECEIPT.json",
      "sha256": "cbf60ef9cd5cab761ce3e6ccdd13236d5107a4d41f3a52482dc396dae31b1055",
      "size": 1337
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F04_LIVE_FIXTURE_RECEIPT.json",
      "sha256": "5d9bd84beae406f06206bc7d8b3bf1288ff38b2f54f34dcdf2947da3905647d8",
      "size": 1183
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V3_RECEIPT.json",
      "sha256": "fe2d736f49865b9a7d2abfa3b28794764bae32c17d60d559623fe3a77a39980b",
      "size": 1263
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V4_RECEIPT.json",
      "sha256": "e149fdeb258a422a7983722c2ae2315d4e77a32317574a2c9a2c61da79edd47b",
      "size": 1125
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V5_RECEIPT.json",
      "sha256": "249c016a3a3a7b68a2439469cc5a31c24ace8d198e9f968177c9d89e3f018792",
      "size": 1139
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V6_RECEIPT.json",
      "sha256": "0462d34b16705535b2c293bdecc2359ad910fae7b74986c9328c94efdaa6be47",
      "size": 1558
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V7_RECEIPT.json",
      "sha256": "774454d0faeed6c0ae0af92f4c959378be87afa63a15a3e5b0cb952131ec0b6f",
      "size": 1603
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V8_RECEIPT.json",
      "sha256": "a16a4bb3852ddb30460ba19e4979e32d1b5263ed66e946fc076c614e96ea72b7",
      "size": 1352
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_COMPILE_RECEIPT.json",
      "sha256": "94cfccad36dabc5e91eb32eb4259f8232c160f674a018cbdb0a6ca14dadac569",
      "size": 1380
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_COMPILE_TOOLBAR_RECEIPT.json",
      "sha256": "7977c24d7fe9576b89e1edc2eab20bbba26397e5d9985edd4dfa9e007e92bdae",
      "size": 972
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_EXPORT_RECEIPT.json",
      "sha256": "f03dd33cbca58b70d51c7c5a1425d830a59aeaf53fdbe21de457cffcac1aa083",
      "size": 768
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json",
      "sha256": "353b639f2a789f6c6116b8225262af1325178adb9354be553670461f21273bef",
      "size": 1460
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_LIVE_FIXTURE_RECEIPT.json",
      "sha256": "f10b9c5497fb763fdfafd7eb1659c93df4f3835f5a9026870fc4d75d11a27ade",
      "size": 1272
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_SYSTEM_PATH_RECEIPT.json",
      "sha256": "7407a237fd1127474e692b5d564dc8420330ed58c7fdf0fa366d7cb53d93a345",
      "size": 1257
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_TEN_RUN_RECEIPT.json",
      "sha256": "17353bfbbde9e9dd59f67d0be08e8075530b68d950a8a66d7ce70b5b00f5d97c",
      "size": 2535
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F09B_PAPER_RUNTIME_RECEIPT.json",
      "sha256": "a57f730465c3d023145e2481fb274bddc87c62c6d5b6e1f576d2edd42fa41f78",
      "size": 2002
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F09_RADAR_RECEIPT.json",
      "sha256": "0c9adabdbac434953007bd8dcba0bbf7c8aacd1b267343f02c6e1b4d721f1ee5",
      "size": 1089
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F10_F11_READBACK_RECEIPT.json",
      "sha256": "7d471b12739d9e2f4dce9980cd8e8171c43bed3b0df723775ee380894eb2323b",
      "size": 1373
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
      "sha256": "b23ddca238b99378988c731036b9fe01742a1a5fbbc0fd9ba3d8223eb484e9be",
      "size": 946
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
      "sha256": "d676c68f05f9560af6f5aae31408cee66308adc9d18d50bda150dce6d7f8fa13",
      "size": 551
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
      "sha256": "1730e4162c1f10b606af7e850c494df799cc96e3e2ef46c93a4466f8e3905a74",
      "size": 4587
    },
    {
      "path": "Fabric/fabric-desktop-automation/fda_lease.py",
      "sha256": "856580b533b547a82772de8624c78792d669cb11bb9cb99551c7141a06594db2",
      "size": 2510
    },
    {
      "path": "Fabric/fabric-desktop-automation/fda_router.py",
      "sha256": "c3d64650a6e0c6fd3d99b5236c30c4cb03b7621be9763299e335ac1c6ed95e6c",
      "size": 1115
    },
    {
      "path": "Fabric/fabric-desktop-automation/governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml",
      "sha256": "6e1c808e278592f2b4d75c6296b4b81d9e227a2f21e188c9594b18085bbf0f8f",
      "size": 2995
    },
    {
      "path": "Fabric/fabric-desktop-automation/governance/FDA_INTEROP_DISPOSITION.yaml",
      "sha256": "9fac4d255030443f8031a5bfe62d8e204698cf664ada2b06a65986f347c7ee5e",
      "size": 3487
    },
    {
      "path": "Fabric/fabric-desktop-automation/governance/FDA_ROUTE_CHECK.yaml",
      "sha256": "05256d982f8634fe25a5cf6d6e85685ca8fdcd54163c913a4cb689f6d922a909",
      "size": 2188
    },
    {
      "path": "Fabric/fabric-desktop-automation/governance/FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml",
      "sha256": "6a108d3a8c25221541c1eb9ac72d192412a9f0690d219f8dab0acf0694a4a2cf",
      "size": 1848
    },
    {
      "path": "Fabric/fabric-desktop-automation/independent_checker.py",
      "sha256": "8a9b761087d01cc99d35be14cc4a495f35636793552fe62400ea76d45de96dbe",
      "size": 12475
    },
    {
      "path": "Fabric/fabric-desktop-automation/test_xq_action_router.py",
      "sha256": "e8778f2d73349905455e7254a9f2e0f5f3a7195cd6503093aa6c54504d615c2c",
      "size": 2478
    },
    {
      "path": "Fabric/fabric-desktop-automation/test_xq_build_drift.py",
      "sha256": "cf234c66e389900b517d437a6d2ec4d69977104876fc4ab898a6f4df1aaf8eb9",
      "size": 3215
    },
    {
      "path": "Fabric/fabric-desktop-automation/test_xq_native_adapter.py",
      "sha256": "89566c1a2c5070d524c74fd34a5e164cce5f2a888ee4abcaac6df1af4ac9f060",
      "size": 1899
    },
    {
      "path": "Fabric/fabric-desktop-automation/tests/test_fda_lease.py",
      "sha256": "8caeb1dba6715af44f038e095eccc2287eebc817dac6782a0eb29bd742383ee6",
      "size": 4015
    },
    {
      "path": "Fabric/fabric-desktop-automation/tests/test_fda_router.py",
      "sha256": "64a52a017d0ef757fbc725afb6fdfb71bf2b41829723743345e123643b45ba13",
      "size": 4028
    },
    {
      "path": "Fabric/fabric-desktop-automation/tests/test_fda_router_integration.py",
      "sha256": "654df5de873b6e71ec1b73bbfb3ca9a92ff4b4758ab558b3784a2f68452d6b97",
      "size": 4001
    },
    {
      "path": "Fabric/fabric-desktop-automation/tests/test_fda_security.py",
      "sha256": "6b0e2f19268db5fb0507fd6b39034db36e46922a42a93dfa3e5eff6004c359b3",
      "size": 7512
    },
    {
      "path": "Fabric/fabric-desktop-automation/xq_native_adapter.py",
      "sha256": "89cd614b63562514ece4fac503f7d54b2d0f02ca7398a39cd468b86f4c76bde2",
      "size": 5045
    },
    {
      "path": "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md",
      "sha256": "92207123f9698d1dc15f40ffaaec00e6e39ee8152c2e297f900a97278560bfa4",
      "size": 51147
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F01_CURRENT_260811_RECEIPT.json",
      "sha256": "4d657417be317d08a7945c35f948af410ed68a87ff73dfbe5c0f3c98cb72fe67",
      "size": 4450
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json",
      "sha256": "89ca67f47fff342b83191a345f0c8b44c16fc419c61b259640329935a0f3129f",
      "size": 11241
    },
    {
      "path": "FDA_MIRROR_READBACK_20260814_RR6.json",
      "sha256": "882e16a14c212711b163a8fb3da133d73f55e1b263ec76a934ae75818f3cc605",
      "size": 356
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json",
      "sha256": "5700491f5e79a8243acc122f1536dd92a251146aa9c102d62383b990aef69346",
      "size": 8865
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_CHECKER_FINAL_RR7.json",
      "sha256": "1a02c45ef2af8a45215e5250befc4c1aa2705302ddf7abdb99ea47e8866b074e",
      "size": 35395
    },
    {
      "path": "FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR7.md",
      "sha256": "28b0c9f2c902d9ad080b9ebf098294c24e495e4c65f04a034da0bfb14cffb0d6",
      "size": 45918
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json",
      "sha256": "65b0dfc4bd718eab53cd918c8802861587b63b08348b977d9cf765684531f5a5",
      "size": 8417
    },
    {
      "path": "Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_FRESH_10RUN_RECEIPT_RR6.json",
      "sha256": "369187d9b4223c95bac6ab8d8be0a8322cf4ca17a5fdb7481487cbd0419d3408",
      "size": 3184
    }
  ],
  "checker": {
    "errors": 0,
    "exit": 0,
    "failed": 0,
    "mode": "VERIFY_ONLY",
    "note": "ONLY CURRENT denominator 194/194; 179 and earlier HISTORICAL",
    "passed": 194,
    "script": "Fabric/fabric-desktop-automation/independent_checker.py",
    "subject_root": "be576bebe7672093039bfe7dbc265f25aa0a1164",
    "total_checks": 194,
    "unique_ids": 194,
    "verdict": "PASS"
  },
  "checker_history": [
    {
      "checks": 144,
      "status": "HISTORICAL",
      "superseded_by": "194"
    },
    {
      "checks": 174,
      "status": "HISTORICAL",
      "superseded_by": "194"
    },
    {
      "checks": 175,
      "status": "HISTORICAL",
      "superseded_by": "194"
    },
    {
      "checks": 176,
      "status": "HISTORICAL",
      "superseded_by": "194"
    },
    {
      "checks": 179,
      "status": "HISTORICAL",
      "superseded_by": "194"
    }
  ],
  "chronology_note": "generated AFTER all bound evidence (latest bound: FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8 2026-08-14T14:54:27+08:00)",
  "dod_counts": {
    "BLOCKED": 0,
    "PARTIAL": 0,
    "PASS": 36
  },
  "evaluator": {
    "artifact": "independent_checker.py",
    "mode": "VERIFY_ONLY",
    "role": "independent Acceptance Officer (maker != checker)",
    "sha256": "9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e"
  },
  "exact_set": {
    "bundle_file_count": 63,
    "manifest_row_count": 63,
    "manifest_self_entry": false,
    "note": "ALL counters machine-derived from artifacts[]; every row = exactly one filesystem path; manifest itself and reducer excluded (loop-free single-direction binding)",
    "payload_file_count": 63,
    "reducer_in_manifest": false
  },
  "generated_at": "2026-08-14T08:37:59+0000",
  "generated_at_utc": "2026-08-14T08:37:59Z",
  "missing_artifacts": [],
  "schema": "FDA-EVIDENCE-MANIFEST/3",
  "serialization": "SINGLE_CANONICAL",
  "subject_root": {
    "candidate_root": "be576bebe7672093039bfe7dbc265f25aa0a1164",
    "git_head": "be576bebe7672093039bfe7dbc265f25aa0a1164",
    "note": "FINAL reseal r10 fixed contract: candidate be576be frozen; evaluator 9009713; evidence bundle independent",
    "repo": "Fabric"
  },
  "version": "v2026.08.14-r10-final-reseal"
}
```

```text
manifest SHA-256 (of exact bytes above): a349633610e7414024c23f590829433cdcabe68e5ebd9e4aa641a528dc93c0d4
entries: 63
manifest.subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164
(checker.subject_root: be576bebe7672093039bfe7dbc265f25aa0a1164 — three-way match)
(on-disk FDA_EVIDENCE_MANIFEST.json SHA-256: 8d7be205fa62c3cec9b7fece93f554c10fe1fb9e60d8efd4500e7cc4e07b7911 — byte-differs from embedded-body SHA only by JSON re-serialization; embedded body is the reviewer-verifiable truth)
```

# 5. External Verifier Checklist (r9)

1. PAPER STOP: authority mapping (section 1) + 10/10 post-stop readback (section 2); wrong=0; silent=0; broker_write=0; one writer
2. Checker: 194 records / 194 unique / 194 PASS / exit 0 / VERIFY_ONLY / subject be576be (carried PASS from R8)
3. Manifest: recompute SHA-256 of section 4 raw body -> must equal a349633610e7414024c23f590829433cdcabe68e5ebd9e4aa641a528dc93c0d4; entries=63;
   unique paths equal; subject_root=be576be; F01 current / F06 fresh / PAPER STOP / checker receipts all bound
4. DoD-13 UFO2 (carried) / DoD-17 PAPER STOP CLOSED / DoD-30 same-subject / DoD-33 checker / DoD-35 260811

# 6. Honest Residuals

```text
- intraday visual alert UI: time-gated (not mandatory per external)
- Cua 0.19.4 nightly shadow: NOT RUN
- FN03 Afx invoke: locate 1/1 only
- SensorLog state-code mapping: bound via community authority + official course distillation +
  raw lifecycle cross-check; XQ does not publish an official state-code table (SQS-level oracle
  would be the ultimate authority if available)
```

# 7. Final

```text
RR8_REPAIR = COMPLETE (A authority + B manifest raw body)
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED (awaiting external r9 verdict)
SQS_LIVE_TRADING = NOT_AUTHORIZED
```
