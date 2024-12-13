import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message

from config import Config

from firebase import check_user_exists 
from firebase import add_user
from firebase import store_message_data
from firebase import delete_message

from utils import send_self_destructive_message
from utils import load_languages

# Initialize logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# Load languages
languages = load_languages()
DEFAULT_LANGUAGE = "en"

# Example logger usage
logger = logging.getLogger(__name__)

# Initialize bot configuration
config = Config()

bot = Bot(token=config.bot_token)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_command_handler(message: Message):
    # Access user's information
    user_id = message.from_user.id  # Telegram user ID
    username = message.from_user.username  # Username (can be None if user doesn't have one)
    full_name = message.from_user.full_name  # First and last name (combined)

    # Log the username and ID
    logger.info(f"User {username or 'no_username'} (ID: {user_id}) started the bot.")

    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    is_bot = message.from_user.is_bot
    timestamp = message.date  # Timestamp of when the user interacted with the bot
    # Check user's default language in bot's languages
    if language_code not in languages:
        user_language = DEFAULT_LANGUAGE
    else:
        user_language = language_code
    
    commands = [
        types.InlineKeyboardButton(text=f"{languages[user_language]["register"]}", callback_data=f"start_register_{user_id}"),
        types.InlineKeyboardButton(text=f"{languages[user_language]["info"]}", callback_data=f"get_info_{user_id}"),
        types.InlineKeyboardButton(text=f"{languages[user_language]["guest"]}", callback_data=f"start_guest_{user_id}")
    ]
    commands_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button] for button in commands])
    # Check if the user exists in the database
    if not check_user_exists(user_id):
        logger.info(f"User {user_id} does not exist in the database. Adding them now.")
        add_user(user_id, username, first_name, last_name, language_code, is_bot, timestamp)
        welcome_msg = await message.answer(f"{languages[user_language]["welcome"]}, {full_name}!", reply_markup=commands_keyboard)
        logger.info(f"User {user_id} added to the database successfully.")
    else:
        welcome_msg = await message.answer(f"{languages[user_language]["welcome_back"]}, {full_name}!", reply_markup=commands_keyboard)
        logger.info(f"User {user_id} is returning. Welcome back!")
    await delete_message(bot, logger, user_id, message_name="welcome_msg")
    store_message_data(user_id, "welcome_msg", welcome_msg.message_id, message.chat.id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

async def main():
    logger.info("Bot is starting...")  # Log startup message
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
