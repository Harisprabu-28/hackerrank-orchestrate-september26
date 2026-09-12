"""Run the Buy or Wait? affordability pipeline."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from data_loader import DataStore
from decision_engine import AffordabilityEngine


OUTPUT_COLUMNS = [
	"request_id", "amount_safe_to_pay", "affordability_status",
	"recommended_payment_method", "payment_plan",
	"earliest_date_for_full_payment", "spending_changes_needed",
	"decision_explanation",
]


def main() -> None:
	logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
	root = Path(__file__).resolve().parents[1]
	store = DataStore(root / "dataset")
	engine = AffordabilityEngine(store)
	rows = [engine.decide(request) for request in store.tables["requests"]]
	if len({row["request_id"] for row in rows}) != len(rows):
		raise ValueError("Duplicate request IDs in generated output")
	with (root / "output.csv").open("w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
		writer.writeheader()
		writer.writerows(rows)
	logging.info("Generated %d decisions in %s", len(rows), root / "output.csv")


if __name__ == "__main__":
	main()
