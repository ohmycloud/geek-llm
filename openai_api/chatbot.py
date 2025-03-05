from client import openai_client

messages = [
    {
        'role': 'system',
        'content': '你是一个有100年经验的河南方言专家'
    },
    {
        "role": "user",
        "content": "'With Today' 是啥意思?"
    }
]

response = openai_client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = messages,
)

messages.append({
    'role': response.choices[0].message.role,
    'content': response.choices[0].message.content
})

response = openai_client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages = messages,
)

print(response.choices[0].message.content)
