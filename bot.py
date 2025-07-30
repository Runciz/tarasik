
import telebot
import openai
import os

# 🔑 Получаем токены и чат ID из переменных окружения или вшиваем вручную
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_CHAT_ID = -1001678704994  # ← Только этот Telegram-чат

# 🔧 Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# 📂 Загружаем контекст из файла
with open("clean_chat.txt", "r", encoding="utf-8") as f:
    base_context = f.read()

# ✅ Проверка: отвечать ли на сообщение
def should_respond(message):
    if message.chat.id != ALLOWED_CHAT_ID:
        return False
    if not message.text:
        return False
    try:
        bot_username = bot.get_me().username
    except Exception:
        return False
    return f"@{bot_username}" in message.text

# 🧠 Генерация ответа от GPT
def generate_reply(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_context},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message["content"]

# 📩 Обработка сообщений
@bot.message_handler(func=should_respond)
def handle_message(message):
    try:
        reply = generate_reply(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Kļūda: {str(e)}")

# ▶️ Запуск
print("🤖 Бот запущен и слушает чат...")
bot.polling()
