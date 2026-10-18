import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("BOUNDLESS_API_KEY"),
    base_url=os.getenv("BOUNDLESS_BASE_URL", "https://api.inference.boundless.network/v1")
)

def ask(prompt):
    response = client.chat.completions.create(
        model="deepseek-v4.1-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Boundless bot ready. Type a prompt (or 'quit'):")
    while True:
        user_input = input("> ")
        if user_input.lower() in ["quit", "exit"]:
            break
        print(ask(user_input))
        print()
