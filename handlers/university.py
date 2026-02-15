from telegram import Update
from telegram.ext import ContextTypes
from sympy import sympify, diff, integrate, symbols, solve, SympifyError
import re  # ← برای چک متن غیر ریاضی


x = symbols('x')  # متغیر پیش‌فرض

# ذخیره تاریخچه کاربران
user_history = {}
HISTORY_LIMIT = 10

# فقط کاراکترهای مجاز ریاضی
valid_chars = re.compile(r'^[0-9xX+\-*/^().= ]+$')

async def math_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.message.from_user.id

    # ---------- چک اولیه متن غیر ریاضی ----------
    if not valid_chars.match(text):
        await update.message.reply_text(
            "❌ فقط عبارات ریاضی معتبر پذیرفته می‌شوند!\n"
            "نمونه‌ها: diff x**2, int x**2, solve x**2-4"
        )
        return
    
    if text.startswith("plot") or text.startswith("plot3d"):
        await update.message.reply_text("❌ این دستور در این ماژول پشتیبانی نمی‌شود!")
        return

    # ---------- محاسبه دانشگاهی ----------
    try:
        if text.startswith("diff "):
            expr = text[5:]
            result = diff(sympify(expr), x)
            await update.message.reply_text(f"مشتق: {result}")
        elif text.startswith("int "):
            expr = text[4:]
            result = integrate(sympify(expr), x)
            await update.message.reply_text(f"انتگرال: {result}")
        elif text.startswith("solve "):
            expr = text[6:]
            result = solve(sympify(expr), x)
            await update.message.reply_text(f"ریشه‌ها: {result}")
        else:
            return  # اگر دستور دانشگاهی نبود، این ماژول کاری نمی‌کند

        # ---------- ذخیره تاریخچه ----------
        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append(text)
        if len(user_history[user_id]) > HISTORY_LIMIT:
            user_history[user_id] = user_history[user_id][-HISTORY_LIMIT:]

    except SympifyError:
        await update.message.reply_text(
            "❌ عبارت معتبر نیست!\n"
            "نمونه‌ها: diff x**2, int x**2, solve x**2-4"
        )
    except Exception as e:
        await update.message.reply_text(f"خطا: {e}")
