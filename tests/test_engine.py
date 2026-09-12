import unittest
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))

from decision_engine import AffordabilityEngine


class SyntheticStore:
    def __init__(self, balance="100", minimum="20", methods="full_payment"):
        self.dataset_dir = Path(".")
        self.tables = {"exchange_rates": []}
        self._profile = {
            "user_id": "u", "home_currency": "USD", "current_available_balance": balance,
            "minimum_balance_to_keep": minimum, "expense_categories_to_protect": "rent",
            "expense_categories_user_is_willing_to_reduce": "dining",
            "expense_categories_user_is_willing_to_stop": "streaming",
            "payment_methods_user_will_consider": methods, "max_installment_months": "6",
        }
        self._events = []
        self._options = []

    def profile(self, user_id):
        return self._profile

    def user_events(self, user_id):
        return self._events

    def request_options(self, request_id):
        return self._options

    def image_for_event(self, event_id):
        return None

    def _request(self, amount="50", methods=None):
        return {
            "request_id": "r", "user_id": "u", "request_date": "2025-01-01",
            "requested_amount": amount, "desired_completion_date": "2025-03-01",
            "allows_partial_payment": "true", "request_type": "purchase",
            "request_text": "",
        }


def event(event_id, amount, event_date, status="settled", direction="debit", category="dining", flexibility="fixed", linked=""):
    return {
        "event_id": event_id, "user_id": "u", "event_type": "expense", "description": event_id,
        "category": category, "direction": direction, "amount": amount, "currency": "USD",
        "event_date": event_date, "settlement_date": event_date, "status": status,
        "linked_event_id": linked, "flexibility": flexibility, "minimum_allowed_amount": "10",
    }


