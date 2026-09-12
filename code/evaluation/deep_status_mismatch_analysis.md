# Deep Status Mismatch Analysis

This report is generated from the current engine without changing decision logic.
## Status Mismatch Summary

| request_id | user_id | expected | predicted |
|---|---|---|---|
| request_01 | user_01 | affordable_now | not_affordable |
| request_05 | user_05 | not_affordable | affordable_now |
| request_06 | user_06 | affordable_with_plan | affordable_now |
| request_10 | user_10 | not_affordable | affordable_with_plan |
| request_11 | user_11 | affordable_with_plan | affordable_now |
| request_13 | user_13 | affordable_later | affordable_now |
| request_21 | user_21 | affordable_with_plan | affordable_now |
| request_23 | user_23 | affordable_later | not_affordable |

## Root-Cause Summary

| request_id | safe amount expected | safe amount predicted | earliest expected | earliest predicted | classification |
|---|---:|---:|---|---|---|
| request_01 | 25256 | 9498.21 | 2024-03-03 |  | D/E/F: forecast recurrence amount/timing |
| request_05 | 737 | 15488 |  | 2025-11-06 | D/E/F: forecast recurrence amount/timing |
| request_06 | 603.3 | 620.4 | 2026-01-15 | 2026-01-03 | I: flexible spending optimization |
| request_10 | 12700 | 266700 |  | 2024-12-06 | I: flexible spending optimization |
| request_11 | 12510645 | 13110000 | 2025-07-15 | 2025-05-03 | I: flexible spending optimization |
| request_13 | 433.4 | 941.6 | 2024-05-15 | 2024-03-07 | D/E/F: forecast recurrence amount/timing |
| request_21 | 1543.35 | 1574.4 | 2026-04-15 | 2026-04-03 | I: flexible spending optimization |
| request_23 | 9152 | 7510.76 | 2025-07-15 | 2025-07-17 | D/E/F: forecast recurrence amount/timing |


## request_01 / user_01

- Request date: `2024-03-03`
- Requested amount: `ZAR 25256`
- Current balance: `ZAR 58481.1`
- Minimum balance: `ZAR 18000`
- Expected status: `affordable_now`
- Predicted status: `not_affordable`
- Expected method: `full_payment`
- Predicted method: `not_recommended`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; B/K/L: event inclusion, horizon, or date timing difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Pay ZAR 25,256 today. This leaves at least ZAR 18,000 available over the next 90 days.
- Predicted explanation: Do not proceed with the ZAR 25256 request. None of the available options keeps the ZAR 18000 minimum protected.
- Expected safe amount: `25256.00`; predicted safe amount: `9498.21`; difference: `-15757.79`
- Baseline minimum without request: `27498.21` on `2024-05-31`
- Plan minimum with predicted plan: `27498.21` on `2024-05-31`
- Forecast horizon: `2024-03-03` through `2024-05-31`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-03-03 | 58481.1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 58481.1 |
| 2024-03-05 | 58481.1 | 0 | 0 | 0 | 567.6 | 0 | 0 | 0 | 57913.5 |
| 2024-03-08 | 57913.5 | 0 | 761.02 | 0 | 0 | 2244.83 | 0 | 0 | 55668.67 |
| 2024-03-09 | 55668.67 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 55241.93 |
| 2024-03-10 | 55241.93 | 0 | 1821.6 | 0 | 0 | 2891.77 | 0 | 0 | 52350.16 |
| 2024-03-13 | 52350.16 | 0 | 3487 | 0 | 0 | 3722.4 | 0 | 0 | 48627.76 |
| 2024-03-15 | 48627.76 | 23320 | 761.02 | 0 | 0 | 1067.92 | 0 | 0 | 70879.84 |
| 2024-03-16 | 70879.84 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 70453.1 |
| 2024-03-22 | 70453.1 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 69692.08 |
| 2024-03-23 | 69692.08 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 69265.34 |
| 2024-03-24 | 69265.34 | 0 | 0 | 0 | 0 | 1070.17 | 0 | 0 | 68195.17 |
| 2024-03-29 | 68195.17 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 67434.15 |
| 2024-03-30 | 67434.15 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 67007.41 |
| 2024-04-02 | 67007.41 | 0 | 5148 | 0 | 0 | 5148 | 0 | 0 | 61859.41 |
| 2024-04-05 | 61859.41 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 61098.39 |
| 2024-04-06 | 61098.39 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 60671.65 |
| 2024-04-07 | 60671.65 | 0 | 0 | 0 | 0 | 1070.17 | 0 | 0 | 59601.48 |
| 2024-04-08 | 59601.48 | 0 | 0 | 0 | 0 | 1483.81 | 0 | 0 | 58117.67 |
| 2024-04-10 | 58117.67 | 0 | 1821.6 | 0 | 0 | 1821.6 | 0 | 0 | 56296.07 |
| 2024-04-12 | 56296.07 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 55535.05 |
| 2024-04-13 | 55535.05 | 0 | 3487 | 0 | 0 | 4149.14 | 0 | 0 | 51385.91 |
| 2024-04-15 | 51385.91 | 0 | 0 | 0 | 0 | 306.9 | 0 | 0 | 51079.01 |
| 2024-04-19 | 51079.01 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 50317.99 |
| 2024-04-20 | 50317.99 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 49891.25 |
| 2024-04-21 | 49891.25 | 0 | 0 | 0 | 0 | 1070.17 | 0 | 0 | 48821.08 |
| 2024-04-26 | 48821.08 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 48060.06 |
| 2024-04-27 | 48060.06 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 47633.32 |
| 2024-05-03 | 47633.32 | 0 | 5909.02 | 0 | 0 | 5909.02 | 0 | 0 | 41724.3 |
| 2024-05-04 | 41724.3 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 41297.56 |
| 2024-05-05 | 41297.56 | 0 | 0 | 0 | 0 | 1070.17 | 0 | 0 | 40227.39 |
| 2024-05-09 | 40227.39 | 0 | 0 | 0 | 0 | 1483.81 | 0 | 0 | 38743.58 |
| 2024-05-10 | 38743.58 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 37982.56 |
| 2024-05-11 | 37982.56 | 0 | 1821.6 | 0 | 0 | 2248.34 | 0 | 0 | 35734.22 |
| 2024-05-14 | 35734.22 | 0 | 3487 | 0 | 0 | 3722.4 | 0 | 0 | 32011.82 |
| 2024-05-16 | 32011.82 | 0 | 0 | 0 | 0 | 306.9 | 0 | 0 | 31704.92 |
| 2024-05-17 | 31704.92 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 30943.9 |
| 2024-05-18 | 30943.9 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 30517.16 |
| 2024-05-19 | 30517.16 | 0 | 0 | 0 | 0 | 1070.17 | 0 | 0 | 29446.99 |
| 2024-05-24 | 29446.99 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 28685.97 |
| 2024-05-25 | 28685.97 | 0 | 0 | 0 | 0 | 426.74 | 0 | 0 | 28259.23 |
| 2024-05-31 | 28259.23 | 0 | 761.02 | 0 | 0 | 761.02 | 0 | 0 | 27498.21 |

