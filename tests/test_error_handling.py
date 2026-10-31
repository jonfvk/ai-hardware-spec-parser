import unittest
from io import StringIO
from src.ai_hardware_spec_parser.input_handler import InputHandler
from src.ai_hardware_spec_parser.memory_extractor import MemoryExtractor
from src.ai_hardware_spec_parser.performance_extractor import PerformanceExtractor
from src.ai_hardware_spec_parser.power_efficiency_extractor import PowerEfficiencyExtractor
from src.ai_hardware_spec_parser.multi_device_parser import MultiDeviceParser
from src.ai_hardware_spec_parser.exporter import SpecExporter

class TestErrorHandling(unittest.TestCase):
    def test_input_handler_invalid_type(self):
        handler = InputHandler()
        with self.assertRaises(ValueError):
            handler.accept_text(123)  # Not a string
        with self.assertRaises(ValueError):
            handler.accept_text('   ')  # Empty string

    def test_memory_extractor_handles_no_match(self):
        # Should not raise, should return None fields
        text = "No memory info here."
        extractor = MemoryExtractor(text)
        result = extractor.extract()
        self.assertIsNone(result['Memory Size'])
        self.assertIsNone(result['Memory Type'])

    def test_performance_extractor_handles_no_match(self):
        text = "No performance metrics."
        extractor = PerformanceExtractor(text)
        result = extractor.extract()
        self.assertIn('TOPS', result)
        self.assertIsNone(result['TOPS'])

    def test_power_efficiency_extractor_handles_no_match(self):
        text = "No efficiency info."
        extractor = PowerEfficiencyExtractor(text)
        result = extractor.extract()
        self.assertIn('Power Efficiency', result)
        self.assertIsNone(result['Power Efficiency'])

    def test_multi_device_parser_handles_empty_input(self):
        parser = MultiDeviceParser("")
        self.assertEqual(parser.device_count(), 0)
        self.assertEqual(parser.get_device_texts(), [])
        self.assertEqual(parser.parse_all(), [])

    def test_exporter_to_csv_invalid_fields(self):
        specs = {'TOPS': '10 TOPS', 'Memory Size': '8 GB'}
        # Field not present in dict; should not raise
        csv_str = SpecExporter.to_csv(specs, fields=['TOPS', 'Nonexistent'])
        self.assertIn('TOPS', csv_str)
        self.assertIn('Nonexistent', csv_str)

    def test_exporter_to_json_invalid_fields(self):
        specs = {'TOPS': '10 TOPS', 'Memory Size': '8 GB'}
        json_str = SpecExporter.to_json(specs, fields=['TOPS', 'Nonexistent'])
        self.assertIn('"TOPS"', json_str)
        self.assertIn('"Nonexistent"', json_str)

    def test_exporter_to_csv_file_like(self):
        specs = {'TOPS': '10 TOPS', 'Memory Size': '8 GB'}
        buf = StringIO()
        result = SpecExporter.to_csv(specs, file=buf)
        self.assertIsNone(result)
        self.assertIn('TOPS', buf.getvalue())

    def test_exporter_to_json_file_like(self):
        specs = {'TOPS': '10 TOPS', 'Memory Size': '8 GB'}
        buf = StringIO()
        result = SpecExporter.to_json(specs, file=buf)
        self.assertIsNone(result)
        self.assertIn('TOPS', buf.getvalue())

if __name__ == '__main__':
    unittest.main()
