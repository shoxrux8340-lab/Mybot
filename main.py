import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- SERVER QISMI (Render o'chib qolmasligi uchun) ---
app = Flask('')

@app.route('/')
def home(): 
    return "Bot is alive!"

def run(): 
    app.run(host='0.0.0.0', port=8080)

def keep_alive(): 
    Thread(target=run).start()

# --- SOZLAMALAR ---
# DIQQAT: Tokenni @BotFather orqali yangilaganingizdan so'ng yangisini shu yerga qo'ying
TOKEN = '8381400901:AAGauEhemoMPXFYYE6q67kPARilGME1tC9Q' 
CHANNEL_ID = '@Shoxkongilocharparchalar' 
CHANNEL_LINK = 'https://t.me/Shoxkongilocharparchalar'
INSTAGRAM_LINK = 'https://www.instagram.com/shakh_6666_?igsh=MXB6NnVrZDF0Z2o0eA=='

# Kinolar bazasi (Tuzatilgan ko'rinishda)
movies = {
    "1": "BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGA AJ2jgACt6ixSN9WB-x29_McOgQ",
    "3": "BAACAgIAAxkBAAO9aZcy1-mzoL-50denhNx1nG8y0EwAApVFAAL4FcBKkSB1AluE4SA6BA",
    "2": "BAACAgEAAxkBAAOdaZZ7WHZMNYu7t9u-dZ9Yk48kwTcAAt sLAALxtJlEHRVMTD_K0U6BA"
}

# Kanalga a'zolikni tekshirish funksiyasi
async def is_subscribed(user_id, context):
    try:
        # Bu yerda qatorlar birlashtirildi
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Tekshirish tugmasi bosilganda
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await is_subscribed(query.from_user.id, context):
        await query.answer("Rahmat! Endi kodni yuboring.", show_alert=True)
        await query.edit_message_text("✅ Obuna tasdiqlandi. Kino kodini yuboring:")
    else:
        await query.answer("⚠️ Hali a'zo bo'lmadingiz!", show_alert=True)

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_subscribed(user_id, context):
        await update.message.reply_text("Assalomu alaykum! Kino kodini yuboring.")
    else:
        keyboard = [
            [InlineKeyboardButton("1️⃣ Telegram", url=CHANNEL_LINK)],
            [InlineKeyboardButton("2️⃣ Instagram", url=INSTAGRAM_LINK)],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Botdan foydalanish uchun kanalimizga a'zo bo'ling:", reply_markup=reply_markup)

# Xabar yuborilganda (Kino topish)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if not await is_subscribed(user_id, context):
        await start(update, context)
        return

    if text in movies:
        await update.message.reply_video(video=movies[text], caption=f"🎬 Kod: {text}\n\n@Shoxkongilocharparchalar")
    else:
        await update.message.reply_text("❌ Bunday kodli kino topilmadi.")

# Asosiy ishga tushirish qismi
if __name__ == '__main__':
    keep_alive()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(button_callback, pattern='^check_sub$'))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    app_bot.run_polling()