### Inputs Used

- Explicit future events: `2`
- Inferred recurring events: `48`
- Recurring income categories: `none`
- Recurring expense categories: `debt_repayment, delivery_membership, dining, education, groceries, music_subscription, rent, transport, utilities`
- Pending event IDs: `event_102`
- Scheduled event IDs: `event_103`
- Payment option payments in predicted plan: `none`


---

## request_05 / user_05

- Request date: `2025-11-06`
- Requested amount: `ZAR 15488`
- Current balance: `ZAR 46475.1`
- Minimum balance: `ZAR 13100`
- Expected status: `not_affordable`
- Predicted status: `affordable_now`
- Expected method: `not_recommended`
- Predicted method: `full_payment`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; B/K/L: event inclusion, horizon, or date timing difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Do not make this payment by 12 January 2026. None of the available options keeps the ZAR 13,100 minimum protected.
- Predicted explanation: Pay ZAR 15488 today. This protects the ZAR 13100 minimum.
- Expected safe amount: `737.00`; predicted safe amount: `15488.00`; difference: `14751.00`
- Baseline minimum without request: `42274.67` on `2025-11-12`
- Plan minimum with predicted plan: `26786.67` on `2025-11-12`
- Forecast horizon: `2025-11-06` through `2026-02-03`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-11-06 | 46475.1 | 0 | 0 | 0 | 0 | 0 | 0 | 15488 | 30987.1 |
| 2025-11-09 | 30987.1 | 0 | 721.44 | 0 | 0 | 721.44 | 0 | 0 | 30265.66 |
| 2025-11-10 | 30265.66 | 0 | 0 | 0 | 0 | 968 | 0 | 0 | 29297.66 |
| 2025-11-11 | 29297.66 | 0 | 741.58 | 0 | 0 | 1259.12 | 0 | 0 | 28038.54 |
| 2025-11-12 | 28038.54 | 0 | 840.4 | 0 | 0 | 1251.87 | 0 | 0 | 26786.67 |
| 2025-11-14 | 26786.67 | 14740 | 0 | 0 | 0 | 0 | 14740 | 0 | 41526.67 |
| 2025-11-18 | 41526.67 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 40785.09 |
| 2025-11-25 | 40785.09 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 40043.51 |
| 2025-11-26 | 40043.51 | 0 | 0 | 0 | 0 | 411.47 | 0 | 0 | 39632.04 |
| 2025-12-02 | 39632.04 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 38890.46 |
| 2025-12-03 | 38890.46 | 0 | 4972 | 0 | 0 | 4972 | 0 | 0 | 33918.46 |
| 2025-12-05 | 33918.46 | 0 | 0 | 0 | 0 | 706.37 | 0 | 0 | 33212.09 |
| 2025-12-09 | 33212.09 | 0 | 1463.02 | 0 | 0 | 1463.02 | 0 | 0 | 31749.07 |
| 2025-12-10 | 31749.07 | 0 | 0 | 0 | 0 | 1379.47 | 0 | 0 | 30369.6 |
| 2025-12-11 | 30369.6 | 0 | 0 | 0 | 0 | 517.54 | 0 | 0 | 29852.06 |
| 2025-12-12 | 29852.06 | 0 | 840.4 | 0 | 0 | 840.4 | 0 | 0 | 29011.66 |
| 2025-12-14 | 29011.66 | 14740 | 0 | 0 | 0 | 0 | 14740 | 0 | 43751.66 |
| 2025-12-16 | 43751.66 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 43010.08 |
| 2025-12-23 | 43010.08 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 42268.5 |
| 2025-12-24 | 42268.5 | 0 | 0 | 0 | 0 | 411.47 | 0 | 0 | 41857.03 |
| 2025-12-30 | 41857.03 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 41115.45 |
| 2026-01-03 | 41115.45 | 0 | 4972 | 0 | 0 | 4972 | 0 | 0 | 36143.45 |
| 2026-01-04 | 36143.45 | 0 | 0 | 0 | 0 | 706.37 | 0 | 0 | 35437.08 |
| 2026-01-06 | 35437.08 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 34695.5 |
| 2026-01-07 | 34695.5 | 0 | 0 | 0 | 0 | 411.47 | 0 | 0 | 34284.03 |
| 2026-01-08 | 34284.03 | 0 | 721.44 | 0 | 0 | 721.44 | 0 | 0 | 33562.59 |
| 2026-01-09 | 33562.59 | 0 | 0 | 0 | 0 | 968 | 0 | 0 | 32594.59 |
| 2026-01-10 | 32594.59 | 0 | 0 | 0 | 0 | 517.54 | 0 | 0 | 32077.05 |
| 2026-01-11 | 32077.05 | 0 | 840.4 | 0 | 0 | 840.4 | 0 | 0 | 31236.65 |
| 2026-01-13 | 31236.65 | 14740 | 741.58 | 0 | 0 | 741.58 | 14740 | 0 | 45235.07 |
| 2026-01-20 | 45235.07 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 44493.49 |
| 2026-01-21 | 44493.49 | 0 | 0 | 0 | 0 | 411.47 | 0 | 0 | 44082.02 |
| 2026-01-27 | 44082.02 | 0 | 741.58 | 0 | 0 | 741.58 | 0 | 0 | 43340.44 |
| 2026-02-03 | 43340.44 | 0 | 5713.58 | 0 | 0 | 6419.95 | 0 | 0 | 36920.49 |

