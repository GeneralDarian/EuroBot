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


"""___***EUROBOT HELP MENU***___

**Non-Information commands**
    <:emote:{int(emote_id)}> ``/search`` - Look up euro coin designs from numista's coin database. Run ``/search help`` for more information on how to use this commnad.

    <:emote:{int(emote_id)}> ``/banknote <banknote serial>`` - Display euro banknote statistics given its serial number.

    <:emote:{int(emote_id)}> ``eur!tocoin`` - Convert an image to a 2 euro coin. Run ``eur!tocoin help`` for more information on how to use this command.
    (Beware this is not a slash command) 

**Information commands**
    <:emote:{int(emote_id)}> ``/clean`` - Information on cleaning coins.

    <:emote:{int(emote_id)}> ``/crh`` - Information on coin roll hunts.

    <:emote:{int(emote_id)}> ``/rare`` - Information on rare euro coins.

    <:emote:{int(emote_id)}> ``/storage`` - Information on storing coins properly.

    <:emote:{int(emote_id)}> ``/info`` - Displays bot and server information.

    <:emote:{int(emote_id)}> ``/fotw`` - Displays information on find of the week."""
