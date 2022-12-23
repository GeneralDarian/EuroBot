import logging
from os import path

import discord
from discord import Embed
from discord.ext import commands


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

        if (
            msg.content.startswith("eur!")
            or msg.content.startswith("Eur!")
            or msg.content.startswith("€!")
        ):
            embed = discord.Embed(
                title="EuroBot 1.1 has switched to slash commands!",
                description="""EuroBot 1.1 was released on **November 20th, 2022**. With it, we have officially switched to _slash commands_. 
                
Slash commands offer better syntax, more concise arguments, and allow us to add buttons and other cool features to embeds. The old `eur!` and `€!` have thus been replaced.

To execute a slash command, simply use the `/` prefix instead. Most commands in v1.1 still operate the same as they did pre-slash commads, but if you need help, feel free to issue `/help`.""",
                color=0xFFCC00,
            )
            await msg.channel.send(embed=embed)


def setup(client):
    client.add_cog(SlashCMD(client))
