import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

# Put your bot token here directly (get from @BotFather)
TOKEN = "YOUR_BOT_TOKEN_HERE"  # ← Replace this!

logging.basicConfig(level=logging.INFO)

def fetch_top_countries():
    try:
        response = requests.get("https://restcountries.com/v3.1/all?fields=name,population", timeout=10)
        countries = response.json()
        valid = [c for c in countries if c.get('population', 0) > 0]
        sorted_c = sorted(valid, key=lambda x: x['population'], reverse=True)[:20]
        return [f"{i+1}. {c['name']['common']}" for i, c in enumerate(sorted_c)]
    except:
        return ["1. China", "2. India", "3. USA", "4. Indonesia", "5. Pakistan"]

async def start(update, context):
    keyboard = [["📊 Show Top 20"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🌍 Welcome! Click button to see Top 20 countries", reply_markup=reply_markup)

async def show_countries(update, context):
    top20 = fetch_top_countries()
    message = "🌍 Top 20 Countries by Population:\n\n" + "\n".join(top20)
    await update.message.reply_text(message)

async def handle_message(update, context):
    if "Show Top 20" in update.message.text:
        await show_countries(update, context)
    else:
        await update.message.reply_text("Press the button below 👇")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
