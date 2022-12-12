import logging

from discord import bot
from discord.ext import commands

from tools import textHelp


class RareInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command()
    async def rare(self, ctx):
        await ctx.respond(textHelp.rare_coins)
        return


def setup(client):
    client.add_cog(RareInfo(client))
