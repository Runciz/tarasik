import telebot
import os
import requests

# Получаем переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ALLOWED_CHAT_ID = -1002489903172  # ← ID твоего чата

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функция обращения к Groq
def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Отвечай по-русски, как гопник, с юмором, как участник группового чата."},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# Ответить только на обращения в чате
@bot.message_handler(func=lambda message: message.chat.type in ["group", "supergroup"])
def handle_group(message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return  # Не наш чат

    if not (bot.get_me().username.lower() in message.text.lower()):
        return  # Нет обращения к боту по нику

    prompt = message.text
    try:
        reply = ask_groq(prompt)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

# Игнорировать личные сообщения
@bot.message_handler(func=lambda message: message.chat.type == "private")
def handle_private(message):
    bot.send_message(message.chat.id, "⚠️ Я работаю только в групповом чате.")

# Запуск
bot.infinity_polling()
