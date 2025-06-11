import unittest
from unittest.mock import patch, Mock
import requests
from log_parser_sdk.claude_client import ClaudeClient

class TestClaudeClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.client = ClaudeClient(self.api_key)

    @patch("requests.post")
    def test_send_request_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"content": [{"text": "parsed data"}]}
        mock_post.return_value = mock_response

        prompt = "test prompt"
        response = self.client.send_request(prompt)
        self.assertEqual(response, {"content": [{"text": "parsed data"}]})
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_send_request_http_error(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("HTTP Error")
        with self.assertRaises(requests.exceptions.RequestException):
            self.client.send_request("test prompt")

    @patch("requests.post")
    def test_send_request_json_decode_error(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_post.return_value = mock_response

        with self.assertRaises(json.JSONDecodeError):
            self.client.send_request("test prompt")

    @patch.object(ClaudeClient, "send_request")
    def test_parse_log_with_claude_json_format(self, mock_send_request):
        mock_send_request.return_value = {"content": [{"text": "{\"field\": \"value\"}"}]}
        log_entry = "sample log"
        result = self.client.parse_log_with_claude(log_entry, output_format="json")
        self.assertEqual(result, "{\"field\": \"value\"}")
        mock_send_request.assert_called_once()

    @patch.object(ClaudeClient, "send_request")
    def test_parse_log_with_claude_grok_format(self, mock_send_request):
        mock_send_request.return_value = {"content": [{"text": "%{SYSLOGBASE}"}]}
        log_entry = "sample log"
        result = self.client.parse_log_with_claude(log_entry, output_format="grok")
        self.assertEqual(result, "%{SYSLOGBASE}")
        mock_send_request.assert_called_once()

    def test_parse_log_with_claude_unsupported_format(self):
        with self.assertRaises(ValueError):
            self.client.parse_log_with_claude("sample log", output_format="xml")

    @patch.object(ClaudeClient, "send_request")
    def test_parse_log_with_claude_empty_response(self, mock_send_request):
        mock_send_request.return_value = {}
        log_entry = "sample log"
        result = self.client.parse_log_with_claude(log_entry, output_format="json")
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()



import json

