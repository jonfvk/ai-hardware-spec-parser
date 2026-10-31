import re
from typing import Optional, Dict

class MemoryExtractor:
    """
    Extracts memory size and type from hardware spec text.
    """

    # Patterns for memory size and type (case-insensitive)
    # Examples: 8GB LPDDR5, 16 GB GDDR6, 32GB HBM2e, 4 GB DDR4
    MEMORY_PATTERN = re.compile(
        r"(?P<size>[\d,.]+)\s*(?P<unit>GB|MB|TB)\s*(?P<type>LPDDR\d|GDDR\d|HBM\d?\w*|DDR\d|SRAM|DRAM|eMMC|UFS)?",
        re.IGNORECASE
    )

    def __init__(self, text: str):
        self.text = text
        self.memory = {}

    def extract(self) -> Dict[str, Optional[str]]:
        """
        Extracts memory size and type from the input text.
        Returns:
            dict: Dictionary with extracted memory info (e.g., {'Memory Size': '8 GB', 'Memory Type': 'LPDDR5'})
        """
        self.memory = {'Memory Size': None, 'Memory Type': None}
        self._extract_memory()
        return self.memory

    def _extract_memory(self):
        matches = list(self.MEMORY_PATTERN.finditer(self.text))
        if matches:
            # Take the first match as the main memory spec
            match = matches[0]
            size = match.group('size').replace(',', '')
            unit = match.group('unit').upper()
            mem_type = match.group('type')
            self.memory['Memory Size'] = f"{size} {unit}"
            if mem_type:
                self.memory['Memory Type'] = mem_type.upper()
            else:
                self.memory['Memory Type'] = None
        else:
            self.memory['Memory Size'] = None
            self.memory['Memory Type'] = None
