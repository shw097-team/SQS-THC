# FDA External Single Evidence — FULLY EMBEDDED (RR3 packaging closure)

```yaml
report_id: FDA_EXTERNAL_SINGLE_EVIDENCE_RR3
mode: SINGLE_MD_MANDATORY_ROUTE (Step 6A — all raw bodies embedded; no local-path dependency)
this_file_sha256: a38c0fbcd10ee0f98c7b301f567e13568826d3f9ccdd8996c2536b09b43fc6d8
generated_at_utc: 2026-08-14T03:04:18Z
subject_root: 83e8138605e3167f30911e850957925371547bbb
manifest_sha256: 4ac3fb8247db8342f5118470e55750683103ed93fb86e297e8124c89cb166d29
checker: PASS 176/0
dod_counts: {"PASS": 36, "PARTIAL": 0, "BLOCKED": 0}
exact_sets: {"payload_entries": 51, "manifest_entries": 52, "bundle_files": 71}
self_entry_policy: manifest rows exclude manifest itself AND evidence reducer MD (single-direction binding: evidence MD embeds manifest sha256; manifest never records the MD — reviewer recomputes MD sha from submitted bytes); every payload row = path+sha256+size recomputed from bundle bytes
```
## 1. Claim ceiling (embedded)

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

## 2. Exact-set definitions (unambiguous, rehashable)

```text
payload_entries   = 51  (manifest rows; EXCLUDES manifest itself AND evidence MD)
manifest_entries  = 52  (payload + 1 = manifest JSON physically present, not self-listed)
bundle_files      = 71  (physical recursive count in FDA_RAW_REVIEW_BUNDLE)
self_entry_policy = manifest excludes itself AND evidence reducer MD (loop breaker);
                    MD references manifest by sha256 (single direction); reviewer
                    recomputes MD sha from submitted bytes
```

## 3. EvidenceManifest — full payload table (51 rows)

