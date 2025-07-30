import os, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import openai

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("clean_chat.txt", "r", encoding="utf-8") as f:
    history = f.read()[-6000:]

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    prompt = f"Вот стиль общения:\n\n{history}\n\nСообщение: {user_msg}\nОтвет:"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=200
        )
        reply_text = resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        reply_text = f"⚠️ Ошибка: {e}"
    await update.message.reply_text(reply_text)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
