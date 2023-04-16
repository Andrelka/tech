import logging
import openai
import telegram
from telegram.ext import Updater, MessageHandler, filters
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

openai.api_key = "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"

# Создаем объект Updater и передаем ему токен бота
app = ApplicationBuilder().token("6255467470:AAFP8SWHFJ-IFUioTX8StONsnsRGBZNCC_c").build()


# Инициализация токена бота
API_TOKEN = '6255467470:AAFP8SWHFJ-IFUioTX8StONsnsRGBZNCC_c'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализация API OpenAI
# openai.api_key = 'your_openai_api_key_here'

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Класс для хранения состояния пользователей
class QueryState(StatesGroup):
    waiting_for_query = State()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    # Отправляем приветственное сообщение пользователю
    await message.reply("Привет! Я бот, который может отвечать на ваши вопросы. О чем бы вы хотели спросить?")

    # Переводим бота в состояние ожидания запроса
    await QueryState.waiting_for_query.set()

# Обработчик текстовых сообщений
@dp.message_handler(state=QueryState.waiting_for_query)
async def echo_message_handler(message: types.Message, state: FSMContext):
    try:
        # Получаем текст запроса
        query = message.text

        # Генерируем ответ на основе запроса
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7
        )
        generated_text = response.choices[0].text.strip()

        # Отправляем ответ пользователю
        await message.reply(generated_text)

        # Сбрасываем состояние бота
        # await state.finish()
    except Exception as e:
        # Обработка ошибок
        error_message = f"Произошла ошибка: {str(e)}"
        await message.reply(error_message)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
