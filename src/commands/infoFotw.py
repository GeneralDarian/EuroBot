from discord.ext import commands
import logging
from tools import findOfTheWeek

class FotwInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @commands.command()
    async def fotw(self, ctx):
        emote_id = findOfTheWeek.EMOTE_ID
        channel_id = findOfTheWeek.CHANNEL_ID
        await ctx.send(
            f"""**FIND OF THE WEEK (FOTW) HELP**
Find of the Week is a system where finds are 'ranked' by the commmunity. The best find wins this week's find of the week!
For starters, post a picture of your find in <#{channel_id}>. Afterwards, other users can react to the picture with <:emote:{emote_id}> emotes!
On Sundays, the find with the most emotes wins!"""
    )


def setup(client):
    client.add_cog(FotwInfo(client))
