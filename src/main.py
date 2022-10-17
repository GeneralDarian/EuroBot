import os
import time
import typing
import datetime
import logging
import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

import banknote as cmdBanknote
import coinData
import designer
import findOfTheWeek
import textHelp


def main():
    BOT_NAME = "EuroBot"

    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents.all()
    activity = discord.Activity(
        type=discord.ActivityType.playing, name="Help: eur!help"
    )
    client = commands.Bot(
        command_prefix=["eur!", "Eur!", "€!"],
        intents=intents,
        help_command=None,
        activity=activity,
    )


    logging.basicConfig(format="[%(asctime)s] [%(levelname)s]: %(message)s (%(filename)s:%(lineno)d)" ,level=logging.INFO, datefmt="%H:%M:%S")

    @client.event
    async def on_ready():
        logging.info(f"{client.user} has logged in.")

    @client.command()
    async def clean(ctx):  # Displays help information for cleaning coins
        await ctx.send(textHelp.clean_msg)
        return

    @client.command()
    async def storage(ctx):  # Displays help information for storing coins
        await ctx.send(textHelp.storage_msg_1)
        await ctx.send(textHelp.storage_msg_2)
        return

    @client.command()
    async def crh(ctx):  # coin roll hunting information command
        await ctx.send(textHelp.crh_info)
        return

    @client.command()
    async def fotw(ctx):
        emote_id = findOfTheWeek.EMOTE_ID
        channel_id = findOfTheWeek.CHANNEL_ID
        await ctx.send(
            f"""**FIND OF THE WEEK (FOTW) HELP**
Find of the Week is a system where finds are 'ranked' by the commmunity. The best find wins this week's find of the week!
For starters, post a picture of your find in <#{channel_id}>. Afterwards, other users can react to the picture with <:emote:{emote_id}> emotes!
On Sundays, the find with the most emotes wins!"""
        )

    @client.command()
    async def rare(ctx):  # rare coins information command
        await ctx.send(textHelp.rare_coins)
        return

    @client.command()
    async def help(ctx):
        emote_id = os.getenv("HELP_EMOTE_ID")
        msg_prefix = getprefix(ctx.message.content)
        await ctx.send(
            f"""___***EUROBOT HELP MENU***___

**Non-Information commands**
<:emote:{int(emote_id)}> ``{msg_prefix}!search`` - Look up euro coin designs from numista's coin database. Run ``{msg_prefix}!search help`` for more information on how to use this commnad.

<:emote:{int(emote_id)}> ``{msg_prefix}!banknote <banknote serial>`` - Display euro banknote statistics given its serial number.

<:emote:{int(emote_id)}> ``{msg_prefix}!tocoin`` - Convert an image to a 2 euro coin. Run ``{msg_prefix}!tocoin help`` for more information on how to use this command.

**Information commands**
<:emote:{int(emote_id)}> ``{msg_prefix}!clean`` - Information on cleaning coins.

<:emote:{int(emote_id)}> ``{msg_prefix}!crh`` - Information on coin roll hunts.

<:emote:{int(emote_id)}> ``{msg_prefix}!rare`` - Information on rare euro coins.

<:emote:{int(emote_id)}> ``{msg_prefix}!storage`` - Information on storing coins properly.

<:emote:{int(emote_id)}> ``{msg_prefix}!info`` - Displays bot and server information.

<:emote:{int(emote_id)}> ``{msg_prefix}!fotw`` - Displays information on find of the week."""
        )

    @client.command()
    async def banknote(ctx, arg1=None):  # eur!banknote command
        # display help info if arg1 is not set or if arg1 == "help"
        msg_prefix = getprefix(ctx.message.content)
        if arg1 == None:
            await ctx.send(
                f"""**EUR!BANKNOTE HELP**
Use ``{msg_prefix}!banknote <ID>`` to get banknote information, where <ID> is the banknote serial. Do not add printer identification codes or vertical serial numbers.
Here is the location of the euro banknote serials for both Series 1 (top) and Series 2 (bottom): https://imgur.com/u3IraLz"""
            )
            return
        elif "`" in arg1:
            await ctx.send(f"Error: Invalid input")
            return

        # Get banknote info
        banknoteInfo = cmdBanknote.checkSumValidator(str(arg1))
        # Was there an error when getting banknote information?
        if banknoteInfo[0] == 0:
            if len(banknoteInfo) <= 1:
                await ctx.send("Something went wrong... please contact an admin!")
                logging.error("Executing banknote command returned len <= 1.")
                return
            else:
                await ctx.send(f"**Error:** {banknoteInfo[1]}")
                return

        # Display banknote information
        if banknoteInfo[0] == 1:
            await ctx.send(
                f"💶 **Banknote information for serial** ``{arg1}``\n**SERIES:** 1\n**ISSUER:** {textHelp.emojiReplacer(banknoteInfo[1])}\n**VALID:** {banknoteInfo[2]}"
            )
        else:
            await ctx.send(
                f"💶 **Banknote information for serial** ``{arg1}``\n**SERIES:** 2\n**PRINTER:** {textHelp.emojiReplacer(banknoteInfo[1])}\n**VALID:** {banknoteInfo[2]}"
            )
        return

    @client.event
    async def on_message(message):  # FindOfTheWeek
        if message.author.bot:  # is message from bot?
            return

        channel_id = findOfTheWeek.CHANNEL_ID
        if str(message.channel.id) != channel_id:  # is message sent in right channel?
            await client.process_commands(message)
            return

        if len(message.attachments) > 0:
            for file in message.attachments:
                if file.filename.endswith("jpg") or file.filename.endswith(
                    "png"
                ):  # Checks if message has attachments .png or .jpg
                    findOfTheWeek.fotw.addMsg(message.id)
        else:
            content = message.content.split(" ")
            for (
                words
            ) in (
                content
            ):  # checks if message has any links with .jpg or .png at the end
                if ("https://" in words and ".jpg" in words) or (
                    "https://" in words and ".png" in words
                ):
                    findOfTheWeek.fotw.addMsg(message.id)

        await client.process_commands(message)

    async def getFOTWWinner(message_id_list: list) -> None:
        """Given list of FOTW messages, gets the winner(s) and refreshes the files.
        Also posts the list of winners in the respective channel.
        If first place is tied it'll return a list of tied winners.
        Inputs:
        - message_id_list (list): List of discord message IDs, can be retrievable from findOfTheWeek.fotw.getList()
        Outputs:
        - None"""

        emote_id = (
            findOfTheWeek.EMOTE_ID
        )  # Gets EMOTE_ID which is defined in findOfTheWeek
        emote_name = (
            findOfTheWeek.EMOTE_NAME
        )
        channel = client.get_channel(
            int(findOfTheWeek.CHANNEL_ID)
        )  # Gets CHANNEL_ID which is defined in findOfTheWeek
        winners = []  # The list of winners
        count = 1  # The emote count

        for msgID in message_id_list:
            try:
                msg = await channel.fetch_message(msgID)
            except ValueError:
                continue
            if (
                isinstance(msg, discord.NotFound)
                or isinstance(msg, discord.Forbidden)
                or isinstance(msg, discord.HTTPException)
            ):
                continue

            reaction_count = msg.reactions
            for reaction in reaction_count:
                if str(reaction.emoji) == f"<:{emote_name}:{emote_id}>":

                    if (
                        reaction.count == None
                    ):  # If the message doesn't even have any reactions lol
                        continue
                    elif (
                        reaction.count < count
                    ):  # If message has less reactions than count, it is not a winner.
                        continue
                    elif (
                        reaction.count == count
                    ):  # If message has the same reactions as count, append to list.
                        winners.append(msg)
                    elif (
                        reaction.count > count
                    ):  # If message has more reactions than count, replace winners, append, and increase count.
                        count = reaction.count
                        winners = [msg]

        # ASSEMBLE WIN MESSAGE
        if len(winners) < 1:  # No victors
            vMsg = f"""**FIND OF THE WEEK:** <t:{int(time.time())}:D>
It appears as if there aren't any winners for this week's find of the week :/
Remember: React to a message with <:emote:{int(emote_id)}> to enter someone's find into next week's FOTW!
The member with the most <:emote:{int(emote_id)}> reactions will win!
            """

        elif (
            len(winners) == 1
        ):  # One victor. Returns immediately to not tamper with the FOTW class any further.
            vMsg = f"""**FIND OF THE WEEK:** <t:{int(time.time())}:D>
            
<:emote:{int(emote_id)}> Congratulations <@{winners[0].author.id}> for winning this week's FOTW competition! 
Submission: https://discordapp.com/channels/{winners[0].guild.id}/{winners[0].channel.id}/{winners[0].id}\n
    
Remember: React to a message with <:emote:{int(emote_id)}> to enter someone's find into next week's FOTW!
The member with the most <:emote:{int(emote_id)}> reactions will win!
            """
            await channel.send(vMsg)
            return

        elif (
            len(winners) > 1
        ):  # Multiple victors. If this gets above 2000 chars please kill me
            vMsg = f"""**FIND OF THE WEEK:** <t:{int(time.time())}:D>
This week, there are multiple submissions with the same amount of reactions!
    """
            for i in winners:
                vMsg += f"""
<:emote:{int(emote_id)}> Congratulations <@{i.author.id}> for winning this week's FOTW competition! 
Submission: https://discordapp.com/channels/{i.guild.id}/{i.channel.id}/{i.id}
    """

            vMsg += f"""
Remember: React to a message with <:emote:{int(emote_id)}> to enter someone's find into next week's FOTW!
The member with the most <:emote:{int(emote_id)}> reactions will win!"""

        await channel.send(vMsg)

    @client.event
    async def on_message_delete(message):
        findOfTheWeek.fotw.subtractMessage(str(message.id))

    @client.command()
    @commands.has_permissions(administrator=True)
    async def getWinners(ctx):
        try:
            await getFOTWWinner(findOfTheWeek.fotw.getList())
            findOfTheWeek.fotw.refreshList()
        except Exception as error:
            logging.error(f"!getWinners : Encountered an error: {error}")

    @client.command()
    @commands.has_permissions(administrator=True)
    async def refreshAPI(ctx):
        coinData.refreshFiles()

    @client.command()
    async def search(
        ctx,
        arg1: typing.Optional[str],
        arg2: typing.Optional[str],
        arg3: typing.Optional[str],
    ):
        msg_prefix = getprefix(ctx.message.content)
        if arg1 is None or arg1.lower() == "help":
            await ctx.send(
                f"""___***EUR!SEARCH HELP***___
To search numista's euro coin database you can use ``eur!search``. There are two types of searches you can make: 
    
**1.) BROAD SEARCH:** To make a broad search, run the command ``{msg_prefix}!search <country> <year> <denomination>``. 
* ``<country>`` must be either the english name of the country _without gaps_ (i.e. Austria, Sanmarino, Netherlands) or the two-letter country code (AT, SM, NL). This argument is __required__.
 * ``<denomination>`` must be one of ``1c, 2c, 5c, 10c, 20c, 50c, 1, 2, 2cc``. If it has a c in the end, it's a cent. ``1`` and ``2`` are 1 and 2 euro coins, ``2cc`` are 2 euro commemoratives only.
 * ``<year>`` must be between 1999 and 2029. This argument is _optional_. 
``<country>``, ``<year>``, and ``<denomination>`` may be in any order.
Examples:
* ``{msg_prefix}!search mc 2020`` - All Monégasque coins minted in 2020
* ``{msg_prefix}!search 2005 at 2cc`` - All 2 euro commemoratives minted by Austria in 2005
* ``{msg_prefix}!search 1 nl`` - All 1 euro coins minted by The Netherlands.

**2.) EXACT SEARCH:** Sometimes, broad searches will return multiple results. When that happens you can either add more arguments to narrow down the search, or use the IDs returned in the search to make an exact search. In this case you can run the command ``{msg_prefix}!search id <ID> <year>``. 
* ``<ID>`` is required and is equivalent to the numista ID of the coin.
* ``<year>`` is optional and can be used to narrow down mintage statistics if a coin was minted during a large period of time.
Unlike before, ``<ID>`` and ``<year>`` must be in the order specified.
Examples:
* ``{msg_prefix}!search id 49385`` - Displays information of 2 euro coin with Numista ID 49385 (Monaco 2013)
"""
            )
            return
        elif arg1.lower() == "id":
            await post_ID(arg2, int(ctx.channel.id), arg3)
            return

        search_list = [arg1, arg2, arg3]
        processed_search_list = coinData.searchProcessor(search_list)

        if processed_search_list["Status"] != "0":
            await ctx.send(processed_search_list["Status"])
            return

        results = coinData.searchEngine(processed_search_list)
        if len(results) == 1:
            await post_ID(
                results[0]["id"], int(ctx.channel.id), processed_search_list["Year"]
            )
            pass
        elif len(results) < 1:
            await ctx.send("Your search has yielded no results!")
        else:
            pass
            await post_list_results(int(ctx.channel.id), results, processed_search_list)

    async def post_list_results(channel_id: int, results: list, processed_search: dict):
        channel = client.get_channel(int(channel_id))
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
        await channel.send(embed=embed)

    async def post_ID(coin_id: str, channel_id: int, year=None):
        coin_information = coinData.getCoinInfo(coin_id)
        channel = client.get_channel(int(channel_id))
        if coin_information["status"] != "0":
            await channel.send(coin_information["status"])
            return

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
        await channel.send(embed=embed)

    @client.command()
    async def tocoin(ctx, arg1=None):
        """Processes an image using Frakkur's image to 2-euro coin program."""

        # check to make sure this command isn't currently being used. Otherwise file deletion becomes a bit screwed up.
        global using_tocoin
        if using_tocoin is True:
            await ctx.channel.send(
                "This command is currently in use. Please wait a few seconds before running it."
            )
            return
        using_tocoin = True

        # Help menu
        msg_content = ctx.message.content
        if arg1 is not None and arg1.lower() == "help":
            await ctx.channel.send(textHelp.tocoin_help_menu)
            using_tocoin = False
            return

        # Processes arguments into a dict variable
        argument_list = textHelp.tocoin_argument_processor(msg_content)

        # Check to see if the message is a reply to another message.
        try:
            reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except AttributeError:
            reply = None

        # If something goes wrong this variable will detect it.
        response = False

        # Case 1: The message containing the command contains an image. This takes priority over replying to a message with an image.
        if len(ctx.message.attachments) > 0:
            for file in ctx.message.attachments:
                if file.filename.endswith(".jpg") or file.filename.endswith(
                    ".png"
                ):  # Only the first image is used.
                    attachment = ctx.message.attachments[
                        0
                    ]  # Gets first attachment from message
                    response = designer.euro_designer(
                        attachment.url,
                        int(argument_list["Sigma"]),
                        int(argument_list["Intensity"]),
                        int(argument_list["NMD"]),
                    )

        # Case 2: The message containing the command replies to a message. Check to see if replied to msg contains image.
        elif reply is not None:
            if len(reply.attachments) > 0:
                for file in reply.attachments:
                    if file.filename.endswith(".jpg") or file.filename.endswith(".png"):
                        attachment = reply.attachments[
                            0
                        ]  # gets first attachment that user
                        response = designer.euro_designer(
                            attachment.url,
                            int(argument_list["Sigma"]),
                            int(argument_list["Intensity"]),
                            int(argument_list["NMD"]),
                        )
            else:  # msg does not contain image
                await ctx.channel.send(
                    "The message you replied to does not have a valid image! __(The image needs to be uploaded, not supplied via link.)__"
                )
                using_tocoin = False
                return
        else:  # neither Case 1 or Case 2 means no image was supplied or an improper filetype was supplied.
            await ctx.channel.send(
                "You must supply an image or reply to a message containing an image! Run ``eur!tocoin help`` for help with using this command."
            )
            using_tocoin = False
            return

        # If the response is true then conversion was successful.
        # Get the file, send in embed, and then delete the file.
        if response is True:
            file = discord.File("outputs/output.png", filename="image.png")
            embed = discord.Embed(
                title=f"S = {argument_list['Sigma']}, INTENSITY = {argument_list['Intensity']}, NMD = {argument_list['NMD']}"
            )
            embed.set_image(url="attachment://image.png")
            embed.set_footer(
                text="CoinDesigner by @joaoperfig [GH] - https://github.com/joaoperfig"
            )
            await ctx.channel.send(file=file, embed=embed)
            os.remove("outputs//output.png")
            using_tocoin = False
            return
        else:  # If response is False then something went wrong.
            await ctx.channel.send(
                "There was an error processing the image. Please contact an admin!"
            )
            using_tocoin = False
            return
        
        
    @client.command()
    async def info(ctx):
        embed = discord.Embed(
            title="/r/EuroCoins - Server and Bot Information",
            url="https://github.com/GeneralDarian/EuroBot"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/555331630206681108/ce006b24f0d5fb90fbbcfc53c17ab4a2"
        )
        embed.add_field(
            name="Server Members",
            value=len([user for user in client.users if not user.bot]),
            inline=True
        )
        traders_role = ctx.message.guild.get_role(int(findOfTheWeek.TRADER_ROLE_ID))
        embed.add_field(
            name="Verified Traders",
            value=len(traders_role.members)
        )
        guild_creation_time = ctx.message.guild.created_at
        guild_diff = (datetime.datetime.now(datetime.timezone.utc) - guild_creation_time).days
        guild_creation_value = f"{guild_diff} days old\nCreated {guild_creation_time.strftime('%d. %B %Y')}"
        embed.add_field(
            name="Server is currently...",
            value=guild_creation_value,
        )
        embed.add_field(
            name="Bot version:",
            value="BETA",
        )
        embed.add_field(
            name="EuroBot Discord:",
            value="https://discord.gg/ev53PnSaXV",
        )
        embed.set_footer(
            text="EuroBot is an open source project created by @General Darian ✓ᵛᵉʳᶦᶠᶦᵉᵈ#8498 and @Mango Man#0669. Click on the embed title to visit the bot's github!",
            icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
        )
        await ctx.send(embed=embed)

    def getprefix(msg: str) -> str:
        """Returns prefix used for issued command
        Inputs: The command (message.content, MUST be string)
        Outputs: The string used"""
        if msg.startswith("eur!"):
            return "eur"
        elif msg.startswith("Eur!"):
            return "Eur"
        else:
            return "€"


    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    using_tocoin = False
    main()
