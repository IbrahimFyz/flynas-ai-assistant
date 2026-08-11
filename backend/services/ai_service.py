import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def get_ai_response(user_message, context):
    response = client.chat.completions.create(
        model="gpt-5.5",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Relevant information:

{context}

User question:

{user_message}
"""
            }
        ]
    )

    reply = response.choices[0]
    answer = reply.message.content

    return answer


if __name__ == "__main__":
    from services.similarity_service import search_knowledge

    question = "What is the cancellation fee?"

    result = search_knowledge(question)

    answer = get_ai_response(
        question,
        result["chunk"]
    )

    print("----- ANSWER -----")
    print(answer)