from typing import Dict, Optional, List, Tuple

class MissingDataHighlighter:
    """
    Highlights missing or ambiguous data in extracted hardware specs.
    """
    
    DEFAULT_FIELDS = [
        'TOPS',
        'Memory Size',
        'Memory Type',
        'Power Efficiency',
    ]

    def __init__(self, extracted: Dict[str, Optional[str]], fields: Optional[List[str]] = None):
        """
        Initializes the highlighter with extracted fields.
        Args:
            extracted (dict): Dictionary with extracted spec fields.
            fields (list, optional): List of fields to check. Defaults to DEFAULT_FIELDS.
        """
        self.extracted = extracted
        self.fields = fields if fields is not None else self.DEFAULT_FIELDS

    def missing_fields(self) -> List[str]:
        """
        Returns a list of fields that are missing (None or empty).
        Returns:
            list: List of missing field names.
        """
        return [f for f in self.fields if not self._is_present(self.extracted.get(f))]

    def ambiguous_fields(self) -> List[Tuple[str, str]]:
        """
        Returns a list of (field, value) tuples for fields that are ambiguous.
        Ambiguity is detected by presence of uncertain words (e.g., 'approx', '?', 'unknown').
        Returns:
            list: List of (field, value) tuples.
        """
        ambiguous = []
        for f in self.fields:
            val = self.extracted.get(f)
            if self._is_ambiguous(val):
                ambiguous.append((f, val))
        return ambiguous

    def highlight(self) -> Dict[str, str]:
        """
        Returns a dict mapping field names to status:
        - 'OK' if present and not ambiguous
        - 'MISSING' if missing
        - 'AMBIGUOUS' if ambiguous
        Returns:
            dict: Field name -> status
        """
        result = {}
        for f in self.fields:
            val = self.extracted.get(f)
            if not self._is_present(val):
                result[f] = 'MISSING'
            elif self._is_ambiguous(val):
                result[f] = 'AMBIGUOUS'
            else:
                result[f] = 'OK'
        return result

    @staticmethod
    def _is_present(val: Optional[str]) -> bool:
        if val is None:
            return False
        if isinstance(val, str) and not val.strip():
            return False
        return True

    @staticmethod
    def _is_ambiguous(val: Optional[str]) -> bool:
        if not isinstance(val, str) or not val:
            return False
        # Look for common ambiguous indicators
        ambiguous_words = ['?', 'unknown', 'approx', 'approximately', 'tbd', 'n/a', 'not specified', 'not available', 'unclear']
        val_lower = val.lower()
        for word in ambiguous_words:
            if word in val_lower:
                return True
        return False
