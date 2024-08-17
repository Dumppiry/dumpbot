import discord
import logging
from dumpbot import Dumpbot
from util import config, create_logger, get_logger


def main():
    logger = get_logger()
    dc_logger = create_logger("discord", level=logging.WARNING)
    intents = discord.Intents.default()
    intents.message_content = True
    logger.info("Starting Dumpbot")
    client = Dumpbot(intents=intents)
    client.run(token=config.DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
