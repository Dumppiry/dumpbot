import discord
import json
import logging
import random
from discord import app_commands
from util import config, get_logger
from .commands import dev_commands, commands
from models import EventFeed, Event

MY_GUILD = discord.Object(id=config.GUILD_ID)


class Dumpbot(discord.Client):
    logger: logging.Logger
    tree: app_commands.CommandTree
    event_post_channel: discord.TextChannel | None = None

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

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        # Read bot feed only if message has no reference and message is from bot.
        if (
            message.channel.name == "bot-feed"
            and message.reference is None
            and message.author.bot
        ):
            try:
                content_dict: dict = json.loads(message.content)
                self.logger.info(f"Received bot-feed: {content_dict}")
                # Handle different types of feeds
                match content_dict.get("type"):
                    case "event_feed":
                        await self.handle_event_feed(message=message)
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid json received on bot-feed: {e}")
                await message.reply(f"Invalid json: {e}")

    async def handle_event_feed(self, message: discord.Message):
        hype_endings = {
            "tulee räjäyttämään tajunnan!",
            "on tulossa, älä missaa tätä!",
            "lyö sinut ällikällä!",
            "on tulossa, ole valmiina!",
            "laittaa jyväskylän sekaisin!",
            "saa sinut vapisemaan!",
            "on skibidi bop sigma event!",
        }
        self.logger.info("Handling event_feed message.")
        content_dict: dict = json.loads(message.content)
        if not content_dict.get("event"):
            self.logger.error("bot-feed of type event_feed is missing 'event'")
            return
        try:
            feed_data = EventFeed(**content_dict)
            event: Event = Event(**content_dict["event"])
            if (
                self.event_post_channel is None
                or self.event_post_channel.name != feed_data.post_to
            ):
                self.logger.info(f"Looking for channel: {feed_data.post_to}")
                self.event_post_channel = self.get_channel(feed_data.post_to)
                if self.event_post_channel is None:
                    self.logger.error(
                        f"Could not find channel: {feed_data.post_to}"
                    )
                    await message.reply(
                        f"Could not find channel: {feed_data.post_to}",
                        allowed_mentions=discord.AllowedMentions(
                            users=True, roles=True
                        ),
                    )
                    return
            match feed_data.modified:
                case "":
                    hype = random.choice(hype_endings)
                    catch_line = (
                        f"Uusi tapahtuma julkaistiin! {event.title} {hype}"
                    )
                case "price":
                    catch_line = f"Tapahtuman {event.title} hinta muuttui!"
                case "date":
                    catch_line = f"Tapahtuman {event.title} päivämäärä muuttui!"
                case "ticket_sale":
                    catch_line = (
                        f"Tapahtuman {event.title} lipunmyyntiä muutettiin!"
                    )
                case _:
                    pass
            response = await self.event_post_channel.send(
                content=f"{catch_line}\n\n *Tapahtuma päivittymiseen nettisivuille voi mennä muutama minuutti.*",
                embed=event.to_embed(),
            )

        except TypeError as e:
            self.logger.error(f"Error parsing event_feed: {e}")
            await message.reply(f"Error parsing event_feed: {e}")
