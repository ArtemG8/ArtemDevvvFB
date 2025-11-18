# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Проверяем, что все необходимые переменные окружения загружены
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file")
if not ADMIN_ID:
    raise ValueError("ADMIN_ID is not set in the .env file")
if not ADMIN_PASSWORD:
    raise ValueError("ADMIN_PASSWORD is not set in the .env file")

# Преобразуем ADMIN_ID в int, так как он будет использоваться для сравнения с Telegram ID
try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("ADMIN_ID must be an integer in the .env file")


