from aiogram import Router, F, types, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from firebase import check_user_exists 
from firebase import add_user
from firebase import store_message_data
from firebase import delete_message
from firebase import get_saved_message_data
from firebase import save_profile_to_firebase, get_profile_from_firebase, save_likes_to_firebase, get_likes_from_firebase, save_user_bio_to_firebase, users_ref, likes_ref
from models import profiles, like_list

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

class UserBio(StatesGroup):
    waiting_for_bio = State()

# ✅ /start Command Handler
@router.message(F.text == "/start")
async def start_command_handler(message: Message, bot: Bot, state: FSMContext):
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
        welcome_msg = await message.answer(f"{languages[user_language]["text2"]}, {full_name}!")
        logger.info(f"User {user_id} added to the database successfully.")
        await state.update_data(
            created_at=str(timestamp),
            user_id=user_id,
            full_name=full_name,
            sel_language=user_language
        )
        await state.set_state(UserBio.waiting_for_bio)

        
    else:
        welcome_msg = await message.answer(f"{languages[user_language]["welcome_back"]}, {full_name}!", reply_markup=create_menu(main_menu, user_language, "main", user_id))
        logger.info(f"User {user_id} is returning. Welcome back!")
    await delete_message(bot, logger, user_id, message_name="welcome_msg")
    store_message_data(user_id, "welcome_msg", welcome_msg.message_id, message.chat.id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

# /create_profile Команда
@router.message(F.text.startswith("/create_profile"))
async def create_profile(message: Message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    profile = {"name": name, "age": "Не указано", "bio": "Не указано", "photo": "Не добавлено"}
    
    # Локальное сохранение профиля
    profiles.append(profile)
    # Сохранение в Firebase
    save_profile_to_firebase(user_id, profile)

    await message.reply(f"🎉 Профиль для {name} создан! Используйте /update_profile для редактирования.")

# /view_profiles Команда
@router.message(F.text == "/view_profiles")
async def view_profiles(message: Message):
    response = "📇 Анкеты:\n"
    if profiles:
        for idx, profile in enumerate(profiles):
            response += f"{idx + 1}. {profile['name']}, {profile['age']} лет\nОписание: {profile['bio']}\n\n"
    else:
        response = "😕 Пока нет анкет для просмотра."

    await message.reply(response)

# /like Команда
@router.message(F.text.startswith("/like"))
async def like_user(message: Message):
    try:
        liked_user_id = message.text.split()[1]
        user_id = str(message.from_user.id)
        like_list.add_like(liked_user_id)
        likes = like_list.get_likes()
        save_likes_to_firebase(user_id, likes)

        await message.reply(f"❤️ Вы поставили лайк пользователю {liked_user_id}!")
    except IndexError:
        await message.reply("⚠️ Используйте команду: /like [user_id]")

# /update_profile Команда
@router.message(F.text.startswith("/update_profile"))
async def update_profile(message: Message):
    user_id = str(message.from_user.id)
    new_data = message.text.split(maxsplit=1)[1] 
    profile = get_profile_from_firebase(user_id)

    if profile:
        profile['bio'] = new_data 
        save_profile_to_firebase(user_id, profile)
        await message.reply(f"Профиль обновлен: {new_data}")
    else:
        await message.reply("Профиль не найден.")

# /delete_profile Команда
@router.message(F.text == "/delete_profile")
async def delete_profile(message: Message):
    user_id = str(message.from_user.id)
    users_ref.child(user_id).delete()
    likes_ref.child(user_id).delete()
    global profiles
    profiles = [profile for profile in profiles if str(profile['user_id']) != user_id]

    await message.reply("❌ Ваш профиль удален!")

@router.message(UserBio.waiting_for_bio)
async def receive_bio(message: Message, state: FSMContext):
    user_bio = message.text  # Save the bio text
    user_id = message.from_user.id
    data = await state.get_data()

    # Placeholder: Save the bio (replace with your own save logic)
    await save_user_bio_to_firebase(user_id, user_bio, message.from_user.full_name)

    await message.answer(languages[data['sel_language']]["text1"], reply_markup=create_menu(main_menu, data['sel_language'], "main", user_id))
    await state.clear()