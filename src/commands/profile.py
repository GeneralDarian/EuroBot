import logging
from os import path, getenv
import sqlite3
from sqlite3 import Error
import validators

import discord
from discord import bot
from discord.ext import commands
from discord.commands import option

confirmed_trader_role_id = int(getenv('CONFIRMED_TRADER_ROLE_ID'))
moderator_role_id = int(getenv('MODERATOR_ROLE_ID'))

def checkuser(id: int) -> tuple:
    """Checks to see if user exists in database. If they do not, creates new entry in database.
    INPUTS:
    - id: The user ID
    OUTPUTS:
    - Tuple."""

    #sqlite3 boilerplate yada yada
    conn = None
    db_file = "data/UserProfileDatabase.db"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        conn.close()
        return (False, e)
    finally:
        cur = conn.cursor()

    cur.execute(f"SELECT * FROM userprofiledata WHERE ID = {id};")
    rows = cur.fetchone()

    #does user exist? if not, add new entry for user
    if rows is None:
        cur.execute(f"INSERT INTO userprofiledata (ID) VALUES ({id})")
        conn.commit()
        cur.execute(f"SELECT * FROM userprofiledata WHERE ID = {id};")
        rows = cur.fetchone()

    #else return rows
    conn.close()
    return rows

def checkfield(url: str) -> str:
    """Checks if field exists. If it does, makes hyperlink. If not, marks option as not set."""
    if url is None:
        return 'Not set'

    return f'[Link]({url})'

def modfield(id: int, option: str, value: str) -> bool:
    """Modifies the field of a user with id. Returns true if successful and false if not."""
    conn = None
    db_file = "data/UserProfileDatabase.db"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        conn.close()
        return False
    finally:
        cur = conn.cursor()

    cur.execute(f"SELECT * FROM userprofiledata WHERE ID = {id};")
    rows = cur.fetchone()

    # does user exist? if not, FAIL
    if rows is None:
        return False

    #now execute command
    print(option, id, value)
    cur.execute(f"UPDATE userprofiledata SET {option} = ? WHERE ID = {id}", (value,))
    conn.commit()
    return True



class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description='Modify your own server profile.')
    @option(
        "option",
        description="The option you would like to modify.",
        autocomplete=discord.utils.basic_autocomplete(('Collection Link', 'Swaplist Link', 'YouTube Link', 'Instagram Link')),
        required=True)
    async def setprofile(self, ctx, option, value: discord.Option(str, "The value you would like to set the option to", required=False)):
        translator = {
            'Collection Link': 'collection_webpage',
            'Swaplist Link': 'swaplist',
            'YouTube Link': 'youtube',
            'Instagram Link': 'instagram'
        }

        #see if correct option was chosen
        try:
            db = translator[option]
        except KeyError:
            await ctx.respond('**ERROR:** You must select a valid option!')
            return

        #see if url valid
        if not validators.url(value) and value is not None:
            await ctx.respond('**ERROR:** The URL you have provided is invalid!')
            return

        #showtime
        success = modfield(ctx.author.id, db, value)
        if success is True:
            await ctx.respond(f'Your profile option ``{option}`` has been successfully updated. To reset, run the command `/setprofile option:{option}`.')
        else:
            await ctx.respond(f'**ERROR:** An error occured. Please contact a bot developer.')

    @bot.command(description="Display the user's server profile.")
    @option(
        "user",
        description="The user whose profile you would like to view. If not specified, it will display your own profile.",
        required=False,
    )
    async def profile(self, ctx, user: discord.Member):
        if user is None:
            user = ctx.author.id
        else:
            user = user.id

        user = await ctx.author.guild.fetch_member(user)

        if user.bot:
            await ctx.respond('**Error:** Bots cannot collect coins!')
            return

        #check if user is in db, if so get data, if not make new entry
        status = checkuser(user.id)

        #if there is an error its the admin's problem
        if status[0] is False:
            await ctx.respond("**Error:** There has been an error. Please contact the bot developers!")
            return

        #otherwise display the embed
        """reference for status:
        status[0] = ID
        status[1] = collection website
        status[2] = swaplist
        status[3] = youtube
        status[4] = instagram
        status[5] = tradecount"""

        #get color of user
        confirmed_trader_role = ctx.author.guild.get_role(confirmed_trader_role_id)
        if confirmed_trader_role not in ctx.author.roles:
            color = 0x0099E1
        else:
            color = 0x00D166

        #check if guild avatar exists
        if user.guild_avatar is None:
            avatar = user.display_avatar.url
        else:
            avatar = user.guild_avatar.url

        print(user.guild_avatar)
        embed = discord.Embed(
            title=f"User Profile: {user.name}",
            color=color
        )
        embed.set_thumbnail(
            url=avatar
        )
        embed.add_field(
            name="Join Date",
            value=user.joined_at.strftime('%d. %B %Y'),
        )
        embed.add_field(
            name="Collection Site",
            value=checkfield(status[1]),
        )
        embed.add_field(
            name="Swaplist",
            value=checkfield(status[2]),
        )
        embed.add_field(
            name="YouTube",
            value=checkfield(status[3]),
        )
        embed.add_field(
            name="Instagram",
            value=checkfield(status[4]),
        )
        embed.add_field(
            name="# of completed trades",
            value='0',
        )
        embed.set_footer(text="To change an option of your own profile, run the command `/setprofile <option> <value>`. For help with configuring the trade count, run the command `/help tradecount`")


        await ctx.respond(embed=embed)

    @bot.command(description='[MOD COMMAND] Modify another user''s server profile.')
    @option(
        "option",
        description="The option you would like to modify.",
        autocomplete=discord.utils.basic_autocomplete(('Collection Link', 'Swaplist Link', 'YouTube Link', 'Instagram Link')),
        required=True)
    @discord.commands.default_permissions(manage_nicknames=True)
    async def changeprofile(self, ctx, user: discord.Member, option, value: discord.Option(str, "The value you would like to set the option to", required=False)):
        translator = {
            'Collection Link': 'collection_webpage',
            'Swaplist Link': 'swaplist',
            'YouTube Link': 'youtube',
            'Instagram Link': 'instagram'
        }

        #see if correct option was chosen
        try:
            db = translator[option]
        except KeyError:
            await ctx.respond('**ERROR:** You must select a valid option!')
            return

        #see if url valid
        if not validators.url(value) and value is not None:
            await ctx.respond('**ERROR:** The URL you have provided is invalid!')
            return

        #fetch user
        if user is None:
            user = ctx.author.id
        else:
            user = user.id

        user = await ctx.author.guild.fetch_member(user)

        if user.bot:
            await ctx.respond('**Error:** Bot profiles do not exist!')
            return

        #showtime
        success = modfield(user.id, db, value)
        if success is True:
            await ctx.respond(f'Your profile option ``{option}`` has been successfully updated. To reset, run the command `/setprofile option:{option}`.')
        else:
            await ctx.respond(f'**ERROR:** An error occured. Please contact a bot developer.')


def setup(client):
    client.add_cog(Profile(client))