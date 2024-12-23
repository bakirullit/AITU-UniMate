from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from keyboard_builder import create_menu, create_back_button, clear_keyboard
from firebase import get_saved_message_data, save_feedback_to_database
from utils import get_logger
from utils import load_language, load_menu_structure, delete_last_message
from text_creator import create_feedback_text
from states import FeedbackStates
import time
logger = get_logger(__name__)
main_menu = load_menu_structure("bot/config_files/main_menu.json")
router = Router(name=__name__)
@router.callback_query()
async def handle_approval_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    data_parts = callback.data.split('_')
    start_time = time.time()
    logger.info(f"Callback data received: {callback.data}")
    logger.info(f"Callback data parts: {data_parts}")
    if data_parts[2] == "menu" and len(data_parts) == 4:
        user_id, selected_language, command, destination = data_parts
        messages = get_saved_message_data(user_id)
        lang = load_language(selected_language)
        print(messages)
        await bot.edit_message_text(
            chat_id=messages["welcome_msg"]['chat_id'],
            message_id=messages["welcome_msg"]['message_id'],
            text=lang[destination],
            reply_markup=create_menu(main_menu, selected_language, destination, user_id)
        )
        end_time = time.time()
        await bot.send_message(
            chat_id=messages["welcome_msg"]['chat_id'],
            text=f"Execution time: {end_time - start_time:.6f} seconds",
            reply_markup=clear_keyboard()
        )
    elif data_parts[2] == "about" and len(data_parts) == 4:
        user_id, selected_language, command, destination = data_parts
        messages = get_saved_message_data(user_id)
        lang = load_language(selected_language)
        print(messages)
        await bot.edit_message_text(
            chat_id=messages["welcome_msg"]['chat_id'],
            message_id=messages["welcome_msg"]['message_id'],
            text=lang[destination],
            reply_markup=create_menu(main_menu, selected_language, destination, user_id)
        )

    elif data_parts[1] == "action" and len(data_parts) == 4:
        if data_parts[2] == "clear":
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await callback.answer("Message cleared!")
    
    
        
    