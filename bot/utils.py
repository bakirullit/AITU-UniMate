# utils.py
import asyncio
from aiogram import Bot
import json
import os
import logging

def get_logger(package_name):
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(package_name)

async def send_self_destructive_message(bot: Bot, chat_id: int, text: str, time: int):
    """
    Sends a message that will be automatically deleted after a specified time.
    
    :param bot: The Bot instance to send and delete the message.
    :param chat_id: The chat ID where the message will be sent.
    :param text: The message text.
    :param time: The time in seconds after which the message will be deleted.
    """
    # Send the message
    sent_message = await bot.send_message(chat_id, text)
    
    # Wait for the specified time
    await asyncio.sleep(time)
    
    # Delete the message
    await bot.delete_message(chat_id, sent_message.message_id)
    print(f"Message deleted after {time} seconds.")

def load_languages(languages_path: str = "bot/languages") -> dict:
    """
    Load all language files from the specified folder.

    Args:
        languages_path (str): Path to the folder containing language files.

    Returns:
        dict: A dictionary where keys are language codes and values are the translations.
    """
    languages = {}
    for filename in os.listdir(languages_path):
        if filename.endswith(".json"):
            lang_code = os.path.splitext(filename)[0]  # Get language code from filename
            file_path = os.path.join(languages_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as lang_file:
                    languages[lang_code] = json.load(lang_file)  # Load translations
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return languages

def load_menu_structure(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_language(file_name):
    with open(f"bot/languages/{file_name}.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
async def delete_last_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"Message {message_id} deleted successfully in chat {chat_id}.")
    except Exception as e:
        print(f"Failed to delete message {message_id} in chat {chat_id}: {e}")
