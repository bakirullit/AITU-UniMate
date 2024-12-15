import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase
cred = credentials.Certificate("config_files/firebase_security_key.json")
initialize_app(cred)
db = firestore.client()

# Bot token
API_TOKEN = "config_files/.env"

# Logging
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher setup
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Load language files
def load_language(lang_code):
    try:
        with open(f"{lang_code}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Language file {lang_code}.json not found.")
        return {}

# Define states for the form
class Form(StatesGroup):
    language = State()
    name = State()
    age = State()
    course = State()
    photo = State()
    bio = State()

# Recursive menu handler
def create_menu(options, level=0):
    if level >= len(options):
        return ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options[level]:
        keyboard.add(KeyboardButton(option))

    return keyboard

# Start command handler
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = create_menu([[
        "KZ", "RU", "EN"]])
    await Form.language.set()
    await message.answer("\U0001F1F0\U0001F1FF \U0001F1F7\U0001F1FA \U0001F1EC\U0001F1E7 \nChoose your language / Выберите язык:", reply_markup=keyboard)

@dp.message_handler(state=Form.language)
async def select_language(message: types.Message, state: FSMContext):
    selected_language = message.text
    if selected_language not in ["KZ", "RU", "EN"]:
        await message.answer("Please select a valid language.")
        return

    await state.update_data(language=selected_language)
    language_data = load_language(selected_language.lower())
    if not language_data:
        await message.answer("Language file missing or invalid. Defaulting to English.")
        language_data = load_language("en")

    await Form.next()
    await message.answer(language_data.get("start_name", "What is your name?"))

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "EN").lower()
    language_data = load_language(language)

    await state.update_data(name=message.text)
    await Form.next()
    await message.answer(language_data.get("ask_age", "How old are you?"))


@dp.message_handler(state=Form.course)
async def process_course(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "EN").lower()
    language_data = load_language(language)

    await state.update_data(course=message.text)
    await Form.next()
    await message.answer(language_data.get("ask_photo", "Please send your photo."))

@dp.message_handler(content_types=['photo'], state=Form.photo)
async def process_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "EN").lower()
    language_data = load_language(language)

    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await Form.next()
    await message.answer(language_data.get("ask_bio", "Tell us about yourself."))

@dp.message_handler(state=Form.bio)
async def process_bio(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "EN").lower()
    language_data = load_language(language)

    user_data['bio'] = message.text

    # Save to Firebase
    db.collection('profiles').add(user_data)

    await message.answer(language_data.get("profile_saved", "Your profile has been saved."))
    await state.finish()

# Run the bot
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
