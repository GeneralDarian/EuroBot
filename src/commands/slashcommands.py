import logging
from os import path

import discord
from discord import Embed
from discord.ext import commands

from tools import textHelp


class SlashCMD(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Don’t react to a bots message
        if msg.author.bot:
            return

        s = msg.casefold()
        if s.startswith("eur!") or s.startswith("€!"):
            embed = discord.Embed(
                title="EuroBot 1.1 has switched to slash commands!",
                description=textHelp.slashcommands_notice,
                color=0xFFCC00,
            )
            embed.add_default_footer()
            await msg.channel.send(embed=embed)


def setup(client):
    client.add_cog(SlashCMD(client))
