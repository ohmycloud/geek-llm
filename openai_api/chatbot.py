from client import openai_client

messages = [
    {
        "role": "user",
        "content": "Today is a beautiful day."
    }
]

response = openai_client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = messages,
)

print(response)
