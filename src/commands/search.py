import logging
import os
from os import path

import discord
from discord import bot
from discord.commands import Option, SlashCommandGroup, option
from discord.ext import commands, pages

from tools import coinData, textHelp


class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    search = SlashCommandGroup("search", "Use the search command!")

    @search.command(
        description="Search a coin by its Numista ID. Add year to end if mintages are difficult to sort through."
    )
    async def id(
        self,
        ctx,
        numista_id: Option(str, "The Numista ID of the coin", required=True),
        year: Option(
            int, "The year the coin was minted in", required=False, default=None
        ),
    ):
        embed = post_ID(numista_id, year)
        await ctx.respond(embed=embed)

    @search.command(
        description="Look up a euro coin in our database for information, pictures, and mintages!"
    )
    @option(
        "country",
        description="The country of the coin (can either be the name in English or the 2-letter country code",
        autocomplete=discord.utils.basic_autocomplete(
            dict.keys(textHelp.country_to_french)
        ),
        required=True,
    )
    @option(
        "year",
        description="The year the coin was minted in",
        autocomplete=discord.utils.basic_autocomplete(
            [year for year in range(1999, 2030)]
        ),
        required=False,
        default=None,
    )
    @option(
        "type",
        description="The type of coin",
        autocomplete=discord.utils.basic_autocomplete(
            [
                "1 Cent",
                "2 Cents",
                "5 Cents",
                "10 Cents",
                "20 Cents",
                "50 Cents",
                "1 Euro",
                "2 Euro",
                "2 Euro Commemorative",
            ]
        ),
        required=False,
        default=None,
    )
    async def coin(self, ctx, country: str, year: int, type: str):
        # convert type
        if type is not None and type.lower() not in textHelp.types:
            try:
                type = textHelp.from_type[type.lower()]
            except KeyError:
                await ctx.respond("Error: Invalid type entered.")
                return
        if country == "San Marino":
            country = "sanmarino"
        processed_search_list = {"Issuer": country, "Year": year, "Type": type}
        logging.info(processed_search_list)
        results = coinData.searchEngine(processed_search_list)
        if len(results) == 1:
            embed = post_ID(results[0]["id"], processed_search_list["Year"])
            await ctx.respond(embed=embed)
        elif len(results) < 1:
            await ctx.respond("Your search has yielded no results!")
        elif len(results) > 12:
            paginator = pages.Paginator(
                pages=self.result_page(results, processed_search_list)
            )
            await paginator.respond(ctx.interaction, ephemeral=False)
        else:
            embed = self.post_list_results(
                int(ctx.channel.id), results, processed_search_list
            )
            await ctx.respond(embed=embed, view=SearchDropDownView(results))

    @bot.command(
        description="Fast search (without specifying arguments) - do /search help to learn how to use this."
    )
    @option(
        "query",
        description="A shortened search query. Run /help fsearch to see what one looks like.",
        required=True,
    )
    async def fsearch(self, ctx, query):
        search_list = query.split()
        if len(search_list) > 3:
            await ctx.respond("You have added too many arguments! (max 3)")
        processed_search_list = coinData.searchProcessor(search_list)

        if processed_search_list["Status"] != "0":
            await ctx.respond(processed_search_list["Status"])
            return

        results = coinData.searchEngine(processed_search_list)
        logging.info(results)
        if len(results) == 1:
            embed = post_ID(results[0]["id"], processed_search_list["Year"])
            await ctx.respond(embed=embed)
            return
        elif len(results) < 1:
            await ctx.respond("Your search has yielded no results!")
            return
        elif len(results) > 12:
            paginator = pages.Paginator(
                pages=self.result_page(results, processed_search_list)
            )
            await paginator.respond(ctx.interaction, ephemeral=False)
            return
        else:
            embed = self.post_list_results(
                int(ctx.channel.id), results, processed_search_list
            )
            await ctx.respond(embed=embed, view=SearchDropDownView(results))

    def post_list_results(self, channel_id: int, results: list, processed_search: dict):
        embed = discord.Embed(
            title=f"Search results:",
            description=f"Your search yielded multiple results. To view detailed information about a coin, select a dropdown option or run the command `/search id <ID>`. Add <YEAR> to the end of the previous command to narrow things down a bit.",
            color=0xFFCC00,
        )
        embed.add_field(
            name="Displaying results for:",
            value=textHelp.get_multiple_result_desc(processed_search),
            inline=False,
        )
        for coin in results:
            field_title = coin["title"]
            if coin["issuer"]["code"] in textHelp.french_to_emoji:
                field_title = (
                    f"{field_title} {textHelp.french_to_emoji[coin['issuer']['code']]}"
                )
            if coin["title"].startswith("2 Euro") and not (
                coin["title"].startswith("2 Euro Cent")
            ):
                if (
                    ("(" in coin["title"])
                    and not ("1st map" in coin["title"])
                    and not ("2nd map" in coin["title"])
                    and not ("(Pattern)" in coin["title"])
                ):
                    field_title = f"{field_title} ⭐"
            field_title = field_title.replace("&quot;", "'")

            field_desc = f"ID: {coin['id']}"
            if coin["min_year"] == coin["max_year"]:
                field_desc = f"{field_desc}\n{coin['min_year']}"
            else:
                field_desc = f"{field_desc}\n{coin['min_year']} - {coin['max_year']}"

            embed.add_field(name=field_title, value=field_desc, inline=True)

        return embed

    def result_page(self, results: list, processed_search: dict) -> list[pages.Page]:
        """Returns the results page (with the dropdown menu) given results and processed search.
        Inputs:
        - results [list]: The results obtained from the search
        - processed_search [dict]: The processed search menu (needed for the post_list_results method)
        Outputs:
        - list[pages.Page]: A list of all pages.Page objects to be displayed by the bot"""
        # how many pages will there be
        max_page = len(results) // 12 + 1

        # content for each page
        pages_content = []

        for i in range(max_page - 1):
            # Create the actual page with the embed
            embed = self.post_list_results(
                1, results[i * 12 : i * 12 + 12], processed_search
            )
            pages_content.append(
                pages.Page(
                    embeds=[embed],
                    custom_view=SearchDropDownView(results[i * 12 : i * 12 + 12]),
                )
            )

        # create final page
        if len(results) % 12 != 0:
            pages_content.append(
                pages.Page(
                    embeds=[
                        self.post_list_results(
                            1,
                            results[(max_page - 1) * 12 : len(results)],
                            processed_search,
                        )
                    ],
                    custom_view=SearchDropDownView(
                        results[(max_page - 1) * 12 : len(results)]
                    ),
                )
            )

        return pages_content


