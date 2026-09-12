"""Deterministic extraction of financial facts from untrusted messages."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re


@dataclass(frozen=True)
class MessageFact:
    message_id: str
    classification: str
    dates: tuple[str, ...]
    amounts: tuple[tuple[str, Decimal], ...]


class MessageProcessor:
    DATE_PATTERN = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
    AMOUNT_PATTERN = re.compile(r"\b(INR|IDR|ZAR|USD|EUR)\s*([0-9][0-9,]*(?:\.[0-9]+)?)\b", re.IGNORECASE)
    UNCERTAIN_PATTERN = re.compile(r"pending|not approved|not been credited|may change|not withdrawable|not been approved|not confirmed", re.IGNORECASE)
    CONFIRMED_PATTERN = re.compile(r"confirmed|guaranteed|approved|currently scheduled|has reached your account|credited", re.IGNORECASE)

    def parse(self, row: dict[str, str]) -> MessageFact:
        text = row.get("message_text", "")
        if self.UNCERTAIN_PATTERN.search(text):
            classification = "uncertain"
        elif self.CONFIRMED_PATTERN.search(text):
            classification = "confirmed"
        else:
            classification = "informational"
        amounts = []
        for currency, raw in self.AMOUNT_PATTERN.findall(text):
            try:
                amounts.append((currency.upper(), Decimal(raw.replace(",", ""))))
            except InvalidOperation:
                continue
        return MessageFact(
            message_id=row.get("message_id", ""),
            classification=classification,
            dates=tuple(self.DATE_PATTERN.findall(text)),
            amounts=tuple(amounts),
        )
