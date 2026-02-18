import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

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
# Diqqat: Tokeningizni quyidagi qo'shtirnoq ichiga yozing
TOKEN = '8381400901:AAHdoC6zuEDx3oQdzFBRWJAHsJA7Lcs7fEI' 
CHANNEL_ID = '@Shoxkongilocharparchalar' 
CHANNEL_LINK = 'https://t.me/Shoxkongilocharparchalar'
INSTAGRAM_LINK = 'https://www.instagram.com/shakh_6666_?igsh=MXB6NnVrZDF0Z2o0eA=='

# Kinolar ro'yxati (Kino kodlarini shu yerga qo'shib borasiz)
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
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception:
        return False

# Start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Assalomu alaykum, {user_name}! Kino ko'rish uchun kino kodini yuboring.")

# "Tekshirish" tugmasi bosilganda ishlaydigan qism
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    subscribed = await is_subscribed(user_id, context)
    
    if subscribed:
        await query.answer("Rahmat! Endi kino kodini yuborishingiz mumkin.", show_alert=True)
        await query.edit_message_text("✅ Obuna tasdiqlandi. Kino kodini yuboring:")
    else:
        await query.answer("⚠️ Siz hali kanalga a'zo bo'lmadingiz! Iltimos, avval obuna bo'ling.", show_alert=True)

# Kino kodini tekshirish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    subscribed = await is_subscribed(user_id, context)

    if not subscribed:
        keyboard = [
            [InlineKeyboardButton("1️⃣ Telegram kanalga a'zo bo'lish", url=CHANNEL_LINK)],
            [InlineKeyboardButton("2️⃣ Instagramga obuna bo'lish", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ **Kino ko'rish uchun avval sahifalarimizga obuna bo'lishingiz kerak!**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    if text in movies:
        await update.message.reply_video(
            video=movies[text],
            caption=f"🎬 Kino kodi: {text}\n\nDo'stlaringizga ham ulashing!"
        )
    else:
        await update.message.reply_text("❌ Bunday kodli kino topilmadi. Iltimos, kodni to'g'ri yozing.")

# Botni ishga tushirish
if __name__ == '__main__':
    keep_alive()
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback, pattern='^check_sub$'))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
