import unittest
from unittest.mock import patch, MagicMock
import os
import json
from log_parser_sdk.log_parser import LogParsingSDK

class TestLogParsingSDK(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.sdk = LogParsingSDK(self.api_key)
        self.test_log_file_path = "test_logs_for_sdk.txt"
        with open(self.test_log_file_path, "w") as f:
            f.write("log entry 1\n")
            f.write("log entry 2\n")

    def tearDown(self):
        if os.path.exists(self.test_log_file_path):
            os.remove(self.test_log_file_path)

    @patch("log_parser_sdk.claude_client.ClaudeClient.parse_log_with_claude")
    def test_parse_log_entry_success(self, mock_parse_log_with_claude):
        mock_parse_log_with_claude.return_value = json.dumps({"field": "value"})
        log_entry = "sample log"
        result = self.sdk.parse_log_entry(log_entry)
        self.assertEqual(result, {"field": "value"})
        mock_parse_log_with_claude.assert_called_once_with(log_entry, output_format="json")

    @patch("log_parser_sdk.claude_client.ClaudeClient.parse_log_with_claude")
    def test_parse_log_entry_claude_error(self, mock_parse_log_with_claude):
        mock_parse_log_with_claude.side_effect = Exception("Claude error")
        with patch.object(self.sdk.error_handler, "handle_error") as mock_handle_error:
            result = self.sdk.parse_log_entry("sample log")
            self.assertEqual(result, {})
            mock_handle_error.assert_called_once()

    @patch("log_parser_sdk.claude_client.ClaudeClient.parse_log_with_claude")
    def test_parse_log_file_success(self, mock_parse_log_with_claude):
        mock_parse_log_with_claude.side_effect = [json.dumps({"field": "value1"}), json.dumps({"field": "value2"})]
        result = self.sdk.parse_log_file(self.test_log_file_path)
        self.assertEqual(result, [{"field": "value1"}, {"field": "value2"}])
        self.assertEqual(mock_parse_log_with_claude.call_count, 2)

    @patch("log_parser_sdk.claude_client.ClaudeClient.parse_log_with_claude")
    def test_parse_log_file_json_decode_error(self, mock_parse_log_with_claude):
        mock_parse_log_with_claude.side_effect = ["invalid json", json.dumps({"field": "value2"})]
        with patch.object(self.sdk.error_handler, "handle_error") as mock_handle_error:
            result = self.sdk.parse_log_file(self.test_log_file_path)
            self.assertEqual(len(result), 2)
            self.assertIn("parsing_error", result[0])
            self.assertEqual(result[1], {"field": "value2"})
            mock_handle_error.assert_called_once()

    @patch("log_parser_sdk.claude_client.ClaudeClient.parse_log_with_claude")
    def test_generate_grok_pattern_success(self, mock_parse_log_with_claude):
        mock_parse_log_with_claude.return_value = "%{SYSLOGBASE}"
        log_entry = "sample log"
        result = self.sdk.generate_grok_pattern(log_entry)
        self.assertEqual(result, "%{SYSLOGBASE}")
        mock_parse_log_with_claude.assert_called_once_with(log_entry, output_format="grok")

    @patch("log_parser_sdk.claude_client.ClaudeClient.parse_log_with_claude")
    def test_generate_grok_pattern_claude_error(self, mock_parse_log_with_claude):
        mock_parse_log_with_claude.side_effect = Exception("Claude error")
        with patch.object(self.sdk.error_handler, "handle_error") as mock_handle_error:
            result = self.sdk.generate_grok_pattern("sample log")
            self.assertEqual(result, "")
            mock_handle_error.assert_called_once()

if __name__ == '__main__':
    unittest.main()


