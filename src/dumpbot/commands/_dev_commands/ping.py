import discord
from discord import app_commands


async def callback(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


ping = app_commands.Command(
    name="ping", description="A simple ping command", callback=callback
)
