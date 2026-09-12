"""Small, dependency-free data access layer for the challenge datasets."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class DataStore:
    def __init__(self, dataset_dir: str | Path):
        self.dataset_dir = Path(dataset_dir)
        self.tables = {
            name: self._read(name)
            for name in (
                "requests", "sample_requests", "financial_profiles",
                "financial_events", "request_payment_options", "messages",
                "images", "exchange_rates",
            )
        }
        self.profiles = {row["user_id"]: row for row in self.tables["financial_profiles"]}
        self.events = self._group("financial_events", "user_id")
        self.options = self._group("request_payment_options", "request_id")
        self.messages = self._group("messages", "user_id")
        self.images = self._group("images", "user_id")
        self.rates = self.tables["exchange_rates"]

    def _read(self, name: str) -> list[dict[str, str]]:
        path = self.dataset_dir / f"{name}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Required dataset file is missing: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def _group(self, table: str, key: str) -> dict[str, list[dict[str, str]]]:
        result: dict[str, list[dict[str, str]]] = {}
        for row in self.tables[table]:
            result.setdefault(row.get(key, ""), []).append(row)
        return result

    def profile(self, user_id: str) -> dict[str, str]:
        return self.profiles.get(user_id, {})

    def user_events(self, user_id: str) -> list[dict[str, str]]:
        return self.events.get(user_id, [])

    def request_options(self, request_id: str) -> list[dict[str, str]]:
        return self.options.get(request_id, [])

    def user_messages(self, user_id: str) -> list[dict[str, str]]:
        return self.messages.get(user_id, [])

    def image_for_event(self, event_id: str) -> dict[str, str] | None:
        for row in self.tables["images"]:
            if row.get("related_event_id") == event_id:
                return row
        return None
