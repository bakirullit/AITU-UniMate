from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Config(BaseSettings):
    bot_token: str
    class Config:
        env_file = ".env"
