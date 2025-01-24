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

def search_user_bios(user_bios, keywords):
    
    results = []
    
    for user_id, bio in user_bios:
        matched_kws = []
        lower_bio = bio.lower()
        
        for kw in keywords:
            if kw.lower() in lower_bio:
                matched_kws.append(kw)
        
        if matched_kws:
            results.append((user_id, matched_kws))
    
    return results
def bubble_sort(items, key):
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j][key] > items[j + 1][key]:
                items[j], items[j + 1] = items[j + 1], items[j]

def merge_sort(items, key):
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left_half = merge_sort(items[:mid], key)
    right_half = merge_sort(items[mid:], key)
    
    return merge(left_half, right_half, key)

def merge(left, right, key):
    sorted_list = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i][key] < right[j][key]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
    
    while i < len(left):
        sorted_list.append(left[i])
        i += 1
    while j < len(right):
        sorted_list.append(right[j])
        j += 1
    
    return sorted_list

def quick_sort(items, key, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low < high:
        p = partition(items, key, low, high)
        quick_sort(items, key, low, p - 1)
        quick_sort(items, key, p + 1, high)

def partition(items, key, low, high):
    pivot = items[high][key]
    i = low - 1
    for j in range(low, high):
        if items[j][key] < pivot:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[i + 1], items[high] = items[high], items[i + 1]
    return i + 1

def linear_search(items, key, target, partial=False):
    results = []
    for item in items:
        value = str(item[key]).lower()
        target_str = str(target).lower()
        if partial:
            if target_str in value:
                results.append(item)
        else:
            if value == target_str:
                results.append(item)
    return results

def binary_search(items, key, target):
    low = 0
    high = len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid][key] == target:
            return items[mid]
        elif items[mid][key] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None