from discord.ext import commands
from discord.commands import Option
from discord import bot, Embed, ui, SelectOption
import discord
import logging
from tools import textHelp

class CRHInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command(description="Display information about Coin Roll Hunting (CRH) in the EU.")
    async def crh(self, ctx):  # coin roll hunting information command
        embed = Embed(
            title="🇪🇺 Coin Roll Hunting in the EU - General Information",
            description=textHelp.crh_info,
            color=0xffcc00
        )
        await ctx.respond(embed=embed, view=CRHDropDown())
        return

class CRHDropDown(discord.ui.View):

    options = []
    if len(options) == 0:
        for country in textHelp.country_to_french:
            if country == "sanmarino":
                title = "San Marino"
            else:
                title = country
            options.append(
                SelectOption(
                    label=title.title(),
                    description=f"Information about coin roll hunting in {title.title()}",
                    emoji=textHelp.french_to_emoji[textHelp.country_to_french[country]]
                )
            )
    def __init__(self):
        super().__init__()

    @discord.ui.select(
    placeholder="Select a country for more detailed information",
    min_values=1,
    max_values=1,
    options=options
    )
    async def select_callback(self, select, interaction):
        await interaction.message.edit(content=None, embed=self.crh_info_embed_maker(select.values[0]))
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
            color=0xffcc00
        )
        return embed



def setup(client):
    client.add_cog(CRHInfo(client))

