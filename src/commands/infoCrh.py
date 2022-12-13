import logging
from os import path

import discord
from discord import Embed, SelectOption, bot, ui
from discord.ext import commands

from tools import textHelp


class CRHInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(
        description="Display information about Coin Roll Hunting (CRH) in the EU."
    )
    async def crh(self, ctx):  # coin roll hunting information command
        embed = Embed(
            title="🇪🇺 Coin Roll Hunting in the EU - General Information",
            description=textHelp.crh_info,
            color=0xFFCC00,
        )
        await ctx.respond(embed=embed, view=CRHDropDown())
        return


class CRHDropDown(discord.ui.View):
    options = []
    for country in textHelp.country_to_french:
        if country == "sanmarino":
            title = "San Marino"
        else:
            title = country
        options.append(
            SelectOption(
                label=title.title(),
                description=f"Information about coin roll hunting in {title.title()}",
                emoji=textHelp.french_to_emoji[textHelp.country_to_french[country]],
            )
        )

    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="Select a country for more detailed information",
        min_values=1,
        max_values=1,
        options=options,
    )
    async def select_callback(self, select, interaction):
        await interaction.message.edit(
            content=None, embed=self.crh_info_embed_maker(select.values[0])
        )
        await interaction.response.defer(ephemeral=True)

    def crh_info_embed_maker(self, country: str):
        french_name = textHelp.country_to_french[country]
        if french_name == "pays-bas":
            country = "The Netherlands"
        elif french_name == "saint-marin":
            country = "San Marino"
        embed = discord.Embed(
            title=f"{textHelp.french_to_emoji[french_name]} Coin Roll Hunting in {country.title()}",
            description=textHelp.french_to_crhhelp[french_name],
            color=0xFFCC00,
        )
        return embed

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content=None, view=self)


def setup(client):
    client.add_cog(CRHInfo(client))
