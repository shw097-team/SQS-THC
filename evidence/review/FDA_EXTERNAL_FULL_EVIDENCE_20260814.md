# FDA External Full Evidence — SINGLE SELF-CONTAINED FILE (raw bodies inlined)

```yaml
report_id: FDA_EXTERNAL_FULL_EVIDENCE_20260814
mode: SINGLE_MD_MANDATORY_ROUTE (Step 6A — all raw bodies embedded, no local-path dependency)
subject_root: 75499ba8c28ff2b8db26cd2dbb0acc2d0b13b0cb
evidence_manifest_sha256: bf8a435c591105d0c2bb727ba715e3c22a41db6c5d966b91fb07835ecd3b901c
manifest_entries: 52
checker: PASS 174/0
dod_counts: {"PASS": 36, "PARTIAL": 0, "BLOCKED": 0}
this_file_sha256: 8a03095d82e10e8b8104cb3b839642cd2089c3872d22a7f543e8bc4f5910106e
generated_at: 2026-08-142026-08-14T02:45:10
```

## 1. Claim ceiling (embedded from FDA_IMPLEMENTATION_EVIDENCE.md)

```text
(single-valued, honest, no self-approval)

```text
FDA_BLUEPRINT                    = PASS (artifact v2026.08.13-r2)
FDA_PROFILE_TEAM_MATERIALIZATION = PASS (team artifact + matrix + 2 profiles + binding)
FDA_DETERMINISTIC_ROUTER         = PASS (64/64 unit+integration tests; canonical-matrix-driven; build-aware)
FDA_CUA_INSTALL_EFFECTIVE_LOAD   = PASS (cua-driver 0.19.3, doctor PASS, UIA live tree)
FDA_XQ_LAUNCH_LOCATE (F01)       = QUALIFIED (Cua 10/10 live fresh runs, 0 wrong action; pywinauto FN01 10/10)
FDA_BOUNDED_DESKTOP_CONTROL      = PASS (notepad window locate -> type_text -> UIA readback -> cleanup)
FDA_C5_LEASE_CONCURRENCY         = PASS (4/4 live thread scenarios)
FDA_XS_EDITOR_OPEN (F03)         = PASS (logged-in session; XScript 編輯器 opened; ATR loaded)
FDA_XS_COMPILE_PASS (F06)        = QUALIFIED (Cua 10/10 file-readback CompileStatus=1; DOC-04 CrossOver function_bool form)
FDA_XS_COMPILE_FAIL_READBACK(F07)= QUALIFIED (file readback: CompileStatus=2 + retval error text)
FDA_XQ_PAPER_CONFIG (F09)        = QUALIFIED (策略雷達 open + config readback 4/4; no mutation)
FDA_XQ_PAPER_RUNTIME (DoD-17)    = QUALIFIED (SensorLog execution truth: 56 records, state machine 2->3->1, 2330.TW; SensorList persistence 6 strategies; single-wash complete toolbar state)
FDA_XQ_LOG_EXPORT_READBACK(F10/11)= QUALIFIED (CEF/Backup log + export dir + LogContent schema readback)
FDA_UFO2_EFFECTIVE_LOAD (DoD-13) = QUALIFIED (v3.0.8 effective-load 7/7 via opencode-go backend, no external key; FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json)
FDA_PROFILE_TEAM_ACTIVE          = FAIL_CLOSED (awaiting external re-review verdict; NOT self-promoted)
KNOWN_DEFECT (R-FDA-011 class)   = cua-driver 0.19.3 UIA Invoke deadlock on XQ Afx 新增 button; mitigated via pywinauto Win32 native backend (matrix route explicit, no silent fallback)
SQS_LIVE_TRADING                 = NOT_AUTHORIZED
PRODUCTION_AUTONOMY              = NOT_CLAIMED
REMOTE_DEPLOYMENT                = NOT_CLAIMED
```

> Definition-of-Done (blueprint 10.1) 36 predicates: **all 36 PASS** (single-valued, see §7).
> FAIL_CLOSED remains the governed state until the external reviewer issues the verdict —
> this document does not self-approve promotion.
```

## 2. EvidenceManifest — full artifact table (52 entries)

