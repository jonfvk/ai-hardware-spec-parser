import re
from typing import Optional, Dict

class PerformanceExtractor:
    """
    Extracts AI performance metrics (e.g., TOPS) from hardware spec text.
    """

    # Patterns for common AI performance metrics (case-insensitive)
    TOPS_PATTERN = re.compile(
        r"(?P<value>[\d.,]+)\s*(?P<unit>[TGMK]?OPS)(?:\s*(?:\([^)]+\))?)?",
        re.IGNORECASE
    )
    # Add more patterns as needed for other metrics

    def __init__(self, text: str):
        self.text = text
        self.metrics = {}

    def extract(self) -> Dict[str, Optional[str]]:
        """
        Extracts AI performance metrics from the input text.
        Returns:
            dict: Dictionary with extracted metrics (e.g., {'TOPS': '40 TOPS'})
        """
        self.metrics = {}
        self._extract_tops()
        # Future: add more metric extractors here
        return self.metrics

    def _extract_tops(self):
        matches = list(self.TOPS_PATTERN.finditer(self.text))
        if matches:
            # Take the first match as the main TOPS value
            match = matches[0]
            value = match.group('value').replace(',', '')
            unit = match.group('unit').upper()
            self.metrics['TOPS'] = f"{value} {unit}"
        else:
            self.metrics['TOPS'] = None
