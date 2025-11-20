import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from lexicon.lexicon_ru import LEXICON_RU
from states.states import UserStates
from config.config import ADMIN_ID

router = Router()
logger = logging.getLogger(__name__)


# Функция для создания инлайн-клавиатуры для главного меню
def get_start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=LEXICON_RU['feedback_channel_button'], url='https://t.me/ArtemDevvvfeedback'),
            InlineKeyboardButton(text=LEXICON_RU['leave_feedback_button'], callback_data='start_feedback'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# Функция для создания инлайн-клавиатуры после отправки отзыва
def get_feedback_sent_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text=LEXICON_RU['feedback_channel_button'], url='https://t.me/ArtemDevvvfeedback'),
            InlineKeyboardButton(text=LEXICON_RU['main_menu_button'], callback_data='main_menu')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Команда /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started bot.")
    await state.clear() # Очищаем состояние, если пользователь вводит /start
    await message.answer(LEXICON_RU['start_message'], reply_markup=get_start_keyboard())

# Команда /cancel
@router.message(Command(commands='cancel'), ~F.text.startswith('/admin'))
async def process_cancel_command(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} canceled current action.")
    await state.clear() # Очищаем состояние
    await message.answer(LEXICON_RU['canceled'])
    # Возвращаем пользователя к главному меню с кнопкой "Оставить отзыв"
    await message.answer(LEXICON_RU['start_message'], reply_markup=get_start_keyboard())


# Этот хэндлер будет ловить отзыв от пользователя
@router.message(UserStates.waiting_for_feedback)
async def process_user_feedback(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    username_tag = f"@{message.from_user.username}" if message.from_user.username else "нет username"

    logger.info(f"User {user_id} sent feedback.")

    # Отправляем подтверждение пользователю с кнопками
    await message.answer(LEXICON_RU['thanks_for_feedback'], reply_markup=get_feedback_sent_keyboard())

    # Отправляем отзыв администратору как пересланное сообщение
    if ADMIN_ID:
        try:
            # Отправляем информацию о пользователе администратору
            await bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Новый отзыв от пользователя: {user_name} (ID: {user_id}, {username_tag})\n\n"
                     f"Сообщение:"
            )
            # Пересылаем оригинальное сообщение с отзывом
            await bot.forward_message(
                chat_id=ADMIN_ID,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            logger.info(f"Feedback from {user_id} forwarded to admin {ADMIN_ID}.")
        except Exception as e:
            logger.error(f"Error sending feedback to admin {ADMIN_ID} from user {user_id}: {e}", exc_info=True)
            await message.answer("Произошла ошибка при отправке отзыва администратору. Пожалуйста, попробуйте позже.")

    await state.clear() # Очищаем состояние после получения отзыва


# Этот хэндлер будет срабатывать на нажатие кнопки "Оставить отзыв"
@router.callback_query(F.data == 'start_feedback')
async def process_start_feedback_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} clicked 'Leave Feedback' button.")
    await callback.answer() # Отвечаем на callbackQuery
    await callback.message.answer(LEXICON_RU['request_feedback'])
    await state.set_state(UserStates.waiting_for_feedback)


# Этот хэндлер будет срабатывать на нажатие кнопки "Главное меню"
@router.callback_query(F.data == 'main_menu')
async def process_main_menu_callback(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} clicked 'Main Menu' button.")
    await callback.answer() # Отвечаем на callbackQuery
    await state.clear() # Убедимся, что состояние очищено
    await callback.message.answer(LEXICON_RU['start_message'], reply_markup=get_start_keyboard())

