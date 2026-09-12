# Financial Rule Audit

This audit compares the current implementation with `problem_statement.md`. It is based on the current code path in `decision_engine.py`; no sample-specific rules are used.

| Rule | Specification | Current implementation | Assessment |
|---|---|---|---|
| Balance snapshot | Start from `current_available_balance`; do not replay settled history | Forecast starts at the profile balance and applies only future flows | Consistent |
| Request date | Include the request date in the 90-day safety window | Forecast iterates from `start` through `start + 89 days` and applies same-day payments before safety is checked | Consistent |
| Settled history | Use settled history before the request date to infer recurring flows | Historical rows require `settled` and date before request date | Consistent; recurrence remains an approximation |
| Future settled rows | Do not use later historical knowledge as known future events | Future settled rows are excluded from explicit future flows | Consistent and prevents leakage |
| Pending debits | Reserve pending obligations | Future pending debits are included | Consistent |
| Pending credits | Do not count until settled | Pending credits are excluded | Consistent |
| Scheduled events | Include confirmed scheduled future cash flows | Scheduled debits and credits are included | Consistent |
| Cancelled/failed | Ignore invalid events | Both statuses are excluded | Consistent |
| Unrealized values | Do not treat as cash | Unrealized rows are excluded | Consistent |
| Refunds | Count only when cash is settled; do not count pending refunds | Settled refunds are credits; pending refunds are excluded | Consistent |
| Investment sales | Settled sale proceeds may be cash | Settled credits are included | Consistent |
| Linked lifecycle rows | Interpret refunds, failed retries, and valuations by status/type | Status and direction rules distinguish these cases; no blanket deduplication is applied | Conservative; legitimate refunds/sales are preserved |
| Missing amounts | Infer only from reliable evidence, otherwise exclude | Optional linked-image OCR is attempted; unresolved values are excluded | Consistent; OCR is optional |
| Currency | Convert using dated supplied rates | Nearest supplied direct rate or inverse rate is used | Consistent, with nearest-date approximation when exact date is absent |
| Forecast horizon | Check the next 90 days | Exactly 90 inclusive start-date observations are generated | Consistent |
| Full payment | Entire payment plan must stay above minimum | Candidate plan is inserted into the daily forecast | Consistent |
| Installments | Use supplied option schedule exactly and finish by deadline | Supplied dates, amount, count, interval, preferences, and max duration are checked | Consistent |
| Partial payment | Only when allowed, positive today, and completion date is safe | Uses safe-today amount and independently searched safe full-payment date | Consistent |
| Earliest full payment | Search candidate days and validate the complete forecast | Searches chronologically and validates the full 90-day forecast for each candidate | Consistent; remaining error is forecast estimation, not a second balance shortcut |
| Flexible spending | Only permitted future recurring flexible expenses may change | Candidate events must be historical, permitted, non-protected, and non-fixed; forecast changes apply to inferred recurring category flows | Mostly consistent; event-level recurrence identity can be improved |
| Messages | Use relevant confirmed amendments/income, ignore uncertain inflows | Messages are currently diagnostic-only | Gap: deterministic message extraction is not yet integrated |

## Findings

The largest remaining correctness risk is recurrence reconstruction: historical rows are grouped by category and direction, and an inferred schedule uses a representative row from the group. The engine does not blanket-deduplicate linked rows because the dataset contains legitimate settled refunds and investment-sale proceeds. The other material gap is message-derived amendments such as changed payroll dates or confirmed salary changes.

## Balance Snapshot Investigation

`financial_profiles.csv` contains no balance-date column and the specification describes `current_available_balance` as the user's available balance for the request. Therefore the engine treats it as the request-date starting snapshot. Replaying settled history would double-subtract historical debits and double-count historical credits. The analysis found no evidence that a second balance reconstruction is supported by the input schema. Pending debits remain future obligations; pending credits do not alter the starting snapshot.

The alternative interpretation, "profile balance is before the latest historical event," cannot be tested consistently because no snapshot timestamp identifies such an event. It would also violate the instruction not to reconstruct the current balance by replaying history, so it was rejected.

The current public sample still provides evidence that broad recurrence changes should not be accepted solely to improve a few rows. Minimum two observations and event-type-plus-category grouping were both tested and preserved the 17/25 status and 19/25 method scores, but neither improved them. The safer default remains three observations and category/direction grouping.

Recurrence diagnostics show mixed cadence types: groceries and transport commonly use fixed weekly intervals, while salary, rent, subscriptions, and debt payments commonly use month-like intervals with day-of-month patterns. The current engine uses a fixed median-day interval for all categories. A category-aware calendar-month model is plausible for some groups, but it was not retained without a controlled score improvement; changing it broadly would risk shifting otherwise correct schedules.
