from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("No API key found. Please check ypur .env file.")


client = OpenAI(
    api_key=api_key,
    base_url='https://vip.apiyi.com/v1'
)

response = client.completions.create(
    model = 'gpt-4o-mini',
    prompt="Write a tagline for an ice cream shop.",
    max_tokens = 50,
    temperature = 0
)

print(response.choices)
