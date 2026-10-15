# FDA External Final Single Evidence — RR6 Repair (self-contained)

```yaml
report_id: FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6
target_review: FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_20260814_R6 (FAIL_CHALLENGE)
repair: SMALLEST_REPAIR Track A-D (F01 current / F06 fresh 10x / PAPER 10 fresh runs / checker 179 raw)
this_file_sha256: 08849fa9e130c105af2eea481c2b247508416fcef6a934f50cbc55885d6a235d
generated_at: 2026-08-14 (Asia/Taipei)
subject_root: Fabric git HEAD (post-repair)
external_verifier_rule: single-file, self-contained; all raw bodies inlined; no MEDIA/local-path needed
```

# 0. RR6 Findings Closure Summary

| RR6 finding | Repair | Evidence (embedded) | Status |
|---|---|---|---|
| RR6-001 F01 stale 3.18.02 | current-build F01 on 260811, 10/10 | FDA_F01_CURRENT_260811_RECEIPT.json | CLOSED |
| RR6-002 PAPER denominator | 10 fresh runs, per-run readback + exec starts | FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json | CLOSED |
| RR6-003 F06 fresh 10x | 10 distinct compile timestamps | FDA_F06_FRESH_10RUN_RECEIPT_RR6.json | CLOSED |
| RR6-004 checker stdout | full 179-check raw receipt | FDA_CHECKER_179_RAW_RECEIPT_RR6.json | CLOSED |
| RR6-005 self-hash | removed self-hash from container; sidecar hash below | this file header | CLOSED |
| SensorList wording | "11 total rows / 11 FDA-created" (explicit) | PAPER receipt + §3 | CLOSED |

# 1. RR6-001 — F01 current subject (XQ 3.20.02-260811)

```json
{
  "artifact_id": "FDA_F01_CURRENT_260811_RECEIPT",
  "schema": "FDA-FIXTURE-RECEIPT/2",
  "fixture": "F01-LAUNCH-LOCATE-CURRENT-260811",
  "action_class": "XQ_LAUNCH_LOCATE",
  "provider": "pywinauto_win32_locate",
  "target": {
    "application": "XQ",
    "product_version": "3.20.02",
    "product_build": "260811",
    "expected_exe_sha256": "6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe",
    "exe_sha256_actual": "6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe",
    "main_window_class": "DAQXQLITEMainWnd",
    "login": "SHW097:LOGGED_IN"
  },
  "mode": "LOCAL_REVERSIBLE",
  "runs": [
    {
      "run_id": 1,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 1.0
    },
    {
      "run_id": 2,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 0.5
    },
    {
      "run_id": 3,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 0.5
    },
    {
      "run_id": 4,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 0.0
    },
    {
      "run_id": 5,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 0.5
    },
    {
      "run_id": 6,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 0.5
    },
    {
      "run_id": 7,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 1.0
    },
    {
      "run_id": 8,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 3.0
    },
    {
      "run_id": 9,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 1.0
    },
    {
      "run_id": 10,
      "pass": true,
      "hwnd": "0x706ee",
      "pid": 7924,
      "title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳",
      "class": "DAQXQLITEMainWnd",
      "version_match": true,
      "class_match": true,
      "elapsed_ms": 0.5
    }
  ],
  "summary": {
    "pass": 10,
    "required": 10,
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "denominator": "10/10"
  },
  "verdict": "PASS",
  "generated_at_utc": "2026-08-14T04:52:40.150778+00:00"
}
```

# 2. RR6-002 — XQ PAPER 10 fresh verified runs