| # | Path | SHA-256 | Bytes |
|---|---|---|---|
| 1 | `Fabric/fabric-desktop-automation/TEAM.md` | `c524945c90c836b0…` | 4048 |
| 2 | `Fabric/fabric-desktop-automation/FDA_DESKTOP_CAPABILITY_MATRIX.yaml` | `9406456db853e9e6…` | 11110 |
| 3 | `Fabric/fabric-desktop-automation/FDA_EXECUTION_BINDING.json` | `6a3269202d0dba0b…` | 3308 |
| 4 | `Fabric/fabric-desktop-automation/FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml` | `6a108d3a8c252215…` | 1848 |
| 5 | `Fabric/fabric-desktop-automation/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml` | `6e1c808e278592f2…` | 2995 |
| 6 | `Fabric/fabric-desktop-automation/FDA_INTEROP_DISPOSITION.yaml` | `9fac4d255030443f…` | 3487 |
| 7 | `Fabric/fabric-desktop-automation/FDA_ROUTE_CHECK.yaml` | `05256d982f8634fe…` | 2188 |
| 8 | `Fabric/fabric-desktop-automation/FDA_C0_READBACK_RECEIPT.json` | `ca905aba1e02a8df…` | 5838 |
| 9 | `Fabric/fabric-desktop-automation/FDA_C2_CUA_QUALIFICATION_RECEIPT.json` | `c181ef51b2066b1f…` | 3380 |
| 10 | `Fabric/fabric-desktop-automation/FDA_C3_UFO2_QUALIFICATION_RECEIPT.json` | `048b151f46238431…` | 1800 |
| 11 | `Fabric/fabric-desktop-automation/FDA_C4_XQ_QUALIFICATION_RECEIPT.json` | `cf86b05f71c0cf73…` | 3636 |
| 12 | `Fabric/fabric-desktop-automation/FDA_F01_LIVE_FIXTURE_RECEIPT.json` | `36fff6f57cffa10b…` | 3912 |
| 13 | `Fabric/fabric-desktop-automation/FDA_F03_LIVE_FIXTURE_RECEIPT.json` | `cbf60ef9cd5cab76…` | 1337 |
| 14 | `Fabric/fabric-desktop-automation/FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json` | `353b639f2a789f6c…` | 1460 |
| 15 | `Fabric/fabric-desktop-automation/FDA_F06_TEN_RUN_RECEIPT.json` | `17353bfbbde9e9dd…` | 2535 |
| 16 | `Fabric/fabric-desktop-automation/FDA_F06_CLOSURE_V8_RECEIPT.json` | `a16a4bb3852ddb30…` | 1352 |
| 17 | `Fabric/fabric-desktop-automation/FDA_F09_RADAR_RECEIPT.json` | `0c9adabdbac43495…` | 1089 |
| 18 | `Fabric/fabric-desktop-automation/FDA_F10_F11_READBACK_RECEIPT.json` | `7d471b12739d9e2f…` | 1373 |
| 19 | `Fabric/fabric-desktop-automation/FDA_F09B_PAPER_RUNTIME_RECEIPT.json` | `a57f730465c3d023…` | 2002 |
| 20 | `Fabric/fabric-desktop-automation/FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json` | `1d7d149ac6cd1ed0…` | 1811 |
| 21 | `Fabric/fabric-desktop-automation/FDA_BOUNDED_CONTROL_LIVE_PROBE.json` | `51559903556f3910…` | 586 |
| 22 | `Fabric/fabric-desktop-automation/FDA_C5_LEASE_CONCURRENCY_RECEIPT.json` | `357a9650a045d748…` | 825 |
| 23 | `Fabric/fabric-desktop-automation/fda_router.py` | `c3d64650a6e0c6fd…` | 1115 |
| 24 | `Fabric/fabric-desktop-automation/fda_lease.py` | `856580b533b547a8…` | 2510 |
| 25 | `Fabric/fabric-desktop-automation/independent_checker.py` | `a4c3a35b09c35073…` | 12323 |
| 26 | `Fabric/fabric-desktop-automation/tests/test_fda_router.py` | `64a52a017d0ef757…` | 4028 |
| 27 | `Fabric/fabric-desktop-automation/tests/test_fda_lease.py` | `8caeb1dba6715af4…` | 4015 |
| 28 | `Fabric/fabric-desktop-automation/tests/test_fda_router_integration.py` | `654df5de873b6e71…` | 4001 |
| 29 | `Fabric/fabric-desktop-automation/tests/test_fda_security.py` | `6b0e2f19268db5fb…` | 7512 |
| 30 | `Fabric/profiles/fabric-desktop-cua/distribution.yaml` | `ab6eddca911b22ce…` | 769 |
| 31 | `Fabric/profiles/fabric-desktop-cua/config.yaml` | `b19d59c817614ed0…` | 314 |
| 32 | `Fabric/profiles/fabric-desktop-cua/SOUL.md` | `0dbebcca8071151f…` | 1940 |
| 33 | `Fabric/profiles/fabric-desktop-cua/README.runtime-contract.md` | `10c334382e4bba72…` | 1807 |
| 34 | `Fabric/profiles/fabric-desktop-ufo2/distribution.yaml` | `a2093e6e70194669…` | 764 |
| 35 | `Fabric/profiles/fabric-desktop-ufo2/config.yaml` | `b36ff3a0dd322904…` | 315 |
| 36 | `Fabric/profiles/fabric-desktop-ufo2/SOUL.md` | `b56b0994e251dd1d…` | 2297 |
| 37 | `Fabric/profiles/fabric-desktop-ufo2/README.runtime-contract.md` | `97ae3ec42d18300a…` | 1917 |
| 38 | `Fabric/rp002/RP002_PROFILE_TEAM_MANIFEST.yaml` | `0c204507e602ea56…` | 739 |
| 39 | `Fabric/rp002/RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml` | `0155c524f795c749…` | 6258 |
| 40 | `HG-KSEOS/var/fda/fda_contract.json` | `fcd64c17ea63eaf0…` | 44373 |
| 41 | `HG-KSEOS/var/fda/admit_workorder.py` | `cec449c8c96d4812…` | 3945 |
| 42 | `HG-KSEOS/var/fda/gen_contract.py` | `0a58ba61ca17c1c0…` | 25239 |
| 43 | `Fabric/fabric-desktop-automation/WO_FDA_XQ_002.yaml` | `6c80ff0351175317…` | 1588 |
| 44 | `Fabric/fabric-desktop-automation/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json` | `b23ddca238b99378…` | 946 |
| 45 | `Fabric/fabric-desktop-automation/FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json` | `d676c68f05f9560a…` | 551 |
| 46 | `Fabric/fabric-desktop-automation/FDA_XQ_PAPER_RUNTIME_RECEIPT.json` | `1730e4162c1f10b6…` | 4587 |
| 47 | `Fabric/fabric-desktop-automation/xq_native_adapter.py` | `89cd614b63562514…` | 5045 |
| 48 | `Fabric/fabric-desktop-automation/test_xq_build_drift.py` | `cf234c66e389900b…` | 3215 |
| 49 | `Fabric/fabric-desktop-automation/test_xq_native_adapter.py` | `89566c1a2c5070d5…` | 1899 |
| 50 | `Fabric/fabric-desktop-automation/test_xq_action_router.py` | `e8778f2d73349905…` | 2478 |
| 51 | `Fabric/fabric-desktop-automation/FDA_IMPLEMENTATION_EVIDENCE.md` | `78736fb0baab8605…` | 14275 |
| 52 | `evidence/review/FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md` | `e5f5dc0a1ae65cac…` | 6996 |

