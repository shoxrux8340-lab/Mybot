from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8381400901:AAHdoC6zuEDx3oQdzFBRWJAHsJA7Lcs7fEI"

# Kino lug'ati: "kod": "file_id"
movies = {
    "1": 
    "BAACAgIAAxkBAAMDaZVZqtffFRkNgH2FLn2WEE_lAAEGAAJ2jgACt6ixSN9WB-x29_McOgQ",
    "2": 
    "BAACAgIAAxkBAAMHaZVdHdaXZant2JK9NWL8-LohbrEAApCOAAK3qLFIjRO0N6tquL86BA"
}

# /start buyrug'iga javob
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Kino bot ishlayapti 😊\n"
        "1 yoki 2 kodni yozib kino olishingiz mumkin"
    )

# Foydalanuvchi xabarini tekshirish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in movies:
        await update.message.reply_text(f"🎬 Kino yuklanmoqda...")
        await update.message.reply_video(movies[text])
    else:
        await update.message.reply_text("❌ Bunday kod mavjud emas. Masalan 1 yoki 2")

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")

app.run_polling()
