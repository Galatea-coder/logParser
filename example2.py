import os
import sys

# Add the SDK directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'log_parser_sdk')))

from log_parser_sdk.log_parser import LogParsingSDK

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_CLAUDE_API_KEY_HERE' with your actual Claude API key.
# It is recommended to set this as an environment variable for production use.
claude_api_key = os.environ.get("CLAUDE_API_KEY", "YOUR_CLAUDE_API_KEY_HERE")

# Define paths for test files and directories
# Note: TEST_LOG_FILE and TEST_PCAP_FILE are still dummy paths for demonstration
# You should replace them with your actual file paths if you want to test them.
TEST_LOG_FILE = "/home/dk/SDK_Parser/raw_logs.txt"  # Updated to user's specified file
TEST_PCAP_FILE = "/home/ubuntu/test_logs/sample.pcap" # Assuming this is still a dummy for PCAP
TEST_LOG_DIRECTORY = "/home/dk/SDK_Parser/raw_logs" # Updated to user's specified directory

# --- Initialize SDK ---
print("\n--- Initializing LogParsingSDK ---")
try:
    sdk = LogParsingSDK(claude_api_key)
    print("SDK initialized successfully.")
except ValueError as e:
    print(f"Error initializing SDK: {e}")
    print("Please ensure CLAUDE_API_KEY is set correctly.")
    sys.exit(1)

# --- Test Single Log Entry Parsing ---
print("\n--- Testing Single Log Entry Parsing ---")
single_log_entry = "Jun 09 17:49:30 TP-PA850-A 1,2021/10/13 12:54:53,011901019052,TRAFFIC,end,2049,2021/10/13 12:54:53,10.80.22.2,8.8.8.8,0.0.0.0,0.0.0.0,Trust to Untrust,,,dns,vsys1,Trust,Untrust,ae2,ae1,Syslog To SOC VM,2021/10/13 12:54:53,3973,1,61879,53,0,0,0x19,udp,allow,1198,103,1095,2,2021/10/13 12:54:22,0,any,0,812631294,0x0,10.0.0.0-10.255.255.255,United States,0,1,1,aged-out,0,0,0,0,,TP-PA850-A,from-policy,,,0,,0,,N/A,0,0,0,0"
parsed_single_log = sdk.parse_log_entry(single_log_entry)
if parsed_single_log:
    # Save JSON Output
    json_output = sdk.output_formatter.format_to_json(parsed_single_log)
    with open("/home/dk/SDK_Parser/output_single_log.json", "w") as f:
        f.write(json_output)
    print("Parsed Single Log (JSON) saved to /home/dk/SDK_Parser/output_single_log.json")

    # Save CSV Output
    csv_output = sdk.output_formatter.format_to_csv([parsed_single_log])
    with open("/home/dk/SDK_Parser/output_single_log.csv", "w") as f:
        f.write(csv_output)
    print("Parsed Single Log (CSV) saved to /home/dk/SDK_Parser/output_single_log.csv")
else:
    print("Failed to parse single log entry.")

# --- Test Log File Parsing ---
print("\n--- Testing Log File Parsing ---")
parsed_file_logs = sdk.parse_log_file(TEST_LOG_FILE)
if parsed_file_logs:
    # Save JSON Output
    json_output = sdk.output_formatter.format_list_to_json(parsed_file_logs)
    with open("/home/dk/SDK_Parser/output_file_logs.json", "w") as f:
        f.write(json_output)
    print(f"Parsed Logs from {TEST_LOG_FILE} (JSON) saved to /home/ubuntu/output_file_logs.json")

    # Save CSV Output
    csv_output = sdk.output_formatter.format_to_csv(parsed_file_logs)
    with open("/home/dk/SDK_Parser/output_file_logs.csv", "w") as f:
        f.write(csv_output)
    print(f"Parsed Logs from {TEST_LOG_FILE} (CSV) saved to /home/dk/SDK_Parser/output_file_logs.csv")
else:
    print(f"Failed to parse logs from file: {TEST_LOG_FILE}")

# --- Test Directory Parsing ---
print("\n--- Testing Directory Parsing ---")
# Ensure your directory '/home/dk/SDK_Parser/raw_logs' exists and contains log files.
parsed_dir_logs = sdk.parse_logs_from_directory(TEST_LOG_DIRECTORY)
if parsed_dir_logs:
    # Save JSON Output
    json_output = sdk.output_formatter.format_list_to_json(parsed_dir_logs)
    with open("/home/dk/SDK_Parser/output_dir_logs.json", "w") as f:
        f.write(json_output)
    print(f"Parsed Logs from directory {TEST_LOG_DIRECTORY} (JSON) saved to /home/ubuntu/output_dir_logs.json")

    # Save CSV Output
    csv_output = sdk.output_formatter.format_to_csv(parsed_dir_logs)
    with open("/home/dk/SDK_Parser//output_dir_logs.csv", "w") as f:
        f.write(csv_output)
    print(f"Parsed Logs from directory {TEST_LOG_DIRECTORY} (CSV) saved to /home/ubuntu/output_dir_logs.csv")
else:
    print(f"Failed to parse logs from directory: {TEST_LOG_DIRECTORY}")

# --- Test Grok Pattern Generation ---
print("\n--- Testing Grok Pattern Generation ---")
grok_pattern = sdk.generate_grok_pattern(single_log_entry)
if grok_pattern:
    print("Generated Grok Pattern:\n", grok_pattern)
else:
    print("Failed to generate Grok pattern.")

print("\n--- All tests completed ---")


