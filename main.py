import os
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Flask server (Render o'chib qolmasligi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# --- SOZLAMALAR ---
# DIQQAT: Tokenni @BotFather orqali yangilashni unutmang!
TOKEN = '8381400901:AAGauEhemoMPXFYYE6q67kPARilGME1tC9Q' 
CHANNEL_ID = '@Shoxkongilocharparchalar'
CHANNEL_LINK = 'https://t.me/Shoxkongilocharparchalar'
INSTAGRAM_LINK = 'https://www.instagram.com/shakh_6666_'

# Kinolar bazasi (Tuzatilgan holati)
movies = {
    "1": "BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGA AJ2jgACt6ixSN9WB-x29_McOgQ",
    "3": "BAACAgIAAxkBAAO9aZcy1-mzoL-50denhNx1nG8y0EwAApVFAAL4FcBKkSB1AluE4SA6BA",
    "2": "BAACAgEAAxkBAAOdaZZ7WHZMNYu7t9u-dZ9Yk48kwTcAAt sLAALxtJlEHRVMTD_K0U6BA"
}

# Kanalga a'zolikni tekshirish funksiyasi
async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_subscribed(user_id, context):
        await update.message.reply_text("Xush kelibsiz! Kino kodini yuboring.")
    else:
        keyboard = [
            [InlineKeyboardButton("Kanalga a'zo bo'lish", url=CHANNEL_LINK)],
            [InlineKeyboardButton("Tekshirish", callback_data='check_sub')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Botdan foydalanish uchun kanalimizga a'zo bo'ling:", reply_markup=reply_markup)

# Kod yuborilganda kinoni topish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    code = update.message.text

    if not await is_subscribed(user_id, context):
        await start(update, context)
        return

    if code in movies:
        await update.message.reply_video(video=movies[code], caption=f"Kino kodi: {code}\n@Shoxkongilocharparchalar")
    else:
        await update.message.reply_text("Xato kod! Bunday kodli kino topilmadi.")

# Asosiy funksiya
def main():
    keep_alive()
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
