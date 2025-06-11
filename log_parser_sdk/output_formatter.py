import json
import csv
from io import StringIO

class OutputFormatter:
    def format_to_json(self, data: dict) -> str:
        """
        Formats a dictionary into a JSON string.
        """
        return json.dumps(data, indent=2)

    def format_list_to_json(self, data_list: list[dict]) -> str:
        """
        Formats a list of dictionaries into a JSON string.
        """
        return json.dumps(data_list, indent=2)

    def format_to_csv(self, data_list: list[dict], output_file: str = None) -> str | None:
        """
        Formats a list of dictionaries (parsed JSON) into CSV format.
        Handles flattening of nested dictionaries.
        """
        if not data_list:
            return "" if output_file is None else None

        # Collect all unique keys from all dictionaries to use as CSV headers
        all_keys = set()
        for item in data_list:
            for key, value in item.items():
                if isinstance(value, dict):
                    # Flatten nested dictionaries
                    for sub_key in value.keys():
                        all_keys.add(f"{key}_{sub_key}")
                else:
                    all_keys.add(key)
        
        fieldnames = sorted(list(all_keys))

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()
        for item in data_list:
            row = {}
            for key, value in item.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        row[f"{key}_{sub_key}"] = sub_value
                else:
                    row[key] = value
            writer.writerow(row)

        if output_file:
            with open(output_file, 'w', newline='') as f:
                f.write(output.getvalue())
            return None
        else:
            return output.getvalue()


