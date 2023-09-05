#!/usr/bin/env python3.10

import logging
import os
from os import path

import discord
from dotenv import load_dotenv


class EuroBot(discord.Bot):
    version = "EuroBot v1.3 [2022.09.05]"


def main():
    discord.Embed.add_default_footer = lambda self: self.set_footer(
        text=EuroBot.version
    )

    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True

    load_dotenv()

    activity = discord.Activity(type=discord.ActivityType.playing, name="Help: /help")
    client = EuroBot(
        intents=intents,
        help_command=None,
        activity=activity,
    )

    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s]: %(message)s (%(filename)s:%(lineno)d)",
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )

    os.chdir(path.dirname(__file__))

    @client.event
    async def on_ready():
        logging.info(f"{client.user} has logged in")

    for filename in filter(lambda f: f.endswith(".py"), os.listdir("commands/")):
        try:
            client.load_extension(f"commands.{filename[:-3]}")
        except Exception as error:
            logging.error(f"Error loading extension: {error}")

    client.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
