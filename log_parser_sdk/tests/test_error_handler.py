import unittest
from unittest.mock import patch
from log_parser_sdk.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.error_handler = ErrorHandler()

    @patch("builtins.print")
    def test_handle_error(self, mock_print):
        with self.assertRaises(ValueError):
            self.error_handler.handle_error(ValueError("Test error"), "Custom message")
        mock_print.assert_called_with("Error: Custom message: Test error")

    @patch("builtins.print")
    def test_handle_error_no_custom_message(self, mock_print):
        with self.assertRaises(TypeError):
            self.error_handler.handle_error(TypeError("Another error"))
        mock_print.assert_called_with("Error: An error occurred: Another error")

if __name__ == '__main__':
    unittest.main()


