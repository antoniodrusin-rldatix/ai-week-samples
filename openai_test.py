import requests
import json

# The OpenAI API Key
api_key = "<Your API Key>"
# OpenAI API base URL
url = "<your region's url>"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make a request to get the list of available models
response = requests.get(f"{url}/models", headers=headers)

# Print the response status
print(f"Status Code: {response.status_code}")

# Parse the JSON response
models_data = json.loads(response.text)

# Search for a model with "llama3-2-11b-instruct" in its ID
llama_model_id = None
if "data" in models_data:
    for model in models_data["data"]:
        if "llama3-2-11b-instruct" in model["id"]:
            llama_model_id = model["id"]
            print(f"Found matching model: {llama_model_id}")
            break

# If a matching model is found, make a text generation request
if llama_model_id:
    # Define the completion endpoint and payload
    completions_url = f"{url}/chat/completions"
    payload = {
        "model": llama_model_id,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a short story about artificial intelligence."}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    # Make the text generation request
    completion_response = requests.post(completions_url, headers=headers, json=payload)

    # Print the completion response
    print("\nText Generation Response:")
    print(f"Status Code: {completion_response.status_code}")

    if completion_response.status_code == 200:
        completion_data = json.loads(completion_response.text)
        if "choices" in completion_data and len(completion_data["choices"]) > 0:
            generated_text = completion_data["choices"][0]["message"]["content"]
            print("\nGenerated Text:")
            print(generated_text)
    else:
        print("Error with text generation request:")
        print(completion_response.text)
else:
    print("No model containing 'llama3-2-11b-instruct' found in the response.")