### Inputs Used

- Explicit future events: `0`
- Inferred recurring events: `43`
- Recurring income categories: `salary`
- Recurring expense categories: `cloud_storage, debt_repayment, family_support, groceries, healthcare, rent, shopping, transport, utilities`
- Pending event IDs: `none`
- Scheduled event IDs: `none`
- Payment option payments in predicted plan: `2025-11-06:15488`


---

## request_06 / user_06

- Request date: `2026-01-03`
- Requested amount: `EUR 620.4`
- Current balance: `EUR 1942.4`
- Minimum balance: `EUR 800`
- Expected status: `affordable_with_plan`
- Predicted status: `affordable_now`
- Expected method: `full_payment`
- Predicted method: `full_payment`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Stop the family streaming plan, then pay EUR 620.40 today. This leaves at least EUR 800 available.
- Predicted explanation: Pay EUR 620.4 today. This protects the EUR 800 minimum.
- Expected safe amount: `603.30`; predicted safe amount: `620.40`; difference: `17.10`
- Baseline minimum without request: `1618.73` on `2026-01-13`
- Plan minimum with predicted plan: `998.33` on `2026-01-13`
- Forecast horizon: `2026-01-03` through `2026-04-02`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-01-03 | 1942.4 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 620.4 | 1294.2 |
| 2026-01-04 | 1294.2 | 0 | 0 | 0 | 0 | 46.84 | 0 | 0 | 1247.36 |
| 2026-01-06 | 1247.36 | 0 | 0 | 0 | 0 | 56.71 | 0 | 0 | 1190.65 |
| 2026-01-07 | 1190.65 | 0 | 26 | 0 | 0 | 26 | 0 | 0 | 1164.65 |
| 2026-01-08 | 1164.65 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 1136.85 |
| 2026-01-09 | 1136.85 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 1117.85 |
| 2026-01-11 | 1117.85 | 0 | 0 | 0 | 0 | 46.84 | 0 | 0 | 1071.01 |
| 2026-01-12 | 1071.01 | 0 | 0 | 0 | 0 | 44.88 | 0 | 0 | 1026.13 |
| 2026-01-13 | 1026.13 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 998.33 |
| 2026-01-14 | 998.33 | 1441 | 0 | 0 | 0 | 35.1 | 1441 | 0 | 2404.23 |
| 2026-01-18 | 2404.23 | 0 | 27.8 | 0 | 0 | 74.64 | 0 | 0 | 2329.59 |
| 2026-01-23 | 2329.59 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2301.79 |
| 2026-01-25 | 2301.79 | 0 | 0 | 0 | 0 | 46.84 | 0 | 0 | 2254.95 |
| 2026-01-28 | 2254.95 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2227.15 |
| 2026-02-01 | 2227.15 | 0 | 254.1 | 0 | 0 | 300.94 | 0 | 0 | 1926.21 |
| 2026-02-02 | 1926.21 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 1898.41 |
| 2026-02-05 | 1898.41 | 0 | 0 | 0 | 0 | 56.71 | 0 | 0 | 1841.7 |
| 2026-02-06 | 1841.7 | 0 | 26 | 0 | 0 | 26 | 0 | 0 | 1815.7 |
| 2026-02-07 | 1815.7 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 1787.9 |
| 2026-02-08 | 1787.9 | 0 | 0 | 0 | 0 | 65.84 | 0 | 0 | 1722.06 |
| 2026-02-11 | 1722.06 | 0 | 0 | 0 | 0 | 44.88 | 0 | 0 | 1677.18 |
| 2026-02-12 | 1677.18 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 1649.38 |
| 2026-02-13 | 1649.38 | 1441 | 0 | 0 | 0 | 35.1 | 1441 | 0 | 3055.28 |
| 2026-02-15 | 3055.28 | 0 | 0 | 0 | 0 | 46.84 | 0 | 0 | 3008.44 |
| 2026-02-17 | 3008.44 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2980.64 |
| 2026-02-22 | 2980.64 | 0 | 27.8 | 0 | 0 | 74.64 | 0 | 0 | 2906 |
| 2026-02-27 | 2906 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2878.2 |
| 2026-03-01 | 2878.2 | 0 | 0 | 0 | 0 | 46.84 | 0 | 0 | 2831.36 |
| 2026-03-03 | 2831.36 | 0 | 254.1 | 0 | 0 | 254.1 | 0 | 0 | 2577.26 |
| 2026-03-04 | 2577.26 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2549.46 |
| 2026-03-07 | 2549.46 | 0 | 0 | 0 | 0 | 56.71 | 0 | 0 | 2492.75 |
| 2026-03-08 | 2492.75 | 0 | 26 | 0 | 0 | 72.84 | 0 | 0 | 2419.91 |
| 2026-03-09 | 2419.91 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2392.11 |
| 2026-03-10 | 2392.11 | 0 | 0 | 0 | 0 | 19 | 0 | 0 | 2373.11 |
| 2026-03-13 | 2373.11 | 0 | 0 | 0 | 0 | 44.88 | 0 | 0 | 2328.23 |
| 2026-03-14 | 2328.23 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 2300.43 |
| 2026-03-15 | 2300.43 | 1441 | 0 | 0 | 0 | 81.94 | 1441 | 0 | 3659.49 |
| 2026-03-19 | 3659.49 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 3631.69 |
| 2026-03-22 | 3631.69 | 0 | 0 | 0 | 0 | 46.84 | 0 | 0 | 3584.85 |
| 2026-03-24 | 3584.85 | 0 | 27.8 | 0 | 0 | 27.8 | 0 | 0 | 3557.05 |
| 2026-03-29 | 3557.05 | 0 | 27.8 | 0 | 0 | 74.64 | 0 | 0 | 3482.41 |
| 2026-04-02 | 3482.41 | 0 | 254.1 | 0 | 0 | 254.1 | 0 | 0 | 3228.31 |

