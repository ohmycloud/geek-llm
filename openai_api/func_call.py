import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from client import api_key
from typing import List


GPT_MODEL = "gpt-3.5-turbo"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    json_data = {
        'model': model,
        'messages': messages
    }

    if functions is not None:
        json_data.update({'functions': functions})

    if function_call is not None:
        json_data.update({'function_call': function_call})

    try:
        response = requests.post(
            'https://vip.apiyi.com/v1/chat/completions',
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print('Unable to generate ChatCompletion response')
        print('f"Exception: {e}"')
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        'system': 'red',
        'user': 'green',
        'assistant': 'blue',
        'function': 'megenta',
    }

    for message in messages:
        if message['role'] == 'system':
            print(colored(f"{message['role'].capitalize()}: {message['content']}", role_to_color[message['role']]))
        elif message['role'] == 'user':
            print(colored(f"{message['role'].capitalize()}: {message['content']}", role_to_color[message['role']]))
        elif message['role'] == 'assistant' and message.get("function_call"):
            print(colored(f"{message['role'].capitalize()}: {message['function_call']}", role_to_color[message['role']]))
        elif message['role'] == 'assistant' and not message.get("function_call"):
            print(colored(f"{message['role'].capitalize()}: {message['content']}", role_to_color[message['role']]))
        elif message['role'] == 'function':
            print(colored(f"{message['name'].capitalize()}: {message['content']}", role_to_color[message['role']]))
        else:
            pass


functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Can be either 'celsius' or 'fahrenheit'."
                }
            },
            "required": ["location", "format"]
        }
    },
    {
        "name": "get_n_day_weather_forecast",
        "description": "Get the weather forecast for the next n days in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "days": {
                    "type": "integer",
                    "description": "The number of days to forecast"
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Can be either 'celsius' or 'fahrenheit'."
                }
            },
            "required": ["location", "days", "format"]
        }
    }
]

messages = []

# 追加一条系统角色的消息
messages.append({
    'role': 'system',
    'content': 'Don\'t make assumptions about what value to plug into functions. Ask for clarification on the input parameters. For example, ask for the location, number of days, and temperature unit.'
})

# 追加一条用户角色的消息
messages.append({
    'role': 'user',
    'content': 'What is the weather like today in New York City?'
})

# 使用定义的 chat_completion_request 函数发起一个请求, 传入 messages 和 functions 作为参数
chat_response = chat_completion_request(messages, functions=functions)

# 解析返回的 JSON 数据, 获取助手的回复消息
assistant_message = chat_response.json()["choices"][0]["message"]

# 将助手消息追加到 messages 中
messages.append(assistant_message)
pretty_print_conversation(messages)
