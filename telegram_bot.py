from telegram.ext import Application, CommandHandler, MessageHandler, filters
from langchain_chroma import Chroma
from query import process_query
from api import bot_token

BOT_TOKEN = bot_token

async def handle_message(update, context):
    reply = process_query(update.message.text)
    await update.message.reply_text(reply)

async def start(update, context):
    await update.message.reply_text("Hello! I'm your bot.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