### Inputs Used

- Explicit future events: `0`
- Inferred recurring events: `55`
- Recurring income categories: `salary`
- Recurring expense categories: `cloud_storage, dining, entertainment, insurance, rent, shopping, streaming, transport, utilities`
- Pending event IDs: `none`
- Scheduled event IDs: `none`
- Payment option payments in predicted plan: `2026-01-03:620.4`


---

## request_10 / user_10

- Request date: `2024-12-06`
- Requested amount: `INR 266700`
- Current balance: `INR 750155`
- Minimum balance: `INR 225400`
- Expected status: `not_affordable`
- Predicted status: `affordable_with_plan`
- Expected method: `not_recommended`
- Predicted method: `installments`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; J: payment option or plan eligibility difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Do not make this payment by 10 February 2025. None of the available options keeps the INR 225,400 minimum protected.
- Predicted explanation: Use 1 installments of INR 266700, starting 2024-12-06.
- Expected safe amount: `12700.00`; predicted safe amount: `266700.00`; difference: `254000.00`
- Baseline minimum without request: `726840.81` on `2024-12-08`
- Plan minimum with predicted plan: `460140.81` on `2024-12-08`
- Forecast horizon: `2024-12-06` through `2025-03-05`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-12-06 | 750155 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 266700 | 477678.92 |
| 2024-12-08 | 477678.92 | 0 | 0 | 0 | 0 | 17538.11 | 0 | 0 | 460140.81 |
| 2024-12-11 | 460140.81 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 525629.17 |
| 2024-12-12 | 525629.17 | 0 | 10635.76 | 0 | 0 | 15495.76 | 0 | 0 | 510133.41 |
| 2024-12-13 | 510133.41 | 0 | 5776.08 | 0 | 0 | 8576.08 | 0 | 0 | 501557.33 |
| 2024-12-14 | 501557.33 | 0 | 0 | 0 | 0 | 8813.96 | 0 | 0 | 492743.37 |
| 2024-12-15 | 492743.37 | 0 | 0 | 0 | 0 | 1895 | 0 | 0 | 490848.37 |
| 2024-12-16 | 490848.37 | 0 | 0 | 0 | 0 | 4700.56 | 0 | 0 | 486147.81 |
| 2024-12-18 | 486147.81 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 551636.17 |
| 2024-12-19 | 551636.17 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 541000.41 |
| 2024-12-20 | 541000.41 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 535224.33 |
| 2024-12-25 | 535224.33 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 600712.69 |
| 2024-12-26 | 600712.69 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 590076.93 |
| 2024-12-27 | 590076.93 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 584300.85 |
| 2024-12-28 | 584300.85 | 0 | 0 | 0 | 0 | 8813.96 | 0 | 0 | 575486.89 |
| 2025-01-01 | 575486.89 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 640975.25 |
| 2025-01-02 | 640975.25 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 630339.49 |
| 2025-01-03 | 630339.49 | 0 | 74876.08 | 0 | 0 | 74876.08 | 0 | 0 | 555463.41 |
| 2025-01-08 | 555463.41 | 65488.36 | 0 | 0 | 0 | 17538.11 | 65488.36 | 0 | 603413.66 |
| 2025-01-09 | 603413.66 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 592777.9 |
| 2025-01-10 | 592777.9 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 587001.82 |
| 2025-01-11 | 587001.82 | 0 | 0 | 0 | 0 | 8813.96 | 0 | 0 | 578187.86 |
| 2025-01-12 | 578187.86 | 0 | 0 | 0 | 0 | 4860 | 0 | 0 | 573327.86 |
| 2025-01-13 | 573327.86 | 0 | 0 | 0 | 0 | 2800 | 0 | 0 | 570527.86 |
| 2025-01-15 | 570527.86 | 65488.36 | 0 | 0 | 0 | 1895 | 65488.36 | 0 | 634121.22 |
| 2025-01-16 | 634121.22 | 0 | 10635.76 | 0 | 0 | 15336.32 | 0 | 0 | 618784.9 |
| 2025-01-17 | 618784.9 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 613008.82 |
| 2025-01-22 | 613008.82 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 678497.18 |
| 2025-01-23 | 678497.18 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 667861.42 |
| 2025-01-24 | 667861.42 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 662085.34 |
| 2025-01-25 | 662085.34 | 0 | 0 | 0 | 0 | 8813.96 | 0 | 0 | 653271.38 |
| 2025-01-29 | 653271.38 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 718759.74 |
| 2025-01-30 | 718759.74 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 708123.98 |
| 2025-01-31 | 708123.98 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 702347.9 |
| 2025-02-03 | 702347.9 | 0 | 69100 | 0 | 0 | 69100 | 0 | 0 | 633247.9 |
| 2025-02-05 | 633247.9 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 698736.26 |
| 2025-02-06 | 698736.26 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 688100.5 |
| 2025-02-07 | 688100.5 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 682324.42 |
| 2025-02-08 | 682324.42 | 0 | 0 | 0 | 0 | 26352.07 | 0 | 0 | 655972.35 |
| 2025-02-12 | 655972.35 | 65488.36 | 0 | 0 | 0 | 4860 | 65488.36 | 0 | 716600.71 |
| 2025-02-13 | 716600.71 | 0 | 10635.76 | 0 | 0 | 13435.76 | 0 | 0 | 703164.95 |
| 2025-02-14 | 703164.95 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 697388.87 |
| 2025-02-15 | 697388.87 | 0 | 0 | 0 | 0 | 1895 | 0 | 0 | 695493.87 |
| 2025-02-16 | 695493.87 | 0 | 0 | 0 | 0 | 4700.56 | 0 | 0 | 690793.31 |
| 2025-02-19 | 690793.31 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 756281.67 |
| 2025-02-20 | 756281.67 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 745645.91 |
| 2025-02-21 | 745645.91 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 739869.83 |
| 2025-02-22 | 739869.83 | 0 | 0 | 0 | 0 | 8813.96 | 0 | 0 | 731055.87 |
| 2025-02-26 | 731055.87 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 796544.23 |
| 2025-02-27 | 796544.23 | 0 | 10635.76 | 0 | 0 | 10635.76 | 0 | 0 | 785908.47 |
| 2025-02-28 | 785908.47 | 0 | 5776.08 | 0 | 0 | 5776.08 | 0 | 0 | 780132.39 |
| 2025-03-05 | 780132.39 | 65488.36 | 0 | 0 | 0 | 0 | 65488.36 | 0 | 845620.75 |

