import logging
import os
from os import path

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands

from tools import textHelp


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Get help for various bot commands")
    @option(
        name="command",
        description="Command to get help for",
        autocomplete=discord.utils.basic_autocomplete(["banknote"]),
        required=False,
        default=None,
    )
    async def help(self, ctx, command: str):
        descriptions = {"banknote": textHelp.help_banknote_text}

        description = (
            textHelp.help_text
            if command is None
            else descriptions.get(
                command, f"No help information for the command /{command}"
            )
        )

        page = "EuroBot" if command is None else f"/{command}"
        embed = discord.Embed(
            title=f"{page} Help", description=description, color=0xFFCC00
        )
        embed.set_footer(text="EuroBot v1.1")
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(HelpCommand(client))