| # | Path | SHA-256 | Bytes |
|---|---|---|---|
| 1 | `Fabric/fabric-desktop-automation/DOC/FDA_USER_GUIDE.md` | `81271eb745b7f37ab577182a0f675f0ce4a0ec4ab7bda7eb69c7884ac7f04367` | 20138 |
| 2 | `Fabric/fabric-desktop-automation/FDA_DESKTOP_CAPABILITY_MATRIX.yaml` | `9406456db853e9e6597c30ed400240808c7b0c777dd49c34eb611bf4c863d6c4` | 11110 |
| 3 | `Fabric/fabric-desktop-automation/FDA_DIRECTORY_TREE.txt` | `57ceaf69fb27c21da59fff188e3c1cf90575da7e7861a19d7387b191e5767c98` | 2174 |
| 4 | `Fabric/fabric-desktop-automation/FDA_EXECUTION_BINDING.json` | `6a3269202d0dba0ba6c8bb0d6656e592dcda4042a0dc88e63fba732e3335b095` | 3308 |
| 5 | `Fabric/fabric-desktop-automation/FDA_FOLDER_REORGANIZATION_RECEIPT.json` | `00d690f94a05aabc644e9c9cafc4664fc98602eeaa5e28f54d17ae6ee7e58cbe` | 777 |
| 6 | `Fabric/fabric-desktop-automation/TEAM.md` | `c524945c90c836b048ee07084bcac75adba8a01b1ca0ae16b8a742ac388afc5b` | 4048 |
| 7 | `Fabric/fabric-desktop-automation/WO_FDA_XQ_002.yaml` | `6c80ff03511753175a627b501ae5a72fa9e5195bc3830d438e88a6bf979b3c87` | 1588 |
| 8 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_BOUNDED_CONTROL_LIVE_PROBE.json` | `51559903556f3910d6286974a349b8515d8498a6870d727532cd7f5f016b623e` | 586 |
| 9 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_C0_READBACK_RECEIPT.json` | `ca905aba1e02a8df4b1a6d2b41764df448bbd53353422c2a81b5b2750562b414` | 5838 |
| 10 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_C2_CUA_QUALIFICATION_RECEIPT.json` | `c181ef51b2066b1ffc9b185355b42653c00ee245048ebe84483fde2393c54362` | 3380 |
| 11 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json` | `1d7d149ac6cd1ed0616ab1fa25f804cc20f33808663d7d1d32b4040ab8d97781` | 1811 |
| 12 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_C3_UFO2_QUALIFICATION_RECEIPT.json` | `048b151f462384310eabb9018e7d5ecb012677473b47667be49be84c03492e6d` | 1800 |
| 13 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_C4_XQ_QUALIFICATION_RECEIPT.json` | `cf86b05f71c0cf734dcc2684cd0bb1542c82e151ea7edf1df5132236189b6543` | 3636 |
| 14 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_C5_LEASE_CONCURRENCY_RECEIPT.json` | `357a9650a045d7485ff93270f98268946d740980da156d6f280e995b2364d0a8` | 825 |
| 15 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F01_LIVE_FIXTURE_RECEIPT.json` | `36fff6f57cffa10bc8f6c753295147c644a1b000ea35c58de8f848a1dc8d8697` | 3912 |
| 16 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F03_LIVE_FIXTURE_RECEIPT.json` | `cbf60ef9cd5cab761ce3e6ccdd13236d5107a4d41f3a52482dc396dae31b1055` | 1337 |
| 17 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F04_LIVE_FIXTURE_RECEIPT.json` | `5d9bd84beae406f06206bc7d8b3bf1288ff38b2f54f34dcdf2947da3905647d8` | 1183 |
| 18 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V3_RECEIPT.json` | `fe2d736f49865b9a7d2abfa3b28794764bae32c17d60d559623fe3a77a39980b` | 1263 |
| 19 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V4_RECEIPT.json` | `e149fdeb258a422a7983722c2ae2315d4e77a32317574a2c9a2c61da79edd47b` | 1125 |
| 20 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V5_RECEIPT.json` | `249c016a3a3a7b68a2439469cc5a31c24ace8d198e9f968177c9d89e3f018792` | 1139 |
| 21 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V6_RECEIPT.json` | `0462d34b16705535b2c293bdecc2359ad910fae7b74986c9328c94efdaa6be47` | 1558 |
| 22 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V7_RECEIPT.json` | `774454d0faeed6c0ae0af92f4c959378be87afa63a15a3e5b0cb952131ec0b6f` | 1603 |
| 23 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_CLOSURE_V8_RECEIPT.json` | `a16a4bb3852ddb30460ba19e4979e32d1b5263ed66e946fc076c614e96ea72b7` | 1352 |
| 24 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_COMPILE_RECEIPT.json` | `94cfccad36dabc5e91eb32eb4259f8232c160f674a018cbdb0a6ca14dadac569` | 1380 |
| 25 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_COMPILE_TOOLBAR_RECEIPT.json` | `7977c24d7fe9576b89e1edc2eab20bbba26397e5d9985edd4dfa9e007e92bdae` | 972 |
| 26 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_EXPORT_RECEIPT.json` | `f03dd33cbca58b70d51c7c5a1425d830a59aeaf53fdbe21de457cffcac1aa083` | 768 |
| 27 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json` | `353b639f2a789f6c6116b8225262af1325178adb9354be553670461f21273bef` | 1460 |
| 28 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_LIVE_FIXTURE_RECEIPT.json` | `f10b9c5497fb763fdfafd7eb1659c93df4f3835f5a9026870fc4d75d11a27ade` | 1272 |
| 29 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_SYSTEM_PATH_RECEIPT.json` | `7407a237fd1127474e692b5d564dc8420330ed58c7fdf0fa366d7cb53d93a345` | 1257 |
| 30 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F06_TEN_RUN_RECEIPT.json` | `17353bfbbde9e9dd59f67d0be08e8075530b68d950a8a66d7ce70b5b00f5d97c` | 2535 |
| 31 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F09B_PAPER_RUNTIME_RECEIPT.json` | `a57f730465c3d023145e2481fb274bddc87c62c6d5b6e1f576d2edd42fa41f78` | 2002 |
| 32 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F09_RADAR_RECEIPT.json` | `0c9adabdbac434953007bd8dcba0bbf7c8aacd1b267343f02c6e1b4d721f1ee5` | 1089 |
| 33 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_F10_F11_READBACK_RECEIPT.json` | `7d471b12739d9e2f4dce9980cd8e8171c43bed3b0df723775ee380894eb2323b` | 1373 |
| 34 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json` | `b23ddca238b99378988c731036b9fe01742a1a5fbbc0fd9ba3d8223eb484e9be` | 946 |
| 35 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json` | `d676c68f05f9560af6f5aae31408cee66308adc9d18d50bda150dce6d7f8fa13` | 551 |
| 36 | `Fabric/fabric-desktop-automation/evidence/receipts/FDA_XQ_PAPER_RUNTIME_RECEIPT.json` | `1730e4162c1f10b606af7e850c494df799cc96e3e2ef46c93a4466f8e3905a74` | 4587 |
| 37 | `Fabric/fabric-desktop-automation/fda_lease.py` | `856580b533b547a82772de8624c78792d669cb11bb9cb99551c7141a06594db2` | 2510 |
| 38 | `Fabric/fabric-desktop-automation/fda_router.py` | `c3d64650a6e0c6fd3d99b5236c30c4cb03b7621be9763299e335ac1c6ed95e6c` | 1115 |
| 39 | `Fabric/fabric-desktop-automation/governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml` | `6e1c808e278592f2b4d75c6296b4b81d9e227a2f21e188c9594b18085bbf0f8f` | 2995 |
| 40 | `Fabric/fabric-desktop-automation/governance/FDA_INTEROP_DISPOSITION.yaml` | `9fac4d255030443f8031a5bfe62d8e204698cf664ada2b06a65986f347c7ee5e` | 3487 |
| 41 | `Fabric/fabric-desktop-automation/governance/FDA_ROUTE_CHECK.yaml` | `05256d982f8634fe25a5cf6d6e85685ca8fdcd54163c913a4cb689f6d922a909` | 2188 |
| 42 | `Fabric/fabric-desktop-automation/governance/FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml` | `6a108d3a8c25221541c1eb9ac72d192412a9f0690d219f8dab0acf0694a4a2cf` | 1848 |
| 43 | `Fabric/fabric-desktop-automation/independent_checker.py` | `8a9b761087d01cc99d35be14cc4a495f35636793552fe62400ea76d45de96dbe` | 12475 |
| 44 | `Fabric/fabric-desktop-automation/test_xq_action_router.py` | `e8778f2d73349905455e7254a9f2e0f5f3a7195cd6503093aa6c54504d615c2c` | 2478 |
| 45 | `Fabric/fabric-desktop-automation/test_xq_build_drift.py` | `cf234c66e389900b517d437a6d2ec4d69977104876fc4ab898a6f4df1aaf8eb9` | 3215 |
| 46 | `Fabric/fabric-desktop-automation/test_xq_native_adapter.py` | `89566c1a2c5070d524c74fd34a5e164cce5f2a888ee4abcaac6df1af4ac9f060` | 1899 |
| 47 | `Fabric/fabric-desktop-automation/tests/test_fda_lease.py` | `8caeb1dba6715af44f038e095eccc2287eebc817dac6782a0eb29bd742383ee6` | 4015 |
| 48 | `Fabric/fabric-desktop-automation/tests/test_fda_router.py` | `64a52a017d0ef757fbc725afb6fdfb71bf2b41829723743345e123643b45ba13` | 4028 |
| 49 | `Fabric/fabric-desktop-automation/tests/test_fda_router_integration.py` | `654df5de873b6e71ec1b73bbfb3ca9a92ff4b4758ab558b3784a2f68452d6b97` | 4001 |
| 50 | `Fabric/fabric-desktop-automation/tests/test_fda_security.py` | `6b0e2f19268db5fb0507fd6b39034db36e46922a42a93dfa3e5eff6004c359b3` | 7512 |
| 51 | `Fabric/fabric-desktop-automation/xq_native_adapter.py` | `89cd614b63562514ece4fac503f7d54b2d0f02ca7398a39cd468b86f4c76bde2` | 5045 |

