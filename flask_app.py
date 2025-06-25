from flask import Flask, request
from telegram import Update
from telegram.ext import Application
from bot import message_handler, start  # bot.py ফাইল থেকে import করো

import os

TOKEN = os.getenv("BOT_TOKEN", "7429762049:AAEq4iAITSkIFlohNRu0le4Vtt0U2xILUiw")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://tanim0677.pythonanywhere.com{WEBHOOK_PATH}"  # তোমার PythonAnywhere username অনুযায়ী URL

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok"

@app.route("/")
def home():
    return "✅ Bot is live via Webhook!"

if __name__ == "__main__":
    app.run()
