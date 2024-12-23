from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import load_language

def create_menu(menu_structure: dict, selected_language: dict, menu_name: str, user_id: int) -> InlineKeyboardMarkup:
    keyboard = []
    language_texts = load_language(selected_language)
    menu_data = menu_structure.get(menu_name, {})
    for key, value in menu_data.items():
        translated_label = language_texts[key] # Get translation, fallback to the key if not found
        callback_data = f"{user_id}_{selected_language}_{value}"   # Append user_id to callback data
        button = InlineKeyboardButton(text=translated_label, callback_data=callback_data)
        keyboard.append([button])  # Each button in a new row

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_feedback_submit_menu(selected_language_text, selected_language, user_id, feedback_type) -> InlineKeyboardMarkup:
    base_callback = f"{user_id}_{selected_language}_{feedback_type}"

    # Buttons
    anon_button = InlineKeyboardButton(
        text=selected_language_text["remain_anonymus"],
        callback_data=f"{base_callback}_hide"
    )
    edit_button = InlineKeyboardButton(
        text=selected_language_text["edit"],
        callback_data=f"{base_callback}_resend"
    )
    cancel_button = InlineKeyboardButton(
        text=selected_language_text["cancel"],
        callback_data=f"{base_callback}_cancel"
    )
    confirm_button = InlineKeyboardButton(
        text=selected_language_text["confirm"],
        callback_data=f"{base_callback}_confirm"
    )

    # Create keyboard layout
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [edit_button, cancel_button],  # First row
        [confirm_button]  # Second row
    ])

    return keyboard

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_back_button(selected_language_text, user_id, feedback_type, command) -> InlineKeyboardMarkup:

    user_lang = selected_language_text.get("lang", "en")  # Assume 'lang' defines language
    base_callback = f"{user_id}_{user_lang}_{feedback_type}"

    # Back button
    back_button = InlineKeyboardButton(
        text=selected_language_text.get("back", "Back ⬅️"),
        callback_data=f"{base_callback}_{command}"
    )

    # Create keyboard layout
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [back_button]  # Single button in one row
    ])

    return keyboard
def clear_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Clear 🗑️", callback_data="void_action_clear_message")]
        ]
    )
    return keyboard
