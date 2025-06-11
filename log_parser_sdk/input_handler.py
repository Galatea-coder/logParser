import os
from scapy.all import PcapReader, Packet
import string
import json

class InputHandler:
    def read_log_file(self, file_path: str) -> list[str]:
        """
        Reads a file containing multiple log entries, one per line.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            content = f.read()
            
            potential_json_entries = []
            current_json_block = []
            brace_count = 0
            in_json_block = False

            for line in content.splitlines():
                stripped_line = line.strip()
                if not stripped_line:
                    if in_json_block and brace_count == 0 and current_json_block:
                        entry = "\n".join(current_json_block)
                        potential_json_entries.append(entry)
                        current_json_block = []
                        in_json_block = False
                    continue

                for char in stripped_line:
                    if char == '{':
                        brace_count += 1
                        in_json_block = True
                    elif char == '}':
                        brace_count -= 1
                
                current_json_block.append(stripped_line)

                if in_json_block and brace_count == 0 and current_json_block:
                    entry = "\n".join(current_json_block)
                    potential_json_entries.append(entry)
                    current_json_block = []
                    in_json_block = False
            
            if current_json_block:
                entry = "\n".join(current_json_block)
                potential_json_entries.append(entry)

            if potential_json_entries:
                return potential_json_entries
            else:
                f.seek(0) # Reset file pointer
                lines = [line.strip() for line in f if line.strip()]
                return lines

    def read_log_entry(self, log_entry: str) -> str:
        """
        Returns a single log entry string.
        """
        if not isinstance(log_entry, str):
            raise TypeError("Log entry must be a string.")
        return log_entry

    def _extract_printable_payload(self, packet: Packet) -> str:
        """
        Recursively extracts printable strings from all layers of a packet.
        """
        extracted_text = []
        for layer in packet.layers():
            if hasattr(packet[layer], 'payload') and packet[layer].payload:
                payload = bytes(packet[layer].payload)
                try:
                    decoded_payload = payload.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        decoded_payload = payload.decode('latin-1')
                    except UnicodeDecodeError:
                        decoded_payload = ''.join(filter(lambda x: x in string.printable, payload.decode('latin-1', errors='ignore')))
                
                if decoded_payload.strip():
                    extracted_text.append(decoded_payload.strip())
        return '\n'.join(extracted_text)

    def read_pcap_file(self, file_path: str, max_packets: int = None) -> list[str]:
        """
        Reads a .pcap file and extracts relevant text data from packet payloads.
        This method will attempt to decode common protocols to get text-based logs.
        Optionally, limits the number of packets read.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logs = []
        packet_count = 0
        try:
            with PcapReader(file_path) as pcap_reader:
                for packet in pcap_reader:
                    if max_packets and packet_count >= max_packets:
                        break

                    extracted_data = self._extract_printable_payload(packet)
                    if extracted_data:
                        logs.append(extracted_data)
                    
                    packet_count += 1

        except Exception as e:
            print(f"Error reading pcap file {file_path}: {e}")
        return [log for log in logs if log] # Filter out empty strings

    def read_logs_from_directory(self, directory_path: str) -> dict[str, list[str]]:
        """
        Reads all text-based log files from a given directory and returns a dictionary
        mapping file paths to lists of log entries from those files.
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")
        
        all_logs_by_file = {}
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if file.endswith(('.log', '.txt', '.json', '.csv')):
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            all_logs_by_file[file_path] = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
        return all_logs_by_file


