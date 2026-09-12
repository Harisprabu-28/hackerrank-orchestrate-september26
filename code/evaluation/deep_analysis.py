"""Generate a detailed, decision-engine-neutral trace for status mismatches."""

from __future__ import annotations

import csv
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_loader import DataStore
from decision_engine import AffordabilityEngine, dec, ddate, money


ROOT = Path(__file__).resolve().parents[2]
STATUS_FIELDS = ("affordability_status", "recommended_payment_method")


def parse_plan(plan: str) -> list[tuple[date, Decimal]]:
    if not plan or plan == "none":
        return []
    result = []
    for part in plan.split("|"):
        when, amount = part.split(":", 1)
        result.append((date.fromisoformat(when), dec(amount)))
    return result


def fmt(value: Decimal) -> str:
    return money(value)


def build_trace(store: DataStore, engine: AffordabilityEngine, request: dict[str, str], expected: dict[str, str], predicted: dict[str, str]) -> str:
    profile = store.profile(request["user_id"])
    start = date.fromisoformat(request["request_date"])
    home = profile.get("home_currency", "")
    explicit, recurring = engine._events(request["user_id"], home, start, 90)
    payments = parse_plan(predicted["payment_plan"])
    forecast = engine._forecast(request, payments)
    flow_dates = {start} | set(forecast["balances"])
    relevant = explicit + recurring
    flow_dates |= {item["date"] for item in relevant}
    flow_dates |= {when for when, _ in payments}
    flow_dates = sorted(when for when in flow_dates if start <= when < start + timedelta(days=90))
    protected = {part.strip().lower() for part in profile.get("expense_categories_to_protect", "").split("|") if part.strip()}
    recurring_ids = {id(item) for item in recurring}
    balance = dec(profile.get("current_available_balance"))
    rows = []
    for when in flow_dates:
        starting = balance
        income = Decimal("0")
        essential = Decimal("0")
        scheduled = Decimal("0")
        pending = Decimal("0")
        recurring_expense = Decimal("0")
        recurring_income = Decimal("0")
        for item in relevant:
            if item["date"] != when:
                continue
            signed = item["amount"]
            row = item["row"]
            if item["direction"] == "credit":
                income += signed
                if id(item) in recurring_ids:
                    recurring_income += signed
            else:
                if id(item) in recurring_ids:
                    recurring_expense += signed
                elif row.get("status") == "scheduled":
                    scheduled += signed
                elif row.get("status") == "pending":
                    pending += signed
                if item["category"] in protected:
                    essential += signed
        payment = sum((amount for payment_date, amount in payments if payment_date == when), Decimal("0"))
        # Essential is a classification of debits, not an additional cash-flow.
        balance = starting + income - scheduled - pending - recurring_expense - payment
        if any(value != 0 for value in (income, essential, scheduled, pending, recurring_expense, recurring_income, payment)) or when == start:
            rows.append((when, starting, income, essential, scheduled, pending, recurring_expense, recurring_income, payment, balance))
    minimum_date = min(forecast["balances"], key=forecast["balances"].get)
    baseline = engine._forecast(request)
    predicted_amount = dec(predicted["amount_safe_to_pay"])
    expected_amount = dec(expected["amount_safe_to_pay"])
    causes = []
    if expected_amount != predicted_amount:
        causes.append("E/F: recurring amount or timing / forecast cash-flow difference")
    if expected["recommended_payment_method"] != predicted["recommended_payment_method"]:
        if predicted["recommended_payment_method"] in {"installments", "partial_payment"} or expected["recommended_payment_method"] in {"installments", "partial_payment"}:
            causes.append("J: payment option or plan eligibility difference")
        elif expected["spending_changes_needed"] != predicted["spending_changes_needed"]:
            causes.append("I: flexible spending optimization")
        else:
            causes.append("B/K/L: event inclusion, horizon, or date timing difference")
    if expected["earliest_date_for_full_payment"] != predicted["earliest_date_for_full_payment"]:
        causes.append("F/L: earliest-safe date timing difference")
    if any(item["row"].get("amount", "").strip() == "" for item in explicit + recurring):
        causes.append("M: missing amount evidence may affect the trace")
    cause_text = "; ".join(dict.fromkeys(causes)) or "N: no single numerical cause isolated"
    lines = [
        f"## {request['request_id']} / {request['user_id']}",
        "", f"- Request date: `{request['request_date']}`", f"- Requested amount: `{home} {request['requested_amount']}`",
        f"- Current balance: `{home} {profile.get('current_available_balance', '')}`", f"- Minimum balance: `{home} {profile.get('minimum_balance_to_keep', '')}`",
        f"- Expected status: `{expected['affordability_status']}`", f"- Predicted status: `{predicted['affordability_status']}`",
        f"- Expected method: `{expected['recommended_payment_method']}`", f"- Predicted method: `{predicted['recommended_payment_method']}`",
        f"- Root-cause classification: **{cause_text}**", "",
        "### Expected and Predicted Reasoning", "",
        f"- Expected explanation: {expected.get('decision_explanation', '')}",
        f"- Predicted explanation: {predicted.get('decision_explanation', '')}",
        f"- Expected safe amount: `{expected_amount}`; predicted safe amount: `{predicted_amount}`; difference: `{predicted_amount - expected_amount}`",
        f"- Baseline minimum without request: `{fmt(baseline['minimum'])}` on `{min(baseline['balances'], key=baseline['balances'].get).isoformat()}`",
        f"- Plan minimum with predicted plan: `{fmt(forecast['minimum'])}` on `{minimum_date.isoformat()}`",
        f"- Forecast horizon: `{start.isoformat()}` through `{(start + timedelta(days=89)).isoformat()}`; safe amount formula: minimum baseline balance minus required minimum, capped to request amount.", "",
        "### Chronological Forecast", "",
        "| date | starting balance | income | essential expenses | scheduled expenses | pending obligations | recurring expenses | recurring income | payment option payment | ending balance |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append("| " + " | ".join([row[0].isoformat()] + [fmt(value) for value in row[1:]]) + " |")
    lines.extend(["", "### Inputs Used", "", f"- Explicit future events: `{len(explicit)}`", f"- Inferred recurring events: `{len(recurring)}`", f"- Recurring income categories: `{', '.join(sorted({item['category'] for item in recurring if item['direction'] == 'credit'})) or 'none'}`", f"- Recurring expense categories: `{', '.join(sorted({item['category'] for item in recurring if item['direction'] == 'debit'})) or 'none'}`", f"- Pending event IDs: `{', '.join(item['row'].get('event_id', '') for item in explicit if item['row'].get('status') == 'pending') or 'none'}`", f"- Scheduled event IDs: `{', '.join(item['row'].get('event_id', '') for item in explicit if item['row'].get('status') == 'scheduled') or 'none'}`", f"- Payment option payments in predicted plan: `{predicted['payment_plan']}`", ""])
    return "\n".join(lines)


def classify(request: dict[str, str], expected: dict[str, str], predicted: dict[str, str]) -> str:
    if expected["spending_changes_needed"] != predicted["spending_changes_needed"]:
        return "I: flexible spending optimization"
    if expected["recommended_payment_method"] != predicted["recommended_payment_method"] and {expected["recommended_payment_method"], predicted["recommended_payment_method"]} & {"installments", "partial_payment"}:
        return "J: payment option evaluation"
    if expected["amount_safe_to_pay"] != predicted["amount_safe_to_pay"]:
        return "D/E/F: forecast recurrence amount/timing"
    if expected["earliest_date_for_full_payment"] != predicted["earliest_date_for_full_payment"]:
        return "F/L: recurring timing or date/rounding"
    return "B/K/N: event inclusion or horizon"


def main() -> None:
    store = DataStore(ROOT / "dataset")
    engine = AffordabilityEngine(store)
    with (ROOT / "dataset" / "sample_requests.csv").open(newline="", encoding="utf-8-sig") as handle:
        samples = list(csv.DictReader(handle))
    sections = ["# Deep Status Mismatch Analysis", "", "This report is generated from the current engine without changing decision logic.", ""]
    status_rows = []
    for request in samples:
        predicted = engine.decide(request)
        if predicted["affordability_status"] == request["affordability_status"]:
            continue
        status_rows.append((request["request_id"], request["user_id"], request["affordability_status"], predicted["affordability_status"]))
        sections.append(build_trace(store, engine, request, request, predicted))
        sections.append("\n---\n")
    sections.insert(3, "## Status Mismatch Summary\n\n| request_id | user_id | expected | predicted |\n|---|---|---|---|\n" + "\n".join(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |" for row in status_rows) + "\n")
    root_rows = []
    for request in samples:
        predicted = engine.decide(request)
        if predicted["affordability_status"] != request["affordability_status"]:
            root_rows.append((request, predicted))
    root_table = ["## Root-Cause Summary", "", "| request_id | safe amount expected | safe amount predicted | earliest expected | earliest predicted | classification |", "|---|---:|---:|---|---|---|"]
    root_table.extend(
        f"| {request['request_id']} | {request['amount_safe_to_pay']} | {predicted['amount_safe_to_pay']} | {request['earliest_date_for_full_payment']} | {predicted['earliest_date_for_full_payment']} | {classify(request, request, predicted)} |"
        for request, predicted in root_rows
    )
    sections.insert(4, "\n".join(root_table) + "\n")
    (ROOT / "code" / "evaluation" / "deep_status_mismatch_analysis.md").write_text("\n".join(sections), encoding="utf-8")


if __name__ == "__main__":
    main()
