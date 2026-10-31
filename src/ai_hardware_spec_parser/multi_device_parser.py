import re
from typing import List, Dict, Optional
from .performance_extractor import PerformanceExtractor
from .memory_extractor import MemoryExtractor
from .power_efficiency_extractor import PowerEfficiencyExtractor

class MultiDeviceParser:
    """
    Parses hardware spec text containing multiple device entries.
    Each device entry is separated by a delimiter or detected heuristically.
    """
    # Default delimiter: two or more newlines or '---' lines
    DEVICE_SPLIT_PATTERN = re.compile(r"(?:^|\n)(?:-{3,}|\n{2,})(?=\s*\S)", re.MULTILINE)

    def __init__(self, text: str):
        self.text = text
        self.device_texts = self._split_devices(text)

    def _split_devices(self, text: str) -> List[str]:
        # Split on delimiter or two or more newlines
        # Remove empty entries
        splits = self.DEVICE_SPLIT_PATTERN.split(text)
        return [s.strip() for s in splits if s.strip()]

    def parse_all(self) -> List[Dict[str, Optional[str]]]:
        """
        Parses all device entries and extracts their specs.
        Returns:
            list of dict: Each dict contains extracted fields for a device.
        """
        results = []
        for device_text in self.device_texts:
            perf = PerformanceExtractor(device_text).extract()
            mem = MemoryExtractor(device_text).extract()
            eff = PowerEfficiencyExtractor(device_text).extract()
            # Merge all extracted fields
            merged = {}
            merged.update(perf)
            merged.update(mem)
            merged.update(eff)
            results.append(merged)
        return results

    def device_count(self) -> int:
        """
        Returns the number of detected device entries.
        """
        return len(self.device_texts)

    def get_device_texts(self) -> List[str]:
        """
        Returns the raw text blocks for each device.
        """
        return self.device_texts
