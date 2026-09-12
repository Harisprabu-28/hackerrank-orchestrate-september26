"""Deterministic affordability engine: event cleaning, recurrence, forecasts and plans."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from itertools import combinations
import re
from typing import Iterable

from data_loader import DataStore
from image_processor import ImageProcessor


MONEY = Decimal("0.01")
BAD_STATUSES = {"cancelled", "failed", "unrealized"}
METHODS = {"full_payment", "partial_payment", "installments"}


def dec(value: object, default: Decimal = Decimal("0")) -> Decimal:
    try:
        if value is None or str(value).strip() == "":
            return default
        return Decimal(str(value).replace(",", "")).quantize(MONEY, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return default


def ddate(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def clean_list(value: object) -> set[str]:
    return {part.strip().lower() for part in str(value or "").split("|") if part.strip()}


def money(value: Decimal) -> str:
    value = value.quantize(MONEY, rounding=ROUND_HALF_UP)
    text = format(value, "f").rstrip("0").rstrip(".")
    return text or "0"


def median(values: list[Decimal | int]) -> Decimal:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return Decimal(str(ordered[middle]))
    return (Decimal(str(ordered[middle - 1])) + Decimal(str(ordered[middle]))) / Decimal("2")


class AffordabilityEngine:
    def __init__(self, store: DataStore, min_recurrence_observations: int = 3, group_recurrence_by_event_type: bool = False):
        self.store = store
        self.min_recurrence_observations = min_recurrence_observations
        self.group_recurrence_by_event_type = group_recurrence_by_event_type
        self.image_processor = ImageProcessor(store.dataset_dir)

    def _rate(self, when: date, source: str, target: str) -> Decimal | None:
        if source == target or not source or not target:
            return Decimal("1")
        candidates = [r for r in self.store.rates if r.get("from_currency") == source and r.get("to_currency") == target]
        candidates.sort(key=lambda r: abs((ddate(r.get("rate_date")) or when) - when))
        if candidates:
            return dec(candidates[0].get("rate"), Decimal("0")) or None
        inverse = [r for r in self.store.rates if r.get("from_currency") == target and r.get("to_currency") == source]
        inverse.sort(key=lambda r: abs((ddate(r.get("rate_date")) or when) - when))
        return (Decimal("1") / dec(inverse[0].get("rate"))) if inverse and dec(inverse[0].get("rate")) else None

    def _amount(self, row: dict[str, str], home: str, when: date) -> Decimal | None:
        raw = row.get("amount", "").strip()
        if not raw:
            image = self.store.image_for_event(row.get("event_id", ""))
            if not image:
                return None
            extracted = self.image_processor.extract_amount(image.get("image_id", ""))
            return extracted if extracted is not None else None
        rate = self._rate(when, row.get("currency", home), home)
        return dec(raw) * rate if rate else None

    def _events(self, user_id: str, home: str, start: date, horizon: int) -> tuple[list[dict], list[dict]]:
        rows = []
        for row in self.store.user_events(user_id):
            status = row.get("status", "").lower()
            direction = row.get("direction")
            if status in BAD_STATUSES or direction not in {"debit", "credit"}:
                continue
            # Pending debits are reserved obligations. Pending credits are
            # uncertain inflows and cannot increase spendable cash.
            if status == "pending" and direction == "credit":
                continue
            effective = ddate(row.get("settlement_date")) or ddate(row.get("event_date"))
            amount = self._amount(row, home, effective or start)
            if not effective or amount is None:
                continue
            item = {"row": row, "date": effective, "amount": amount, "category": row.get("category", "").lower(), "direction": row.get("direction")}
            rows.append(item)

        # A request can use future obligations only when they were already
        # scheduled or pending at the request date. Future settled rows are
        # later historical knowledge and must not leak into this decision.
        explicit = [
            e for e in rows
            if start <= e["date"] <= start + timedelta(days=horizon - 1)
            and e["row"].get("status", "").lower() in {"pending", "scheduled"}
        ]
        historical = [e for e in rows if e["date"] < start and e["row"].get("status") == "settled"]
        recurring: list[dict] = []
        groups: dict[tuple[str, ...], list[dict]] = defaultdict(list)
        for item in historical:
            key = (item["row"].get("event_type", ""), item["category"], item["direction"]) if self.group_recurrence_by_event_type else (item["category"], item["direction"])
            groups[key].append(item)
        explicit_keys = {(e["category"], e["direction"], e["date"]) for e in explicit}
        for key, group in groups.items():
            category, direction = key[-2:]
            group.sort(key=lambda x: x["date"])
            if len(group) < self.min_recurrence_observations:
                continue
            intervals = [(b["date"] - a["date"]).days for a, b in zip(group, group[1:])]
            interval_median = median(intervals)
            if not (5 <= interval_median <= 9 or 12 <= interval_median <= 17 or 25 <= interval_median <= 35):
                continue
            amount = median([x["amount"] for x in group]).quantize(MONEY, rounding=ROUND_HALF_UP)
            next_date = group[-1]["date"] + timedelta(days=int(interval_median))
            while next_date < start:
                next_date += timedelta(days=int(interval_median))
            while next_date <= start + timedelta(days=horizon - 1):
                duplicate_explicit = any(
                    known["category"] == category
                    and known["direction"] == direction
                    and abs((known["date"] - next_date).days) <= 3
                    and abs(known["amount"] - amount) <= max(MONEY, amount * Decimal("0.01"))
                    for known in explicit
                )
                if (category, direction, next_date) not in explicit_keys and not duplicate_explicit:
                    recurring.append({"row": group[-1]["row"], "date": next_date, "amount": amount, "category": category, "direction": direction, "recurring": True})
                next_date += timedelta(days=int(interval_median))
        return explicit, recurring

    def _forecast(self, request: dict[str, str], payments: list[tuple[date, Decimal]] | None = None, changes: list[dict] | None = None, days: int = 90) -> dict:
        profile = self.store.profile(request["user_id"])
        start = ddate(request["request_date"]) or date.today()
        home = profile.get("home_currency", "")
        explicit, recurring = self._events(request["user_id"], home, start, days)
        changes = changes or []
        stopped = {c["category"] for c in changes if c["action"] == "stop"}
        reduced = {c["category"]: c["amount"] for c in changes if c["action"] == "reduce"}
        flows: dict[date, Decimal] = defaultdict(Decimal)
        for item in explicit + recurring:
            if item in recurring and item["category"] in stopped:
                continue
            amount = reduced.get(item["category"], item["amount"])
            flows[item["date"]] += amount if item["direction"] == "credit" else -amount
        for when, amount in payments or []:
            if start <= when <= start + timedelta(days=days - 1):
                flows[when] -= amount
        balance = dec(profile.get("current_available_balance"))
        minimum = dec(profile.get("minimum_balance_to_keep"))
        balances: dict[date, Decimal] = {}
        for offset in range(days):
            when = start + timedelta(days=offset)
            balance += flows[when]
            balances[when] = balance
        minimum_projected = min(balances.values(), default=balance)
        return {"balances": balances, "minimum": minimum_projected, "minimum_required": minimum, "violates": minimum_projected < minimum}

    def _changes(self, request: dict[str, str]) -> list[dict]:
        profile = self.store.profile(request["user_id"])
        protected = clean_list(profile.get("expense_categories_to_protect"))
        allowed_stop = clean_list(profile.get("expense_categories_user_is_willing_to_stop"))
        allowed_reduce = clean_list(profile.get("expense_categories_user_is_willing_to_reduce"))
        start = ddate(request["request_date"]) or date.today()
        home = profile.get("home_currency", "")
        candidates = []
        for row in self.store.user_events(request["user_id"]):
            when = ddate(row.get("settlement_date")) or ddate(row.get("event_date"))
            amount = self._amount(row, home, when or start)
            category = row.get("category", "").lower()
            if not when or when >= start or amount is None or category in protected or row.get("direction") != "debit" or row.get("flexibility") == "fixed":
                continue
            if category in allowed_stop and row.get("flexibility") in {"stoppable", "reducible_or_stoppable"}:
                candidates.append({"action": "stop", "category": category, "row": row, "amount": Decimal("0"), "saving": amount})
            if category in allowed_reduce and row.get("flexibility") in {"reducible", "reducible_or_stoppable"}:
                floor = dec(row.get("minimum_allowed_amount"), Decimal("0"))
                candidates.append({"action": "reduce", "category": category, "row": row, "amount": floor, "saving": amount - floor})
        candidates.sort(key=lambda c: (-c["saving"], c["row"].get("event_id", ""), c["action"]))
        return candidates

    def _safe(self, request: dict[str, str], payments=None, changes=None) -> bool:
        return not self._forecast(request, payments, changes)["violates"]

    def _installment_options(self, request: dict[str, str], deadline: date, changes: list[dict] | None = None) -> list[dict]:
        """Return safe supplied installment schedules in deterministic rank order."""
        profile = self.store.profile(request["user_id"])
        start = ddate(request["request_date"]) or date.today()
        methods = clean_list(profile.get("payment_methods_user_will_consider"))
        max_months = dec(profile.get("max_installment_months"), Decimal("0"))
        if "installments" not in methods:
            return []
        options = []
        for option in self.store.request_options(request["request_id"]):
            first = ddate(option.get("first_payment_date"))
            count = int(dec(option.get("number_of_payments"), Decimal("0")))
            interval = int(dec(option.get("payment_frequency_days"), Decimal("0")))
            if option.get("payment_method", "").lower() != "installments" or not first or count <= 0 or interval < 0:
                continue
            last = first + timedelta(days=interval * (count - 1))
            if (max_months and (last - start).days > int(max_months * 31)) or last > deadline:
                continue
            schedule = [(first + timedelta(days=interval * index), dec(option.get("payment_amount"))) for index in range(count)]
            if self._safe(request, schedule, changes):
                options.append({
                    "fee": dec(option.get("financing_fee")),
                    "count": count,
                    "last": last,
                    "option_id": option.get("payment_option_id", ""),
                    "schedule": schedule,
                })
        options.sort(key=lambda item: (item["fee"], item["count"], item["last"], item["option_id"]))
        return options

    def _minimal_change_set(self, request: dict[str, str], deadline: date, full: list[tuple[date, Decimal]]) -> tuple[list[dict], str, list[tuple[date, Decimal]] | None] | None:
        """Find a bounded, deterministic minimum set of compatible spending changes."""
        methods = clean_list(self.store.profile(request["user_id"]).get("payment_methods_user_will_consider"))
        candidates = self._changes(request)
        candidates.sort(key=lambda item: (item["row"].get("event_id", ""), item["action"]))
        for size in range(1, min(3, len(candidates)) + 1):
            for selected in combinations(candidates, size):
                event_ids = [item["row"].get("event_id", "") for item in selected]
                if len(set(event_ids)) != len(event_ids):
                    continue
                selected_list = list(selected)
                if "full_payment" in methods and self._safe(request, full, selected_list):
                    return selected_list, "full_payment", full
                options = self._installment_options(request, deadline, selected_list)
                if options:
                    return selected_list, "installments", options[0]["schedule"]
        return None

    def decide(self, request: dict[str, str]) -> dict[str, str]:
        profile = self.store.profile(request["user_id"])
        start = ddate(request["request_date"]) or date.today()
        deadline = ddate(request.get("desired_completion_date")) or start + timedelta(days=89)
        amount = dec(request.get("requested_amount"))
        methods = clean_list(profile.get("payment_methods_user_will_consider"))
        baseline = self._forecast(request)
        safe_today = max(Decimal("0"), baseline["minimum"] - baseline["minimum_required"]).quantize(MONEY)
        safe_today = min(safe_today, amount)

        def plan_safe(plan):
            return self._safe(request, plan)

        full = [(start, amount)]
        earliest = ""
        for offset in range(90):
            when = start + timedelta(days=offset)
            if plan_safe([(when, amount)]):
                earliest = when.isoformat()
                break

        changes: list[dict] = []
        if "full_payment" in methods and plan_safe(full):
            chosen_method, chosen_plan, status = "full_payment", full, "affordable_now"
        else:
            chosen_method = chosen_plan = status = None
            options = self._installment_options(request, deadline)
            if options:
                chosen_method, chosen_plan, status = "installments", options[0]["schedule"], "affordable_with_plan"
            elif "partial_payment" in methods and str(request.get("allows_partial_payment", "")).lower() == "true" and Decimal("0") < safe_today < amount and earliest and date.fromisoformat(earliest) <= deadline:
                chosen_method, chosen_plan, status = "partial_payment", [(start, safe_today), (date.fromisoformat(earliest), amount - safe_today)], "affordable_with_plan"
            elif "full_payment" in methods and earliest and date.fromisoformat(earliest) <= deadline:
                chosen_method, chosen_plan, status = "wait", [(date.fromisoformat(earliest), amount)], "affordable_later"

        if chosen_method is None:
            change_result = self._minimal_change_set(request, deadline, full)
            if change_result:
                changes, chosen_method, chosen_plan = change_result
                status = "affordable_with_plan"
            if chosen_method is None:
                chosen_method, chosen_plan, status = "not_recommended", [], "not_affordable"

        change_text = []
        for change in changes:
            event_id = change["row"].get("event_id", "")
            change_text.append(f"stop:{event_id}" if change["action"] == "stop" else f"reduce_to:{event_id}:{money(change['amount'])}")
        plan_text = "|".join(f"{when.isoformat()}:{money(value)}" for when, value in chosen_plan) if chosen_plan else "none"
        if chosen_method == "not_recommended":
            explanation = f"Do not proceed with the {profile.get('home_currency', '')} {money(amount)} request. None of the available options keeps the {profile.get('home_currency', '')} {money(baseline['minimum_required'])} minimum protected."
        elif chosen_method == "wait":
            explanation = f"Pay {profile.get('home_currency', '')} {money(amount)} in full on {earliest}. Paying earlier would risk the {profile.get('home_currency', '')} {money(baseline['minimum_required'])} minimum."
        elif chosen_method == "installments":
            explanation = f"Use {len(chosen_plan)} installments of {profile.get('home_currency', '')} {money(chosen_plan[0][1])}, starting {chosen_plan[0][0].isoformat()}."
        elif chosen_method == "partial_payment":
            explanation = f"Pay {profile.get('home_currency', '')} {money(chosen_plan[0][1])} today and the remaining {profile.get('home_currency', '')} {money(chosen_plan[1][1])} on {chosen_plan[1][0].isoformat()}."
        else:
            explanation = f"Pay {profile.get('home_currency', '')} {money(amount)} today. This protects the {profile.get('home_currency', '')} {money(baseline['minimum_required'])} minimum."
        return {"request_id": request["request_id"], "amount_safe_to_pay": money(safe_today), "affordability_status": status, "recommended_payment_method": chosen_method, "payment_plan": plan_text, "earliest_date_for_full_payment": earliest, "spending_changes_needed": "|".join(change_text) if change_text else "none", "decision_explanation": explanation}