class SearchDropDownView(discord.ui.View):
    def __init__(self, results):
        super().__init__()
        self.add_item(SearchResultsDropDown(results))


class SearchResultsDropDown(discord.ui.Select):
    options_select = []

    def __init__(self, results):
        options_select = []
        for value in results:
            options_select.append(
                discord.SelectOption(
                    label=value["title"],
                    value=str(value["id"]),
                    description=str(value["id"]),
                    emoji=textHelp.french_to_emoji[value["issuer"]["code"]],
                )
            )
            super().__init__(
                placeholder="Choose a search result for more detailed information",
                options=options_select,
            )

    async def callback(self, interaction):
        await interaction.message.edit(embed=post_ID(coin_id=self.values[0]), view=None)
        await interaction.response.defer(ephemeral=True)


def post_ID(coin_id, year=None):
    coin_information = coinData.getCoinInfo(coin_id)
    logging.info(coin_information)

    mintages = coin_information["mintage"]

    embed = discord.Embed(
        title=coin_information["title"],
        url=f"https://en.numista.com/catalogue/pieces{coin_id}.html",
        description=f"Numista ID: {coin_id}",
        color=0xFFCC00,
    )
    embed.set_thumbnail(url=coin_information["reverse_pic"])
    embed.set_image(url=coin_information["obverse_pic"])
    embed.add_field(name="Design", value=coin_information["design_info"], inline=False)
    field_value = ""
    if year is None:
        for a in mintages:
            field_value = ""
            field_title = str(a)
            for data in mintages[a]:
                field_value += f"{data}\n"
            embed.add_field(
                name=field_title,
                value=field_value,
                inline=True,
            )
            if abs(coin_information["min_year"] - coin_information["max_year"]) > 5:
                embed.set_footer(
                    text=f"This sure is a lot of mintages… it may not even be displayed properly!\nUse /search id {coin_id} <year> to narrow things down a bit or add a year to your search."
                )
    else:
        if int(year) not in mintages:
            embed.add_field(
                name=year,
                value="No coins issued during specified year",
                inline=True,
            )
        else:
            for data in mintages[int(year)]:
                field_value += f"{data}\n"
            embed.add_field(name=year, value=field_value, inline=True)

    return embed


def setup(client):
    client.add_cog(Search(client))
