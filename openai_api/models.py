from client import openai_client

data = openai_client.completions.create(
    model = "gpt-4o-mini",
    prompt = "What is Perl 6?",
    max_tokens = 50,
    temperature = 0
)
print(data)
