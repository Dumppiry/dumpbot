from dotenv import dotenv_values
from dataclasses import dataclass
from .file_utils import get_root_dir

config_values = dotenv_values(f"{get_root_dir()}/.env")


@dataclass
class Config:
    DISCORD_TOKEN: str
    GUILD_ID: str


config = Config(**config_values)