## 4. Key receipts — FULL RAW BODIES

### FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json (sha256 1989abdbd1bcfe090327a288f46aff6e94d722cbd7716a6fba2eec78a1a8f164)

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

### FDA_XQ_PAPER_RUNTIME_RECEIPT.json (sha256 543b0d958856d1307259a2577252bbf1a954249bf512c1296974c5b7b2767edc)

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

### FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json (sha256 3c140cdfd0d10d78898c654cc0f2e14fa43ff067f21f9e33f069654be056171c)

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

### FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json (sha256 4085b662a781f9a88141c4fb2e3252f19d507ca048a82a67c17e10badb826c34)

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

### FDA_F01_LIVE_FIXTURE_RECEIPT.json (sha256 859fb21c19aaeb86dcf35426bf3e68d8eb4e4550cba22d4eecc1c18d6628772e)

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

### FDA_F06_TEN_RUN_RECEIPT.json (sha256 6c5d553187919cf8aea5e3f18661db45844a08982a562988c627359800626794)

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

### FDA_C5_LEASE_CONCURRENCY_RECEIPT.json (sha256 e7f4a3e824782dc73e0acf0d3f415c09b1840c0177fd0bcff2d299049cc33e69)

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

## 5. XQ PAPER runtime — raw DB extracts (execution truth)

