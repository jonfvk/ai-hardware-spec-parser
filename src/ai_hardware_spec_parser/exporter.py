import csv
import json
from typing import List, Dict, Optional, Union, IO

class SpecExporter:
    """
    Allows exporting extracted hardware specs to CSV or JSON formats.
    Supports exporting single or multiple device specs.
    """
    
    DEFAULT_FIELDS = [
        'TOPS',
        'Memory Size',
        'Memory Type',
        'Power Efficiency',
    ]

    @staticmethod
    def to_csv(
        specs: Union[Dict[str, Optional[str]], List[Dict[str, Optional[str]]]],
        file: Optional[IO[str]] = None,
        fields: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Exports specs to CSV format.
        Args:
            specs: Single dict or list of dicts with spec fields.
            file: Optional file-like object to write CSV to. If None, returns CSV as string.
            fields: Optional list of fields to include. Defaults to DEFAULT_FIELDS.
        Returns:
            str or None: CSV string if file is None, else None.
        """
        if fields is None:
            fields = SpecExporter.DEFAULT_FIELDS
        # Ensure specs is a list of dicts
        if isinstance(specs, dict):
            rows = [specs]
        else:
            rows = specs
        output = None
        close_file = False
        if file is None:
            import io
            output = io.StringIO()
            file = output
            close_file = True
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            # Replace None with empty string for CSV
            csv_row = {f: (row.get(f) if row.get(f) is not None else '') for f in fields}
            writer.writerow(csv_row)
        if close_file:
            return output.getvalue()
        return None

    @staticmethod
    def to_json(
        specs: Union[Dict[str, Optional[str]], List[Dict[str, Optional[str]]]],
        file: Optional[IO[str]] = None,
        fields: Optional[List[str]] = None,
        indent: int = 2
    ) -> Optional[str]:
        """
        Exports specs to JSON format.
        Args:
            specs: Single dict or list of dicts with spec fields.
            file: Optional file-like object to write JSON to. If None, returns JSON as string.
            fields: Optional list of fields to include. Defaults to DEFAULT_FIELDS.
            indent: Indentation for JSON output.
        Returns:
            str or None: JSON string if file is None, else None.
        """
        if fields is None:
            fields = SpecExporter.DEFAULT_FIELDS
        # Ensure specs is a list of dicts
        if isinstance(specs, dict):
            filtered = {f: specs.get(f) for f in fields}
        else:
            filtered = [{f: s.get(f) for f in fields} for s in specs]
        if file is None:
            return json.dumps(filtered, indent=indent)
        json.dump(filtered, file, indent=indent)
        return None
