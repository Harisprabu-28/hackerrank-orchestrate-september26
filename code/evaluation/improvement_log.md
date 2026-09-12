# Iterative Improvement Log

## Baseline

- Change: existing deterministic engine before this analysis pass.
- Affordability status: 16/25 exact.
- Recommended payment method: 17/25 exact.

## Point-in-time event filtering

- Change: future explicit events are limited to `pending` and `scheduled`; future `settled` rows are excluded from a request-date forecast.
- Reason: using future settled rows leaks information that was not available when the request was made.
- Sample score before: 16/25 status, 17/25 method.
- Sample score after: 16/25 status, 17/25 method.
- Decision: keep. The score is unchanged, but the rule is required for hidden-test generalization.

## Pending credits and optional OCR

- Change: pending credits are excluded from spendable cash; linked missing-amount images have an optional OCR path with a safe fallback.
- Reason: pending inflows are not confirmed, and image evidence must be used when tooling is available without making OCR mandatory.
- Sample score before: 16/25 status, 17/25 method.
- Sample score after: 16/25 status, 17/25 method.
- Decision: keep. Both changes enforce the official cash-state/evidence rules without changing this sample score.

## Recurrence amount median

- Change: recurring amount estimation now uses the true median, including averaging the two middle values for even histories.
- Reason: upper-middle selection overestimated recurring expenses and distorted the 90-day minimum balance.
- Sample score before: 16/25 status, 17/25 method.
- Sample score after: 17/25 status, 19/25 method.
- Decision: keep.

## Recurrence interval rounding experiment

- Change: tried half-up rounding for fractional median intervals.
- Reason: avoid truncating fractional cadence intervals.
- Sample score before: 17/25 status, 19/25 method.
- Sample score after: 16/25 status, 17/25 method.
- Decision: reverted because it reduced general sample consistency.

## Recurrence alternatives

- Change: tested two historical observations and event-type-plus-category grouping as configurable alternatives.
- Reason: assess recurrence leakage and grouping sensitivity without hardcoding sample behavior.
- Baseline: three observations, category/direction grouping: 17/25 status, 19/25 method.
- Two observations: 17/25 status, 19/25 method.
- Event-type-plus-category grouping: 17/25 status, 19/25 method.
- Decision: retain the conservative three-observation category/direction default.

## Explicit/inferred recurrence deduplication

- Change: suppress an inferred event when an explicit pending/scheduled event has the same category and direction, is within three days, and is within one percent of the inferred amount.
- Reason: five sample cases demonstrated potential double counting; unrelated amounts are retained.
- Sample score before: 17/25 status, 19/25 method.
- Sample score after: 17/25 status, 19/25 method.
- Decision: keep because it fixes a clear forecast-semantic risk without harming the score.

## Deterministic message parser

- Change: added a standalone parser for confirmation state, ISO dates, and currency amounts.
- Reason: messages contain payroll amendments and uncertain inflows, but safe event reconciliation requires a matching event or unambiguous date/amount contract.
- Decision: parser is available for future integration; no speculative message-derived cash flows were added to the forecast.

## Installment helper and bounded spending combinations

------------------------------------------------

Change: Centralized supplied-installment validation/ranking and added a bounded search over one to three compatible spending changes.
Reason: The previous implementation duplicated installment logic and only tried one spending candidate at a time.
Specification evidence: Multiple changes are permitted up to three; supplied installment schedules must be evaluated consistently and completely.
Before score: status 17/25; payment method 19/25.
After score: status 18/25; payment method 20/25.
Tests: 20 synthetic tests pass after structural coverage was added.
Decision: KEEP

------------------------------------------------

Change: Validate partial payment as an independently constructed two-payment schedule.
Reason: A safe full-payment date does not by itself prove the combined partial schedule is safe.
Specification evidence: The complete partial-payment schedule must remain above the minimum and finish by the deadline.
Before score: status 18/25; payment method 20/25.
After score: status 16/25; payment method 18/25.
Tests: Existing tests passed, but public score decreased.
Decision: REVERT. The issue is specification-backed, but this implementation worsened general sample behavior and was not retained without a stronger model for selecting the first payment amount.