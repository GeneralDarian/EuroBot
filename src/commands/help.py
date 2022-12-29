import logging
from os import path

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands

from custom_types import CaseInsensitiveDict
from tools import textHelp

descriptions = CaseInsensitiveDict(
    {
        "banknote": textHelp.help_banknote_text,
        "demintmark": textHelp.help_demintmark_text,
        "info": textHelp.help_info_text,
    }
)


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
        autocomplete=discord.utils.basic_autocomplete(descriptions.keys()),
        required=False,
        default=None,
    )
    async def help(self, ctx, command: str):
        description = (
            textHelp.help_text
            if command is None
            else descriptions.get(
                command,
                f"No help information for the command `/{command}`. Run `/help` for a full list of commands.",
            )
        )

        page = "EuroBot" if command is None else f"/{command}"
        embed = discord.Embed(
            title=f"{page} Help", description=description, color=0xFFCC00
        )
        embed.add_default_footer()
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(HelpCommand(client))
