import requests

# The Bedrock API Key.
api_key = "ABSKQmVkcm9ja0FQSUtleS01a3ZqLWF0LTI5ODQ4MzYxMDEyOTpGaWpmazBFRVU2ZFR4dGNnZGRTMjhyUnZHcGI5QjAwbmp0WXBWQnlKQXo4eDNlK0FIN1FuTm9HNEhYOD0="
# Available regions: us-east-2, eu-west-1, us-east1
region = "us-east-1"
# Example model IDs:
# For the US: us.anthropic.claude-3-5-haiku-20241022-v1:0
# For the EU: eu.anthropic.claude-3-sonnet-20240229-v1:0
model = "us.anthropic.claude-3-5-haiku-20241022-v1:0"



url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model}/converse"

payload = {
    "messages": [
        {
            "role": "user",
            "content": [{"text": "Hello"}]
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.request("POST", url, json=payload, headers=headers, verify=False)

print(response.text)