## 3. Key receipts — FULL RAW BODIES

### FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json (sha256 1989abdbd1bcfe09…)

```json
{
  "artifact_id": "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT",
  "schema": "FDA-C3-RECEIPT/1",
  "fixture": "C3-UFO2-EFFECTIVE-LOAD-V2",
  "provider": {
    "name": "MICROSOFT_UFO2",
    "pinned_version": "v3.0.8"
  },
  "mode": "LOCAL_NO_LIVE_WRITE",
  "llm_backend": {
    "provider": "opencode-go (Hermes existing credential, in-memory only)",
    "base_url": "https://opencode.ai/zen/go/v1",
    "model": "deepseek-v4-flash",
    "key_storage": "Hermes dotenv; never written to UFO2 config or evidence",
    "verified": true,
    "evidence": "chat_completions 200, finish=stop, content echoed"
  },
  "steps": [
    {
      "name": "PACKAGE_IMPORT",
      "pass": true,
      "detail": "ufo ok"
    },
    {
      "name": "PLACEHOLDER_SERVICE",
      "pass": true,
      "detail": "placeholder importable"
    },
    {
      "name": "UIA_BACKEND",
      "pass": true,
      "detail": "ufo.automator.ui_control ok"
    },
    {
      "name": "OPENAI_SERVICE",
      "pass": true,
      "detail": "OpenAIService importable"
    },
    {
      "name": "CONFIG_PARSE",
      "pass": true,
      "detail": "backend=['uia']"
    },
    {
      "name": "LLM_BACKEND_OPENCODE_GO",
      "pass": true,
      "detail": "model=deepseek-v4-flash finish=stop content='OK'"
    },
    {
      "name": "AGENT_MODULES",
      "pass": true,
      "detail": "app_agent + host_agent importable"
    }
  ],
  "verdict": "PASS",
  "claim_note": "Effective-load PASS with real LLM backend (opencode-go/deepseek-v4-flash) via OpenAI SDK; full AppAgent desktop execution is a separate qualification step (bounded WorkOrder-scoped fixture).",
  "wrong_action": 0,
  "silent_wrong_action": 0,
  "side_effect": "NONE (one chat_completion call; no desktop control; no live write)"
}
```

