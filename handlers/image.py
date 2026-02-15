from telegram import Update
from telegram.ext import ContextTypes
from handlers.basic import calculate
from utils.ocr import image_to_text

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return

    # بزرگترین عکس رو دانلود کن
    file = await update.message.photo[-1].get_file()
    path = await file.download_to_drive()

    # استخراج متن از عکس
    text = image_to_text(path)
    if not text:
        await update.message.reply_text("❌ نمی‌توانم متن داخل عکس را بخوانم!")
        return

    # محاسبه متن استخراج شده
    update.message.text = text
    await calculate(update, context)
