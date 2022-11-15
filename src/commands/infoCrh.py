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

    @bot.command()
    async def crh(self, ctx, country:Option(str, "Enter a country for detailed information, or leave bank for general info.", required = False, default = None)):  # coin roll hunting information command
        arg1 = country
        if arg1 is None:
            embed = Embed(
                title="🇪🇺 Coin Roll Hunting in the EU - General Information",
                description=textHelp.crh_info,
                color=0xffcc00
            )
            await ctx.respond(embed=embed, view=CRHDropDown())
            return



        else:
            if arg1.lower() in textHelp.country_to_french:
                country = textHelp.country_to_french[arg1.lower()]
                await ctx.respond(textHelp.french_to_crhhelp[country])
            elif arg1.lower() in textHelp.country_id_to_french:
                country = textHelp.country_id_to_french[arg1.lower()]
                await ctx.respond(textHelp.french_to_crhhelp[country])
            else:
                await ctx.respond(
                    "You must either type a valid 2-letter country ID or the country name in English! For help with coin roll hunts use ``eur!crh``.")

class CRHDropDown(discord.ui.View):

    options = []
    if len(options) == 0:
        for country in textHelp.country_to_french:
            options.append(
                SelectOption(
                    label=country.capitalize(),
                    description=f"Information about coin roll hunting in {country.capitalize()}",
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

    def crh_info_embed_maker(self, country: str):
        french_name = textHelp.country_to_french[country.lower()]
        embed = discord.Embed(
            title=f"{textHelp.french_to_emoji[french_name]} Coin Roll Hunting in {country.capitalize()}",
            description=textHelp.french_to_crhhelp[french_name],
            color=0xffcc00
        )
        return embed



def setup(client):
    client.add_cog(CRHInfo(client))

