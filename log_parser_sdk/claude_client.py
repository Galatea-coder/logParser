import os
import requests
import json
import re
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class ClaudeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        self.timeout = 60  # seconds

    def _extract_json_from_response(self, text):
        # First, try to find JSON within a markdown code block (```json ... ```)
        match = re.search(r"```json\n(.*?)```", text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            try:
                # Validate if the extracted string is indeed valid JSON
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                # If it's not valid JSON even within the block, fall through to broader search
                pass

        # If no markdown block, or if content within block was invalid, try to find a standalone JSON object/array
        stack = []
        json_start = -1
        json_end = -1

        for i, char in enumerate(text):
            if char == '{' or char == '[':
                if json_start == -1:
                    json_start = i
                stack.append(char)
            elif char == '}' or char == ']':
                if stack:
                    last_open = stack.pop()
                    if (char == '}' and last_open != '{') or (char == ']' and last_open != '['):
                        stack = [] # Reset stack to avoid further issues
                        json_start = -1 # Reset start
                        continue
                elif json_start != -1: # If we started a JSON, but this is an unmatched closing brace/bracket
                    pass
            
            if json_start != -1 and not stack and (char == '}' or char == ']'):
                json_end = i + 1
                break
        
        if json_start != -1 and json_end != -1:
            extracted_text = text[json_start:json_end]
            try:
                json.loads(extracted_text) # Final validation
                return extracted_text
            except json.JSONDecodeError:
                pass

        print(f"Warning: Could not extract clean JSON. Returning empty object. Raw: {text[:200]}...")
        return "{}"

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=20),
        retry=retry_if_exception_type((requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError))
    )
    def _make_request(self, prompt, max_tokens=1000, temperature=0.7):
        if not self.api_key:
            raise ValueError("Claude API key is not set. Please set the CLAUDE_API_KEY environment variable.")

        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            response_data = response.json()
            
            if "content" in response_data and len(response_data["content"]) > 0:
                claude_output = response_data["content"][0]["text"]
                json_output = self._extract_json_from_response(claude_output)
                return json_output
            else:
                print("Warning: Claude API response content is empty.")
                return "{}"
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429: # Too Many Requests
                print("Rate limit hit. Retrying...")
            raise
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}. Retrying...")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}. Retrying...")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error from Claude API response: {e}")
            print(f"Raw response text: {response.text if 'response' in locals() else 'No response object'}")
            raise

    def parse_log_with_claude(self, log_entry):
        prompt = f"""You are a security log parsing assistant. Your task is to parse the following raw security log entry into a structured JSON object. Extract all relevant fields and their values. If a field is not explicitly present, you can infer it if possible, or omit it. Ensure the output is a valid JSON object, and do not include any conversational text outside the JSON. If you cannot parse it, return an empty JSON object {{}}.

Raw Log Entry:
{log_entry}

JSON Output:"""
        return self._make_request(prompt)

    def generate_grok_pattern_with_claude(self, log_entry):
        prompt = f"""You are a security log parsing assistant. Your task is to generate a Grok pattern for the following raw security log entry. Provide only the Grok pattern string, without any additional text or explanations.

Raw Log Entry:
{log_entry}

Grok Pattern:"""
        return self._make_request(prompt)


