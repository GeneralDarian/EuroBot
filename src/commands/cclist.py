import logging

import discord
from discord.ext import commands

from tools import textHelp


class CCList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @commands.message_command()
    @commands.has_permissions(administrator=True)
    async def Approve(self, ctx, msg: discord.Message):
        """Processes an image using Frakkur's image to 2-euro coin program."""
        await ctx.respond(
            "Select the country where the cc was minted in.",
            ephemeral=True,
            view=CountryDropDown(),
        )

    def getcountries(self):
        wb = xl.load_workbook(filename="_r_Eurocoins CC 2022.xlsx")
        ws = wb.active
        countries = []
        for col, cell in enumerate(ws["A"]):
            if col < 20:
                continue
            if cell.value not in countries and cell.value is not None:
                countries.append(cell.value)
        return countries

    def gettypes(self, country: str):
        wb = xl.load_workbook(filename="_r_Eurocoins CC 2022.xlsx")
        ws = wb.active
        types = []
        for col, cell in enumerate(ws["A"]):
            if cell.value != country:
                continue
            types.append(ws[f"C{col + 1}"].value)
        print(types)


class CountryDropDown(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CountryDropDownSub())


class CountryDropDownSub(discord.ui.Select):
    def __init__(self):
        country_list = []
        country_list_assembly = []
        wb = xl.load_workbook(filename="_r_Eurocoins CC 2022.xlsx")
        ws = wb.active
        for col, cell in enumerate(ws["A"]):
            if col < 20:
                continue
            if cell.value not in country_list_assembly and cell.value is not None:
                country_list_assembly.append(cell.value)
                country_list.append(
                    discord.SelectOption(
                        label=cell.value,
                        emoji=textHelp.french_to_emoji[
                            textHelp.country_to_french[cell.value]
                        ],
                    )
                )
        country_list.append(
            discord.SelectOption(
                label="Germany",
                emoji=textHelp.french_to_emoji[textHelp.country_to_french["Germany"]],
            )
        )

        super().__init__(
            placeholder="Choose a search result for more detailed information",
            options=country_list,
        )

    async def callback(self, interaction):
        await interaction.response.send_message(
            content="test!", view=GermanMintmarkDropdown(), ephemeral=True
        )


class GermanMintmarkDropdown(discord.ui.View):
    options = []
    if len(options) == 0:
        options.append(discord.SelectOption(label="A", emoji="🇦"))
        options.append(discord.SelectOption(label="D", emoji="🇩"))
        options.append(discord.SelectOption(label="F", emoji="🇫"))
        options.append(discord.SelectOption(label="G", emoji="🇬"))
        options.append(discord.SelectOption(label="J", emoji="🇯"))

    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="Select a mintmark", min_values=1, max_values=1, options=options
    )
    async def select_callback(self, select, interaction):
        await interaction.message.edit(content="test!")


def setup(client):
    client.add_cog(CCList(client))
