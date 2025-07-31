import telebot
import requests
import os

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Разрешённые Telegram-группы
ALLOWED_CHAT_IDS = {-1002489903172}

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda msg: msg.chat.type in ["group", "supergroup"])
def handle_group_message(message):
    if message.chat.id not in ALLOWED_CHAT_IDS:
        return  # Не наша группа

    if f"@{bot.get_me().username.lower()}" not in message.text.lower():
        return  # Бот не упомянут

    prompt = message.text.replace(f"@{bot.get_me().username}", "").strip()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Отвечай понятно, кратко, дружелюбно."},
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

@bot.message_handler(func=lambda msg: msg.chat.type == "private")
def ignore_private(message):
    bot.send_message(message.chat.id, "❌ Я работаю только в групповом чате.")

bot.polling()
