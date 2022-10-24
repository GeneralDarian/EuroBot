#!./bin/python3

import asyncio
import logging
import logging.handlers

import discord
from discord import app_commands

import env

MiB32 = 32 * 1024 * 1024
MODULES = ["misc"]


class EuroBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        guild = discord.Object(id=env.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


def init_logger():
    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=MiB32,
        backupCount=5,
    )
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", datefmt, style="{"
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def main():
    @client.event
    async def on_ready():
        client.logger.info(f"{client.user} has logged in.")

    env.init()
    client.run(env.DISCORD_TOKEN)


if __name__ == "__main__":
    client = EuroBot(
        intents=discord.Intents.all(),
        help_command=None,
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="Help: /help"
        ),
    )

    for module in MODULES:
        __import__(module).init(client)

    client.logger = init_logger()
    main()
