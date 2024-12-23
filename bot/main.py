from aiogram import Bot, Dispatcher

import handlers
import callback_manager
from config import Config

from utils import get_logger

logger = get_logger(__name__)

# Initialize bot configuration
config = Config()

bot = Bot(token=config.bot_token)
dp = Dispatcher()

async def main():
    dp.include_router(callback_manager.router)
    dp.include_routers(handlers.router)
    logger.info("Bot is starting...")  # Log startup message
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
