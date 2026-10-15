# DOC-11-FDA-XQ-GLOBALWINNER-ROUTE — SQS → XQ 全球贏家 FDA 條件 2 常設路由

> Work order: `WO-SQS-FDA-XQ-ROUTE-001`（shared spine `workorders` 表，state=`CREATED`，writer=codex）
> Route: `ROUTE-SQS-XQ-GLOBALWINNER-001`（`FDA_ROUTE_REGISTRY.json`，schema `FDA-ROUTE-REGISTRY/1`，status=`ACTIVE`，expires=`2026-12-31`）
> 消費契約: `Fabric/fabric-desktop-automation/governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml`
> Owner: `SQS` · App: `XQ`（全球贏家）· 生效日: `2026-08-15`

## 1. 用途

本路由登記 SQS 以 FDA（fabric-desktop-automation 安全防護層）操作 XQ 全球贏家的
**條件 2（已登記受治理路由）常設授權**。在此路由生效期間，符合下列邊界的 FDA
操作無需逐次條件 1（用戶明確提及）即可執行；超出邊界的操作一律回歸條件 1 / 條件 3（HITL 詢問）。

背景：FDA 安全防護層已於 `WO-HGK-FDA-GUARD-IMPL-001` 上線；`UD-FDA-GUARDRAIL-2026-08-15-001`
D4=b 原先將 SQS→XQ 全球贏家路由列為未登記，本 WO（`WO-SQS-FDA-XQ-ROUTE-001`）即為補齊此登記。

## 2. 授權條件（機械閘）

1. **preflight**：所有 FDA 操作執行前必須親跑
   `python fda_preflight.py --action-class <CLASS> --route-id ROUTE-SQS-XQ-GLOBALWINNER-001`
   → exit 0 且 `authorization.source == "route"` 才可繼續；exit 2 = BLOCKED（停止、回報、不得重試安裝）。
2. **guard hook**：`pre_tool_call` hook（`fda_guard_hook.py`，fail_closed）於 tool call 層放行
   含 `ROUTE-SQS-XQ-GLOBALWINNER-001` token 且 registry 中該路由 ACTIVE + 未過期之 FDA 相關呼叫。
3. **有效期**：`2026-12-31` 到期；逾期後本路由自動失效（`route_expired`），須重新經 HGK WorkOrder 更新。
4. **registry mutation 權限**：`FDA_ROUTE_REGISTRY.json` 的 `mutation_authority` 為
   `ADMITTED_HGK_WORKORDER_ONLY` —— 本路由文件本身不授權任何人（含 SQS）修改 registry。

## 3. 操作邊界（NO-LIVE-WRITE 鐵律）

| 項目 | 值 | 來源 |
|---|---|---|
| 模式 | `PAPER_SHADOW_READONLY_PLUS_CONFIG` | 本路由 scope |
| Live 下單 / 改單 / 撤單 | **禁止**（`live_write: false`、`broker_write: false`） | 本路由 + FDA_DEFERRED_SEMIAUTO_CONTRACT（`SQS_LIVE_TRADING=NOT_AUTHORIZED`） |
| FDA 版本 | `FDA_V1 = LOCAL / PAPER / SHADOW / NO-LIVE-WRITE` | FDA_DEFERRED_SEMIAUTO_CONTRACT |
| ACTIVE_POSITION | 需 `HUMAN_ENTRY_APPROVAL`（FDA/Hermes/Codex 不得代批、不得進入決策迴圈） | FDA_DEFERRED_SEMIAUTO_CONTRACT phase_boundary.ENTRY |
| 自動建倉 | 禁止（`autonomous_order_submission: false`） | 本路由 |
| 輸入通道 | 僅 `CUA_BACKGROUND_ONLY` / `WIN32_MESSAGES_ONLY`（零滑鼠硬路由：無 foreground、無 bring_to_front、無 SendInput） | fda-desktop-automation skill §1.2 |

**允許的 action_classes**：`XQ_LAUNCH_LOCATE`、`XQ_PAPER_CONFIG`、`XQ_LOG_EXPORT_READBACK`、
`XS_COMPILE_PASS`、`XS_COMPILE_FAIL_READBACK`。

**允許的腳本**（glob）：`**/fda_run.py`、`**/fda_preflight.py`、`**/screen_state_check.py`、`**/xq_native_adapter.py`。
所有自動化一律經 `fda_run.py` 統一執行器（preflight + 異常自動 screen_state_check），不得裸跑。

## 4. 查詢方式（唯讀驗證）

```bash
# (a) 查 registry 路由（條件 2 授權來源）
python -c "import json;d=json.load(open(r'C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\references\FDA_ROUTE_REGISTRY.json',encoding='utf-8'));print([r for r in d['routes'] if r['route_id']=='ROUTE-SQS-XQ-GLOBALWINNER-001'])"

# (b) preflight 驗證（親跑，exit 0 + authorization.source=route 才成立）
python fda_preflight.py --action-class XQ_LAUNCH_LOCATE --route-id ROUTE-SQS-XQ-GLOBALWINNER-001

# (c) spine binding 驗證（binding_wo 必須存在於 workorders 表）
python -c "import sqlite3;c=sqlite3.connect(r'C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db');print(c.execute(\"SELECT workorder_id,state FROM workorders WHERE workorder_id='WO-SQS-FDA-XQ-ROUTE-001'\").fetchall())"

# (d) registry digest 自驗（移除 digest 欄後 canonical json.dumps(ensure_ascii=False, sort_keys=True, indent=2) 的 sha256）
```

## 5. 關聯資產

- `adapters/fda-xq-globalwinner-route.yaml` — 本路由的 SQS 側綁定宣告（machine-readable）
- `FDA_ROUTE_REGISTRY.json` → `ROUTE-SQS-XQ-GLOBALWINNER-001`（canonical 登記）
- `Fabric/fabric-desktop-automation/governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml`（消費契約）
- `Fabric/fabric-desktop-automation/FDA_DESKTOP_CAPABILITY_MATRIX.yaml`（routing truth，action_class 必須 QUALIFIED）
- `adapters/xq-read-watch.yaml` + `DOC-10.md`（TS-010 唯讀 watch，非 FDA；與本路由互補不互斥）

## 6. 非目標 / 邊界

- 不授權任何 live broker 寫入、不下單、不改單、不撤單。
- 不授權自動建倉或任何未經 `HUMAN_ENTRY_APPROVAL` 的部位操作。
- 不授權修改 `FDA_ROUTE_REGISTRY.json`（`ADMITTED_HGK_WORKORDER_ONLY`）。
- 不授權任何 foreground / 滑鼠搶焦點輸入路徑。
- 不授權 `allowed_scripts` 以外之 FDA 腳本執行。
- 本路由到期（`2026-12-31`）或被撤銷後，SQS FDA 操作回歸條件 1 / 條件 3。
