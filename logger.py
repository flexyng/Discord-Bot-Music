import logging
from datetime import datetime
import os

PRODUCTION = os.getenv('ENVIRONMENT', 'production') == 'production'

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"music_bot_{datetime.now().strftime('%Y%m%d')}.log")

logger = logging.getLogger("MusicBot")
logger.setLevel(logging.DEBUG if not PRODUCTION else logging.INFO)
logger.propagate = False

file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.INFO if not PRODUCTION else logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO if not PRODUCTION else logging.WARNING)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_command(user: str, command: str, guild: str = None):
    logger.info(f"Command: {command} | User: {user} | Guild: {guild}")

def log_error(error: str, context: str = None):
    logger.error(f"Error: {error} | Context: {context}")

def log_music_event(event: str, user: str, song: str = None):
    logger.info(f"Music Event: {event} | User: {user} | Song: {song}")
