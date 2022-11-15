import discord
from discord import bot
from discord.commands import SlashCommandGroup, Option, option
from discord.ext import commands
import logging, typing
from tools import coinData, textHelp

class Search(commands.Cog):


    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    search = SlashCommandGroup("search", "Use the search command!")

    @search.command(description="Display help menu for /search")
    async def help(self, ctx):
        await ctx.respond(
            f"""___***SEARCH HELP (NEEDS UPDATING IS NOT ACCURATE)***___
To search numista's euro coin database you can use ``eur!search``. There are two types of searches you can make: 

**1.) BROAD SEARCH:** To make a broad search, run the command ``eur!search <country> <year> <denomination>``. 
* ``<country>`` must be either the english name of the country _without gaps_ (i.e. Austria, Sanmarino, Netherlands) or the two-letter country code (AT, SM, NL). This argument is __required__.
 * ``<denomination>`` must be one of ``1c, 2c, 5c, 10c, 20c, 50c, 1, 2, 2cc``. If it has a c in the end, it's a cent. ``1`` and ``2`` are 1 and 2 euro coins, ``2cc`` are 2 euro commemoratives only.
 * ``<year>`` must be between 1999 and 2029. This argument is _optional_. 
``<country>``, ``<year>``, and ``<denomination>`` may be in any order.
Examples:
* ``eur!search mc 2020`` - All Monégasque coins minted in 2020
* ``eur!search 2005 at 2cc`` - All 2 euro commemoratives minted by Austria in 2005
* ``eur!search 1 nl`` - All 1 euro coins minted by The Netherlands.

**2.) EXACT SEARCH:** Sometimes, broad searches will return multiple results. When that happens you can either add more arguments to narrow down the search, or use the IDs returned in the search to make an exact search. In this case you can run the command ``eur!search id <ID> <year>``. 
* ``<ID>`` is required and is equivalent to the numista ID of the coin.
* ``<year>`` is optional and can be used to narrow down mintage statistics if a coin was minted during a large period of time.
Unlike before, ``<ID>`` and ``<year>`` must be in the order specified.
Examples:
* ``eur!search id 49385`` - Displays information of 2 euro coin with Numista ID 49385 (Monaco 2013)
"""
        )

    @search.command(description="Display 2-letter country codes")
    async def countryid(self, ctx):
        await ctx.respond(textHelp.country_id_help_menu)

    @search.command(description="Search a coin by its Numista ID.")
    async def id(self, ctx,
                 numista_id:Option(str, "The Numista ID of the coin", required = True),
                 year:Option(int, "The year the coin was minted in", required = False, default = None)):
        embed = self.post_ID(numista_id, year)
        await ctx.respond(embed=embed)

    @search.command(description="Look up a euro coin in our database for information, pictures, and mintages!")
    @option(
        "country",
        description="The country of the coin (can either be the name in English or the 2-letter country code",
        autocomplete=discord.utils.basic_autocomplete(dict.keys(textHelp.country_to_french)),
        required=True
    )
    @option(
        "year",
        description="The year the coin was minted in",
        autocomplete=discord.utils.basic_autocomplete([year for year in range(1999, 2030)]),
        required=False,
        default=None
    )
    @option(
        "type",
        description="The type of coin",
        autocomplete=discord.utils.basic_autocomplete(['1 cent', '2 cents', '5 cents', '10 cents', '20 cents', '50 cents', '1 euro', '2 euro', '2 euro commemorative']),
        required=False,
        default=None
    )
    async def coin(self, ctx, country: str, year: int, type: str):
        #convert type
        if type.lower() not in textHelp.types:
            try:
                type = textHelp.from_type[type.lower()]
            except KeyError:
                ctx.respond("Error: Invalid type entered.")
                return
        processed_search_list = {'Issuer': country, 'Year': year, 'Type': type}
        logging.info(processed_search_list)
        results = coinData.searchEngine(processed_search_list)
        if len(results) == 1:
            embed = self.post_ID(
                results[0]["id"], processed_search_list["Year"]
            )
            await ctx.respond(embed=embed)
        elif len(results) < 1:
            await ctx.respond("Your search has yielded no results!")
        else:
            embed = self.post_list_results(int(ctx.channel.id), results, processed_search_list)
            await ctx.respond(embed=embed)



    @bot.command(description="Fast search (without specifying arguments) - do /search help to learn how to use this.")
    @option(
        "query",
        description="A shortened search query. Run /search help to see what one looks like.",
        required=True)
    async def fsearch(
            self,
            ctx,
            query
    ):
        search_list = query.split(" ")
        if len(search_list) > 3:
            await ctx.respond("You have added too many arguments! (max 3)")
        processed_search_list = coinData.searchProcessor(search_list)

        if processed_search_list["Status"] != "0":
            await ctx.respond(processed_search_list["Status"])
            return

        results = coinData.searchEngine(processed_search_list)
        if len(results) == 1:
            embed = self.post_ID(
                results[0]["id"], processed_search_list["Year"]
            )
            await ctx.respond(embed=embed)
        elif len(results) < 1:
            await ctx.respond("Your search has yielded no results!")
        else:
            embed = self.post_list_results(int(ctx.channel.id), results, processed_search_list)
            await ctx.respond(embed=embed)


    def post_list_results(self, channel_id: int, results: list, processed_search: dict):
        channel = self.client.get_channel(int(channel_id))
        embed = discord.Embed(
            title=f"Search results:",
            description=f"Your search yielded multiple results. To view detailed information about a coin, run the command eur!search ID <ID>. Add <YEAR> to the end of the previous command to narrow things down a bit.",
        )
        embed.add_field(
            name="Displaying results for:",
            value=textHelp.get_multiple_result_desc(processed_search),
            inline=False,
        )
        for coin in results:
            print(coin)
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


    def post_ID(self, coin_id, year=None):
        coin_information = coinData.getCoinInfo(coin_id)
        logging.info(coin_information)

        mintages = coin_information["mintage"]

        embed = discord.Embed(
            title=coin_information["title"],
            url=f"https://en.numista.com/catalogue/pieces{coin_id}.html",
            description=f"Numista ID: {coin_id}",
        )
        embed.set_thumbnail(url=coin_information["reverse_pic"])
        embed.set_image(url=coin_information["obverse_pic"])
        embed.add_field(
            name="Design", value=coin_information["design_info"], inline=False
        )
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
                if abs(coin_information["min_year"] - coin_information["max_year"]) > 1:
                    embed.set_footer(
                        text=f"This sure is a lot of mintages... it may not even be displayed properly!\n Use eur!search id {coin_id} <YEAR> to narrow things down a bit or add a year to your search."
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