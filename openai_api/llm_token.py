from numpy import imag
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
