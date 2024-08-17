import os
from dotenv import dotenv_values
from dataclasses import dataclass
from .file_utils import get_root_dir
from .create_logger import create_logger

logger = create_logger()
env = os.getenv("PYENV", "DEV")
dotenv_file = ".env" if env == "PROD" else ".env.dev"
logger.info(f"Loading environment variables from {dotenv_file}")
config_values = dotenv_values(f"{get_root_dir()}/{dotenv_file}")


@dataclass
class Config:
    DISCORD_TOKEN: str
    GUILD_ID: str
    ENV: str = "DEV"

    def __init__(
        self,
        GUILD_ID: str,
        DISCORD_TOKEN: str | None = None,
    ):
        self.DISCORD_TOKEN = DISCORD_TOKEN
        self.GUILD_ID = GUILD_ID
        self.ENV = env


config = Config(**config_values)
