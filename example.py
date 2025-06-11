import os
from log_parser_sdk.log_parser import LogParsingSDK
from log_parser_sdk.input_handler import InputHandler

# Replace with your actual Claude API key
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

if not CLAUDE_API_KEY:
    print("Error: CLAUDE_API_KEY environment variable not set.")
    print("Please set the CLAUDE_API_KEY environment variable before running the example.")
    exit(1)

sdk = LogParsingSDK(CLAUDE_API_KEY)
input_handler = InputHandler()

# Example: Parse a PCAP file and output to JSON and CSV
# NOTE: Replace with a real .pcap file path if you have one
pcap_file_path = "/home/ubuntu/corvil_logs/Corvil-11746-1745241938363000000-1745253638363000000.pcap"
if os.path.exists(pcap_file_path):
    print("\n--- Starting PCAP File Parsing (Very Small Subset) ---")
    # Process only the first 5 packets for testing
    parsed_pcap_logs = sdk.parse_pcap_file(pcap_file_path, max_packets=5)
    print("\n--- Finished PCAP File Parsing (Very Small Subset) ---")

    print("\n--- PCAP Logs (JSON) ---")
    print(sdk.output_formatter.format_list_to_json(parsed_pcap_logs))

    print("\n--- PCAP Logs (CSV) ---")
    csv_output = sdk.format_to_csv(parsed_pcap_logs)
    print(csv_output)
else:
    print(f"\nPCAP file not found at {pcap_file_path}. Skipping PCAP example.")

# Example 1: Parse a single log entry
single_log_entry = "Jun 09 17:49:30 TP-PA850-A 1,2021/10/13 12:54:53,011901019052,TRAFFIC,end,2049,2021/10/13 12:54:53,10.80.22.2,8.8.8.8,0.0.0.0,0.0.0.0,Trust to Untrust,,,dns,vsys1,Trust,Untrust,ae2,ae1,Syslog To SOC VM,2021/10/13 12:54:53,3973,1,61879,53,0,0,0x19,udp,allow,1198,103,1095,2,2021/10/13 12:54:22,0,any,0,812631294,0x0,10.0.0.0-10.255.255.255,United States,0,1,1,aged-out,0,0,0,0,,TP-PA850-A,from-policy,,,0,,0,,N/A,0,0,0,0"

print("\n--- Parsing Single Log Entry ---")
parsed_single_log = sdk.parse_log_entry(single_log_entry)
print(sdk.output_formatter.format_to_json(parsed_single_log))

# Example 2: Generate Grok pattern for a single log entry
print("\n--- Generating Grok Pattern ---")
grok_pattern = sdk.generate_grok_pattern(single_log_entry)
print(grok_pattern)

# Example 3: Parse log entries from a file
# Create a dummy log file for demonstration
dummy_log_file_content = """
Jun 09 17:49:30 TP-PA850-A 1,2021/10/13 12:54:53,011901019052,TRAFFIC,end,2049,2021/10/13 12:54:53,10.80.22.2,8.8.8.8,0.0.0.0,0.0.0.0,Trust to Untrust,,,dns,vsys1,Trust,Untrust,ae2,ae1,Syslog To SOC VM,2021/10/13 12:54:53,3973,1,61879,53,0,0,0x19,udp,allow,1198,103,1095,2,2021/10/13 12:54:22,0,any,0,812631294,0x0,10.0.0.0-10.255.255.255,United States,0,1,1,aged-out,0,0,0,0,,TP-PA850-A,from-policy,,,0,,0,,N/A,0,0,0,0
Jun 09 17:49:31 TP-PA850-B 2,2021/10/13 12:54:54,011901019053,TRAFFIC,start,2050,2021/10/13 12:54:54,10.80.22.3,8.8.4.4,0.0.0.0,0.0.0.0,Untrust to Trust,,,http,vsys1,Untrust,Trust,ae3,ae4,Web Server Access,2021/10/13 12:54:54,4000,1,61880,80,0,0,0x20,tcp,deny,1200,100,1100,3,2021/10/13 12:54:23,0,any,0,812631295,0x0,10.0.0.0-10.255.255.255,Canada,0,1,1,active,0,0,0,0,,TP-PA850-B,to-zone,,,0,,0,,N/A,0,0,0,0
"""
dummy_log_file_path = "/home/dk/SDK_Parser/raw logs.txt"
with open(dummy_log_file_path, "w") as f:
    f.write(dummy_log_file_content)

print("\n--- Parsing Log File ---")
parsed_file_logs = sdk.parse_log_file(dummy_log_file_path)
print(sdk.output_formatter.format_list_to_json(parsed_file_logs))

# Example 5: Parse logs from a directory and output to JSON and CSV
dummy_log_dir = "/home/dk/SDK_Parser/raw_logs"
os.makedirs(dummy_log_dir, exist_ok=True)
with open(os.path.join(dummy_log_dir, "log1.txt"), "w") as f:
    f.write("Jun 09 17:49:32 TP-PA850-C 3,2021/10/13 12:54:55,011901019054,TRAFFIC,end,2051,2021/10/13 12:54:55,10.80.22.4,8.8.8.8,0.0.0.0,0.0.0.0,Trust to Untrust,,,ftp,vsys1,Trust,Untrust,ae5,ae6,Syslog To SOC VM,2021/10/13 12:54:55,3974,1,61881,21,0,0,0x19,tcp,allow,1200,100,1100,2,2021/10/13 12:54:24,0,any,0,812631296,0x0,10.0.0.0-10.255.255.255,United States,0,1,1,aged-out,0,0,0,0,,TP-PA850-C,from-policy,,,0,,0,,N/A,0,0,0,0\n")
with open(os.path.join(dummy_log_dir, "log2.txt"), "w") as f:
    f.write("Jun 09 17:49:33 TP-PA850-D 4,2021/10/13 12:54:56,011901019055,TRAFFIC,start,2052,2021/10/13 12:54:56,10.80.22.5,8.8.4.4,0.0.0.0,0.0.0.0,Untrust to Trust,,,ssh,vsys1,Untrust,Trust,ae7,ae8,Web Server Access,2021/10/13 12:54:56,4001,1,61882,22,0,0,0x20,tcp,deny,1200,100,1100,3,2021/10/13 12:54:25,0,any,0,812631297,0x0,10.0.0.0-10.255.255.255,Canada,0,1,1,active,0,0,0,0,,TP-PA850-D,to-zone,,,0,,0,,N/A,0,0,0,0\n")

print("\n--- Parsing Logs from Directory ---")
parsed_dir_logs = sdk.parse_logs_from_directory(dummy_log_dir)
print("\n--- Directory Logs (JSON) ---")
print(sdk.output_formatter.format_list_to_json(parsed_dir_logs))

print("\n--- Directory Logs (CSV) ---")
csv_output_dir = sdk.format_to_csv(parsed_dir_logs)
print(csv_output_dir)

# Clean up dummy log file and directory
os.remove(dummy_log_file_path)
os.remove(os.path.join(dummy_log_dir, "log1.txt"))
os.remove(os.path.join(dummy_log_dir, "log2.txt"))
os.rmdir(dummy_log_dir)


