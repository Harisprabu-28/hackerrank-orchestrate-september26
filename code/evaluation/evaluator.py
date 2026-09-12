"""Evaluate the deterministic engine on the solved public sample requests."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path
import sys
from datetime import date
import os

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_loader import DataStore
from decision_engine import AffordabilityEngine, ddate, median


FIELDS = [
    "affordability_status", "recommended_payment_method", "payment_plan",
    "earliest_date_for_full_payment", "spending_changes_needed",
]

REPORT_FIELDS = [
    "request_id", "user_id", "request_date", "requested_amount",
    "expected_affordability_status", "predicted_affordability_status",
    "expected_recommended_payment_method", "predicted_recommended_payment_method",
    "expected_amount_safe_to_pay", "predicted_amount_safe_to_pay",
    "expected_payment_plan", "predicted_payment_plan",
    "expected_earliest_date_for_full_payment", "predicted_earliest_date_for_full_payment",
    "expected_spending_changes_needed", "predicted_spending_changes_needed",
    "current_available_balance", "minimum_balance_to_keep", "forecast_minimum_balance",
    "forecast_minimum_balance_date", "recurring_income_included",
    "recurring_expenses_included", "scheduled_income_included", "scheduled_expenses_included",
    "pending_events_included", "linked_events_involved", "missing_amount_events_involved",
    "message_derived_events_included",
]

SUMMARY_FIELDS = [
    "request_id", "user_id", "expected_affordability_status", "predicted_affordability_status",
    "expected_recommended_payment_method", "predicted_recommended_payment_method",
    "expected_amount_safe_to_pay", "predicted_amount_safe_to_pay",
    "expected_earliest_date_for_full_payment", "predicted_earliest_date_for_full_payment",
]


def _join(values: list[str]) -> str:
    return "|".join(sorted(set(value for value in values if value))) or "none"


def diagnostic_row(store: DataStore, engine: AffordabilityEngine, request: dict[str, str], prediction: dict[str, str], expected: dict[str, str]) -> dict[str, str]:
    profile = store.profile(request["user_id"])
    start = date.fromisoformat(request["request_date"])
    explicit, recurring = engine._events(request["user_id"], profile.get("home_currency", ""), start, 90)
    forecast = engine._forecast(request)
    minimum_date = min(forecast["balances"], key=forecast["balances"].get)
    future = explicit
    return {
        "request_id": request["request_id"], "user_id": request["user_id"],
        "request_date": request["request_date"], "requested_amount": request["requested_amount"],
        "expected_affordability_status": expected["affordability_status"], "predicted_affordability_status": prediction["affordability_status"],
        "expected_recommended_payment_method": expected["recommended_payment_method"], "predicted_recommended_payment_method": prediction["recommended_payment_method"],
        "expected_amount_safe_to_pay": expected["amount_safe_to_pay"], "predicted_amount_safe_to_pay": prediction["amount_safe_to_pay"],
        "expected_payment_plan": expected["payment_plan"], "predicted_payment_plan": prediction["payment_plan"],
        "expected_earliest_date_for_full_payment": expected["earliest_date_for_full_payment"], "predicted_earliest_date_for_full_payment": prediction["earliest_date_for_full_payment"],
        "expected_spending_changes_needed": expected["spending_changes_needed"], "predicted_spending_changes_needed": prediction["spending_changes_needed"],
        "current_available_balance": profile.get("current_available_balance", ""), "minimum_balance_to_keep": profile.get("minimum_balance_to_keep", ""),
        "forecast_minimum_balance": str(forecast["minimum"]), "forecast_minimum_balance_date": minimum_date.isoformat(),
        "recurring_income_included": _join([item["category"] for item in recurring if item["direction"] == "credit"]),
        "recurring_expenses_included": _join([item["category"] for item in recurring if item["direction"] == "debit"]),
        "scheduled_income_included": _join([item["row"].get("event_id", "") for item in future if item["direction"] == "credit" and item["row"].get("status") == "scheduled"]),
        "scheduled_expenses_included": _join([item["row"].get("event_id", "") for item in future if item["direction"] == "debit" and item["row"].get("status") == "scheduled"]),
        "pending_events_included": _join([item["row"].get("event_id", "") for item in future if item["row"].get("status") == "pending"]),
        "linked_events_involved": _join([item["row"].get("linked_event_id", "") for item in future if item["row"].get("linked_event_id", "")]),
        "missing_amount_events_involved": _join([row.get("event_id", "") for row in store.user_events(request["user_id"]) if not row.get("amount", "").strip()]),
        "message_derived_events_included": "none",
    }


def write_recurrence_diagnostics(store: DataStore, engine: AffordabilityEngine, requests: list[dict[str, str]], root: Path) -> None:
    rows = []
    seen = set()
    for request in requests:
        start = date.fromisoformat(request["request_date"])
        profile = store.profile(request["user_id"])
        home = profile.get("home_currency", "")
        historical = [
            row for row in store.user_events(request["user_id"])
            if (row.get("status", "").lower() == "settled")
            and (ddate(row.get("settlement_date")) or ddate(row.get("event_date")))
            and (ddate(row.get("settlement_date")) or ddate(row.get("event_date"))) < start
            and row.get("direction") in {"debit", "credit"}
        ]
        groups = {}
        for row in historical:
            when = ddate(row.get("settlement_date")) or ddate(row.get("event_date"))
            amount = engine._amount(row, home, when or start)
            if amount is not None:
                groups.setdefault((row.get("category", "").lower(), row.get("direction", "")), []).append((when, amount, row))
        for (category, direction), values in groups.items():
            values.sort(key=lambda item: item[0])
            if len(values) < 2:
                continue
            intervals = [(right[0] - left[0]).days for left, right in zip(values, values[1:])]
            key = (request["request_id"], category, direction)
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "request_id": request["request_id"], "user_id": request["user_id"],
                "category": category, "direction": direction, "event_type_values": "|".join(sorted(set(v[2].get("event_type", "") for v in values))),
                "observation_count": len(values), "historical_dates": "|".join(v[0].isoformat() for v in values),
                "intervals_days": "|".join(str(value) for value in intervals),
                "median_interval_days": str(median(intervals)),
                "amounts": "|".join(str(v[1]) for v in values),
                "median_amount": str(median([v[1] for v in values]).quantize(Decimal("0.01"))),
                "inferred_by_current_engine": any(item["category"] == category and item["direction"] == direction for item in engine._events(request["user_id"], home, start, 90)[1]),
            })
    path = root / "code" / "evaluation" / "recurrence_diagnostics.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        fields = list(rows[0]) if rows else ["request_id", "user_id", "category", "direction"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run() -> int:
    root = Path(__file__).resolve().parents[2]
    store = DataStore(root / "dataset")
    engine = AffordabilityEngine(
        store,
        min_recurrence_observations=int(os.environ.get("RECURRENCE_MIN_OBSERVATIONS", "3")),
        group_recurrence_by_event_type=os.environ.get("RECURRENCE_GROUP_EVENT_TYPE", "0") == "1",
    )
    with (root / "dataset" / "sample_requests.csv").open(newline="", encoding="utf-8-sig") as handle:
        samples = list(csv.DictReader(handle))
    predictions = {row["request_id"]: engine.decide(row) for row in samples}
    report = ["Public sample evaluation", "========================", f"samples: {len(samples)}"]
    for field in FIELDS:
        matches = sum(predictions[row["request_id"]][field] == row[field] for row in samples)
        report.append(f"{field}: {matches}/{len(samples)} exact")
    amount_matches = sum(
        abs(Decimal(predictions[row["request_id"]]["amount_safe_to_pay"]) - Decimal(row["amount_safe_to_pay"])) <= Decimal("0.01")
        for row in samples
    )
    report.append(f"amount_safe_to_pay: {amount_matches}/{len(samples)} within 0.01")
    mismatches = []
    detailed = []
    for row in samples:
        prediction = predictions[row["request_id"]]
        amount_mismatch = abs(Decimal(prediction["amount_safe_to_pay"]) - Decimal(row["amount_safe_to_pay"])) > Decimal("0.01")
        if amount_mismatch or any(prediction[field] != row[field] for field in FIELDS):
            mismatches.append(f"{row['request_id']}: predicted {prediction['affordability_status']}/{prediction['recommended_payment_method']} vs {row['affordability_status']}/{row['recommended_payment_method']}")
            detailed.append(diagnostic_row(store, engine, row, prediction, row))
    report.extend(mismatches[:10])
    output = "\n".join(report) + "\n"
    print(output, end="")
    (root / "evaluation_report.txt").write_text(output, encoding="utf-8")
    with (root / "code" / "evaluation" / "mismatch_report.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(detailed)
    summary = [output.rstrip(), "", f"Detailed mismatches: {len(detailed)}", "", "Diagnostic records:"]
    categories = {
        "affordability_status_mismatch": lambda item: item["expected_affordability_status"] != item["predicted_affordability_status"],
        "payment_method_mismatch": lambda item: item["expected_recommended_payment_method"] != item["predicted_recommended_payment_method"],
        "amount_mismatch": lambda item: abs(Decimal(item["expected_amount_safe_to_pay"]) - Decimal(item["predicted_amount_safe_to_pay"])) > Decimal("0.01"),
        "payment_plan_mismatch": lambda item: item["expected_payment_plan"] != item["predicted_payment_plan"],
        "earliest_date_mismatch": lambda item: item["expected_earliest_date_for_full_payment"] != item["predicted_earliest_date_for_full_payment"],
        "spending_change_mismatch": lambda item: item["expected_spending_changes_needed"] != item["predicted_spending_changes_needed"],
        "pending_event_context": lambda item: item["pending_events_included"] != "none",
        "linked_event_context": lambda item: item["linked_events_involved"] != "none",
        "missing_amount_context": lambda item: item["missing_amount_events_involved"] != "none",
    }
    summary.extend(["", "Mismatch category counts:"])
    summary.extend(f"{name}: {sum(test(item) for item in detailed)}" for name, test in categories.items())
    for item in detailed:
        summary.append(", ".join(f"{key}={item[key]}" for key in REPORT_FIELDS))
    (root / "code" / "evaluation" / "mismatch_report.txt").write_text("\n".join(summary) + "\n", encoding="utf-8")
    unique_summary = []
    seen_ids = set()
    for item in detailed:
        if item["request_id"] in seen_ids:
            continue
        seen_ids.add(item["request_id"])
        unique_summary.append({field: item[field] for field in SUMMARY_FIELDS})
    summary_path = root / "code" / "evaluation" / "remaining_mismatches_summary.md"
    markdown = ["# Remaining Mismatches", "", f"Unique requests with at least one mismatch: {len(unique_summary)}", "", "| " + " | ".join(SUMMARY_FIELDS) + " |", "|" + "|".join("---" for _ in SUMMARY_FIELDS) + "|"]
    markdown.extend("| " + " | ".join(row[field] for field in SUMMARY_FIELDS) + " |" for row in unique_summary)
    summary_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    status_traces = ["", "Status mismatch traces:"]
    for item in detailed:
        if item["expected_affordability_status"] != item["predicted_affordability_status"]:
            status_traces.append(
                f"{item['request_id']}: date={item['request_date']}; amount={item['requested_amount']}; "
                f"balance={item['current_available_balance']}; minimum={item['minimum_balance_to_keep']}; "
                f"forecast_minimum={item['forecast_minimum_balance']} on {item['forecast_minimum_balance_date']}; "
                f"recurring_income={item['recurring_income_included']}; recurring_expenses={item['recurring_expenses_included']}; "
                f"scheduled_income={item['scheduled_income_included']}; scheduled_expenses={item['scheduled_expenses_included']}; "
                f"pending={item['pending_events_included']}; expected={item['expected_affordability_status']}; predicted={item['predicted_affordability_status']}"
            )
    with (root / "code" / "evaluation" / "mismatch_report.txt").open("a", encoding="utf-8") as handle:
        handle.write("\n".join(status_traces) + "\n")
    write_recurrence_diagnostics(store, engine, samples, root)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
