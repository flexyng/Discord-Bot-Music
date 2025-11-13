import logging
from datetime import datetime
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"music_bot_{datetime.now().strftime('%Y%m%d')}.log")

logger = logging.getLogger("MusicBot")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
