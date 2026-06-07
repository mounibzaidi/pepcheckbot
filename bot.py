import os
from flask import Flask, request
from telegram import Bot, BotCommand, InlineQueryResultArticle, InputTextMessageContent
import logging
import json
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

SALES_REPS = [
    {"name": "Barn", "role": "Seller", "phone": "+1 914 426 6031"},
    {"name": "Genxell Bio", "role": "Seller", "phone": "+1 312 217 7158"},
]

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

def register_commands():
    try:
        commands = [BotCommand("contacts", "Get sales contact - use /contacts or /contacts barn")]
        asyncio.run(bot.set_my_commands(commands))
        logger.info("Commands registered")
    except Exception as e:
        logger.error(f"Failed to register commands: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        logger.info(f"Webhook: {json.dumps(data)}")

        if "inline_query" in data:
            query = data["inline_query"]["query"].lower()
            inline_query_id = data["inline_query"]["id"]
            results = []
            for rep in SALES_REPS:
                if query == "" or query in rep["name"].lower():
                    result = InlineQueryResultArticle(
                        id=rep["name"],
                        title=rep["name"],
                        description=f"{rep['role']} - {rep['phone']}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"📞 *{rep['name']}*\n{rep['role']}\n`{rep['phone']}`",
                            parse_mode="Markdown"
                        )
                    )
                    results.append(result)
            try:
                asyncio.run(bot.answer_inline_query(inline_query_id, results, cache_time=0))
            except Exception as e:
                logger.error(f"Failed to answer inline query: {e}")

        if "message" in data and "text" in data["message"]:
            text = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]

            if text.startswith("/contacts"):
                # Get search term after /contacts
                parts = text.split(maxsplit=1)
                search = parts[1].lower() if len(parts) > 1 else ""

                # Filter reps
                matches = [r for r in SALES_REPS if search in r["name"].lower()] if search else SALES_REPS

                if matches:
                    lines = ["📋 *Sales Contacts*\n"]
                    for rep in matches:
                        lines.append(f"🏷 *{rep['name']}* — {rep['role']}")
                        lines.append(f"📞 `{rep['phone']}`\n")
                    message_text = "\n".join(lines)
                else:
                    message_text = f"❌ No contact found for *{search}*"

                try:
                    asyncio.run(bot.send_message(chat_id=chat_id, text=message_text, parse_mode="Markdown"))
                    logger.info(f"Sent contacts to {chat_id}")
                except Exception as send_error:
                    logger.error(f"Failed to send message: {send_error}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

    return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    register_commands()
    app.run(host="0.0.0.0", port=PORT, debug=False)
