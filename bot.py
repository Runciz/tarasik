import telebot
import openai
import os

# 🔑 Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_CHAT_ID = -1001678704994  # ← Только этот Telegram-чат

# 🔧 Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# 📂 Загружаем обучающий контекст из файла
with open("clean_chat.txt", "r", encoding="utf-8") as f:
    base_context = f.read()

# 🧠 Генерация ответа с GPT-3.5
def generate_reply(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # ← GPT-4 заменили на 3.5
        messages=[
            {"role": "system", "content": base_context},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message["content"]

# 📩 Ответ только в заданном чате
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return  # игнорируем чужие чаты

    try:
        reply = generate_reply(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Kļūda: {str(e)}")

# ▶️ Запуск
print("🤖 Бот запущен и слушает чат...")
bot.polling()