### Inputs Used

- Explicit future events: `0`
- Inferred recurring events: `61`
- Recurring income categories: `salary`
- Recurring expense categories: `delivery_membership, dining, entertainment, groceries, gym, music_subscription, rent, transport, utilities`
- Pending event IDs: `none`
- Scheduled event IDs: `none`
- Payment option payments in predicted plan: `2024-12-06:266700`


---

## request_11 / user_11

- Request date: `2025-05-03`
- Requested amount: `IDR 13110000`
- Current balance: `IDR 63531795`
- Minimum balance: `IDR 34140600`
- Expected status: `affordable_with_plan`
- Predicted status: `affordable_now`
- Expected method: `full_payment`
- Predicted method: `full_payment`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Reduce the weekend food delivery to IDR 665,950, then pay IDR 13,110,000 today. This leaves at least IDR 34,140,600 available.
- Predicted explanation: Pay IDR 13110000 today. This protects the IDR 34140600 minimum.
- Expected safe amount: `12510645.00`; predicted safe amount: `13110000.00`; difference: `599355.00`
- Baseline minimum without request: `73804558.33` on `2025-05-11`
- Plan minimum with predicted plan: `60694558.33` on `2025-05-11`
- Forecast horizon: `2025-05-03` through `2025-07-31`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-05-03 | 63531795 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 13110000 | 72055848.23 |
| 2025-05-06 | 72055848.23 | 0 | 2954500 | 0 | 0 | 2954500 | 0 | 0 | 69101348.23 |
| 2025-05-09 | 69101348.23 | 0 | 2796165.18 | 0 | 0 | 2796165.18 | 0 | 0 | 66305183.05 |
| 2025-05-10 | 66305183.05 | 0 | 0 | 0 | 0 | 1881000 | 0 | 0 | 64424183.05 |
| 2025-05-11 | 64424183.05 | 0 | 2544100 | 0 | 0 | 3729624.72 | 0 | 0 | 60694558.33 |
| 2025-05-12 | 60694558.33 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 0 | 82328611.56 |
| 2025-05-13 | 82328611.56 | 0 | 0 | 0 | 0 | 2973572.96 | 0 | 0 | 79355038.6 |
| 2025-05-15 | 79355038.6 | 0 | 0 | 0 | 0 | 168150 | 0 | 0 | 79186888.6 |
| 2025-05-17 | 79186888.6 | 0 | 0 | 0 | 0 | 1649906.5 | 0 | 0 | 77536982.1 |
| 2025-05-21 | 77536982.1 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 0 | 99171035.33 |
| 2025-05-25 | 99171035.33 | 0 | 0 | 0 | 0 | 1185524.72 | 0 | 0 | 97985510.61 |
| 2025-05-30 | 97985510.61 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 0 | 119619563.84 |
| 2025-06-06 | 119619563.84 | 0 | 2954500 | 0 | 0 | 2954500 | 0 | 0 | 116665063.84 |
| 2025-06-08 | 116665063.84 | 21634053.23 | 0 | 0 | 0 | 1185524.72 | 21634053.23 | 0 | 137113592.35 |
| 2025-06-09 | 137113592.35 | 0 | 2796165.18 | 0 | 0 | 2796165.18 | 0 | 0 | 134317427.17 |
| 2025-06-10 | 134317427.17 | 0 | 0 | 0 | 0 | 1881000 | 0 | 0 | 132436427.17 |
| 2025-06-11 | 132436427.17 | 0 | 2544100 | 0 | 0 | 2544100 | 0 | 0 | 129892327.17 |
| 2025-06-13 | 129892327.17 | 0 | 0 | 0 | 0 | 2973572.96 | 0 | 0 | 126918754.21 |
| 2025-06-15 | 126918754.21 | 0 | 0 | 0 | 0 | 168150 | 0 | 0 | 126750604.21 |
| 2025-06-17 | 126750604.21 | 21634053.23 | 0 | 0 | 0 | 1649906.5 | 21634053.23 | 0 | 146734750.94 |
| 2025-06-22 | 146734750.94 | 0 | 0 | 0 | 0 | 1185524.72 | 0 | 0 | 145549226.22 |
| 2025-06-26 | 145549226.22 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 0 | 167183279.45 |
| 2025-07-05 | 167183279.45 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 0 | 188817332.68 |
| 2025-07-06 | 188817332.68 | 0 | 0 | 0 | 0 | 1185524.72 | 0 | 0 | 187631807.96 |
| 2025-07-07 | 187631807.96 | 0 | 2954500 | 0 | 0 | 2954500 | 0 | 0 | 184677307.96 |
| 2025-07-10 | 184677307.96 | 0 | 2796165.18 | 0 | 0 | 2796165.18 | 0 | 0 | 181881142.78 |
| 2025-07-11 | 181881142.78 | 0 | 0 | 0 | 0 | 1881000 | 0 | 0 | 180000142.78 |
| 2025-07-12 | 180000142.78 | 0 | 2544100 | 0 | 0 | 2544100 | 0 | 0 | 177456042.78 |
| 2025-07-14 | 177456042.78 | 21634053.23 | 0 | 0 | 0 | 2973572.96 | 21634053.23 | 0 | 196116523.05 |
| 2025-07-16 | 196116523.05 | 0 | 0 | 0 | 0 | 168150 | 0 | 0 | 195948373.05 |
| 2025-07-18 | 195948373.05 | 0 | 0 | 0 | 0 | 1649906.5 | 0 | 0 | 194298466.55 |
| 2025-07-20 | 194298466.55 | 0 | 0 | 0 | 0 | 1185524.72 | 0 | 0 | 193112941.83 |
| 2025-07-23 | 193112941.83 | 21634053.23 | 0 | 0 | 0 | 0 | 21634053.23 | 0 | 214746995.06 |

