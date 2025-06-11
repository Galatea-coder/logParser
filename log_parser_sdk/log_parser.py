from .input_handler import InputHandler
from .claude_client import ClaudeClient
from .output_formatter import OutputFormatter
from .error_handler import ErrorHandler
import json
import os

class LogParsingSDK:
    def __init__(self, claude_api_key):
        self.input_handler = InputHandler()
        self.claude_client = ClaudeClient(claude_api_key)
        self.output_formatter = OutputFormatter()
        self.error_handler = ErrorHandler()

    def _is_json(self, text):
        try:
            json.loads(text)
            return True
        except ValueError:
            return False

    def parse_log_entry(self, log_entry):
        try:
            if self._is_json(log_entry):
                parsed_data = json.loads(log_entry)
            else:
                parsed_data_str = self.claude_client.parse_log_with_claude(log_entry)
                if not parsed_data_str.strip().startswith(("{", "[")):
                    parsed_data_str = json.dumps({"raw_output": parsed_data_str})
                parsed_data = json.loads(parsed_data_str)
            return parsed_data
        except Exception as e:
            self.error_handler.handle_error(e, f"Error parsing single log entry: {log_entry}")

    def parse_log_file(self, file_path):
        parsed_results = []
        try:
            log_entries = self.input_handler.read_log_file(file_path)
            for entry in log_entries:
                try:
                    if self._is_json(entry):
                        parsed_results.append(json.loads(entry))
                    else:
                        parsed_data_str = self.claude_client.parse_log_with_claude(entry)
                        
                        if not parsed_data_str.strip().startswith(("{", "[")):
                            parsed_data_str = json.dumps({"raw_output": parsed_data_str})

                        parsed_results.append(json.loads(parsed_data_str))
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError for entry: {entry}")
                    print(f"Problematic string: {parsed_data_str}")
                    self.error_handler.handle_error(e, f"Error decoding JSON for entry: {entry}")
                except Exception as e:
                    self.error_handler.handle_error(e, f"Error parsing log entry from file: {entry}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error processing log file: {file_path}")
        return parsed_results

    def parse_logs_from_directory(self, directory_path):
        parsed_results = []
        try:
            print(f"[DEBUG] LogParsingSDK: Starting directory parsing for: {directory_path}")
            log_entries_map = self.input_handler.read_logs_from_directory(directory_path)
            print(f"[DEBUG] LogParsingSDK: InputHandler returned {len(log_entries_map)} files for directory parsing.")
            for file_path, entries in log_entries_map.items():
                print(f"[DEBUG] LogParsingSDK: Processing file: {file_path} with {len(entries)} entries.")
                for i, entry in enumerate(entries):
                    print(f"[DEBUG] LogParsingSDK: Processing entry {i+1}/{len(entries)} from {file_path}: {entry[:100]}...")
                    try:
                        if self._is_json(entry):
                            parsed_results.append(json.loads(entry))
                            print(f"[DEBUG] LogParsingSDK: Parsed pre-formatted JSON for entry {i+1} from {file_path}.")
                        else:
                            print(f"[DEBUG] LogParsingSDK: Sending entry {i+1} from {file_path} to Claude for parsing.")
                            parsed_data_str = self.claude_client.parse_log_with_claude(entry)
                            print(f"[DEBUG] LogParsingSDK: Received from Claude for entry {i+1} from {file_path}: {parsed_data_str[:100]}...")
                            if not parsed_data_str.strip().startswith(("{", "[")):
                                parsed_data_str = json.dumps({"raw_output": parsed_data_str})

                            parsed_results.append(json.loads(parsed_data_str))
                            print(f"[DEBUG] LogParsingSDK: Successfully parsed Claude output for entry {i+1} from {file_path}.")
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError for entry: {entry}")
                        print(f"Problematic string: {parsed_data_str}")
                        self.error_handler.handle_error(e, f"Error decoding JSON for entry from file {file_path}: {entry}")
                    except Exception as e:
                        self.error_handler.handle_error(e, f"Error parsing log entry from directory {file_path}: {entry}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error processing directory: {directory_path}")
        return parsed_results

    def parse_pcap_file(self, file_path, max_packets=None):
        parsed_results = []
        try:
            pcap_data = self.input_handler.read_pcap_file(file_path, max_packets)
            for entry in pcap_data:
                try:
                    if self._is_json(entry):
                        parsed_results.append(json.loads(entry))
                    else:
                        parsed_data_str = self.claude_client.parse_log_with_claude(entry)
                        if not parsed_data_str.strip().startswith(("{", "[")):
                            parsed_data_str = json.dumps({"raw_output": parsed_data_str})

                        parsed_results.append(json.loads(parsed_data_str))
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError for PCAP entry: {entry}")
                    print(f"Problematic string: {parsed_data_str}")
                    self.error_handler.handle_error(e, f"Error decoding JSON for PCAP entry: {entry}")
                except Exception as e:
                    self.error_handler.handle_error(e, f"Error parsing PCAP entry: {entry}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error processing PCAP file: {file_path}")
        return parsed_results

    def generate_grok_pattern(self, log_entry):
        try:
            grok_pattern = self.claude_client.generate_grok_pattern_with_claude(log_entry)
            return grok_pattern
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating Grok pattern for log entry: {log_entry}")

    def format_to_csv(self, parsed_data):
        try:
            return self.output_formatter.format_to_csv(parsed_data)
        except Exception as e:
            self.error_handler.handle_error(e, f"Error formatting data to CSV: {e}")


