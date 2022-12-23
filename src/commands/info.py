import logging
from os import path

import discord
from discord import bot
from discord.commands import option
from discord.ext import commands
from discord.ext.pages import Page, Paginator

from custom_types import CaseInsensitiveDict
from tools import textHelp

pages = CaseInsensitiveDict(
    {
        "cleaning": textHelp.info_cleaning_text,
        "mintmarks": textHelp.info_mintmarks_text,
        "rare coins": textHelp.info_rare_coins_text,
        "storage": (
            textHelp.info_storage_text_opener,
            textHelp.info_storage_text_albums,
            textHelp.info_storage_text_boxes,
            textHelp.info_storage_text_capsules,
            textHelp.info_storage_text_flips,
        ),
    }
)


class InfoCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Get help for various bot commands")
    @option(
        name="topic",
        description="Topic to get information on",
        autocomplete=discord.utils.basic_autocomplete(pages.keys()),
        required=True,
        default=None,
    )
    async def info(self, ctx, topic: str):
        if topic is None:
            embed = discord.Embed(
                title=f"Invalid `/info` Usage",
                description="No topic was provided! For help using the `/info` command, try `/help info`.",
                color=0xFFCC00,
            )
            embed.set_footer(text=self.client.version)
            await ctx.respond(embed=embed)

        data = pages.get(topic, f"No information found for the topic “{topic}”")

        if type(data) is str:
            embed = discord.Embed(
                title=f"“{topic.title()}” Info Page",
                description=data,
                color=0xFFCC00,
            )
            embed.set_footer(text=self.client.version)
            await ctx.respond(embed=embed)
        else:
            numpages = len(data)
            builtpages = []
            for i in range(numpages):
                embed = discord.Embed(
                    title=f"“{topic.title()}” Info Page [{i + 1} / {numpages}]",
                    description=data[i],
                    color=0xFFCC00,
                )
                embed.set_footer(text=self.client.version)
                builtpages.append(Page(embeds=[embed]))
            await Paginator(pages=builtpages, show_disabled=False).respond(
                ctx.interaction, ephemeral=False
            )


def setup(client):
    client.add_cog(InfoCommand(client))
