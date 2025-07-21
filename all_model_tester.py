import requests
import json
import math

# The OpenAI API Key
api_key = "<your key>"
# OpenAI API base URL
url = "<your url>"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def generate_response(selected_model_id):
    completions_url = f"{url}/chat/completions"
    payload = {
        "model": selected_model_id,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the Battle of Austerlitz in one sentence."}
        ],
        "max_tokens": 300,
        "temperature": 0.0,
    }
    # Make the text generation request
    completion_response = requests.post(completions_url, headers=headers, json=payload)
    # Print the completion response
    if completion_response.status_code == 200:
        completion_data = json.loads(completion_response.text)
        if "choices" in completion_data and len(completion_data["choices"]) > 0:
            generated_text = completion_data["choices"][0]["message"]["content"]
            print(f"\n{selected_model_id} in {math.ceil(completion_response.elapsed.total_seconds()*1000)} ms: :")
            print(generated_text)
    else:
        print(f"Error with text generation request for {selected_model_id}:")
        print(completion_response.text)


# Make a request to get the list of available models
response = requests.get(f"{url}/models", headers=headers)

# Print the response status
print(f"Status Code: {response.status_code}")

# Parse the JSON response
models_data = json.loads(response.text)
for model in models_data["data"]:
    print(model["id"])

# Search for a model with "llama3-2-11b-instruct" in its ID
if "data" in models_data:
    for model in models_data["data"]:
        generate_response(model["id"])