### Inputs Used

- Explicit future events: `0`
- Inferred recurring events: `37`
- Recurring income categories: `salary`
- Recurring expense categories: `cloud_storage, education, entertainment, healthcare, housing, insurance, transport, utilities`
- Pending event IDs: `none`
- Scheduled event IDs: `none`
- Payment option payments in predicted plan: `2025-05-03:13110000`


---

## request_13 / user_13

- Request date: `2024-03-07`
- Requested amount: `EUR 941.6`
- Current balance: `EUR 2789.52`
- Minimum balance: `EUR 1300`
- Expected status: `affordable_later`
- Predicted status: `affordable_now`
- Expected method: `wait`
- Predicted method: `full_payment`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; B/K/L: event inclusion, horizon, or date timing difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Pay EUR 941.60 in full on 15 May 2024. Paying earlier would take the balance below the EUR 1,300 minimum.
- Predicted explanation: Pay EUR 941.6 today. This protects the EUR 1300 minimum.
- Expected safe amount: `433.40`; predicted safe amount: `941.60`; difference: `508.20`
- Baseline minimum without request: `2491.43` on `2024-03-14`
- Plan minimum with predicted plan: `1549.83` on `2024-03-14`
- Forecast horizon: `2024-03-07` through `2024-06-04`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2024-03-07 | 2789.52 | 0 | 0 | 0 | 0 | 0 | 0 | 941.6 | 1847.92 |
| 2024-03-12 | 1847.92 | 0 | 100.05 | 0 | 0 | 161.05 | 0 | 0 | 1686.87 |
| 2024-03-13 | 1686.87 | 0 | 45.33 | 0 | 0 | 74.33 | 0 | 0 | 1612.54 |
| 2024-03-14 | 1612.54 | 0 | 0 | 0 | 0 | 62.71 | 0 | 0 | 1549.83 |
| 2024-03-15 | 1549.83 | 1343.54 | 0 | 0 | 0 | 21 | 0 | 0 | 2872.37 |
| 2024-03-16 | 2872.37 | 0 | 0 | 0 | 0 | 31.8 | 0 | 0 | 2840.57 |
| 2024-03-19 | 2840.57 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 2740.52 |
| 2024-03-20 | 2740.52 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 2695.19 |
| 2024-03-26 | 2695.19 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 2595.14 |
| 2024-03-27 | 2595.14 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 2549.81 |
| 2024-03-28 | 2549.81 | 0 | 0 | 0 | 0 | 62.71 | 0 | 0 | 2487.1 |
| 2024-03-31 | 2487.1 | 1343.54 | 0 | 0 | 0 | 0 | 1343.54 | 0 | 3830.64 |
| 2024-04-02 | 3830.64 | 0 | 722.65 | 0 | 0 | 722.65 | 0 | 0 | 3107.99 |
| 2024-04-03 | 3107.99 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 3062.66 |
| 2024-04-06 | 3062.66 | 0 | 0 | 0 | 0 | 143.55 | 0 | 0 | 2919.11 |
| 2024-04-09 | 2919.11 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 2819.06 |
| 2024-04-10 | 2819.06 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 2773.73 |
| 2024-04-11 | 2773.73 | 0 | 0 | 0 | 0 | 62.71 | 0 | 0 | 2711.02 |
| 2024-04-12 | 2711.02 | 0 | 0 | 0 | 0 | 61 | 0 | 0 | 2650.02 |
| 2024-04-13 | 2650.02 | 0 | 0 | 0 | 0 | 29 | 0 | 0 | 2621.02 |
| 2024-04-15 | 2621.02 | 1343.54 | 0 | 0 | 0 | 21 | 1343.54 | 0 | 3943.56 |
| 2024-04-16 | 3943.56 | 0 | 100.05 | 0 | 0 | 131.85 | 0 | 0 | 3811.71 |
| 2024-04-17 | 3811.71 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 3766.38 |
| 2024-04-23 | 3766.38 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 3666.33 |
| 2024-04-24 | 3666.33 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 3621 |
| 2024-04-25 | 3621 | 0 | 0 | 0 | 0 | 62.71 | 0 | 0 | 3558.29 |
| 2024-04-30 | 3558.29 | 1343.54 | 100.05 | 0 | 0 | 100.05 | 1343.54 | 0 | 4801.78 |
| 2024-05-01 | 4801.78 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 4756.45 |
| 2024-05-03 | 4756.45 | 0 | 622.6 | 0 | 0 | 622.6 | 0 | 0 | 4133.85 |
| 2024-05-07 | 4133.85 | 0 | 100.05 | 0 | 0 | 243.6 | 0 | 0 | 3890.25 |
| 2024-05-08 | 3890.25 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 3844.92 |
| 2024-05-09 | 3844.92 | 0 | 0 | 0 | 0 | 62.71 | 0 | 0 | 3782.21 |
| 2024-05-13 | 3782.21 | 0 | 0 | 0 | 0 | 61 | 0 | 0 | 3721.21 |
| 2024-05-14 | 3721.21 | 0 | 100.05 | 0 | 0 | 129.05 | 0 | 0 | 3592.16 |
| 2024-05-15 | 3592.16 | 1343.54 | 45.33 | 0 | 0 | 45.33 | 1343.54 | 0 | 4890.37 |
| 2024-05-16 | 4890.37 | 0 | 0 | 0 | 0 | 21 | 0 | 0 | 4869.37 |
| 2024-05-17 | 4869.37 | 0 | 0 | 0 | 0 | 31.8 | 0 | 0 | 4837.57 |
| 2024-05-21 | 4837.57 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 4737.52 |
| 2024-05-22 | 4737.52 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 4692.19 |
| 2024-05-23 | 4692.19 | 0 | 0 | 0 | 0 | 62.71 | 0 | 0 | 4629.48 |
| 2024-05-28 | 4629.48 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 4529.43 |
| 2024-05-29 | 4529.43 | 0 | 45.33 | 0 | 0 | 45.33 | 0 | 0 | 4484.1 |
| 2024-05-30 | 4484.1 | 1343.54 | 0 | 0 | 0 | 0 | 1343.54 | 0 | 5827.64 |
| 2024-06-03 | 5827.64 | 0 | 622.6 | 0 | 0 | 622.6 | 0 | 0 | 5205.04 |
| 2024-06-04 | 5205.04 | 0 | 100.05 | 0 | 0 | 100.05 | 0 | 0 | 5104.99 |

