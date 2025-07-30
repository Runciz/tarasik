import telebot
import openai
import os

# 🔑 Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_CHAT_ID = -1001678704994  # ← Только этот чат

# 🔧 Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# 📂 Загружаем историю чата
with open("clean_chat.txt", "r", encoding="utf-8") as f:
    base_context = f.read()

# 🤖 Генерация ответа
def generate_reply(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": base_context},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response.choices[0].message["content"]

# 📨 Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return  # Игнорируем чужие чаты

    try:
        reply = generate_reply(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "⚠️ Kļūda: " + str(e))

# ▶️ Запуск
print("🤖 Бот запущен и слушает чат...")
bot.polling()
