from telegram import Update
from telegram.ext import ContextTypes
import openai

openai.api_key = "YOUR_OPENAI_KEY"

async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text.strip()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"لطفاً مرحله به مرحله حل کن: {question}"}],
            temperature=0
        )
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"خطا در AI: {e}")
