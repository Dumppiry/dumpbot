import discord
from discord import app_commands
from util import config

MY_GUILD = discord.Object(id=config.GUILD_ID)


class Dumpbot(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(client=self)

    async def setup_hook(self):
        # Here we can add commands
        self.tree.add_command(
            app_commands.Command(
                name="ping", description="A simple ping command", callback=self.ping
            )
        )
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")


def get_client():
    intents = discord.Intents.default()
    intents.message_content = True
    client = Dumpbot(intents=intents)

    return client