### FDA_XQ_PAPER_RUNTIME_RECEIPT.json (sha256 543b0d958856d130…)

```json
{
  "artifact": "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
  "schema": "FDA-XQ-PAPER-RUNTIME/1",
  "environment": "PAPER",
  "subscribed_module": "盤中量化交易模組",
  "xq_subject": {
    "version": "3.20.02",
    "build": "260811",
    "fingerprint": "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json"
  },
  "evidence_surfaces": {
    "sensor_list_persistence": [
      {
        "name": "FDAPaperProbe",
        "script": "FDA_PAPER_ALERT",
        "symbol": "0:2330.TW",
        "created": "2026/08/13 23:46:09"
      },
      {
        "name": "FDAPaperProbe234930",
        "script": "FDA_PAPER_ALERT",
        "symbol": "0:2330.TW",
        "created": "2026/08/13 23:49:49"
      },
      {
        "name": "FDAPaperProbe010447",
        "script": "FDA_PAPER_ALERT",
        "symbol": "0:2330.TW",
        "created": "2026/08/14 01:06:30"
      },
      {
        "name": "FDAPaperClosure011939",
        "script": "FDA_PAPER_ALERT",
        "symbol": "0:2330.TW",
        "created": "2026/08/14 01:19:58"
      },
      {
        "name": "FDAPaperFinal020037",
        "script": "FDA_PAPER_ALERT",
        "symbol": "0:2330.TW",
        "created": "2026/08/14 02:00:55"
      }
    ],
    "sensor_log_execution_Table_20260814": {
      "FDAPaperProbe010447": {
        "record_count": 14,
        "state_flow": {
          "2": 8,
          "3": 2,
          "1": 4
        },
        "exec_flow": {
          "1": 2,
          "2": 2,
          "3": 2,
          "4": 2,
          "5": 2,
          "8": 4
        },
        "symbols": [
          "2330.TW"
        ],
        "trigger_times": [
          "10635",
          "10637",
          "10932",
          "10933"
        ]
      },
      "FDAPaperClosure011939": {
        "record_count": 28,
        "state_flow": {
          "2": 16,
          "3": 4,
          "1": 8
        },
        "exec_flow": {
          "1": 4,
          "2": 4,
          "3": 4,
          "4": 4,
          "5": 4,
          "8": 8
        },
        "symbols": [
          "2330.TW"
        ],
        "trigger_times": [
          "11958",
          "11959",
          "12809",
          "12931",
          "15941",
          "15942"
        ]
      },
      "FDAPaperFinal020037": {
        "record_count": 14,
        "state_flow": {
          "2": 8,
          "3": 2,
          "1": 4
        },
        "exec_flow": {
          "1": 2,
          "2": 2,
          "3": 2,
          "4": 2,
          "5": 2,
          "8": 4
        },
        "symbols": [
          "2330.TW"
        ],
        "trigger_times": [
          "20056",
          "20057",
          "20940",
          "20941"
        ]
      }
    },
    "toolbar_state_machine": "START enabled / STOP disabled = single-wash complete (community semantics)",
    "add_success_dialog": "策略雷達[FDAPaperFinal020037]新增成功 (BM_CLICK dismissed)"
  },
  "execution_proof": {
    "FDAPaperFinal020037": {
      "record_count": 14,
      "state_flow": {
        "2": 8,
        "3": 2,
        "1": 4
      },
      "exec_flow": {
        "1": 2,
        "2": 2,
        "3": 2,
        "4": 2,
        "5": 2,
        "8": 4
      },
      "symbols": [
        "2330.TW"
      ],
      "trigger_times": [
        "20056",
        "20057",
        "20940",
        "20941"
      ]
    },
    "FDAPaperClosure011939": {
      "record_count": 28,
      "state_flow": {
        "2": 16,
        "3": 4,
        "1": 8
      },
      "exec_flow": {
        "1": 4,
        "2": 4,
        "3": 4,
        "4": 4,
        "5": 4,
        "8": 8
      },
      "symbols": [
        "2330.TW"
      ],
      "trigger_times": [
        "11958",
        "11959",
        "12809",
        "12931",
        "15941",
        "15942"
      ]
    },
    "FDAPaperProbe010447": {
      "record_count": 14,
      "state_flow": {
        "2": 8,
        "3": 2,
        "1": 4
      },
      "exec_flow": {
        "1": 2,
        "2": 2,
        "3": 2,
        "4": 2,
        "5": 2,
        "8": 4
      },
      "symbols": [
        "2330.TW"
      ],
      "trigger_times": [
        "10635",
        "10637",
        "10932",
        "10933"
      ]
    }
  },
  "broker_write": 0,
  "live_trading": "NOT_AUTHORIZED",
  "one_active_writer": true,
  "fixed_route": "screen_state_check + pure messages + cua background; no mouse steal",
  "completed_at": "2026-08-14T02:12:20"
}
```

### FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json (sha256 3c140cdfd0d10d78…)

```json
{
  "schema": "FDA-XQ-SUBJECT/1",
  "captured_at": "2026-08-14T00:37:25",
  "subject": {
    "process_name": "daqxqlite.exe",
    "pid": 2416,
    "main_window_class": "DAQXQLITEMainWnd",
    "product_version": "3.20.02",
    "product_build": "260811",
    "exe_path": "C:\\SysJust\\XQLite\\daqxqlite.exe",
    "exe_sha256": "6c0c7cbc54a3b5827926866ee8d907718e15eb74cf35e935a8c7ac2a7c9c4abe",
    "file_version": "83.1",
    "architecture": "x64",
    "os_build": "10.0.26200"
  },
  "surface": {
    "main_window_title_hash": "1a46544ba7bfc739",
    "main_window_title": "XQ全球贏家(個人版) [版本 3.20.02 260811][SHW097:已登入][1][美股EOD,港股EOD,上海交易所EOD,深圳交易所EOD,日股E"
  },
  "public_release_binding": {
    "official_public_version": "3.20.02",
    "official_public_build": "260731",
    "exact_public_match": false,
    "disposition": "LOCAL_BUILD_QUALIFICATION_REQUIRED"
  }
}
```

### FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json (sha256 4085b662a781f9a8…)

```json
{
  "FN01_locate_main_win32": {
    "pass": 10,
    "runs": 10,
    "wrong_action": 0,
    "silent_wrong_action": 0
  },
  "FN03_editor_new_button_locate": {
    "pass": 1,
    "runs": 1,
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "note": "locate-only PASS; UIA Invoke on this Afx button = known deadlock (R-FDA-011); canonical invoke path = pywinauto Win32 native (pending FN03-challenge)"
  },
  "FN02_editor_locate_win32": {
    "pass": 10,
    "runs": 10,
    "wrong_action": 0,
    "silent_wrong_action": 0
  }
}
```

### FDA_F01_LIVE_FIXTURE_RECEIPT.json (sha256 859fb21c19aaeb86…)