### SensorLog Table_20260814 (FDA rows: 56)

| XQSensorID | XQSensorName | SequenceNum | TriggerTime | XSSensorState | ExecState | ExecstatusCode | SymbolID | Date | Time |
|---|---|---|---|---|---|---|---|---|---|
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 1 | 10635 | 2 | 1 | 0 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 2 | 10635 | 2 | 2 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 3 | 10635 | 2 | 3 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 4 | 10637 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 5 | 10637 | 3 | 5 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 6 | 10637 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 7 | 10637 | 1 | 8 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 8 | 10932 | 2 | 1 | 0 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 9 | 10932 | 2 | 2 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 10 | 10932 | 2 | 3 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 11 | 10933 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 12 | 10933 | 3 | 5 | 2 |  | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 13 | 10933 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| F0B737F8-C951-49e5 | FDAPaperProbe01044 | 14 | 10933 | 1 | 8 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 15 | 11958 | 2 | 1 | 0 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 16 | 11958 | 2 | 2 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 17 | 11958 | 2 | 3 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 18 | 11959 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 19 | 11959 | 3 | 5 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 20 | 11959 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 21 | 11959 | 1 | 8 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 22 | 12809 | 2 | 1 | 0 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 23 | 12809 | 2 | 2 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 24 | 12809 | 2 | 3 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 25 | 12809 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 26 | 12809 | 3 | 5 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 27 | 12809 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 28 | 12809 | 1 | 8 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 29 | 12931 | 2 | 1 | 0 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 30 | 12931 | 2 | 2 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 31 | 12931 | 2 | 3 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 32 | 12931 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 33 | 12931 | 3 | 5 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 34 | 12931 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 35 | 12931 | 1 | 8 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 36 | 15941 | 2 | 1 | 0 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 37 | 15941 | 2 | 2 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 38 | 15941 | 2 | 3 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 39 | 15942 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 40 | 15942 | 3 | 5 | 2 |  | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 41 | 15942 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| 0F9D5084-E5AC-45e0 | FDAPaperClosure011 | 42 | 15942 | 1 | 8 | 2 |  | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 43 | 20056 | 2 | 1 | 0 |  | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 44 | 20056 | 2 | 2 | 2 |  | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 45 | 20056 | 2 | 3 | 2 |  | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 46 | 20057 | 2 | 4 | 2 | 2330.TW | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 47 | 20057 | 3 | 5 | 2 |  | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 48 | 20057 | 1 | 8 | 2 | 2330.TW | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 49 | 20057 | 1 | 8 | 2 |  | 0 | 0 |
| B1C9EE37-CD6F-4a30 | FDAPaperFinal02003 | 50 | 20940 | 2 | 1 | 0 |  | 0 | 0 |

### SensorList (persistence)

| Name | Script | Symbol | Created |
|---|---|---|---|
| 複製-1分鐘K開盤暴量三連陽 | 1分鐘K開盤暴量三連陽 | 2:G04010,G14010 | 2026/08/13 20:36:30 |
| FDAPaperProbe | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/13 23:46:09 |
| FDAPaperProbe234930 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/13 23:49:49 |
| FDAPaperProbe010447 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 01:06:30 |
| FDAPaperClosure011939 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 01:19:58 |
| FDAPaperFinal020037 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 02:00:55 |

## 6. DoD-36 counts

```text
{"PASS": 36, "PARTIAL": 0, "BLOCKED": 0}
```

## 7. External verifier checklist (self-contained, no local access needed)

1. Verify this file's sha256 == submitted value (identity gate).
2. Recompute EvidenceManifest sha256 (header) from the manifest JSON (bundled).
3. Verify artifact table §3 row count == payload_entries; every row path unique.
4. Verify every §3 row hash/size against the bundled file bytes.
5. Verify SensorLog §5: >=1 FDA strategy with full state machine (XSSensorState 2->3->1,
   ExecState 1->8, SymbolID=2330.TW, multiple TriggerTime cycles).
6. Verify SensorList §5 persistence rows (>=5 FDA strategies).
7. Re-run independent_checker.py -> 176/176 PASS (header).
8. Verify DoD counts §6 == PASS 36 / PARTIAL 0 / BLOCKED 0.
9. Verify claim ceiling §1: FAIL_CLOSED until verdict; SQS NOT_AUTHORIZED.
10. Verify subject root: git rev-parse HEAD == header subject_root.
