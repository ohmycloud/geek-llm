import pandas as pd
import tiktoken
from openai import OpenAI


def main():
    input_path = "../data/fine_food_reviews_1k.csv"
    df = pd.read_csv(input_path, index_col=0)
    df = df[['Time', 'ProductId', 'UserId', 'Score', 'Summary', 'Text']]
    df = df.dropna()
    df['combined'] = (
        'Title: ' + df.Summary.str.strip() + '; Content: ' + df.Text.str.strip()
    )
    print(df.head(2))
    print(df['combined'])

    embedding_model = "text-embedding-ada-002"
    embedding_encoding = "cl100k_base"
    max_tokens = 8000
    top_n = 1000
    df = df.sort_values('Time').tail(top_n * 2)
    df.drop('Time', axis=1, inplace=True)

    encoding = tiktoken.get_encoding(embedding_encoding)
    df['n_tokens'] = df.combined.apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens <= max_tokens].tail(top_n)
    print(df)

    client = OpenAI()
    res = client.embeddings.create(input='abc', model=embedding_model)
    print(res.data[0].embedding)


if __name__ == "__main__":
    main()