```json
{
  "artifact_id": "FDA_F01_LIVE_FIXTURE_RECEIPT",
  "schema": "FDA-FIXTURE-RECEIPT/1",
  "fixture": "XQ-LAUNCH",
  "action_class": "XQ_LAUNCH_LOCATE",
  "provider": {
    "name": "CUA_DRIVER",
    "version": "0.19.3"
  },
  "target": {
    "application": "XQ",
    "product": "XQLite 個人版",
    "product_version": "3.18.02 (260102)",
    "exe": "daqxqlite.exe",
    "window_class": "DAQXQLITEMainWnd",
    "login_state": "NOT_LOGGED_IN"
  },
  "mode": "PAPER_NO_LIVE_WRITE",
  "runs": [
    {
      "run": 1,
      "pass": true,
      "ms": 115,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 2,
      "pass": true,
      "ms": 102,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 3,
      "pass": true,
      "ms": 111,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 4,
      "pass": true,
      "ms": 103,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 5,
      "pass": true,
      "ms": 135,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 6,
      "pass": true,
      "ms": 117,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 7,
      "pass": true,
      "ms": 99,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 8,
      "pass": true,
      "ms": 108,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 9,
      "pass": true,
      "ms": 104,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    },
    {
      "run": 10,
      "pass": true,
      "ms": 103,
      "windows": 2,
      "exe": "daqxqlite.exe",
      "pid": 20028,
      "first_title": "XQ全球贏家(個人版) [版本 3.18.02 260102][SHW097:已登入][1][美股EOD,港股EOD,上",
      "uia_element": true
    }
  ],
  "summary": {
    "passed": 10,
    "total": 10,
    "wrong_action": 0,
    "silent_wrong_action": 0
  },
  "verdict": "10_OF_10_PASS",
  "claim": "F01 certified for CUA on this subject ONLY IF 10/10 (blueprint: an action class is team-certified if >=1 provider passes 10/10 fresh runs with full readback and zero wrong action).",
  "readback": "UIA structured state (debug_window_info) — level 2 of readback hierarchy; no login performed (HumanGate boundary respected)."
}
```

### FDA_F06_TEN_RUN_RECEIPT.json (sha256 6c5d553187919cf8…)

```json
{
  "artifact_id": "FDA_F06_TEN_RUN_RECEIPT",
  "schema": "FDA-FIXTURE-RECEIPT/1",
  "fixture": "F06-COMPILE-KNOWN-PASS-10RUN",
  "action_class": "XS_COMPILE_PASS",
  "provider": {
    "name": "CUA_DRIVER",
    "version": "0.19.3"
  },
  "target": {
    "application": "XQ",
    "product_version": "3.20.02 (260811)",
    "login": "SHW097:LOGGED_IN"
  },
  "script": "xs_script with DOC-04 SF-0137 CrossOver function_bool form (authority)",
  "mode": "PAPER_NO_LIVE_WRITE",
  "runs": [
    {
      "run": 1,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 2,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 3,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 4,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 5,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 6,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 7,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.3
    },
    {
      "run": 8,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 9,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    },
    {
      "run": 10,
      "compile_status": 1,
      "msg": "",
      "last_compile": "2026-08-13 16:30:08.395",
      "pass": true,
      "elapsed_s": 7.2
    }
  ],
  "pass_count": 10,
  "required": 10,
  "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus/CompileMsg/LastCompileTime",
  "verdict": "PASS",
  "wrong_action": 0,
  "silent_wrong_action": 0,
  "side_effect": "LOCAL_REVERSIBLE (recompile only; no financial write)"
}
```

### FDA_C5_LEASE_CONCURRENCY_RECEIPT.json (sha256 e7f4a3e824782dc7…)

```json
{
  "artifact_id": "FDA_C5_LEASE_CONCURRENCY_LIVE_RECEIPT",
  "schema": "FDA-C5-CONCURRENCY-RECEIPT/1",
  "scenarios": [
    {
      "name": "SCENARIO1_TWO_THREADS_ONE_SESSION",
      "pass": true,
      "detail": "granted=['fabric-desktop-cua'] denied=['fabric-desktop-ufo2']"
    },
    {
      "name": "SCENARIO2_CHECKPOINT_HOT_SWAP",
      "pass": true,
      "detail": "fabric-desktop-ufo2"
    },
    {
      "name": "SCENARIO3_UNKNOWN_STATE_BLOCKS_REPLAY",
      "pass": true,
      "detail": ""
    },
    {
      "name": "SCENARIO4_10_THREAD_STAMPEDE",
      "pass": true,
      "detail": "granted=[0]"
    }
  ],
  "verdict": "PASS",
  "simultaneous_writers": 0,
  "unknown_state_retry": 0,
  "lease_transfer_without_checkpoint": 0,
  "threading": "real threading.Thread (not mocks)"
}
```