class EngineTests(unittest.TestCase):
    def engine(self, store=None):
        return AffordabilityEngine(store or SyntheticStore())

    def test_full_payment_safe(self):
        result = self.engine().decide(SyntheticStore()._request("50"))
        self.assertEqual(result["recommended_payment_method"], "full_payment")

    def test_full_payment_unsafe(self):
        store = SyntheticStore(balance="50", minimum="20")
        store._events = [event("future", "40", "2025-01-02")]
        result = self.engine(store).decide(store._request("40"))
        self.assertNotEqual(result["recommended_payment_method"], "full_payment")

    def test_installment_plan_safe(self):
        store = SyntheticStore(balance="70", minimum="20", methods="installments")
        store._options = [{"payment_option_id": "o", "request_id": "r", "payment_method": "installments", "payment_amount": "20", "number_of_payments": "2", "first_payment_date": "2025-01-02", "payment_frequency_days": "30", "financing_fee": "0"}]
        result = self.engine(store).decide(store._request("40"))
        self.assertEqual(result["recommended_payment_method"], "installments")

    def test_installment_plan_unsafe(self):
        store = SyntheticStore(balance="50", minimum="20", methods="installments")
        store._events = [event("future", "40", "2025-01-02")]
        store._options = [{"payment_option_id": "o", "request_id": "r", "payment_method": "installments", "payment_amount": "20", "number_of_payments": "2", "first_payment_date": "2025-01-02", "payment_frequency_days": "30", "financing_fee": "0"}]
        result = self.engine(store).decide(store._request("40"))
        self.assertNotEqual(result["recommended_payment_method"], "installments")

    def test_partial_payment_requires_permission(self):
        store = SyntheticStore(balance="50", minimum="20", methods="partial_payment")
        request = store._request("40")
        request["allows_partial_payment"] = "false"
        self.assertNotEqual(self.engine(store).decide(request)["recommended_payment_method"], "partial_payment")

    def test_minimum_balance_violation(self):
        store = SyntheticStore(balance="25", minimum="20")
        forecast = self.engine(store)._forecast(store._request("10"), [(date(2025, 1, 1), 10)])
        self.assertTrue(forecast["violates"])

    def test_recurring_expense(self):
        store = SyntheticStore()
        store._events = [event("a", "5", "2024-11-01"), event("b", "5", "2024-12-01"), event("c", "5", "2024-12-31")]
        forecast = self.engine(store)._forecast(store._request("1"))
        self.assertLess(forecast["balances"][date(2025, 1, 31)], 100)

    def test_scheduled_income_included(self):
        store = SyntheticStore()
        store._events = [event("salary", "50", "2025-01-02", "scheduled", "credit", "salary")]
        forecast = self.engine(store)._forecast(store._request("1"))
        self.assertEqual(forecast["balances"][date(2025, 1, 2)], 150)

    def test_pending_expense_included(self):
        store = SyntheticStore()
        store._events = [event("pending", "10", "2025-01-02", "pending")]
        self.assertEqual(self.engine(store)._forecast(store._request("1"))["balances"][date(2025, 1, 2)], 90)

    def test_cancelled_event_excluded(self):
        store = SyntheticStore()
        store._events = [event("cancelled", "90", "2025-01-02", "cancelled")]
        self.assertEqual(self.engine(store)._forecast(store._request("1"))["balances"][date(2025, 1, 2)], 100)

    def test_failed_event_excluded(self):
        store = SyntheticStore()
        store._events = [event("failed", "90", "2025-01-02", "failed")]
        self.assertEqual(self.engine(store)._forecast(store._request("1"))["balances"][date(2025, 1, 2)], 100)

    def test_pending_refund_excluded(self):
        store = SyntheticStore()
        store._events = [event("refund", "90", "2025-01-02", "pending", "credit", "shopping")]
        self.assertEqual(self.engine(store)._forecast(store._request("1"))["balances"][date(2025, 1, 2)], 100)

    def test_linked_event_does_not_crash(self):
        store = SyntheticStore()
        store._events = [event("original", "10", "2024-12-01"), event("retry", "10", "2025-01-02", "pending", linked="original")]
        self.assertEqual(self.engine(store)._forecast(store._request("1"))["balances"][date(2025, 1, 2)], 90)

    def test_missing_amount_is_excluded(self):
        store = SyntheticStore()
        store._events = [event("missing", "", "2025-01-02")]
        self.assertEqual(self.engine(store)._forecast(store._request("1"))["balances"][date(2025, 1, 2)], 100)

    def test_earliest_full_payment_searches_forecast(self):
        store = SyntheticStore(balance="50", minimum="20")
        store._events = [event("income", "30", "2025-01-02", "scheduled", "credit", "salary")]
        result = self.engine(store).decide(store._request("50"))
        self.assertEqual(result["earliest_date_for_full_payment"], "2025-01-02")

    def test_multiple_spending_changes_can_be_required(self):
        store = SyntheticStore(balance="100", minimum="20")
        store._profile["expense_categories_user_is_willing_to_stop"] = "streaming|dining"
        store._events = [
            event("stream_1", "20", "2024-10-01", category="streaming", flexibility="stoppable"),
            event("stream_2", "20", "2024-11-01", category="streaming", flexibility="stoppable"),
            event("stream_3", "20", "2024-12-01", category="streaming", flexibility="stoppable"),
            event("dining_1", "15", "2024-10-01", category="dining", flexibility="stoppable"),
            event("dining_2", "15", "2024-11-01", category="dining", flexibility="stoppable"),
            event("dining_3", "15", "2024-12-01", category="dining", flexibility="stoppable"),
        ]
        request = store._request("80")
        engine = self.engine(store)
        result = engine._minimal_change_set(request, date(2025, 3, 1), [(date(2025, 1, 1), 80)])
        self.assertIsNotNone(result)
        self.assertEqual(len(result[0]), 2)

    def test_one_spending_change_is_preferred_when_sufficient(self):
        store = SyntheticStore(balance="100", minimum="20")
        store._profile["expense_categories_user_is_willing_to_stop"] = "streaming|dining"
        store._events = [
            event("stream_1", "20", "2024-10-01", category="streaming", flexibility="stoppable"),
            event("stream_2", "20", "2024-11-01", category="streaming", flexibility="stoppable"),
            event("stream_3", "20", "2024-12-01", category="streaming", flexibility="stoppable"),
            event("dining_1", "5", "2024-10-01", category="dining", flexibility="stoppable"),
            event("dining_2", "5", "2024-11-01", category="dining", flexibility="stoppable"),
            event("dining_3", "5", "2024-12-01", category="dining", flexibility="stoppable"),
        ]
        request = store._request("60")
        result = self.engine(store)._minimal_change_set(request, date(2025, 3, 1), [(date(2025, 1, 1), 60)])
        self.assertIsNotNone(result)
        self.assertEqual(len(result[0]), 1)

    def test_protected_and_fixed_events_are_not_candidates(self):
        store = SyntheticStore()
        store._events = [
            event("rent_1", "30", "2024-10-01", category="rent", flexibility="stoppable"),
            event("rent_2", "30", "2024-11-01", category="rent", flexibility="stoppable"),
            event("rent_3", "30", "2024-12-01", category="rent", flexibility="stoppable"),
            event("fixed_1", "30", "2024-10-01", category="streaming", flexibility="fixed"),
            event("fixed_2", "30", "2024-11-01", category="streaming", flexibility="fixed"),
            event("fixed_3", "30", "2024-12-01", category="streaming", flexibility="fixed"),
        ]
        candidate_ids = {item["row"]["event_id"] for item in self.engine(store)._changes(store._request("80"))}
        self.assertNotIn("rent_1", candidate_ids)
        self.assertNotIn("fixed_1", candidate_ids)

    def test_best_installment_selection_is_reusable(self):
        store = SyntheticStore(balance="100", minimum="20", methods="installments")
        store._options = [
            {"payment_option_id": "z", "request_id": "r", "payment_method": "installments", "payment_amount": "20", "number_of_payments": "2", "first_payment_date": "2025-01-02", "payment_frequency_days": "30", "financing_fee": "5"},
            {"payment_option_id": "a", "request_id": "r", "payment_method": "installments", "payment_amount": "21", "number_of_payments": "2", "first_payment_date": "2025-01-03", "payment_frequency_days": "30", "financing_fee": "1"},
        ]
        options = self.engine(store)._installment_options(store._request("40"), date(2025, 3, 1))
        self.assertEqual(options[0]["option_id"], "a")

    def test_reduce_change_respects_minimum_allowed_amount(self):
        store = SyntheticStore()
        store._events = [
            event("dining_1", "20", "2024-10-01", category="dining", flexibility="reducible"),
            event("dining_2", "20", "2024-11-01", category="dining", flexibility="reducible"),
            event("dining_3", "20", "2024-12-01", category="dining", flexibility="reducible"),
        ]
        candidates = self.engine(store)._changes(store._request("80"))
        self.assertTrue(any(item["action"] == "reduce" and item["amount"] == 10 for item in candidates))

    def test_complete_partial_schedule_is_checked_as_one_plan(self):
        store = SyntheticStore(balance="60", minimum="20")
        store._events = [event("income", "30", "2025-01-15", "scheduled", "credit", "salary")]
        request = store._request("50")
        safe_plan = [(date(2025, 1, 1), 20), (date(2025, 2, 1), 30)]
        unsafe_plan = [(date(2025, 1, 1), 20), (date(2025, 1, 2), 30)]
        self.assertTrue(self.engine(store)._safe(request, safe_plan))
        self.assertFalse(self.engine(store)._safe(request, unsafe_plan))

    def test_spending_change_does_not_remove_explicit_nonrecurring_event(self):
        store = SyntheticStore(balance="100", minimum="20")
        store._profile["expense_categories_user_is_willing_to_stop"] = "streaming"
        store._events = [
            event("history_1", "10", "2024-10-01", category="streaming", flexibility="stoppable"),
            event("history_2", "10", "2024-11-01", category="streaming", flexibility="stoppable"),
            event("history_3", "10", "2024-12-01", category="streaming", flexibility="stoppable"),
            event("future", "25", "2025-01-02", status="scheduled", category="streaming", flexibility="stoppable"),
        ]
        request = store._request("1")
        candidate = next(item for item in self.engine(store)._changes(request) if item["action"] == "stop")
        forecast = self.engine(store)._forecast(request, changes=[candidate])
        self.assertEqual(forecast["balances"][date(2025, 1, 2)], 75)


if __name__ == "__main__":
    unittest.main()