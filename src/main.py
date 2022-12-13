#!/usr/bin/env python3.10

import logging
import os
from os import path

import discord
from dotenv import load_dotenv


def main():
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True

    BOT_NAME = "EuroBot"

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    activity = discord.Activity(type=discord.ActivityType.playing, name="Help: /help")
    client = discord.Bot(
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

    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
