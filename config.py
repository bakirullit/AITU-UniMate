from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class Config(BaseSettings):
    bot_token: str

    # The bot token will be loaded from the environment variables
    class Config:
        env_file = "config_files/.env"  # Specify that the environment variables are in .env