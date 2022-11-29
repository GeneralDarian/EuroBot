import logging

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands

from tools import textHelp


class DeMintMark(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command(
        description="Look up the position of the German mintmark on the commemorative coin issued in the year specified."
    )
    @option(
        "year",
        description="The year the German Commemorative was minted.",
        autocomplete=discord.utils.basic_autocomplete(
            [str(y) for y in range(2005, 2023)]
        ),
        required=True,
    )
    async def demintmark(self, ctx, year):  # rare coins information command
        if int(year) < 2006 or int(year) > 2022:
            await ctx.respond("Invalid year (must be between 2005 and 2022)")
        file = discord.File(f"data/DeMintMark/{year}.png", filename="image.png")
        await ctx.respond(file=file)
        return


def setup(client):
    client.add_cog(DeMintMark(client))
