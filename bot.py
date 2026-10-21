import os
import sys
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("BOUNDLESS_API_KEY"),
    base_url=os.getenv("BOUNDLESS_BASE_URL", "https://api.inference.boundless.network/v1")
)

# Available models on Boundless
MODELS = {
    "1": "deepseek-v4.1-flash",
    "2": "glm-5.2",
    "3": "dsv4",           # cheaper DeepSeek V4 Flash
    "4": "kimi-k3",
}

DEFAULT_MODEL = "deepseek-v4.1-flash"

def ask(prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    # Allow model via command line: python bot.py glm-5.2
    if len(sys.argv) > 1:
        model = sys.argv[1]
    else:
        model = DEFAULT_MODEL

    print("Boundless bot ready.")
    print(f"Current model: {model}")
    print("Commands: /model <name> | /models | quit")
    print("-" * 40)

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue

        low = user_input.lower()

        if low in ("quit", "exit", "/quit"):
            break

        if low == "/models":
            print("Available models:")
            for k, v in MODELS.items():
                print(f"  {k}: {v}")
            print(f"Current: {model}")
            continue

        if low.startswith("/model"):
            parts = user_input.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: /model <model-name>")
                continue
            new_model = parts[1].strip()
            # Allow number shortcut
            if new_model in MODELS:
                new_model = MODELS[new_model]
            model = new_model
            print(f"Switched to: {model}")
            continue

        # Normal prompt
        try:
            reply = ask(user_input, model)
            print(reply)
            print()
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
