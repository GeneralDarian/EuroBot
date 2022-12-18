import logging
from os import path

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands

from tools import textHelp

descriptions = {
    "cleaning": textHelp.info_cleaning_text,
    "mintmarks": textHelp.info_mintmarks_text,
}


class InfoCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Get help for various bot commands")
    @option(
        name="topic",
        description="Topic to get information on",
        autocomplete=discord.utils.basic_autocomplete(descriptions.keys()),
        required=True,
        default=None,
    )
    async def info(self, ctx, topic: str):
        embed = discord.Embed(
            title=f"“{topic.title()}” Title Page",
            description=descriptions.get(
                topic, f"No information found for the topic “{topic}”."
            ),
            color=0xFFCC00,
        )
        embed.set_footer(text=self.client.version)
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(InfoCommand(client))
