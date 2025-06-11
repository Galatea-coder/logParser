import unittest
import os
from log_parser_sdk.input_handler import InputHandler

class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.input_handler = InputHandler()
        self.test_file_path = "test_logs.txt"
        with open(self.test_file_path, "w") as f:
            f.write("log entry 1\n")
            f.write("log entry 2\n")
            f.write("\n") # Empty line
            f.write("log entry 3\n")

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_read_log_file(self):
        logs = self.input_handler.read_log_file(self.test_file_path)
        self.assertEqual(logs, ["log entry 1", "log entry 2", "log entry 3"])

    def test_read_log_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.input_handler.read_log_file("non_existent_file.txt")

    def test_read_log_entry(self):
        log_entry = "This is a single log entry."
        result = self.input_handler.read_log_entry(log_entry)
        self.assertEqual(result, log_entry)

    def test_read_log_entry_type_error(self):
        with self.assertRaises(TypeError):
            self.input_handler.read_log_entry(123)

if __name__ == '__main__':
    unittest.main()


