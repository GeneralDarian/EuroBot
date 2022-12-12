import logging
import os

import discord
from discord import bot
from discord.ext import commands

from tools import textHelp


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command()
    async def help(self, ctx):
        help_text = textHelp.help_text
        emote_id = os.getenv("HELP_EMOTE_ID")
        embed = discord.Embed(
            title="""EuroBot Help""", description=help_text, color=0xFFCC00
        )
        embed.set_footer(text="EuroBot Version 1.1")
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(HelpCommand(client))
