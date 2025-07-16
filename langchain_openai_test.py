from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import requests
import json

openai_key = '<your OpenAI API Key>'
openai_url = '<OpenAI API base URL ending in /api/v1>'

headers = {
    "Authorization": f"Bearer {openai_key}",
    "Content-Type": "application/json"
}

# Make a request to get the list of available models
response = requests.get(f"{openai_url}/models", headers=headers)
models_data = json.loads(response.text)

desired_model = 'llama3-2'
model = None
for m in models_data.get('data', []):
    if (desired_model in m.get('id', '')):
        model = m['id']
        break

print('model selected: ', model)

chat = ChatOpenAI(
    model=model,
    temperature=0,
    openai_api_key=openai_key,
    openai_api_base=openai_url,
)

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(prompt=prompt, llm=chat)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
response = llm_chain.invoke(question)
print(response)