### Inputs Used

- Explicit future events: `1`
- Inferred recurring events: `53`
- Recurring income categories: `salary`
- Recurring expense categories: `delivery_membership, dining, entertainment, groceries, gym, music_subscription, rent, transport, utilities`
- Pending event IDs: `none`
- Scheduled event IDs: `event_1161`
- Payment option payments in predicted plan: `2024-03-07:941.6`


---

## request_21 / user_21

- Request date: `2026-04-03`
- Requested amount: `USD 1574.4`
- Current balance: `USD 3911.35`
- Minimum balance: `USD 1800`
- Expected status: `affordable_with_plan`
- Predicted status: `affordable_now`
- Expected method: `full_payment`
- Predicted method: `full_payment`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Stop the online backup subscription and reduce the streaming subscription to USD 23.50, then pay USD 1,574.40 today. This leaves at least USD 1,800 available.
- Predicted explanation: Pay USD 1574.4 today. This protects the USD 1800 minimum.
- Expected safe amount: `1543.35`; predicted safe amount: `1574.40`; difference: `31.05`
- Baseline minimum without request: `3557.43` on `2026-04-11`
- Plan minimum with predicted plan: `1983.03` on `2026-04-11`
- Forecast horizon: `2026-04-03` through `2026-07-01`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-04-03 | 3911.35 | 0 | 0 | 0 | 0 | 0 | 0 | 1574.4 | 2336.95 |
| 2026-04-05 | 2336.95 | 0 | 122.18 | 0 | 53 | 122.18 | 0 | 0 | 2161.77 |
| 2026-04-08 | 2161.77 | 0 | 0 | 0 | 0 | 47 | 0 | 0 | 2114.77 |
| 2026-04-11 | 2114.77 | 0 | 0 | 0 | 0 | 131.74 | 0 | 0 | 1983.03 |
| 2026-04-15 | 1983.03 | 2256 | 0 | 0 | 0 | 0 | 0 | 0 | 4239.03 |
| 2026-05-03 | 4239.03 | 0 | 718.8 | 0 | 0 | 718.8 | 0 | 0 | 3520.23 |
| 2026-05-05 | 3520.23 | 0 | 122.18 | 0 | 0 | 122.18 | 0 | 0 | 3398.05 |
| 2026-05-08 | 3398.05 | 0 | 0 | 0 | 0 | 47 | 0 | 0 | 3351.05 |
| 2026-05-11 | 3351.05 | 0 | 0 | 0 | 0 | 131.74 | 0 | 0 | 3219.31 |
| 2026-05-14 | 3219.31 | 2256 | 0 | 0 | 0 | 0 | 2256 | 0 | 5475.31 |
| 2026-06-03 | 5475.31 | 0 | 718.8 | 0 | 0 | 718.8 | 0 | 0 | 4756.51 |
| 2026-06-04 | 4756.51 | 0 | 122.18 | 0 | 0 | 122.18 | 0 | 0 | 4634.33 |
| 2026-06-07 | 4634.33 | 0 | 0 | 0 | 0 | 47 | 0 | 0 | 4587.33 |
| 2026-06-10 | 4587.33 | 0 | 0 | 0 | 0 | 131.74 | 0 | 0 | 4455.59 |
| 2026-06-13 | 4455.59 | 2256 | 0 | 0 | 0 | 0 | 2256 | 0 | 6711.59 |