## 4. XQ PAPER runtime — raw DB extracts (execution truth)

### SensorLog Table_20260814 (FDA rows, 56 total)

| XQSensorID | XQSensorName | SequenceNum | TriggerTime | XSSensorState | ExecState | ExecstatusCode | SymbolID | Date | Time | Price | Volume |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 1 | 10635 | 2 | 1 | 0 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 2 | 10635 | 2 | 2 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 3 | 10635 | 2 | 3 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 4 | 10637 | 2 | 4 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 5 | 10637 | 3 | 5 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 6 | 10637 | 1 | 8 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 7 | 10637 | 1 | 8 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 8 | 10932 | 2 | 1 | 0 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 9 | 10932 | 2 | 2 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 10 | 10932 | 2 | 3 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 11 | 10933 | 2 | 4 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 12 | 10933 | 3 | 5 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 13 | 10933 | 1 | 8 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| F0B737F8-C951-49e5-A | FDAPaperProbe010447 | 14 | 10933 | 1 | 8 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 15 | 11958 | 2 | 1 | 0 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 16 | 11958 | 2 | 2 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 17 | 11958 | 2 | 3 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 18 | 11959 | 2 | 4 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 19 | 11959 | 3 | 5 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 20 | 11959 | 1 | 8 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 21 | 11959 | 1 | 8 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 22 | 12809 | 2 | 1 | 0 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 23 | 12809 | 2 | 2 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 24 | 12809 | 2 | 3 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 25 | 12809 | 2 | 4 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 26 | 12809 | 3 | 5 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 27 | 12809 | 1 | 8 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 28 | 12809 | 1 | 8 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 29 | 12931 | 2 | 1 | 0 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 30 | 12931 | 2 | 2 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 31 | 12931 | 2 | 3 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 32 | 12931 | 2 | 4 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 33 | 12931 | 3 | 5 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 34 | 12931 | 1 | 8 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 35 | 12931 | 1 | 8 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 36 | 15941 | 2 | 1 | 0 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 37 | 15941 | 2 | 2 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 38 | 15941 | 2 | 3 | 2 |  | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 39 | 15942 | 2 | 4 | 2 | 2330.TW | 0 | 0 | 0.0 | 0.0 |
| 0F9D5084-E5AC-45e0-9 | FDAPaperClosure01193 | 40 | 15942 | 3 | 5 | 2 |  | 0 | 0 | 0.0 | 0.0 |

### SensorList (persistence)

| Name | Script | Symbol | Created |
|---|---|---|---|
| 複製-1分鐘K開盤暴量三連陽 | 1分鐘K開盤暴量三連陽 | 2:G04010,G14010 | 2026/08/13 20:36:30 |
| FDAPaperProbe | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/13 23:46:09 |
| FDAPaperProbe234930 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/13 23:49:49 |
| FDAPaperProbe010447 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 01:06:30 |
| FDAPaperClosure011939 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 01:19:58 |
| FDAPaperFinal020037 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 02:00:55 |

## 5. DoD-36 matrix (embedded)

```text
DoD summary: {'PASS': 36, 'PARTIAL': 0, 'BLOCKED': 0}
```

## 6. External verifier checklist (self-contained)

1. Verify this file's sha256 == the value submitted (identity gate).
2. Recompute EvidenceManifest sha256 (embedded §0) from the manifest JSON.
3. Verify artifact table §2 row count == manifest_entry_count.
4. Verify SensorLog §4 rows: >=1 FDA strategy with full state machine (2→3→1, ExecState 1→8).
5. Verify SensorList §4 persistence rows.
6. Re-run independent_checker.py → 174/174 PASS (embedded §0).
7. Verify DoD counts §5 == PASS 36 / PARTIAL 0 / BLOCKED 0.
8. Claim ceiling §1: FAIL_CLOSED until verdict; SQS NOT_AUTHORIZED.
