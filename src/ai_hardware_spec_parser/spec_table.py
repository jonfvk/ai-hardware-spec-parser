from typing import Dict, Optional, List

class SpecTable:
    """
    Summarizes extracted hardware specs in a table format.
    """
    
    DEFAULT_FIELDS = [
        'TOPS',
        'Memory Size',
        'Memory Type',
        'Power Efficiency',
    ]

    def __init__(self, extracted: Dict[str, Optional[str]]):
        """
        Initializes the SpecTable with extracted fields.
        Args:
            extracted (dict): Dictionary with extracted spec fields.
        """
        self.extracted = extracted

    def as_dict(self) -> Dict[str, Optional[str]]:
        """
        Returns the extracted specs as a dictionary with default fields.
        Returns:
            dict: Spec fields as key-value pairs.
        """
        return {field: self.extracted.get(field) for field in self.DEFAULT_FIELDS}

    def as_table(self, fields: Optional[List[str]] = None) -> str:
        """
        Returns a formatted table (as a string) of the extracted specs.
        Args:
            fields (list, optional): List of fields to include. Defaults to DEFAULT_FIELDS.
        Returns:
            str: Table as a string.
        """
        if fields is None:
            fields = self.DEFAULT_FIELDS
        # Prepare header and row
        header = fields
        row = [self.extracted.get(f) if self.extracted.get(f) is not None else '-' for f in fields]
        # Calculate column widths
        col_widths = [max(len(str(h)), len(str(r))) for h, r in zip(header, row)]
        # Build table lines
        header_line = ' | '.join(h.ljust(w) for h, w in zip(header, col_widths))
        sep_line = '-+-'.join('-' * w for w in col_widths)
        row_line = ' | '.join(str(r).ljust(w) for r, w in zip(row, col_widths))
        table = f"{header_line}\n{sep_line}\n{row_line}"
        return table

    @staticmethod
    def merge_dicts(*dicts: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        """
        Merges multiple extracted spec dicts into one.
        Later dicts override earlier ones for the same key.
        Args:
            *dicts: Dictionaries to merge.
        Returns:
            dict: Merged dictionary.
        """
        result = {}
        for d in dicts:
            result.update(d)
        return result
