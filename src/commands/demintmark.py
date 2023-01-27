import logging
from datetime import datetime
from os import path

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands

THIS_YEAR = datetime.today().year


class DeMintMark(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Locate the mintmark on German CCs")
    @option(
        name="year",
        description="The year the German commemorative was minted.",
        autocomplete=discord.utils.basic_autocomplete(
            [str(y) for y in range(2002, THIS_YEAR + 1)]
        ),
        required=True,
    )
    async def demintmark(self, ctx, year):  # rare coins information command
        await ctx.defer()
        if not 2002 <= int(year) <= THIS_YEAR:
            await ctx.respond(f"Invalid year (must be between 2002 and {THIS_YEAR})")
        try:
            file = discord.File(
                f"data/german_mintmarks/{year}.png", filename="image.png"
            )
            await ctx.respond(file=file)
        except FileNotFoundError:
            await ctx.respond(
                f"No €2 commemorative coins were released by Germany in {year}"
            )


def setup(client):
    client.add_cog(DeMintMark(client))
