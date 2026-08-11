from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


if __name__ == "__main__":
    embedding = create_embedding("Can I add baggage to my booking?")
    print(len(embedding))