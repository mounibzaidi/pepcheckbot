import os
from flask import Flask, request
from telegram import Bot
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

SALES_REPS = [
    {"name": "Barn", "role": "Seller", "phone": "+1 914 426 6031"},
    {"name": "Genxell Bio", "role": "Seller", "phone": "+1 312 217 7158"},
]

app = Flask(__name__)
bot = None

def get_bot():
    global bot
    if bot is None:
        bot = Bot(token=BOT_TOKEN)
    return bot

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        logger.info(f"Webhook: {json.dumps(data)}")
        
        if "message" in data and "text" in data["message"]:
            text = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]
            
            if "/contacts" in text:
                lines = ["📋 *Sales Contacts*\n"]
                for rep in SALES_REPS:
                    lines.append(f"🏷 *{rep['name']}* — {rep['role']}")
                    lines.append(f"📞 `{rep['phone']}`\n")
                
                get_bot().send_message(chat_id=chat_id, text="\n".join(lines), parse_mode="Markdown")
                logger.info(f"Sent contacts to {chat_id}")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    
    return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
