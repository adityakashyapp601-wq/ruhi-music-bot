import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
API_ID = int(os.getenv('API_ID', '30137612'))
API_HASH = os.getenv('API_HASH', '8a5ff838315a4bc122dcca04f373fc5d')
BOT_TOKEN = os.getenv('BOT_TOKEN', '8500544506:AAFIf16VbGjCDH2VMy0gG6YMWbr1rujKxT0')

# Admin Configuration
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '7342935260').split(',')]

# Bot Name
BOT_NAME = 'Ruhi Music Bot'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
