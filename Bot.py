import os
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

AFFILIATE_LINKS = {
    "rozetka": "https://rozetka.com.ua/",
    "aliexpress": "https://aliexpress.com/",
    "cashback": "https://letyshops.com/",
}


@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🛒 Rozetka — знижки", callback_data="rozetka"),
        types.InlineKeyboardButton("📦 AliExpress — промокоди", callback_data="aliexpress"),
        types.InlineKeyboardButton("💰 Кешбек-сервіс", callback_data="cashback"),
    )
    bot.send_message(
        message.chat.id,
        "Привіт! 👋\n\nЯ допоможу знайти знижки та промокоди на популярні магазини.\nОбери категорію нижче 👇",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data in AFFILIATE_LINKS:
        link = AFFILIATE_LINKS[call.data]
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"Ось твоє посилання зі знижкою 👇\n{link}\n\nКупуй за цим посиланням — так магазин бачить, що ти прийшов від нас 😉",
        )


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    query = message.text
    bot.send_message(
        message.chat.id,
        f"Шукаю знижки на «{query}»...\n\n(поки що ця функція в розробці — обери категорію через /start)",
    )


if __name__ == "__main__":
    print("Бот запущено.")
    bot.infinity_polling()
