import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from tools import coinData, designer, textHelp


def main():

    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True

    BOT_NAME = "EuroBot"

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    activity = discord.Activity(type=discord.ActivityType.playing, name="Help: /help")
    client = discord.Bot(
        command_prefix=["!"],
        intents=intents,
        help_command=None,
        activity=activity,
    )

    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s]: %(message)s (%(filename)s:%(lineno)d)",
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    @client.event
    async def on_ready():
        logging.info(f"{client.user} has logged in. Version {discord.__version__}")

    def load_extensions():
        for fileName in os.listdir("./commands"):
            print(fileName)
            if fileName.endswith(".py"):
                try:
                    client.load_extension(f"commands.{fileName[:-3]}")
                except Exception as error:
                    logging.error(f"Error loading extension: {error}")

    load_extensions()
    client.run(DISCORD_TOKEN)
    # client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()


def deprecated():
    """Deprecated content whiich might be brought back in the future."""
    pass
    # @client.command()
    # @commands.has_permissions(administrator=True)
    async def refreshAPI(ctx):
        coinData.refreshFiles()

    def getprefix(msg: str) -> str:
        """Returns prefix used for issued command
        Inputs: The command (message.content, MUST be string)
        Outputs: The string used"""
        if msg.startswith("eur!"):
            return "eur"
        elif msg.startswith("Eur!"):
            return "Eur"
        else:
            return "€"
