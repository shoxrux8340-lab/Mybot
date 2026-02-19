import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# SERVER QISMI
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# SOZLAMALAR
TOKEN = '8381400901:AAHdoC6zuEDx3oQdzFBRWJAHsJA7Lcs7fEI' 
CHANNEL_ID = '@Shoxkongilocharparchalar' 
CHANNEL_LINK = 'https://t.me/Shoxkongilocharparchalar'
INSTAGRAM_LINK = 'https://www.instagram.com/shakh_6666_?igsh=MXB6NnVrZDF0Z2o0eA=='

movies = {
    "1": 
"BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGAAJ2jgACt6ixSN9WB-x29_McOgQ",
    "2": 
"BAACAgIAAxkBAAMHaZVdHdaXZant2JK9NWL8-LohbrEAApCOAAK3qLFIjRO0N6tquL86BA"
}

async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return False

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await is_subscribed(query.from_user.id, context):
        await query.answer("Rahmat! Endi kodni yuboring.", show_alert=True)
        await query.edit_message_text("✅ Obuna tasdiqlandi. Kino kodini yuboring:")
    else:
        await query.answer("⚠️ Hali a'zo bo'lmadingiz!", show_alert=True)

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.video.file_id
    await update.message.reply_text(f"Kino ID si:\n\n`{file_id}`", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if not await is_subscribed(user_id, context):
        keyboard = [[InlineKeyboardButton("1️⃣ Telegram", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("2️⃣ Instagram", url=INSTAGRAM_LINK)],
                    [InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")]]
        await update.message.reply_text("Obuna bo'ling:", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    if text in movies:
        await update.message.reply_video(video=movies[text], caption=f"🎬 Kod: {text}")
    else:
        await update.message.reply_text("❌ Kod xato.")

async def start(update, context):
    await update.message.reply_text("Assalomu alaykum! Kino kodini yuboring.")

if __name__ == '__main__':
    keep_alive()
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler('start', start))
    app_bot.add_handler(CallbackQueryHandler(button_callback, pattern='^check_sub$'))
    app_bot.add_handler(MessageHandler(filters.VIDEO, get_video_id))
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_bot.run_polling()
