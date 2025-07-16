import os
import boto3
import json

# The Bedrock API Key.
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "<your bedrock api key>"
# Available regions: us-east-2, eu-west-1
REGION = "us-east-2"

# Create Bedrock clients
bedrock_client = boto3.client(
    service_name="bedrock",
    region_name=REGION
)

bedrock_runtime_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

def list_all_models():
    """List all available models in Amazon Bedrock"""
    print("Available Bedrock Models:")
    print("-" * 50)

    # Get list of foundation models
    response = bedrock_client.list_foundation_models()

    # Print model details
    for model in response["modelSummaries"]:
        print(f"Model ID: {model['modelId']}")
        print(f"Model Name: {model['modelName']}")
        print(f"Provider: {model['providerName']}")
        print("-" * 50)

    return response["modelSummaries"]

def query_claude_3_7(prompt):
    """Make a request to Claude 3.7 Sonnet"""
    print("\nQuerying Claude 3.7 Sonnet...")

    model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    messages = [{"role": "user", "content": [{"text": prompt}]}]

    response = bedrock_runtime_client.converse(
        modelId=model_id,
        messages=messages,
    )

    print("\nClaude 3.7 Sonnet Response:")
    print("-" * 50)
    print(response['output']['message']['content'][0]['text'])
    print("-" * 50)

def query_nova_pro(prompt):
    """Make a request to Cohere Nova Pro"""
    print("\nQuerying Cohere Nova Pro...")

    model_id = "us.amazon.nova-pro-v1:0"  # Nova Pro model ID

    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    response = bedrock_runtime_client.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    print("\nCohere Nova Pro Response:")
    print("-" * 50)
    print(response["output"]["message"]["content"][0]["text"])
    print("-" * 50)

def query_deepseek_r1(prompt):
    """Make a request to DeepSeek-R1"""
    print("\nQuerying DeepSeek-R1...")

    model_id = "us.deepseek.r1-v1:0"  # DeepSeek-R1 model ID

    body = json.dumps({
        "prompt": prompt,
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 500
    })

    response = bedrock_runtime_client.invoke_model(
        modelId=model_id,
        body=body
    )

    response_body = json.loads(response["body"].read())

    print("\nDeepSeek-R1 Response:")
    print("-" * 50)
    # Updated to use the correct response structure
    print(response_body["choices"][0]["text"])
    print("-" * 50)

if __name__ == "__main__":
    # List all available models
    models = list_all_models()

    # Test prompt for all models
    test_prompt = "What are the key differences between Python and JavaScript? List 3 main differences."

    # Make requests to specific models
    query_nova_pro(test_prompt)
    query_claude_3_7(test_prompt)
    query_deepseek_r1(test_prompt)
