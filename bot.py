import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")

SALES_REPS = [
    {"name": "Barn", "role": "Seller", "phone": "+1 914 426 6031"},
    {"name": "Genxell Bio", "role": "Seller", "phone": "+1 312 217 7158"},
]

async def contacts(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lines = ["📋 *Sales Contacts*\n"]
    for rep in SALES_REPS:
        lines.append(f"🏷 *{rep['name']}* — {rep['role']}")
        lines.append(f"📞 `{rep['phone']}`\n")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("contacts", contacts))
app.run_polling()
