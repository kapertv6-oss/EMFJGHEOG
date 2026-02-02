import telebot

TOKEN = "7872623247:AAEth4pJELZdmyQfcYUf8c3Kzdo77uaAoYw"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! 👋\nЯ простой тестовый бот."
    )

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(
        message.chat.id,
        f"Ты написал: {message.text}"
    )

bot.infinity_polling()
