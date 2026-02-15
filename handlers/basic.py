from telegram import Update
from telegram.ext import ContextTypes
from sympy import sympify, SympifyError
import re

# ذخیره تاریخچه کاربران
user_history = {}
HISTORY_LIMIT = 10

# فقط کاراکترهای مجاز ریاضی
valid_chars = re.compile(r'^[0-9xX+\-*/^().= ]+$')

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.message.from_user.id

    # ---------- پیام plot یا plot3d را نادیده بگیر ----------
    if text.startswith("plot") or text.startswith("plot3d"):
        return

    # ---------- چک اولیه متن غیر ریاضی ----------
    if not valid_chars.match(text):
        await update.message.reply_text(
            "❌ فقط عبارات ریاضی معتبر پذیرفته می‌شوند!\n"
            "مثال‌ها:\n2+3*5\n(5+3)^2"
        )
        return

    # ---------- محاسبه با sympy ----------
    try:
        result = sympify(text)
        await update.message.reply_text(f"نتیجه: {result}")

        # ---------- ذخیره تاریخچه ----------
        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append(text)
        if len(user_history[user_id]) > HISTORY_LIMIT:
            user_history[user_id] = user_history[user_id][-HISTORY_LIMIT:]

    except SympifyError:
        await update.message.reply_text(
            "❌ عبارت معتبر نیست!\nمثال‌های درست: 2+3*5, (5+3)^2"
        )
