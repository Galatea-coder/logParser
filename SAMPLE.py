from log_parser_sdk.log_parser import LogParsingSDK
import os

api_key = os.environ.get("CLAUDE_API_KEY")
sdk = LogParsingSDK(api_key)
file_path ="/home/ubuntu/raw logs.txt"
parsed_logs = sdk.parse_log_file(file_path)

# Save JSON Output to file
json_output = sdk.output_formatter.format_list_to_json(parsed_logs)
with open("/home/ubuntu/output.json", "w") as f:
    f.write(json_output)
print("JSON output saved to /home/ubuntu/output.json")

# Save CSV Output to file
csv_output = sdk.format_to_csv(parsed_logs)
with open("/home/ubuntu/output.csv", "w") as f:
    f.write(csv_output)
print("CSV output saved to /home/ubuntu/output.csv")


