# utils.py

import asyncio
from aiogram import Bot
import json
import os
import re
from datetime import datetime

async def send_self_destructive_message(bot: Bot, chat_id: int, text: str, time: int):
    sent_message = await bot.send_message(chat_id, text)
    await asyncio.sleep(time)
    await bot.delete_message(chat_id, sent_message.message_id)
    print(f"Message deleted after {time} seconds.")

def load_languages(languages_path: str = "languages") -> dict:
    languages = {}
    for filename in os.listdir(languages_path):
        if filename.endswith(".json"):
            lang_code = os.path.splitext(filename)[0]
            file_path = os.path.join(languages_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as lang_file:
                    languages[lang_code] = json.load(lang_file)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return languages

def check_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def check_birthday(birthday):
    try:
        formatted_birthday = birthday.replace("_", "-")
        date_obj = datetime.strptime(formatted_birthday, '%m-%d-%Y')
        return date_obj <= datetime.now()
    except ValueError:
        return False

def check_username(username):
    username_regex = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(username_regex, username))