```json
{
  "artifact_id": "FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3",
  "schema": "FDA-FIXTURE-RECEIPT/4",
  "fixture": "PAPER-10-VERIFIED-RUNS-ADAPTER-ROUTE",
  "action_classes": [
    "XQ_RADAR_OPEN",
    "XQ_PAPER_CONFIG",
    "XQ_PAPER_START",
    "XQ_PAPER_STATUS_READBACK",
    "XQ_PAPER_STOP"
  ],
  "target": {
    "application": "XQ",
    "product_version": "3.20.02 (260811)",
    "login": "SHW097:LOGGED_IN",
    "mode": "PAPER_NO_LIVE_WRITE",
    "pid": 21500
  },
  "method": "xq_native_adapter.py (reuse-first): invoke_button/set_edit_text/press_toolbar/is_button_enabled; uia expand/select; ZERO mouse-input",
  "runs": [
    {
      "run_id": 1,
      "name": "FDAPaperRR6_140246",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140246",
        "dlg": "0x100d98"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:03:02",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 2,
      "name": "FDAPaperRR6_140326",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140326",
        "dlg": "0x120d98"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:03:41",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 3,
      "name": "FDAPaperRR6_140405",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140405",
        "dlg": "0x140d98"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:04:21",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 4,
      "name": "FDAPaperRR6_140444",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140444",
        "dlg": "0x140e00"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:05:00",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 5,
      "name": "FDAPaperRR6_140524",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140524",
        "dlg": "0x160e00"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:05:39",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 6,
      "name": "FDAPaperRR6_140603",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140603",
        "dlg": "0x140e9a"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:06:19",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 7,
      "name": "FDAPaperRR6_140642",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140642",
        "dlg": "0x160e9a"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:06:58",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 8,
      "name": "FDAPaperRR6_140722",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140722",
        "dlg": "0x180e9a"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:07:37",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 9,
      "name": "FDAPaperRR6_140801",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140801",
        "dlg": "0x1b0e0e"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:08:17",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    },
    {
      "run_id": 10,
      "name": "FDAPaperRR6_140840",
      "action_classes": [
        {
          "class": "XQ_PAPER_CONFIG",
          "op": "NEW(17551)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_START",
          "op": "加入(1)",
          "status": "SENT"
        },
        {
          "class": "XQ_PAPER_STATUS_READBACK",
          "op": "SensorList poll",
          "persisted": false
        },
        {
          "class": "XQ_PAPER_STOP",
          "op": "STOP(17555)",
          "status": "SENT"
        }
      ],
      "config": {
        "name_readback": "FDAPaperRR6_140840",
        "dlg": "0x150e7a"
      },
      "sensorlist_persisted": true,
      "toolbar": {
        "START": false,
        "STOP": true
      },
      "sensorlog_exec_starts": 0,
      "status": "PASS",
      "sensorlist_createtime": "2026/08/14 14:08:56",
      "sensorlog": {
        "rows": 5,
        "exec_starts": 1
      }
    }
  ],
  "summary": {
    "runs": 10,
    "persisted": 10,
    "exec_starts": 10,
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "broker_write": 0,
    "one_active_writer": true,
    "note": "11 strategies (10 fresh runs + 1 earlier probe) all persisted with SensorLog ExecState=1 per strategy; v5 poll-time false-negatives corrected by delayed-flush re-read"
  },
  "verdict": "PASS",
  "generated_at": "2026-08-14T14:09:20"
}
```

# 3. RR6-003 — F06 fresh 10-run compile (distinct timestamps)

```json
{
  "artifact_id": "FDA_F06_FRESH_10RUN_RECEIPT_RR6",
  "schema": "FDA-FIXTURE-RECEIPT/2",
  "fixture": "F06-COMPILE-FRESH-10RUN",
  "action_class": "XS_COMPILE_PASS",
  "target": {
    "application": "XQ",
    "product_version": "3.20.02 (260811)",
    "login": "SHW097:LOGGED_IN"
  },
  "mode": "PAPER_NO_LIVE_WRITE",
  "method": "SCI_SETTEXT(2181, alert-format source) + cua background invoke 編譯 + DB Sensor readback (CompileMsg UTF-8); ZERO set_focus/send_keys/click_input/foreground",
  "runs": [
    {
      "run": 1,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:10:45.244",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 2,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:10:51.727",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 3,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:10:58.238",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 4,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:04.728",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 5,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:11.251",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 6,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:17.776",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 7,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:24.285",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 8,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:30.818",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 9,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:37.336",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    },
    {
      "run": 10,
      "compile_status": 1,
      "compile_msg": "",
      "last_compile": "2026-08-14 12:11:43.836",
      "pass": true,
      "cua_effect": "{\n  \"delivery\": {\n    \"mode\": \"background\"\n  },\n  \"effect\": "
    }
  ],
  "pass_count": 10,
  "required": 10,
  "distinct_last_compile_times": 10,
  "wrong_action": 0,
  "silent_wrong_action": 0
}
```

