import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Config
BOUNDLESS_API_KEY = os.getenv("BOUNDLESS_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(
    api_key=BOUNDLESS_API_KEY,
    base_url="https://api.inference.boundless.network/v1"
)

# Models
MODELS = {
    "1": "deepseek-v4.1-flash",
    "2": "glm-5.2",
    "3": "dsv4",
    "4": "kimi-k3",
}
DEFAULT_MODEL = "deepseek-v4.1-flash"

# Per-user model preference (simple in-memory)
user_models = {}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Boundless bot ready.\n\n"
        "Commands:\n"
        "/model <name or number> — switch model\n"
        "/models — list models\n"
        "/current — show current model\n\n"
        f"Default model: {DEFAULT_MODEL}\n"
        "Just type a message to chat."
    )

async def models_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["Available models:"]
    for k, v in MODELS.items():
        lines.append(f"{k}: {v}")
    lines.append(f"\nCurrent: {get_user_model(update.effective_user.id)}")
    await update.message.reply_text("\n".join(lines))

async def current_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Current model: {get_user_model(update.effective_user.id)}")

async def model_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /model <name or number>\nExample: /model glm-5.2 or /model 2")
        return
    choice = " ".join(context.args).strip()
    if choice in MODELS:
        choice = MODELS[choice]
    user_models[update.effective_user.id] = choice
    await update.message.reply_text(f"Switched to: {choice}")

def get_user_model(user_id):
    return user_models.get(user_id, DEFAULT_MODEL)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    model = get_user_model(user_id)
    prompt = update.message.text

    await update.message.reply_text(f"Thinking with {model}...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        # Telegram has a 4096 char limit
        if len(reply) > 4000:
            reply = reply[:4000] + "\n\n[truncated]"
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    if not TELEGRAM_TOKEN:
        print("Set TELEGRAM_TOKEN environment variable")
        return
    if not BOUNDLESS_API_KEY:
        print("Set BOUNDLESS_API_KEY environment variable")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("models", models_cmd))
    app.add_handler(CommandHandler("current", current_cmd))
    app.add_handler(CommandHandler("model", model_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Telegram bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
