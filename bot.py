import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8668093662:AAHgPo5Uw0siICWEV8FygwTg_EpnCLzos6I")
WEBHOOK_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "http://localhost:8000")

SALES_REPS = [
    {"name": "Barn", "role": "Seller", "phone": "+1 914 426 6031"},
    {"name": "Genxell Bio", "role": "Seller", "phone": "+1 312 217 7158"},
]

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

async def contacts(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lines = ["📋 *Sales Contacts*\n"]
    for rep in SALES_REPS:
        lines.append(f"🏷 *{rep['name']}* — {rep['role']}")
        lines.append(f"📞 `{rep['phone']}`\n")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot)
    
    if update.message and update.message.text == "/contacts":
        await contacts(update, None)
    
    return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    # Set webhook
    bot.set_webhook(url=f"https://{WEBHOOK_URL}/webhook")
    logger.info(f"Webhook set to https://{WEBHOOK_URL}/webhook")
    app.run(host="0.0.0.0", port=8000)
