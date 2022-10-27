import glob
import importlib
import logging
import logging.handlers
import pathlib
from logging import Logger

import discord
from discord import app_commands

import env


class EuroBot(discord.Client):
    name = "eurobot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    def loadModules(self) -> None:
        func = lambda n: f"modules.{n.removesuffix('.py')}"
        modules = glob.glob("*.py", root_dir=pathlib.Path("src/modules"))
        for module in map(func, modules):
            self.logger.info(f"Importing module “{module}”")
            importlib.import_module(module).init(self)

    def initLogger(self, debug: bool) -> None:
        MiB32 = 32 * 1024 * 1024
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
        self.logger = logging.getLogger(EuroBot.name)
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)

    async def setup_hook(self) -> None:
        guild = discord.Object(id=env.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def send(self, interaction, s) -> None:
        await interaction.response.send_message(s)
