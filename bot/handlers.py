from aiogram import Router, F, types, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from firebase import check_user_exists 
from firebase import add_user
from firebase import store_message_data
from firebase import delete_message
from firebase import get_saved_message_data

from utils import load_languages
from utils import get_logger
from utils import load_menu_structure
from utils import send_self_destructive_message
from text_creator import create_feedback_text

from keyboard_builder import create_menu, create_feedback_submit_menu

from states import FeedbackStates

logger = get_logger(__name__)

router = Router(name=__name__)

# Load languages
languages = load_languages()
DEFAULT_LANGUAGE = "ru"

main_menu = load_menu_structure("bot/config_files/main_menu.json")

@router.message(F.text == "/start")
async def start_command_handler(message: Message, bot: Bot):
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
    # Check if the user exists in the database
    if not check_user_exists(user_id):
        logger.info(f"User {user_id} does not exist in the database. Adding them now.")
        add_user(user_id, username, first_name, last_name, language_code, is_bot, timestamp)
        welcome_msg = await message.answer(f"{languages[user_language]["welcome"]}, {full_name}!", reply_markup=create_menu(main_menu, user_language, "main", user_id))
        logger.info(f"User {user_id} added to the database successfully.")
    else:
        welcome_msg = await message.answer(f"{languages[user_language]["welcome_back"]}, {full_name}!", reply_markup=create_menu(main_menu, user_language, "main", user_id))
        logger.info(f"User {user_id} is returning. Welcome back!")
    await delete_message(bot, logger, user_id, message_name="welcome_msg")
    store_message_data(user_id, "welcome_msg", welcome_msg.message_id, message.chat.id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
