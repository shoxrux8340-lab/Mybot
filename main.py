import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- RENDER UCHUN VEB-SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT LOGIKASI ---
TOKEN = "8381400901:AAHdoC6zuEDx3oQdzFBRWJAHsJA7Lcs7fEI"

movies = {
    "1": 
    "BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGAAJ2jgACt6ixSN9WB-x29_McOgQ", # O'zgartirmang
    "2": 
    "BAACAgIAAxkBAAMHaZVdHdaXZant2JK9NWL8-LohbrEAApCOAAK3qLFIjRO0N6tquL86BA"  # O'zgartirmang
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Kino bot ishlayapti 😊\nKod yuboring.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in movies:
        await update.message.reply_video(video=movies[text])
    else:
        await update.message.reply_text("Kino topilmadi.")

# --- ISHGA TUSHIRISH ---
if __name__ == '__main__':
    keep_alive() # Render uchun shart
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Buyruqlarni ulash
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot Renderda ishga tushdi!")
    application.run_polling()
    
