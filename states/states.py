# states/states.py
from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    waiting_for_feedback = State()

class AdminStates(StatesGroup):
    waiting_for_password = State()
    in_admin_panel = State()
