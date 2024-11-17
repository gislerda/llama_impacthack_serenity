import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

TG_API_ID = os.getenv("TG_API_ID")
TG_API_HASH = os.getenv("TG_API_HASH")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_database.db')

# Bot Settings
CHECK_IN_INTERVALS = [12, 24, 48]  # Hours between check-ins
MAX_CONVERSATION_HISTORY = 10  # Number of messages to keep in context
IMAGE_UPLOAD_DIR = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)