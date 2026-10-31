import re
from typing import Optional, Dict

class PowerEfficiencyExtractor:
    """
    Extracts power efficiency details from hardware spec text.
    """

    # Patterns for power efficiency (e.g., 1.2 TOPS/W, 20 TOPS per Watt, 0.5 W/TOPS)
    # Handles both TOPS/W and W/TOPS (inverse)
    EFFICIENCY_PATTERNS = [
        re.compile(r"(?P<value>[\d.,]+)\s*(?P<perf>[TGMK]?OPS)\s*/\s*(?P<unit>W|WATT|WATTS)", re.IGNORECASE),
        re.compile(r"(?P<value>[\d.,]+)\s*(?P<unit>W|WATT|WATTS)\s*/\s*(?P<perf>[TGMK]?OPS)", re.IGNORECASE),
        re.compile(r"(?P<value>[\d.,]+)\s*(?P<perf>[TGMK]?OPS)\s*(?:per|PER)\s*(?P<unit>W|WATT|WATTS)", re.IGNORECASE),
        re.compile(r"(?P<value>[\d.,]+)\s*(?P<unit>W|WATT|WATTS)\s*(?:per|PER)\s*(?P<perf>[TGMK]?OPS)", re.IGNORECASE),
    ]

    def __init__(self, text: str):
        self.text = text
        self.efficiency = {}

    def extract(self) -> Dict[str, Optional[str]]:
        """
        Extracts power efficiency details from the input text.
        Returns:
            dict: Dictionary with extracted efficiency info (e.g., {'Power Efficiency': '1.2 TOPS/W'})
        """
        self.efficiency = {'Power Efficiency': None}
        self._extract_efficiency()
        return self.efficiency

    def _extract_efficiency(self):
        for pattern in self.EFFICIENCY_PATTERNS:
            match = pattern.search(self.text)
            if match:
                value = match.group('value').replace(',', '')
                perf = match.group('perf').upper() if match.group('perf') else ''
                unit = match.group('unit').upper()
                # Normalize to TOPS/W if possible
                if perf and unit.startswith('W'):
                    if pattern.pattern.find('/\\s*(?P<unit>W') != -1 or 'per' in pattern.pattern:
                        # e.g., 1.2 TOPS/W or 1.2 TOPS per W
                        self.efficiency['Power Efficiency'] = f"{value} {perf}/{unit}"
                    else:
                        # e.g., 0.5 W/TOPS or 0.5 W per TOPS
                        self.efficiency['Power Efficiency'] = f"{value} {unit}/{perf}"
                else:
                    # Fallback, just join what we have
                    self.efficiency['Power Efficiency'] = f"{value} {perf}/{unit}"
                return
        # If no match, leave as None
        self.efficiency['Power Efficiency'] = None
