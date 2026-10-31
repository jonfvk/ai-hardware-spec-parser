# AI Hardware Spec Parser

Parse and summarize AI hardware specifications from plain text, helping developers quickly extract key device capabilities for offline reference.

## Project Motivation
AI developers often need to compare hardware specs, but device documentation is unstructured and hard to scan for key metrics. This tool parses pasted hardware spec text and extracts metrics like TOPS, memory, and efficiency into a structured summary.

## Features
- Accepts plain text hardware specs as input
- Extracts AI performance metrics (e.g., TOPS)
- Extracts memory size and type
- Extracts power efficiency details
- Summarizes extracted specs in a table
- Highlights missing or ambiguous data
- Supports multiple device entries in a single input
- Allows export to CSV or JSON
- Basic error handling for invalid or incomplete input

## Installation
This tool is pure Python and requires Python 3.7+.

Clone the repository and ensure `src/` is on your `PYTHONPATH`:

```
export PYTHONPATH=$PWD/src
```

No external dependencies are required.

## Usage

### 1. Parsing a Single Device Spec
```python
from ai_hardware_spec_parser.input_handler import InputHandler
from ai_hardware_spec_parser.performance_extractor import PerformanceExtractor
from ai_hardware_spec_parser.memory_extractor import MemoryExtractor
from ai_hardware_spec_parser.power_efficiency_extractor import PowerEfficiencyExtractor
from ai_hardware_spec_parser.spec_table import SpecTable
from ai_hardware_spec_parser.highlight_missing import MissingDataHighlighter

# Example hardware spec text
spec_text = """
NVIDIA Jetson Orin Nano
AI Performance: up to 40 TOPS
Memory: 8GB LPDDR5
Power Efficiency: 1.2 TOPS/W
"""

# Accept input
handler = InputHandler()
handler.accept_text(spec_text)
text = handler.get_text()

# Extract fields
perf = PerformanceExtractor(text).extract()
mem = MemoryExtractor(text).extract()
eff = PowerEfficiencyExtractor(text).extract()

# Merge and display
spec = SpecTable.merge_dicts(perf, mem, eff)
table = SpecTable(spec).as_table()
print(table)

# Highlight missing/ambiguous fields
highlighter = MissingDataHighlighter(spec)
print(highlighter.highlight())
```

**Output:**
```
TOPS | Memory Size | Memory Type | Power Efficiency
-----+-------------+------------+-----------------
40 TOPS | 8 GB        | LPDDR5     | 1.2 TOPS/W      
{'TOPS': 'OK', 'Memory Size': 'OK', 'Memory Type': 'OK', 'Power Efficiency': 'OK'}
```

### 2. Parsing Multiple Devices
```python
from ai_hardware_spec_parser.multi_device_parser import MultiDeviceParser
from ai_hardware_spec_parser.spec_table import SpecTable

multi_text = """
NVIDIA Jetson Orin Nano
AI Performance: up to 40 TOPS
Memory: 8GB LPDDR5
Power Efficiency: 1.2 TOPS/W

---

Coral Edge TPU
AI Performance: 4 TOPS
Memory: 1GB LPDDR4
Power Efficiency: 2 TOPS/W
"""

parser = MultiDeviceParser(multi_text)
results = parser.parse_all()
for i, spec in enumerate(results):
    print(f"Device {i+1}:")
    print(SpecTable(spec).as_table())
```

**Output:**
```
Device 1:
TOPS | Memory Size | Memory Type | Power Efficiency
-----+-------------+------------+-----------------
40 TOPS | 8 GB        | LPDDR5     | 1.2 TOPS/W      
Device 2:
TOPS | Memory Size | Memory Type | Power Efficiency
-----+-------------+------------+-----------------
4 TOPS  | 1 GB        | LPDDR4     | 2 TOPS/W        
```

### 3. Exporting to CSV or JSON
```python
from ai_hardware_spec_parser.exporter import SpecExporter

# Export single device
csv_str = SpecExporter.to_csv(results[0])
print(csv_str)

# Export all devices to JSON
json_str = SpecExporter.to_json(results)
print(json_str)
```

**Output:**
```
TOPS,Memory Size,Memory Type,Power Efficiency
40 TOPS,8 GB,LPDDR5,1.2 TOPS/W

[
  {
    "TOPS": "40 TOPS",
    "Memory Size": "8 GB",
    "Memory Type": "LPDDR5",
    "Power Efficiency": "1.2 TOPS/W"
  },
  {
    "TOPS": "4 TOPS",
    "Memory Size": "1 GB",
    "Memory Type": "LPDDR4",
    "Power Efficiency": "2 TOPS/W"
  }
]
```

### 4. Handling Missing or Ambiguous Data
If a field is missing or ambiguous (e.g., contains "unknown", "approx", "?"), the highlighter will flag it:

```python
spec_text = "AI Performance: approx 10 TOPS\nMemory: unknown\n"
perf = PerformanceExtractor(spec_text).extract()
mem = MemoryExtractor(spec_text).extract()
eff = PowerEfficiencyExtractor(spec_text).extract()
spec = SpecTable.merge_dicts(perf, mem, eff)
highlighter = MissingDataHighlighter(spec)
print(highlighter.highlight())
```

**Output:**
```
{'TOPS': 'AMBIGUOUS', 'Memory Size': 'MISSING', 'Memory Type': 'MISSING', 'Power Efficiency': 'MISSING'}
```

## Error Handling
- Non-string or empty input raises `ValueError` in `InputHandler`.
- Extraction modules return `None` for missing fields.
- Exporters handle missing fields gracefully.

## Source URLs
- https://techgig.com/news/ai/nvidia-unveils-jetson-orin-nano-2-for-edge-ai-robotics/134930001 (retrieved 2024-06)

## License
MIT License
