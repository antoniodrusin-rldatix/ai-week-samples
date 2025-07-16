# Sample Usage

This repository contains sample Python scripts for testing Bedrock and OpenAI API functionality.

- `openai_test.py`: Test script for OpenAI API integration. Searches for Llama models and demonstrates text generation.

- `bedrock_test.py`: Main test script for Bedrock.
- `bedrock_test_http.py`: HTTP-based test script for Bedrock.
- `openai_test.py`: Test script for OpenAI API integration. Searches for Llama models and demonstrates text generation.
- `bedrock_models.py`: An example on calling three different models. Note that each model has its own API and parameters, so you need to adjust the code accordingly.

## Setup

Before running the scripts, open each file and set the API key variable to the key that was shared in the chat. Update the relevant variable directly in `bedrock_test.py`, `bedrock_test_http.py`, and `openai_test.py`.


Run the scripts using Python:

Before running the scripts, open each file and set the API key variable to the key that was shared in the chat. Update the relevant variable directly in `bedrock_test.py`, `bedrock_test_http.py`, and `openai_test.py`.
```
python bedrock_test.py
python bedrock_test_http.py
python openai_test.py
```

# Note on inference profiles.
When using a model id for bedrock (using the bedrock apis), you should specify a profile id instead of the model id, for certain models.
The profile id is not listed when querying the models, so you need to use the following table to find the profile id for the model you want to use.

You can use the bedrock_list_inference_profiles.py script to list the inference profiles available in your region.

# Inference Profiles USA

| Name                             | Profile ID                                   | ARN                                                                                                   |
|:---------------------------------|:---------------------------------------------|:------------------------------------------------------------------------------------------------------|
| US Anthropic Claude 3 Haiku      | us.anthropic.claude-3-haiku-20240307-v1:0    | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0    |
| US Meta Llama 3.2 1B Instruct    | us.meta.llama3-2-1b-instruct-v1:0            | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-2-1b-instruct-v1:0            |
| US Meta Llama 3.2 11B Instruct   | us.meta.llama3-2-11b-instruct-v1:0           | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-2-11b-instruct-v1:0           |
| US Meta Llama 3.2 3B Instruct    | us.meta.llama3-2-3b-instruct-v1:0            | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-2-3b-instruct-v1:0            |
| US Meta Llama 3.2 90B Instruct   | us.meta.llama3-2-90b-instruct-v1:0           | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-2-90b-instruct-v1:0           |
| US Meta Llama 3.1 8B Instruct    | us.meta.llama3-1-8b-instruct-v1:0            | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-1-8b-instruct-v1:0            |
| US Meta Llama 3.1 70B Instruct   | us.meta.llama3-1-70b-instruct-v1:0           | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-1-70b-instruct-v1:0           |
| US Nova Micro                    | us.amazon.nova-micro-v1:0                    | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.amazon.nova-micro-v1:0                    |
| US Nova Lite                     | us.amazon.nova-lite-v1:0                     | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.amazon.nova-lite-v1:0                     |
| US Nova Pro                      | us.amazon.nova-pro-v1:0                      | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.amazon.nova-pro-v1:0                      |
| US Anthropic Claude 3.5 Haiku    | us.anthropic.claude-3-5-haiku-20241022-v1:0  | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0  |
| US Meta Llama 3.1 Instruct 405B  | us.meta.llama3-1-405b-instruct-v1:0          | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-1-405b-instruct-v1:0          |
| US Meta Llama 3.3 70B Instruct   | us.meta.llama3-3-70b-instruct-v1:0           | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama3-3-70b-instruct-v1:0           |
| US Anthropic Claude 3.5 Sonnet   | us.anthropic.claude-3-5-sonnet-20240620-v1:0 | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-3-5-sonnet-20240620-v1:0 |
| US Claude 3.5 Sonnet v2          | us.anthropic.claude-3-5-sonnet-20241022-v2:0 | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0 |
| US DeepSeek-R1                   | us.deepseek.r1-v1:0                          | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.deepseek.r1-v1:0                          |
| US Mistral Pixtral Large 25.02   | us.mistral.pixtral-large-2502-v1:0           | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.mistral.pixtral-large-2502-v1:0           |
| US Llama 4 Scout 17B Instruct    | us.meta.llama4-scout-17b-instruct-v1:0       | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama4-scout-17b-instruct-v1:0       |
| US Llama 4 Maverick 17B Instruct | us.meta.llama4-maverick-17b-instruct-v1:0    | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.meta.llama4-maverick-17b-instruct-v1:0    |
| US Nova Premier                  | us.amazon.nova-premier-v1:0                  | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.amazon.nova-premier-v1:0                  |
| US Claude Opus 4                 | us.anthropic.claude-opus-4-20250514-v1:0     | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-opus-4-20250514-v1:0     |
| US Claude Sonnet 4               | us.anthropic.claude-sonnet-4-20250514-v1:0   | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0   |
| US Anthropic Claude 3.7 Sonnet   | us.anthropic.claude-3-7-sonnet-20250219-v1:0 | arn:aws:bedrock:us-east-2:298483610129:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0 |

# Inference Profiles EU

| Name                           | Profile ID                                   | ARN                                                                                                   |
|:-------------------------------|:---------------------------------------------|:------------------------------------------------------------------------------------------------------|
| EU Anthropic Claude 3 Sonnet   | eu.anthropic.claude-3-sonnet-20240229-v1:0   | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.anthropic.claude-3-sonnet-20240229-v1:0   |
| EU Anthropic Claude 3 Haiku    | eu.anthropic.claude-3-haiku-20240307-v1:0    | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.anthropic.claude-3-haiku-20240307-v1:0    |
| EU Anthropic Claude 3.5 Sonnet | eu.anthropic.claude-3-5-sonnet-20240620-v1:0 | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.anthropic.claude-3-5-sonnet-20240620-v1:0 |
| EU Meta Llama 3.2 3B Instruct  | eu.meta.llama3-2-3b-instruct-v1:0            | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.meta.llama3-2-3b-instruct-v1:0            |
| EU Meta Llama 3.2 1B Instruct  | eu.meta.llama3-2-1b-instruct-v1:0            | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.meta.llama3-2-1b-instruct-v1:0            |
| EU Nova Micro                  | eu.amazon.nova-micro-v1:0                    | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.amazon.nova-micro-v1:0                    |
| EU Nova Lite                   | eu.amazon.nova-lite-v1:0                     | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.amazon.nova-lite-v1:0                     |
| EU Mistral Pixtral Large 25.02 | eu.mistral.pixtral-large-2502-v1:0           | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.mistral.pixtral-large-2502-v1:0           |
| EU Anthropic Claude 3.7 Sonnet | eu.anthropic.claude-3-7-sonnet-20250219-v1:0 | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.anthropic.claude-3-7-sonnet-20250219-v1:0 |
| EU Nova Pro                    | eu.amazon.nova-pro-v1:0                      | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.amazon.nova-pro-v1:0                      |
| EU Claude Sonnet 4             | eu.anthropic.claude-sonnet-4-20250514-v1:0   | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.anthropic.claude-sonnet-4-20250514-v1:0   |
| EU TwelveLabs Pegasus v1.2     | eu.twelvelabs.pegasus-1-2-v1:0               | arn:aws:bedrock:eu-west-1:298483610129:inference-profile/eu.twelvelabs.pegasus-1-2-v1:0               |