import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


if not BOT_TOKEN or not CHAT_ID:
    raise Exception("BOT_TOKEN or ADMIN_ID is not set")
