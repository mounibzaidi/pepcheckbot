import os
import asyncio
import logging
from flask import Flask, request
from telegram import Update, Bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8668093662:AAHgPo5Uw0siICWEV8FygwTg_EpnCLzos6I")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://pepcheckbot-production.up.railway.app/webhook")

SALES_REPS = [
    {"name": "Barn", "role": "Seller", "phone": "+1 914 426 6031"},
    {"name": "Genxell Bio", "role": "Seller", "phone": "+1 312 217 7158"},
]

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot)

    async def handle():
        if update.message and update.message.text:
            if "/contacts" in update.message.text:
                lines = ["📋 *Sales Contacts*\n"]
                for rep in SALES_REPS:
                    lines.append(f"🏷 *{rep['name']}* — {rep['role']}")
                    lines.append(f"📞 `{rep['phone']}`\n")
                await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
                logger.info(f"Sent contacts to {update.message.chat.id}")

    asyncio.run(handle())
    return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    async def set_webhook():
        await bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"Webhook set to {WEBHOOK_URL}")

    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=8000)
