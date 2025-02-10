import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Инициализация игры
cities = set()
last_city = ""

with open(file='Путь к текстовому файлу с городами', encoding='utf-8', mode="r") as filepipka:
    bot_cities = [city.strip() for city in filepipka.readlines()]

def get_valid_last_letter(city: str) -> str:
    last_letter = city[-1].lower()
    if last_letter in ('ь', 'й', 'ы'):
        return city[-2].lower() if len(city) > 1 else ''
    return last_letter

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Играем в города. Напиши город, и я продолжу!')

async def city_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global last_city
    user_city = update.message.text.strip()

    if user_city in cities:
        await update.message.reply_text('Этот город уже был. Попробуй другой!')
        return

    if last_city and user_city[0].lower() != get_valid_last_letter(last_city):
        await update.message.reply_text(f'Город должен начинаться с буквы "{get_valid_last_letter(last_city)}".')
        return

    cities.add(user_city)
    last_city = user_city

    # Фильтруем города для бота
    valid_last_letter = get_valid_last_letter(last_city)
    available_bot_cities = [city for city in bot_cities if city not in cities and city[-1].lower() == valid_last_letter]

    if available_bot_cities:
        bot_city = random.choice(available_bot_cities)
        cities.add(bot_city)
        last_city = bot_city
        await update.message.reply_text(
            f'Отлично! Теперь мой город: {bot_city}. Твой ход! Новый город должен начинаться на "{valid_last_letter}".')
    else:
        await update.message.reply_text('У меня не осталось городов для игры. Ты победил!')

def main() -> None:
    application = ApplicationBuilder().token("7642651035:AAF93MlLgjsvkqrWF6BqA47NMPhpaO_zKbg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, city_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
