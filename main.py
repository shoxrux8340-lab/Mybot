import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. RENDER UCHUN VEB-SERVER (BU SHART!) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render avtomatik beradigan PORT-ni ishlatish
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOT LOGIKASI ---
TOKEN = "8381400901:AAHdoC6zuEDx3oQdzFBRWJAHsJA7Lcs7fEI"

movies = {
    "1": "BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2...", # To'liq id-ni o'zingizda boricha qoldiring
    "2": "BAACAgIAAxkBAAMHaZVdHdaXZant2JK9NWL..."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Kino bot ishlayapti 😊\n"
        "1 yoki 2 kodni yozib kino olishingiz mumkin"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in movies:
        await update.message.reply_text("Kino topildi, yuborilmoqda...")
        await update.message.reply_video(video=movies[text])
    else:
        await update.message.reply_text("Bunday kodli kino topilmadi.")

# --- 3. ASOSIY ISHGA TUSHIRISH QISMI ---
if __name__ == '__main__':
    # Avval veb-serverni fonda ishga tushiramiz
    keep_alive()
    
    # Botni sozlash
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlerlarni (buyruqlarni) ulash (Rasmingizda bular yo'q edi!)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot Render-da ishga tushdi!")
    application.run_polling()
    
