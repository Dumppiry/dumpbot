import discord
import logging
from discord import app_commands
from util import config, get_logger
from .commands import dev_commands, commands

MY_GUILD = discord.Object(id=config.GUILD_ID)


class Dumpbot(discord.Client):
    logger: logging.Logger

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.logger = get_logger()
        self.tree = app_commands.CommandTree(client=self)

    async def on_ready(self):
        self.logger.info(f"Logged on as {self.user}")

    async def setup_hook(self):
        # Load development commands
        if config.ENV == "DEV":
            self._load_dev_commands()
            self.logger.info("Loaded development commands")
        # Load commands
        self._load_commands()
        self.logger.info("Loaded regular commands")

        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    def _load_dev_commands(self):
        for command in dev_commands:
            self.tree.add_command(command)

    def _load_commands(self):
        for command in commands:
            self.tree.add_command(command)

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
