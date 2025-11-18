# main.py
import asyncio
import logging # Импортируем модуль логирования
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config.config import BOT_TOKEN
from handlers import private_user, admin
# from states.states import UserStates # Нет необходимости импортировать сюда, если не используем напрямую
# from lexicon.lexicon_ru import LEXICON_RU # Нет необходимости импортировать сюда

# Настраиваем логирование
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)


# Инициализируем хранилище (в данном случае - оперативная память)
dp = Dispatcher(storage=MemoryStorage())
# Инициализируем бота с использованием DefaultBotProperties
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


# Регистрируем роутеры
dp.include_router(private_user.router)
dp.include_router(admin.router)

# Функция для установки начальных команд для бота
async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        {"command": "start", "description": "Начать общение / Оставить отзыв"},
        {"command": "cancel", "description": "Отменить текущее действие"},
    ])
    logger.info("Default commands set.")

# Запуск бота
async def main():
    logger.info("Bot starting...")
    # Устанавливаем команды
    await set_default_commands(bot)
    # Очищаем все незавершенные FSM состояния при запуске бота
    # Это важно, чтобы при перезапуске бота пользователи не зависали в старых состояниях
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped by KeyboardInterrupt')
    except Exception as e:
        logger.exception(f"An error occurred: {e}") # Используем exception для вывода стектрейса
