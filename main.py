import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- FLASK SERVER (RENDER UCHUN) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT SOZLAMALARI ---
TOKEN = '8381400901:AAHdoC6zuEDx3oQdzFBRWJAHsJA7Lcs7fEI' # O'z tokeningizni tekshirib oling
CHANNEL_ID = '@Shoxkongilocharparchalar' 
CHANNEL_LINK = 'https://t.me/Shoxkongilocharparchalar'
INSTAGRAM_LINK = 'https://www.instagram.com/shakh_6666_?igsh=MXB6NnVrZDF0Z2o0eA=='

# Kinolar ro'yxati (Kodni shu yerga qo'shib borasiz)
movies = {
    "1": 
    "BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGAAJ2jgACt6ixSN9WB-x29_McOgQ",
    "2": 
    "BAACAgIAAxkBAAMHaZVdHdaXZant2JK9NWL8-LohbrEAApCOAAK3qLFIjRO0N6tquL86BA"
}

# Obunani tekshirish funksiyasi
async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Faqat a'zo, admin yoki yaratuvchi bo'lsa True qaytaradi
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Xato: {e}")
        return False

# Start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Assalomu alaykum, {user_name}! Kino kodini yuboring.")

# Kino va Obunani tekshirish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Obunani tekshiramiz
    subscribed = await is_subscribed(user_id, context)

    if not subscribed:
        # Ikkala havola uchun tugmalar
        keyboard = [
            [InlineKeyboardButton("1️⃣ Telegram kanalga a'zo bo'lish", url=CHANNEL_LINK)],
            [InlineKeyboardButton("2️⃣ Instagramga obuna bo'lish", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton("✅ Tekshirish (Qaytadan kod yozing)", callback_data="check")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ **Kechirasiz, kino ko'rish uchun avval sahifalarimizga obuna bo'lishingiz kerak!**\n\n"
            "Obuna bo'lib, keyin kino kodini qaytadan yuboring.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # Agar obuna bo'lgan bo'lsa
    if text in movies:
        await update.message.reply_video(
            video=movies[text],
            caption=f"🎬 Kino kodi: {text}\n\nDo'stlaringizga ham ulashing!"
        )
    else:
        await update.message.reply_text("❌ Bunday kodli kino topilmadi. Iltimos, kodni to'g'ri yozing.")

if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
    
