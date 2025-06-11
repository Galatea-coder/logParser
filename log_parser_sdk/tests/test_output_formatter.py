import unittest
import json
from log_parser_sdk.output_formatter import OutputFormatter

class TestOutputFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = OutputFormatter()

    def test_format_to_json(self):
        data = {"key": "value", "number": 123}
        expected_json = json.dumps(data, indent=2)
        self.assertEqual(self.formatter.format_to_json(data), expected_json)

    def test_format_list_to_json(self):
        data_list = [{"key1": "value1"}, {"key2": 123}]
        expected_json = json.dumps(data_list, indent=2)
        self.assertEqual(self.formatter.format_list_to_json(data_list), expected_json)

    def test_format_to_json_empty(self):
        data = {}
        expected_json = json.dumps(data, indent=2)
        self.assertEqual(self.formatter.format_to_json(data), expected_json)

    def test_format_list_to_json_empty(self):
        data_list = []
        expected_json = json.dumps(data_list, indent=2)
        self.assertEqual(self.formatter.format_list_to_json(data_list), expected_json)

if __name__ == '__main__':
    unittest.main()


