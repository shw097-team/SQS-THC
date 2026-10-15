# Five-Clocks 時鐘契約｜DSV-DAILY-2026-08-13-r2（FOCUSED-02）

```yaml
artifact_id: FIVE_CLOCKS_CONTRACT_DAILY_2026-08-13
workorder: WO-RP2-DAILY-003
binding_finding: DA-EXT-004（REOPENED_PARTIAL）
owner: SQS-THC / TW-ICT FSDT-Stack owner
checker: independent acceptance officer
generated_at: 2026-08-13
model: DAILY_EOD_CONSERVATIVE（publication_time := availability_time := known_at）
```

## 1. 五時鐘 canonical 語義（materialized projection，不新增實體欄位）

| Clock | 本 DSV 欄位/值 | Derivation | 語義 |
|---|---|---|---|
| **event_time** | `asof`（DATE, 交易日） | TWSE 官方 STOCK_DAY 交易日曆日 | 事實（EOD bar）之有效日；EOD bar 無盤中時間戳，event_time 為日粒度 |
| **publication_time** | `known_at`（DATE = asof + 1 曆日） | 保守 EOD 發佈模型（見 §2） | 官方 EOD 資料最早可被視為已發佈之時間 |
| **availability_time** | `known_at`（同欄位） | **publication_time := availability_time**（owner-backed equivalence, §2） | 資料獲授權可供決策使用之時間 |
| **ingest_time** | `retrieved_at`（TIMESTAMPTZ, UTC） | 實際抓取時點（fetch 當下記錄） | 資料物理進入本系統之時間 |
| **decision_time** | consumer 決策時間戳 | 消費端 predicate 輸入 | bar 可見條件：`availability_time <= decision_time` |

## 2. Owner/source-backed equivalence（publication := availability := known_at）

**Equivalence 宣告（owner: SQS-THC / TW-ICT FSDT-Stack；basis: TWSE 官方 EOD 發佈模型 + DOC-06 五時鐘契約 + 保守回測慣例）：**

```text
publication_time := availability_time := known_at := asof + 1 calendar day
```

依據：
1. **Source model**：TWSE 官方 STOCK_DAY 為每日收盤後發佈之 EOD 資料（13:30 收盤後陸續發佈）；官方回應不含盤中發佈時間戳。
2. **保守性**：資料來源無法證明「D 日收盤在 D 日 00:00 即可用」，故取**最保守可用時間 = D+1 00:00**（D 日收盤自 D+1 起可用）。
3. **Conservation consequence（明示）**：任何 D 日決策（即使 13:30 收盤後）**不得**使用 D 日收盤列——系統以 `known_at(D+1) > decision_time(D)` 拒絕；此為刻意保守之 trade-off（犧牲 D 日收盤後即時可用性，換取無同日前瞻保證）。
4. **Equivalence 不增加新欄位**：single field `known_at` 同時服務 publication 與 availability；結構性等值由 C10（known_at == asof+1d 全列）與 C11（causal ordering）驗證。

## 3. Causal ordering predicates（fresh checker 驗證）

```text
P1  event_time < publication_time        : known_at > asof            （全列, C11 late_publication == 0）
P2  event_time <= ingest_time            : retrieved_at >= asof       （全列, C11 early_ingest == 0）
P3  publication_time == availability_time: 結構性（single field known_at, C10 == asof+1d）
P4  availability_time <= decision_time   : 決策時點 gate（PIT canary 負例, 見 §4）
```

- P1/P2/P3 由 `check_daily` C10+C11 驗證（11/11 PASS）。
- P4 由 `pit_canary_daily.py` 驗證（same-day negative fixture 維持 PASS）。

## 4. Negative fixture（維持 PASS）

```text
2026-08-13 EOD rows 存在於 DB（257 列）
decision_time = 2026-08-13 09:30  →  visible = 0（reject/abstain）
decision_time = 2026-08-14 09:00  →  visible = 257（全部可用）
```

## 5. Revision policy 綁定

- raw：immutable（逐窗 sha256 receipts；無 revision/transaction 時鐘——無修訂即無 transaction time）。
- DSV：r1 → r2 lineage（catalog + manifest parent 欄位）；sealed snapshot 絕不原地改寫；未來改版 = 新 semantic version。
- 本契約與 DSV manifest、schema metadata、evidence 三邊一致（manifest 之 dataset_version / rows / symbol_count 與本契約 subject 相同；無矛盾）。

## 6. 驗證

- 檢查：五時鐘全數具 canonical 值/欄位、equivalence 宣告 + basis 具備、causal predicates 全 PASS、負例 PASS、revision policy 明確 ＝ PASS。
- 負例：任何 known_at <= asof 或 retrieved_at < asof 之列 → C11 FAIL（0 容忍）；任何 D 日決策看到 D 日收盤 → canary FAIL（0 容忍）。
