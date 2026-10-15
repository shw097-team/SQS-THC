# FDA RAW EVIDENCE — SINGLE FILE (RR5 minimum external set, 8/8 embedded)

```yaml
report_id: FDA_RAW_EVIDENCE_SINGLE_MD_RR5
this_file_sha256: 4611fe561ac1d539581e1161fd9906f4bbb829d1c7c49ca816b44a5298bd4820
generated_at_utc: 2026-08-14T03:30:26Z
subject_root: e7b289449775ba9be622d69c0547e7bad1256c18
manifest_sha256: b07d5d810d6ee2d4f18d6acaa93e0661cf43998b5987fbebf9296571aca804ea
checker: 179/179 PASS (fresh run below)
mode: ALL RAW BODIES EMBEDDED — external reviewer needs no local-path/MEDIA access
```
## 1. Final subject-root / git readback (fresh)

```text
git rev-parse HEAD (evidence packaging commit) = a7b3a42a760554a7ac3dc5e22813ee843ec9bc49
frozen artifacts subject root (reducer-declared) = e7b289449775ba9be622d69c0547e7bad1256c18
  (exists: git cat-file -e e7b289449775ba9be622d69c0547e7bad1256c18)

git log -3:
a7b3a42 FDA (RR4 minimal evidence closure, Track A-E): FINAL post-reorg freeze — HEAD e7b2894; EvidenceManifest regenerated from final paths (54 rows = 54 payload = exactly one path each, reducer_in_manifest=false, manifest_self_entry=false, sha b07d5d81); ONE current checker denominator 179/179 (144/174/175/176 all marked HISTORICAL subject-bound); final reducer machine-generated LAST (sha 025bd73d), no mutation after Final; loop-free verified (manifest sha stable after reducer sync); 5-way reducer byte-equal; raw bundle complete
e7b2894 FDA (Plan A + Step 6B Evidence Home Rule): evidence/ convergence layer — FDA_IMPLEMENTATION_EVIDENCE.md + manifest + single-MD + readback + tree now live in fabric-desktop-automation/evidence/ (team home, matching FAR/SQS structure); Fabric/HGK/SQS evidence/review remain byte-identical mirrors; bundle re-synced (payload 55, manifest 2920cd48); checker 179/179; HGK skill Step 6B added to prevent recurrence on other projects
590ea59 FDA (Step 6A mandatory route): single fully-embedded external review evidence MD (RR3 packaging closure) — all raw bodies inlined: 7 receipt JSONs, SensorLog Table_20260814 + SensorList raw rows, 51-row manifest payload table, exact sets, DoD 36/36, checker 176/176, subject 83e8138, manifest sha 4ac3fb82; sha256 2687e4d5; 3-way mirror byte-equal; external reviewer needs zero local-path/MEDIA access
```

## 2. FDA_EVIDENCE_MANIFEST.json (full body)

### FDA_EVIDENCE_MANIFEST.json (final)

```json
{
  "artifact_id": "FDA_EVIDENCE_MANIFEST",
  "schema": "FDA-EVIDENCE-MANIFEST/3",
  "version": "FINAL_RR4_POST_REORG",
  "generated_at_utc": "2026-08-14T03:21:39Z",
  "subject_root": {
    "repo": "Fabric",
    "git_head": "e7b289449775ba9be622d69c0547e7bad1256c18",
    "note": "FINAL post-folder-reorg frozen HEAD (RR4 Track A)"
  },
  "exact_set": {
    "manifest_row_count": 54,
    "payload_file_count": 54,
    "bundle_file_count": 76,
    "reducer_in_manifest": false,
    "manifest_self_entry": false,
    "note": "manifest_row_count == payload_file_count == number of rows; every row = exactly one filesystem path; reducer MD and manifest itself are EXCLUDED (reducer_in_manifest=false, manifest_self_entry=false); bundle_file_count includes non-payload support files (manifest, index, readbacks, reducer MD)."
  },
  "checker": {
    "script": "Fabric/fabric-desktop-automation/independent_checker.py",
    "verdict": "PASS",
    "checks": 179,
    "failed": 0,
    "note": "single fresh run on final HEAD (RR4 Track C); historical denominators 144/174/175/176 superseded — see checker_history"
  },
  "checker_history": [
    {
      "checks": 144,
      "status": "HISTORICAL",
      "subject": "pre-XQ-patch",
      "superseded_by": "176"
    },
    {
      "checks": 174,
      "status": "HISTORICAL",
      "subject": "XQ build-aware + T160-T177",
      "superseded_by": "176"
    },
    {
      "checks": 175,
      "status": "HISTORICAL",
      "subject": "folder-reorg path checks (interim)",
      "superseded_by": "176"
    },
    {
      "checks": 176,
      "status": "HISTORICAL",
      "subject": "post-reorg stable (RR3)",
      "superseded_by": "179"
    },
    {
      "checks": 179,
      "status": "CURRENT",
      "subject": "post-reorg final HEAD e7b289449775"
    }
  ],
  "dod_counts": {
    "PASS": 36,
    "PARTIAL": 0,
    "BLOCKED": 0
  },
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
    }
  ],
  "artifact_count": 54,
  "missing_artifacts": []
}
```

