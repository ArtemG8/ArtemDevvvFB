# handlers/admin.py
import logging # Импортируем модуль логирования
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from lexicon.lexicon_ru import LEXICON_RU
from states.states import AdminStates
from config.config import ADMIN_ID, ADMIN_PASSWORD

router = Router()
logger = logging.getLogger(__name__)


# Этот хэндлер будет срабатывать на команду /admin
@router.message(Command(commands='admin'))
async def process_admin_command(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        logger.info(f"Admin {message.from_user.id} attempted to access admin panel.")
        await message.answer(LEXICON_RU['admin_welcome'])
        await message.answer(LEXICON_RU['admin_password_request']) # Добавим запрос пароля явно
        await state.set_state(AdminStates.waiting_for_password)
    else:
        logger.warning(f"Unauthorized access attempt to admin panel by user {message.from_user.id}.")
        await message.answer(LEXICON_RU['admin_access_denied'])

# Этот хэндлер будет ловить пароль для админки
@router.message(AdminStates.waiting_for_password)
async def process_admin_password(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        logger.info(f"Admin {message.from_user.id} granted access to admin panel.")
        await state.clear() # Очищаем состояние после успешного входа
        await message.answer(LEXICON_RU['admin_access_granted'])
        # Теперь админ авторизован, и бот не будет перехватывать его сообщения
        # как попытку ввода пароля.
    else:
        logger.warning(f"Admin {message.from_user.id} entered wrong password.")
        await message.answer(LEXICON_RU['admin_wrong_password'])
        await message.answer(LEXICON_RU['admin_password_request']) # Просим ввести снова

# Отмена действия в админке
@router.message(Command(commands='cancel'), AdminStates.waiting_for_password)
async def process_admin_cancel(message: Message, state: FSMContext):
    logger.info(f"Admin {message.from_user.id} canceled admin login.")
    await state.clear()
    await message.answer(LEXICON_RU['canceled'])

