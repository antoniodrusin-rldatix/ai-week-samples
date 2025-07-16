import os
import boto3

# The Bedrock API Key.
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "<Bedrock API Key>"
# Available regions: us-east-2, eu-west-1
REGION = "us-east-2"

client = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

# Define the model and message
model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
messages = [{"role": "user", "content": [{"text": "Hello! Can you tell me about Amazon Bedrock?"}]}]

# Make the API call
response = client.converse(
    modelId=model_id,
    messages=messages,
)

# Print the response
print(response['output']['message']['content'][0]['text'])