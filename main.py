import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.basic import calculate, user_history as basic_history
from handlers.university import math_university
from handlers.plotting import plot_2d, plot_3d

# Load token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Build bot
app = ApplicationBuilder().token(TOKEN).build()

# Start command
async def start(update, context):
    await update.message.reply_text(
        "سلام 😈 آماده‌ای برای حال کردن با ریاضی!\n"
        "برای استفاده از فرمت‌ها مثال ها :\n"
        "diff x**2  -> مشتق\n"
        "int x**2   -> انتگرال\n"
        "plot x**2 + 3*x - 5 -> رسم نمودار ۲ بعدی\n"
        "plot3d x**2 + y**2 -> رسم نمودار ۳ بعدی\n"
        "solve x**2-4 -> حل معادله\n"
        "یا محاسبات ساده مثل 2+3*5"
    )

# History command
async def show_history(update, context):
    user_id = update.message.from_user.id
    history = basic_history.get(user_id, [])
    if not history:
        await update.message.reply_text("تاریخی وجود ندارد ❌")
    else:
        text = "\n".join([f"{i+1}. {expr}" for i, expr in enumerate(history)])
        await update.message.reply_text(f"۱۰ محاسبه آخر شما:\n{text}")

# فیلتر برای پیام‌های دانشگاهی
def university_filter(message):
    text = message.text.strip()
    return text.startswith("diff ") or text.startswith("int ") or text.startswith("solve ")

# Add handlers
# ابتدا handlerهای plot
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r'^plot3d '), plot_3d))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r'^plot '), plot_2d))

# سپس handler دانشگاهی
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r'^(diff |int |solve )'), math_university))

# در آخر handler محاسبات ساده
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))


# Run bot
print("بات داره اجرا میشه...")
app.run_polling()
