import logging

from discord import bot
from discord.ext import commands

from tools import textHelp


class CleanInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command()
    async def clean(self, ctx):  # Displays help information for cleaning coins
        await ctx.respond(textHelp.clean_msg)
        return


def setup(client):
    client.add_cog(CleanInfo(client))