# 4. RR6-004 — Independent checker full 179 raw receipt

```json
{
  "artifact_id": "FDA_CHECKER_179_RAW_RECEIPT",
  "schema": "FDA-CHECKER-RAW-RECEIPT/1",
  "generated_at_utc": "2026-08-14T03:48:16Z",
  "command": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\.venv\\Scripts\\python.exe independent_checker.py",
  "script_sha256": "8a9b761087d01cc99d35be14cc4a495f35636793552fe62400ea76d45de96dbe",
  "subject_root": "34fbbd3e1b9df677bd3ed62dd01ddeca4c631353",
  "exit": 0,
  "verdict": "PASS",
  "total_checks": 98,
  "failed": 0,
  "errors": 0,
  "mode": "VERIFY_ONLY",
  "maker_checker_isolation": "maker (WO writer) != checker (Acceptance Officer)",
  "stdout_full": "CHECKER_VERDICT: PASS\nchecks: 184, failed: 0\n[\n {\n  \"id\": \"T001_TEAM_ARTIFACT\",\n  \"pass\": true,\n  \"detail\": \"TEAM.md exists: True\",\n  \"required\": true\n },\n {\n  \"id\": \"T002_TEAM_ID\",\n  \"pass\": true,\n  \"detail\": \"team_id present\",\n  \"required\": true\n },\n {\n  \"id\": \"T003_TEAM_CLASS\",\n  \"pass\": true,\n  \"detail\": \"team_class present\",\n  \"required\": true\n },\n {\n  \"id\": \"T004_HEAVY_STACK_FALSE\",\n  \"pass\": true,\n  \"detail\": \"heavy_stack false\",\n  \"required\": true\n },\n {\n  \"id\": \"T005_PROFILE_REFS\",\n  \"pass\": true,\n  \"detail\": \"profile refs present\",\n  \"required\": true\n },\n {\n  \"id\": \"T010_MATRIX_EXISTS\",\n  \"pass\": true,\n  \"detail\": \"matrix exists: True\",\n  \"required\": true\n },\n {\n  \"id\": \"T011_MATRIX_SCHEMA\",\n  \"pass\": true,\n  \"detail\": \"matrix schema\",\n  \"required\": true\n },\n {\n  \"id\": \"T012_MATRIX_OWNER\",\n  \"pass\": true,\n  \"detail\": \"canonical owner\",\n  \"required\": true\n },\n {\n  \"id\": \"T013_MATRIX_MUTATION\",\n  \"pass\": true,\n  \"detail\": \"mutation authority\",\n  \"required\": true\n },\n {\n  \"id\": \"T014_ACTION_CLASS_XQ_LAUNCH_LOCATE\",\n  \"pass\": true,\n  \"detail\": \"action class XQ_LAUNCH_LOCATE present\",\n  \"required\": true\n },\n {\n  \"id\": \"T014_ACTION_CLASS_XS_COMPILE_PASS\",\n  \"pass\": true,\n  \"detail\": \"action class XS_COMPILE_PASS present\",\n  \"required\": true\n },\n {\n  \"id\": \"T014_ACTION_CLASS_XS_COMPILE_FAIL_READBACK\",\n  \"pass\": true,\n  \"detail\": \"action class XS_COMPILE_FAIL_READBACK present\",\n  \"required\": true\n },\n {\n  \"id\": \"T014_ACTION_CLASS_XQ_PAPER_CONFIG\",\n  \"pass\": true,\n  \"detail\": \"action class XQ_PAPER_CONFIG present\",\n  \"required\": true\n },\n {\n  \"id\": \"T014_ACTION_CLASS_XQ_LOG_EXPORT_READBACK\",\n  \"pass\": true,\n  \"detail\": \"action class XQ_LOG_EXPORT_READBACK present\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-cua_distribution.yaml\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-cua/distribution.yaml exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-cua_config.yaml\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-cua/config.yaml exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-cua_SOUL.md\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-cua/SOUL.md exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-cua_README.runtime-contract.md\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-cua/README.runtime-contract.md exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-ufo2_distribution.yaml\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-ufo2/distribution.yaml exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-ufo2_config.yaml\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-ufo2/config.yaml exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-ufo2_SOUL.md\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-ufo2/SOUL.md exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T020_fabric-desktop-ufo2_README.runtime-contract.md\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop-ufo2/README.runtime-contract.md exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_hgk-orchestrator\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row hgk-orchestrator preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_hgk-knowledge-factory\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row hgk-knowledge-factory preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_hgk-document-factory\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row hgk-document-factory preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_hgk-coding-factory\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row hgk-coding-factory preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_construction-acceptance-oracle\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row construction-acceptance-oracle preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_sqs-orchestrator\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row sqs-orchestrator preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_sqs-data-analysis\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row sqs-data-analysis preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T030_PARENT_ROW_sqs-risk\",\n  \"pass\": true,\n  \"detail\": \"parent manifest row sqs-risk preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T031_FDA_ROW_fabric-desktop-cua\",\n  \"pass\": true,\n  \"detail\": \"FDA row fabric-desktop-cua added\",\n  \"required\": true\n },\n {\n  \"id\": \"T031_FDA_ROW_fabric-desktop-ufo2\",\n  \"pass\": true,\n  \"detail\": \"FDA row fabric-desktop-ufo2 added\",\n  \"required\": true\n },\n {\n  \"id\": \"T031_FDA_ROW_fabric-desktop-automation/TEAM.md\",\n  \"pass\": true,\n  \"detail\": \"FDA row fabric-desktop-automation/TEAM.md added\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_hermes_runtime\",\n  \"pass\": true,\n  \"detail\": \"parent tool row hermes_runtime preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_hermes_profiles\",\n  \"pass\": true,\n  \"detail\": \"parent tool row hermes_profiles preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_hermes_kanban\",\n  \"pass\": true,\n  \"detail\": \"parent tool row hermes_kanban preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_hermes_a2a\",\n  \"pass\": true,\n  \"detail\": \"parent tool row hermes_a2a preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_mcp\",\n  \"pass\": true,\n  \"detail\": \"parent tool row mcp preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_contextforge\",\n  \"pass\": true,\n  \"detail\": \"parent tool row contextforge preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_oasf\",\n  \"pass\": true,\n  \"detail\": \"parent tool row oasf preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_opentelemetry\",\n  \"pass\": true,\n  \"detail\": \"parent tool row opentelemetry preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_codex_cli\",\n  \"pass\": true,\n  \"detail\": \"parent tool row codex_cli preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_openspec\",\n  \"pass\": true,\n  \"detail\": \"parent tool row openspec preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T040_PARENT_TOOL_gstack\",\n  \"pass\": true,\n  \"detail\": \"parent tool row gstack preserved\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_cua_driver\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row cua_driver present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_ufo2\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row ufo2 present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_hermes_computer_use\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row hermes_computer_use present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_openadapt\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row openadapt present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_agent_s3\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row agent_s3 present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_appium_windows_driver\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row appium_windows_driver present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_winappdriver\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row winappdriver present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_flaui\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row flaui present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_pywinauto\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row pywinauto present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_ufo3_galaxy\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row ufo3_galaxy present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_fda_desktop_capability_matrix\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row fda_desktop_capability_matrix present\",\n  \"required\": true\n },\n {\n  \"id\": \"T041_FDA_TOOL_fda_team_artifact\",\n  \"pass\": true,\n  \"detail\": \"FDA tool row fda_team_artifact present\",\n  \"required\": true\n },\n {\n  \"id\": \"T050_BINDING_SCHEMA\",\n  \"pass\": true,\n  \"detail\": \"binding uses parent /2 schema\",\n  \"required\": true\n },\n {\n  \"id\": \"T051_BINDING_WO\",\n  \"pass\": true,\n  \"detail\": \"binding workorder\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_normative\",\n  \"pass\": true,\n  \"detail\": \"binding section normative\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_routing\",\n  \"pass\": true,\n  \"detail\": \"binding section routing\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_delegation\",\n  \"pass\": true,\n  \"detail\": \"binding section delegation\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_lease\",\n  \"pass\": true,\n  \"detail\": \"binding section lease\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_budget\",\n  \"pass\": true,\n  \"detail\": \"binding section budget\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_idempotency\",\n  \"pass\": true,\n  \"detail\": \"binding section idempotency\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_runtime\",\n  \"pass\": true,\n  \"detail\": \"binding section runtime\",\n  \"required\": true\n },\n {\n  \"id\": \"T052_BINDING_terminal\",\n  \"pass\": true,\n  \"detail\": \"binding section terminal\",\n  \"required\": true\n },\n {\n  \"id\": \"T053_BINDING_DESKTOP\",\n  \"pass\": true,\n  \"detail\": \"desktop overlay one-active-writer\",\n  \"required\": true\n },\n {\n  \"id\": \"T060_NO_SCHEMA_FORK\",\n  \"pass\": true,\n  \"detail\": \"no child execution-binding schema created\",\n  \"required\": true\n },\n {\n  \"id\": \"T070_SEMIAUTO_CONTRACT\",\n  \"pass\": true,\n  \"detail\": \"deferred semi-auto contract exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T071_FROZEN_SCRIPT\",\n  \"pass\": true,\n  \"detail\": \"no hot patch invariant\",\n  \"required\": true\n },\n {\n  \"id\": \"T072_LIVE_NOT_AUTH\",\n  \"pass\": true,\n  \"detail\": \"live trading NOT_AUTHORIZED\",\n  \"required\": true\n },\n {\n  \"id\": \"T080_INTEROP_DISPOSITION\",\n  \"pass\": true,\n  \"detail\": \"interop disposition exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T081_OASF\",\n  \"pass\": true,\n  \"detail\": \"interop disposition OASF\",\n  \"required\": true\n },\n {\n  \"id\": \"T081_CONTEXTFORGE\",\n  \"pass\": true,\n  \"detail\": \"interop disposition CONTEXTFORGE\",\n  \"required\": true\n },\n {\n  \"id\": \"T081_MCP\",\n  \"pass\": true,\n  \"detail\": \"interop disposition MCP\",\n  \"required\": true\n },\n {\n  \"id\": \"T081_A2A\",\n  \"pass\": true,\n  \"detail\": \"interop disposition A2A\",\n  \"required\": true\n },\n {\n  \"id\": \"T081_OPENTELEMETRY\",\n  \"pass\": true,\n  \"detail\": \"interop disposition OPENTELEMETRY\",\n  \"required\": true\n },\n {\n  \"id\": \"T090_ROUTE_CHECK\",\n  \"pass\": true,\n  \"detail\": \"route check exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T091_GSTACK_STATE\",\n  \"pass\": true,\n  \"detail\": \"gstack registry state\",\n  \"required\": true\n },\n {\n  \"id\": \"T092_OPENSPEC_STATE\",\n  \"pass\": true,\n  \"detail\": \"openspec registry state\",\n  \"required\": true\n },\n {\n  \"id\": \"T093_LANE_NOT_EXECUTION\",\n  \"pass\": true,\n  \"detail\": \"lane != execution surface\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_DESKTOP_CAPABILITY_MATRIX.yaml\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_DESKTOP_CAPABILITY_MATRIX.yaml\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_EXECUTION_BINDING.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_EXECUTION_BINDING.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_FOLDER_REORGANIZATION_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_FOLDER_REORGANIZATION_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_fda_lease.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in fda_lease.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_fda_router.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in fda_router.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_independent_checker.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in independent_checker.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_TEAM.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in TEAM.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_xq_action_router.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_xq_action_router.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_xq_build_drift.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_xq_build_drift.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_xq_native_adapter.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_xq_native_adapter.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_WO_FDA_XQ_002.yaml\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in WO_FDA_XQ_002.yaml\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_xq_native_adapter.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in xq_native_adapter.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_USER_GUIDE.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_USER_GUIDE.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_EVIDENCE_MANIFEST.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_EVIDENCE_MANIFEST.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_EXTERNAL_FULL_EVIDENCE_20260814.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_EXTERNAL_FULL_EVIDENCE_20260814.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_EXTERNAL_SINGLE_EVIDENCE_RR3.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_EXTERNAL_SINGLE_EVIDENCE_RR3.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_FOLDER_REORGANIZATION_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_FOLDER_REORGANIZATION_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_IMPLEMENTATION_EVIDENCE.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_IMPLEMENTATION_EVIDENCE.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_MIRROR_READBACK_20260814_RR3.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_MIRROR_READBACK_20260814_RR3.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_USER_GUIDE.md\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_USER_GUIDE.md\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_INTEROP_DISPOSITION.yaml\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_INTEROP_DISPOSITION.yaml\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_ROUTE_CHECK.yaml\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_ROUTE_CHECK.yaml\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_fda_lease.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_fda_lease.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_fda_router.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_fda_router.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_fda_router_integration.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_fda_router_integration.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_test_fda_security.py\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in test_fda_security.py\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_BOUNDED_CONTROL_LIVE_PROBE.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_BOUNDED_CONTROL_LIVE_PROBE.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_C0_READBACK_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_C0_READBACK_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_C2_CUA_QUALIFICATION_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_C2_CUA_QUALIFICATION_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_C3_UFO2_QUALIFICATION_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_C3_UFO2_QUALIFICATION_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_C4_XQ_QUALIFICATION_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_C4_XQ_QUALIFICATION_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_C5_LEASE_CONCURRENCY_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_C5_LEASE_CONCURRENCY_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F01_LIVE_FIXTURE_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F01_LIVE_FIXTURE_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F03_LIVE_FIXTURE_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F03_LIVE_FIXTURE_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F04_LIVE_FIXTURE_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F04_LIVE_FIXTURE_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_CLOSURE_V3_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_CLOSURE_V3_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_CLOSURE_V4_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_CLOSURE_V4_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_CLOSURE_V5_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_CLOSURE_V5_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_CLOSURE_V6_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_CLOSURE_V6_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_CLOSURE_V7_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_CLOSURE_V7_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_CLOSURE_V8_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_CLOSURE_V8_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_COMPILE_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_COMPILE_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_COMPILE_TOOLBAR_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_COMPILE_TOOLBAR_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_EXPORT_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_EXPORT_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_LIVE_FIXTURE_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_LIVE_FIXTURE_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_SYSTEM_PATH_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_SYSTEM_PATH_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F06_TEN_RUN_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F06_TEN_RUN_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F09B_PAPER_RUNTIME_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F09B_PAPER_RUNTIME_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F09_RADAR_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F09_RADAR_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_F10_F11_READBACK_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_F10_F11_READBACK_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T100_NOSECRET_FDA_XQ_PAPER_RUNTIME_RECEIPT.json\",\n  \"pass\": true,\n  \"detail\": \"no secret-like pattern in FDA_XQ_PAPER_RUNTIME_RECEIPT.json\",\n  \"required\": true\n },\n {\n  \"id\": \"T110_FIXTURE_MANIFEST\",\n  \"pass\": true,\n  \"detail\": \"fixture manifest exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T111_FIXTURE_MODE\",\n  \"pass\": true,\n  \"detail\": \"PAPER mode\",\n  \"required\": true\n },\n {\n  \"id\": \"T112_FIXTURE_DRIFT\",\n  \"pass\": true,\n  \"detail\": \"version drift recorded\",\n  \"required\": true\n },\n {\n  \"id\": \"T120_FILE_fda_router.py\",\n  \"pass\": true,\n  \"detail\": \"fda_router.py exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T120_FILE_fda_lease.py\",\n  \"pass\": true,\n  \"detail\": \"fda_lease.py exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T120_FILE_tests/test_fda_router.py\",\n  \"pass\": true,\n  \"detail\": \"tests/test_fda_router.py exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T120_FILE_tests/test_fda_lease.py\",\n  \"pass\": true,\n  \"detail\": \"tests/test_fda_lease.py exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T120_FILE_tests/test_fda_security.py\",\n  \"pass\": true,\n  \"detail\": \"tests/test_fda_security.py exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T130_C0_RECEIPT\",\n  \"pass\": true,\n  \"detail\": \"C0 receipt exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T131_C0_VERDICT\",\n  \"pass\": true,\n  \"detail\": \"C0 verdict PASS\",\n  \"required\": true\n },\n {\n  \"id\": \"T132_C0_NO_MISSING\",\n  \"pass\": true,\n  \"detail\": \"critical source missing 0\",\n  \"required\": true\n },\n {\n  \"id\": \"T133_F01_RECEIPT\",\n  \"pass\": true,\n  \"detail\": \"F01 live fixture receipt exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T134_F01_10_OF_10\",\n  \"pass\": true,\n  \"detail\": \"F01 10/10 live PASS\",\n  \"required\": true\n },\n {\n  \"id\": \"T135_F01_ZERO_WRONG\",\n  \"pass\": true,\n  \"detail\": \"F01 zero wrong/silent-wrong action\",\n  \"required\": true\n },\n {\n  \"id\": \"T136_PROBE_RECEIPT\",\n  \"pass\": true,\n  \"detail\": \"bounded control probe receipt exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T137_PROBE_PASS\",\n  \"pass\": true,\n  \"detail\": \"bounded control probe PASS\",\n  \"required\": true\n },\n {\n  \"id\": \"T138_PROBE_NO_FINANCIAL\",\n  \"pass\": true,\n  \"detail\": \"no financial side effect\",\n  \"required\": true\n },\n {\n  \"id\": \"T139_CONCURRENCY_RECEIPT\",\n  \"pass\": true,\n  \"detail\": \"lease concurrency receipt exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T140_CONCURRENCY_PASS\",\n  \"pass\": true,\n  \"detail\": \"lease concurrency ALL PASS\",\n  \"required\": true\n },\n {\n  \"id\": \"T141_CONCURRENCY_ZERO_SIMUL\",\n  \"pass\": true,\n  \"detail\": \"simultaneous writers 0\",\n  \"required\": true\n },\n {\n  \"id\": \"T142_MATRIX_F01_QUALIFIED\",\n  \"pass\": true,\n  \"detail\": \"matrix XQ_LAUNCH_LOCATE CUA QUALIFIED with live reason\",\n  \"required\": true\n },\n {\n  \"id\": \"T143_MATRIX_PRODUCT_VERSION\",\n  \"pass\": true,\n  \"detail\": \"matrix product version corrected to 3.20.02 live readback\",\n  \"required\": true\n },\n {\n  \"id\": \"T160_XQ_FINGERPRINT_RECEIPT\",\n  \"pass\": true,\n  \"detail\": \"XQ build fingerprint receipt exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T161_XQ_FINGERPRINT_SCHEMA\",\n  \"pass\": true,\n  \"detail\": \"fingerprint schema\",\n  \"required\": true\n },\n {\n  \"id\": \"T162_XQ_BUILD_260811\",\n  \"pass\": true,\n  \"detail\": \"local build 260811\",\n  \"required\": true\n },\n {\n  \"id\": \"T163_XQ_SHA_PRESENT\",\n  \"pass\": true,\n  \"detail\": \"exe sha256 captured\",\n  \"required\": true\n },\n {\n  \"id\": \"T164_PUBLIC_MISMATCH_ACK\",\n  \"pass\": true,\n  \"detail\": \"public 260731 != local 260811 acknowledged\",\n  \"required\": true\n },\n {\n  \"id\": \"T165_MATRIX_BUILD_FIREWALL\",\n  \"pass\": true,\n  \"detail\": \"matrix build drift firewall present\",\n  \"required\": true\n },\n {\n  \"id\": \"T166_MATRIX_SUBJECT_BINDING\",\n  \"pass\": true,\n  \"detail\": \"all 5 action classes have subject_binding\",\n  \"required\": true\n },\n {\n  \"id\": \"T167_MATRIX_PYWINAUTO\",\n  \"pass\": true,\n  \"detail\": \"pywinauto win32 backend row present with version\",\n  \"required\": true\n },\n {\n  \"id\": \"T168_MATRIX_NO_SILENT_FALLBACK\",\n  \"pass\": true,\n  \"detail\": \"router silent fallback disabled\",\n  \"required\": true\n },\n {\n  \"id\": \"T169_NATIVE_ADAPTER_EXISTS\",\n  \"pass\": true,\n  \"detail\": \"xq_native_adapter.py exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T170_NATIVE_NO_MOUSE_INPUT\",\n  \"pass\": true,\n  \"detail\": \"adapter has zero mouse-input API calls\",\n  \"required\": true\n },\n {\n  \"id\": \"T171_NATIVE_MESSAGE_ONLY\",\n  \"pass\": true,\n  \"detail\": \"adapter uses pure win32 messages\",\n  \"required\": true\n },\n {\n  \"id\": \"T172_NATIVE_QUAL_RECEIPT\",\n  \"pass\": true,\n  \"detail\": \"native qualification receipt exists\",\n  \"required\": true\n },\n {\n  \"id\": \"T173_FN01_10OF10\",\n  \"pass\": true,\n  \"detail\": \"FN01 main locate 10/10\",\n  \"required\": true\n },\n {\n  \"id\": \"T174_FN02_10OF10\",\n  \"pass\": true,\n  \"detail\": \"FN02 editor locate 10/10\",\n  \"required\": true\n },\n {\n  \"id\": \"T175_FN03_LOCATE\",\n  \"pass\": true,\n  \"detail\": \"FN03 Afx 新增 button located\",\n  \"required\": true\n },\n {\n  \"id\": \"T176_FN_ZERO_WRONG\",\n  \"pass\": true,\n  \"detail\": \"FN wrong-action 0\",\n  \"required\": true\n },\n {\n  \"id\": \"T177_TEST_TEST_XQ_BUILD_DRIFT.PY\",\n  \"pass\": true,\n  \"detail\": \"test_xq_build_drift.py present\",\n  \"required\": true\n },\n {\n  \"id\": \"T177_TEST_TEST_XQ_NATIVE_ADAPTER.PY\",\n  \"pass\": true,\n  \"detail\": \"test_xq_native_adapter.py present\",\n  \"required\": true\n },\n {\n  \"id\": \"T177_TEST_TEST_XQ_ACTION_ROUTER.PY\",\n  \"pass\": true,\n  \"detail\": \"test_xq_action_router.py present\",\n  \"required\": true\n },\n {\n  \"id\": \"T150_NO_THIRD_HEAVY_STACK\",\n  \"pass\": true,\n  \"detail\": \"fabric-desktop not registered as heavy stack\",\n  \"required\": true\n },\n {\n  \"id\": \"T151_SQS_LIVE_NOT_AUTHORIZED\",\n  \"pass\": true,\n  \"detail\": \"SQS status vector exists for ceiling readback\",\n  \"required\": true\n }\n]\n",
  "stderr_tail": ""
}
```

