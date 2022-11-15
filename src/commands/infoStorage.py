from discord.ext import commands
from discord import bot
import logging
from tools import textHelp

class StorageInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command()
    async def storage(self, ctx):  # Displays help information for storing coins
        await ctx.respond(textHelp.storage_msg_1)
        await ctx.respond(textHelp.storage_msg_2)
        return


def setup(client):
    client.add_cog(StorageInfo(client))

