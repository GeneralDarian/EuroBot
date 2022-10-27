#!./bin/python3

import glob
import importlib
import logging
import logging.handlers
import pathlib
import sys
from logging import Logger

import discord
from discord import app_commands

import env

MiB32 = 32 * 1024 * 1024


class EuroBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    def loadModules(self) -> None:
        func = lambda n: f"modules.{n.removesuffix('.py')}"
        modules = glob.glob("*.py", root_dir=pathlib.Path("src/modules"))
        for module in map(func, modules):
            importlib.import_module(module).init(self)

    async def setup_hook(self) -> None:
        guild = discord.Object(id=env.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def send(self, interaction, s) -> None:
        await interaction.response.send_message(s)


def initLogger(debug: bool) -> Logger:
    FMT = "[{asctime}] [{levelname:<8}] {name}: {message}"
    DATEFMT = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(FMT, DATEFMT, style="{")
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(discord.utils._ColourFormatter())
    fileHandler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=MiB32,
        backupCount=5,
    )
    fileHandler.setFormatter(formatter)

    logging.getLogger("discord").addHandler(fileHandler)
    logger = logging.getLogger("eurobot")
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    return logging.getLogger("eurobot")


def main() -> None:
    if len(sys.argv) > 2:
        print(f"Usage: {sys.argv[0]} [--debug]", file=sys.stderr)
        sys.exit(1)

    client = EuroBot(
        intents=discord.Intents.all(),
        help_command=None,
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="Help: /help"
        ),
    )

    @client.event
    async def on_ready() -> None:
        client.logger.info(f"“{client.user}” has logged in.")

    env.init()
    client.logger = initLogger(len(sys.argv) == 2 and sys.argv[1] == "--debug")
    client.loadModules()
    client.run(env.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