```text
recomputed manifest sha256 = b07d5d810d6ee2d4f18d6acaa93e0661cf43998b5987fbebf9296571aca804ea
rows = 54 · payload = 54 · bundle = 76
reducer_in_manifest = False · manifest_self_entry = False
```

## 3. Independent checker — fresh raw stdout (VERIFY_ONLY)

```text

command: C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe independent_checker.py
exit: 0

XQ_LAUNCH_LOCATE CUA QUALIFIED with live reason",
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

```

## 4. UFO2 effective-load receipt (full body)

### FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json

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

## 5. XQ PAPER runtime receipt (full body)

### FDA_XQ_PAPER_RUNTIME_RECEIPT.json

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

## 6. SensorLog / SensorList deterministic raw extract (fresh query)

```text
DB: C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite
table: Table_20260814
FDA strategy rows: 56
columns: ['XQSensorID', 'XQSensorName', 'SequenceNum', 'TriggerTime', 'XSSensorState', 'ExecState', 'ExecstatusCode', 'SymbolID', 'Date', 'Time', 'Price', 'Volume']

first 30 rows (raw bytes, cp950-decoded):

  F0B737F8-C951-49 | FDAPaperProbe010 | 1 | 10635 | 2 | 1 | 0 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 2 | 10635 | 2 | 2 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 3 | 10635 | 2 | 3 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 4 | 10637 | 2 | 4 | 2 | 2330.TW | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 5 | 10637 | 3 | 5 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 6 | 10637 | 1 | 8 | 2 | 2330.TW | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 7 | 10637 | 1 | 8 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 8 | 10932 | 2 | 1 | 0 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 9 | 10932 | 2 | 2 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 10 | 10932 | 2 | 3 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 11 | 10933 | 2 | 4 | 2 | 2330.TW | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 12 | 10933 | 3 | 5 | 2 |  | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 13 | 10933 | 1 | 8 | 2 | 2330.TW | 0 | 0

  F0B737F8-C951-49 | FDAPaperProbe010 | 14 | 10933 | 1 | 8 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 15 | 11958 | 2 | 1 | 0 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 16 | 11958 | 2 | 2 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 17 | 11958 | 2 | 3 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 18 | 11959 | 2 | 4 | 2 | 2330.TW | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 19 | 11959 | 3 | 5 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 20 | 11959 | 1 | 8 | 2 | 2330.TW | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 21 | 11959 | 1 | 8 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 22 | 12809 | 2 | 1 | 0 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 23 | 12809 | 2 | 2 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 24 | 12809 | 2 | 3 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 25 | 12809 | 2 | 4 | 2 | 2330.TW | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 26 | 12809 | 3 | 5 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 27 | 12809 | 1 | 8 | 2 | 2330.TW | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 28 | 12809 | 1 | 8 | 2 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 29 | 12931 | 2 | 1 | 0 |  | 0 | 0

  0F9D5084-E5AC-45 | FDAPaperClosure0 | 30 | 12931 | 2 | 2 | 2 |  | 0 | 0

```

```text
DB: C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite
SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList
rows: 6

  複製-1分鐘K開盤暴量三連陽 | 1分鐘K開盤暴量三連陽 | 2:G04010,G1401 | 2026/08/13 20:36:30

  FDAPaperProbe | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/13 23:46:09

  FDAPaperProbe234930 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/13 23:49:49

  FDAPaperProbe010447 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 01:06:30

  FDAPaperClosure011939 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 01:19:58

  FDAPaperFinal020037 | FDA_PAPER_ALERT | 0:2330.TW | 2026/08/14 02:00:55

```

## 7. F01/F06 wrong_action / silent_wrong_action receipts (full bodies)

### FDA_F01_LIVE_FIXTURE_RECEIPT.json (wrong_action / silent_wrong_action)

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

### FDA_F06_TEN_RUN_RECEIPT.json (wrong_action / silent_wrong_action)

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

## 8. broker_write = 0 negative receipt

```text
broker_write field from FDA_XQ_PAPER_RUNTIME_RECEIPT.json: 
0


no-live-write scan (PAPER/no-live-write fixture; SQS live trading NOT_AUTHORIZED):

  - fixture mode: PAPER_NO_LIVE_WRITE
  - broker adapter: none (no broker write path in FDA)
  - SQS_LIVE_TRADING = NOT_AUTHORIZED (claim ceiling)
```