### Inputs Used

- Explicit future events: `2`
- Inferred recurring events: `16`
- Recurring income categories: `salary`
- Recurring expense categories: `cloud_storage, rent, shopping, streaming, utilities`
- Pending event IDs: `event_1857`
- Scheduled event IDs: `event_1858`
- Payment option payments in predicted plan: `2026-04-03:1574.4`


---

## request_23 / user_23

- Request date: `2025-05-07`
- Requested amount: `ZAR 38016`
- Current balance: `ZAR 51957.9`
- Minimum balance: `ZAR 27000`
- Expected status: `affordable_later`
- Predicted status: `not_affordable`
- Expected method: `wait`
- Predicted method: `not_recommended`
- Root-cause classification: **E/F: recurring amount or timing / forecast cash-flow difference; B/K/L: event inclusion, horizon, or date timing difference; F/L: earliest-safe date timing difference**

### Expected and Predicted Reasoning

- Expected explanation: Pay ZAR 38,016 in full on 15 July 2025. Paying earlier would take the balance below the ZAR 27,000 minimum.
- Predicted explanation: Do not proceed with the ZAR 38016 request. None of the available options keeps the ZAR 27000 minimum protected.
- Expected safe amount: `9152.00`; predicted safe amount: `7510.76`; difference: `-1641.24`
- Baseline minimum without request: `34510.76` on `2025-05-15`
- Plan minimum with predicted plan: `34510.76` on `2025-05-15`
- Forecast horizon: `2025-05-07` through `2025-08-04`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.

### Chronological Forecast

| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-05-07 | 51957.9 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 50251.05 |
| 2025-05-09 | 50251.05 | 0 | 0 | 0 | 0 | 2813.94 | 0 | 0 | 47437.11 |
| 2025-05-11 | 47437.11 | 0 | 1553.2 | 0 | 1553.2 | 0 | 0 | 0 | 45883.91 |
| 2025-05-13 | 45883.91 | 0 | 1341.05 | 0 | 0 | 1341.05 | 0 | 0 | 44542.86 |
| 2025-05-14 | 44542.86 | 0 | 1706.85 | 0 | 0 | 7558.85 | 0 | 0 | 36984.01 |
| 2025-05-15 | 36984.01 | 0 | 0 | 0 | 0 | 2473.25 | 0 | 0 | 34510.76 |
| 2025-05-16 | 34510.76 | 45760 | 4270.2 | 0 | 0 | 4270.2 | 45760 | 0 | 76000.56 |
| 2025-05-21 | 76000.56 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 74293.71 |
| 2025-05-28 | 74293.71 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 72586.86 |
| 2025-05-29 | 72586.86 | 0 | 0 | 0 | 0 | 896.02 | 0 | 0 | 71690.84 |
| 2025-06-04 | 71690.84 | 0 | 17018.85 | 0 | 0 | 17018.85 | 0 | 0 | 54671.99 |
| 2025-06-09 | 54671.99 | 0 | 0 | 0 | 0 | 2813.94 | 0 | 0 | 51858.05 |
| 2025-06-11 | 51858.05 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 50151.2 |
| 2025-06-12 | 50151.2 | 0 | 0 | 0 | 0 | 896.02 | 0 | 0 | 49255.18 |
| 2025-06-13 | 49255.18 | 0 | 1341.05 | 0 | 0 | 1341.05 | 0 | 0 | 47914.13 |
| 2025-06-14 | 47914.13 | 0 | 0 | 0 | 0 | 5852 | 0 | 0 | 42062.13 |
| 2025-06-15 | 42062.13 | 0 | 0 | 0 | 0 | 1577.23 | 0 | 0 | 40484.9 |
| 2025-06-16 | 40484.9 | 45760 | 4270.2 | 0 | 0 | 4270.2 | 45760 | 0 | 81974.7 |
| 2025-06-18 | 81974.7 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 80267.85 |
| 2025-06-25 | 80267.85 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 78561 |
| 2025-06-26 | 78561 | 0 | 0 | 0 | 0 | 896.02 | 0 | 0 | 77664.98 |
| 2025-07-02 | 77664.98 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 75958.13 |
| 2025-07-05 | 75958.13 | 0 | 15312 | 0 | 0 | 15312 | 0 | 0 | 60646.13 |
| 2025-07-09 | 60646.13 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 58939.28 |
| 2025-07-10 | 58939.28 | 0 | 0 | 0 | 0 | 3709.96 | 0 | 0 | 55229.32 |
| 2025-07-14 | 55229.32 | 0 | 1341.05 | 0 | 0 | 1341.05 | 0 | 0 | 53888.27 |
| 2025-07-15 | 53888.27 | 0 | 0 | 0 | 0 | 5852 | 0 | 0 | 48036.27 |
| 2025-07-16 | 48036.27 | 0 | 1706.85 | 0 | 0 | 3284.08 | 0 | 0 | 44752.19 |
| 2025-07-17 | 44752.19 | 45760 | 4270.2 | 0 | 0 | 4270.2 | 45760 | 0 | 86241.99 |
| 2025-07-23 | 86241.99 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 84535.14 |
| 2025-07-24 | 84535.14 | 0 | 0 | 0 | 0 | 896.02 | 0 | 0 | 83639.12 |
| 2025-07-30 | 83639.12 | 0 | 1706.85 | 0 | 0 | 1706.85 | 0 | 0 | 81932.27 |

### Inputs Used

- Explicit future events: `1`
- Inferred recurring events: `42`
- Recurring income categories: `salary`
- Recurring expense categories: `cloud_storage, debt_repayment, family_support, groceries, healthcare, rent, shopping, transport, utilities`
- Pending event IDs: `event_2042`
- Scheduled event IDs: `none`
- Payment option payments in predicted plan: `none`


---
