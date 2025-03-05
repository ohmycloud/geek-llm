import os
from openai import OpenAI


api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url='https://vip.apiyi.com/v1'
)

data = client.completions.create(
    model = "gpt-4o-mini",
    prompt = "What is Perl 6?",
    max_tokens = 50,
    temperature = 0
)
print(data)
