import logging

from discord import bot
from discord.ext import commands

from tools import textHelp


class StorageInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command()
    async def storage(self, ctx):
        await ctx.respond(textHelp.storage_msg_1)
        await ctx.respond(textHelp.storage_msg_2)
        return


def setup(client):
    client.add_cog(StorageInfo(client))
