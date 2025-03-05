from client import openai_client


response = openai_client.completions.create(
    model = 'gpt-4o-mini',
    prompt="Write a tagline for an ice cream shop.",
    max_tokens = 50,
    temperature = 0
)

print(response.choices)
