import requests

# The Bedrock API Key.
api_key = "<Bedrock API Key>"
# Available regions: us-east-2, eu-west-1
REGION = "us-east-2"


url = f"https://bedrock-runtime.{REGION}.amazonaws.com/model/us.anthropic.claude-3-5-haiku-20241022-v1:0/converse"

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