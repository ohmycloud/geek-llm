import tiktoken
from utils import num_tokens_from_string


encoding = tiktoken.get_encoding('cl100k_base')
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

# [81, 587, 360, 526, 23902, 0]
print(encoding.encode('rakulang rocks!'))

num_tokens = num_tokens_from_string('rakulang rocks!', 'cl100k_base')
print(num_tokens)

embeddings = [81, 587, 360, 526, 23902, 0]

# turn embeddings into text
origin_content = encoding.decode(embeddings)
print(origin_content)

for token in embeddings:
    print(encoding.decode_single_token_bytes(token))


def compare_encodings(input: str) -> None:
    """Compare a comparsion of three string encodings."""
    for encoding_name in ['gpt2', 'p50k_base', 'cl100k_base']:
        encoding = tiktoken.get_encoding(encoding_name)
        print(f"Encoding: {encoding_name}")
        print(f"Tokens: {encoding.encode(input)}")
        print(f"Number of tokens: {num_tokens_from_string(input, encoding_name)}")
        print(f"Decoded text: {encoding.decode(encoding.encode(input))}")
        print(f"Single token bytes: {[encoding.decode_single_token_bytes(token) for token in encoding.encode(input)]}")
        print("\n")

compare_encodings('rakulang rocks!')

def num_tokens_from_messages(messages, model='gpt-3.5-turbo'):
    """Return the number of tokens used by a list of messages."""
    try:
        # 尝试获取模型的编码
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # 如果模型没有找到, 使用 cl100k_base
        print("Model not found, using cl100k_base")
        encoding = tiktoken.get_encoding('cl100k_base')

    if model in [
        'gpt-3.5-turbo-0613',
        'gpt-3.5-turbo-16k-0613',
        'gpt-4-0314',
        'gpt-4-32k-0314',
        'gpt-4-0613',
        'gpt-4-32k-0613'
    ]:
        tokens_per_message = 3
        tokens_per_name =1
    elif model == 'gpt-3.5-turbo-0301':
        tokens_per_message = 4
        tokens_per_name = -1 # 如果有名字, 角色会被省略
    elif 'gpt-3.5-turbo' in model:
        # 对于 gpt-3.5-turbo 模型可能会有更新, 此处返回假设为 gpt-3.5-turbo-0613 的 token 数量
        print("Waring: gpt-3.5-turbo may be update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model='gpt-3.5-turbo-0613')
    elif 'gpt-4' in model:
        # 对于 gpt-4 模型可能会有更新, 此处返回假设为 gpt-4-0613 的 token 数量
        print("Waring: gpt-4 may be update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model='gpt-4-0613')
    elif model in [
        'davinci',
        'curie',
        'babbage',
        'ada'
    ]:
        print('Waring: gpt-3 related model is used. Returning num tokens assuming gpt2.')
        encoding = tiktoken.get_encoding('gpt2')
        num_tokens = 0
        for message in messages:
            for key, value in message.items():
                if key == 'content':
                    num_tokens += len(encoding.encode(value))
        return num_tokens
    else:
        # 对于没有实现的模型, 抛出未实现错误
        raise NotImplementedError(
            f"""num_tokens_from_messages is not implemented for model {model}"""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == 'name':
                num_tokens += tokens_per_name
    num_tokens +=3 # 每条回复都以助手为首
    return num_tokens
