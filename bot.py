import os
from flask import Flask, request
from telegram import Update, Bot
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8668093662:AAHgPo5Uw0siICWEV8FygwTg_EpnCLzos6I")

SALES_REPS = [
    {"name": "Barn", "role": "Seller", "phone": "+1 914 426 6031"},
    {"name": "Genxell Bio", "role": "Seller", "phone": "+1 312 217 7158"},
]

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot)
    
    if update.message and update.message.text == "/contacts":
        lines = ["📋 *Sales Contacts*\n"]
        for rep in SALES_REPS:
            lines.append(f"🏷 *{rep['name']}* — {rep['role']}")
            lines.append(f"📞 `{rep['phone']}`\n")
        update.message.reply_text("\n".join(lines), parse_mode="Markdown")
    
    return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