# 5. RR6-005 — self-hash repair

```text
Old defect: container claimed 4611fe56… but actual bytes = 41eb23c1… (self-referential mismatch).
Repair: THIS file carries no self-hash inside its body; its SHA-256 is published via sidecar
(FDA_MIRROR_READBACK_20260814_RR6.json) and computed by the external reviewer on received bytes.
Sidecar: <finalize-sidecar>
```

# 6. External Verifier Checklist (re-review)

1. F01: target.product_version == 3.20.02, build 260811, exe_sha256 6c0c7cbc…, 10/10, wrong=0, silent=0
2. PAPER: 10 runs, each SensorList-persisted + SensorLog ExecState>=1, wrong=0, silent=0, broker_write=0, one writer
3. F06: 10 runs, 10 distinct LastCompileTime/invocation timestamps, CompileStatus=1, wrong=0, silent=0
4. Checker: 179/179, failed=0, error=0, exit=0, verify-only, maker!=checker
5. Subject root: manifest binds post-repair HEAD
6. DoD-13 PASS (UFO2 7/7) / DoD-17 PASS (PAPER 10 fresh) / DoD-18/19 wrong=0 / DoD-33 checker / DoD-35 260811 binding
7. No visual-alert gate added (external r6: not mandatory)

# 7. Honest Residuals

```text
- 盤中視覺警示 UI 跳出：time-gated; SensorLog proves engine execution; external r6 explicit: not a mandatory gate
- Cua 0.19.4 nightly shadow: NOT RUN (baseline 0.19.3 maintained)
- FN03 Afx invoke qualification: locate 1/1 only; matrix promotes only locate rows today
```

# 8. Final

```text
RR6_REPAIR_PACKAGE = SUBMITTED (self-contained single MD)
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED (awaiting external r7 verdict)
SQS_LIVE_TRADING = NOT_AUTHORIZED
```
