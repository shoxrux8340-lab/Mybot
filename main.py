import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- SOZLAMALAR ---
TOKEN = '8381400901:AAGauEhemoMPXFYYE6q67kPARilGME1tC9Q' 
CHANNEL_ID = '@Shoxkongilocharparchalar' 
CHANNEL_LINK = 'https://t.me/Shoxkongilocharparchalar'
INSTAGRAM_LINK = 'https://www.instagram.com/shakh_6666_?igsh=MXB6NnVrZDF0Z2o0eA=='

movies = {
    "1":
"BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGAJ2jgACt6ixSN9WB-x29_McOgQ",
    "3": "BAACAgIAAxkBAAO9aZcy1-mzoL-50denhNx1nG8y0EwAApVFAAL4FcBKkSB1AluE4SA6BA",
    "2":
"BAACAgEAAxkBAAOdaZZ7WHZMNYu7t9u-dZ9Yk48kwTcAAsLAALxtJlEHRVMTD_K0U6BA"
}
async def is_subscribed(user_id, context):
    try:
        # Qator bo'linib ketmasligi uchun qavs ichiga olindi
        member = await   context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await is_subscribed(query.from_user.id, context):
        await query.answer("Rahmat! Endi kodni yuboring.", show_alert=True)
        await query.edit_message_text("✅ Obuna tasdiqlandi. Kino kodini yuboring:")
    else:
        await query.answer("⚠️ Hali a'zo bo'lmadingiz!", show_alert=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_subscribed(user_id, context):
        await update.message.reply_text("Xush kelibsiz! Kino kodini yuboring.")
    else:
        keyboard = [[InlineKeyboardButton("1️⃣ Telegram", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("2️⃣ Instagram", url=INSTAGRAM_LINK)],
                    [InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")]]
        await update.message.reply_text("Botdan foydalanish uchun a'zo bo'ling:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if not await is_subscribed(user_id, context):
        await start(update, context)
        return
    if text in movies:
        await update.message.reply_video(video=movies[text], caption=f"🎬 Kod: {text}")
    else:
        await update.message.reply_text("❌ Bunday kodli kino topilmadi.")

if __name__ == '__main__':
    keep_alive()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(button_callback, pattern='^check_sub$'))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_bot.run_polling()
