"""Optional local OCR for linked evidence images; missing OCR never stops a run."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from pathlib import Path
import re


class ImageProcessor:
    def __init__(self, dataset_dir: str | Path):
        self.image_dir = Path(dataset_dir) / "media" / "images"

    def extract_amount(self, image_id: str) -> Decimal | None:
        path = self.image_dir / f"{image_id}.png"
        if not path.exists():
            return None
        try:
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(path))
        except (ImportError, OSError, RuntimeError):
            return None
        labels = r"(?:net\s*pay|total\s*(?:order\s*)?bill|cash\s*paid|amount\s*received|total\s*amount)"
        candidates = re.findall(labels + r"[^0-9]{0,40}([0-9][0-9,]*(?:\.[0-9]+)?)", text, flags=re.IGNORECASE)
        for candidate in reversed(candidates):
            try:
                return Decimal(candidate.replace(",", ""))
            except InvalidOperation:
                continue
        return None
