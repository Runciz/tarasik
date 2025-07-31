import telebot
import requests
import os

# Telegram Bot Token
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Groq API ключ и endpoint
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Загружаем стиль общения из файла
with open("clean_chat.txt", "r", encoding="utf-8") as f:
    CHAT_CONTEXT = f.read()[:3000]

# Разрешённые чаты (группы)
ALLOWED_CHAT_IDS = {-1002489903172}

@bot.message_handler(func=lambda msg: msg.chat.id in ALLOWED_CHAT_IDS and bot.get_me().username in msg.text)
def handle_message(message):
    prompt = message.text.replace(f"@{bot.get_me().username}", "").strip()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": f"Ты бот, который говорит в стиле этого чата:\n{CHAT_CONTEXT}"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        bot.reply_to(message, answer.strip())
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

bot.polling()
