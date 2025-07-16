import requests
import os

api_key = "<Bedrock API Key>"
url = "https://bedrock-runtime.us-east-2.amazonaws.com/model/us.anthropic.claude-3-5-haiku-20241022-v1:0/converse"

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