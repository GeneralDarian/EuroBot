import logging
from os import path, getenv
import sqlite3
from sqlite3 import Error
import validators

import discord
from discord import bot
from discord.ext import commands
from discord.commands import option
import time

confirmed_trader_role_id = int(getenv('VERIFIED_TRADER_GROUP_ID'))

def check_trade_db(user1, user2, check=False) -> int:
    """Checks database to see if user1 and user2 have a pending trade request.
    yser1 (sender), user2 (receiver): discord.Member.id (int)

    If check is True then if 1 is to be returned, the database will not be modified. (Default is False)
    This is required in the case where a request was sent, then rejected, but a button was pressed to accept.

    Returns 0 if there is a confirmed trade which has been completed (automatically removes trade from database)
    Returns 1 if there is not a confirmed trade (automatically adds trade to database)
    Returns 2 if there is a confirmed trade sent by the user already (which should return an error on the other side)
    Returns 3 if the trade timestamp expired (not yet implemented)"""

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

    # scenario 0: trade request was sent by the other side.
    cur.execute(f"SELECT * FROM traderequests WHERE user1_id = {user2} AND user2_id = {user1};")
    rows = cur.fetchone()

    if rows is None:
        pass
    else:
        cur.execute(f"DELETE FROM traderequests WHERE trade_id = {rows[0]}")
        conn.commit()
        conn.close()
        return 0

    cur.execute(f"SELECT * FROM traderequests WHERE user1_id = {user1} AND user2_id = {user2};")
    rows = cur.fetchone()
    #scenario 1: the trade request was not sent by either side..
    if rows is None:
        if not check:
            cur.execute(f"INSERT INTO traderequests (user1_id, user2_id, timestamp) VALUES ({user1}, {user2}, {time.time_ns()})")
            conn.commit()
        conn.close()
        return 1
    #scenario 2: the request has already been sent
    else:
        conn.close()
        return 2

def confirmed_trade_modify_trade_count(user1, user2) -> bool:
    """Adds 1 to the trade count of user1 and user2
    user1 and user2 must be discord.Member.id (int)
    True if done successfully, False if not."""


    conn = None
    db_file = "data/UserProfileDatabase.db"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        conn.close()
        return False
    finally:
        cur = conn.cursor()

    cur.execute(f"SELECT tradecount FROM userprofiledata WHERE ID = {user1};")
    rows = cur.fetchone()
    cur.execute(f"UPDATE userprofiledata SET tradecount = {rows[0] + 1} WHERE ID = {user1}")


    cur.execute(f"SELECT tradecount FROM userprofiledata WHERE ID = {user2};")
    rows = cur.fetchone()
    cur.execute(f"UPDATE userprofiledata SET tradecount = {rows[0] + 1} WHERE ID = {user2}")

    conn.commit()
    conn.close()
    return True

def reject_trade(user1, user2) -> bool:
    """Rejects a trade between 2 users.
    user1, user2 = discord.Member.id (int)
    Returns True if successful, False if not or if there was no trade between the two."""
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

    # scenario 0: trade request was sent by the other side.
    cur.execute(f"SELECT * FROM traderequests WHERE user1_id = {user2} AND user2_id = {user1};")
    rows = cur.fetchone()

    if rows is None:
        pass
    else:
        cur.execute(f"DELETE FROM traderequests WHERE trade_id = {rows[0]}")
        conn.commit()
        conn.close()
        return True

    cur.execute(f"SELECT * FROM traderequests WHERE user1_id = {user1} AND user2_id = {user2};")
    rows = cur.fetchone()

    if rows is None:
        return False
    else:
        cur.execute(f"DELETE FROM traderequests WHERE trade_id = {rows[0]}")
        conn.commit()
        conn.close()
        return True

class ConfirmTradeConfirmation(discord.ui.Button):
    """Confirm a trade request."""
    def __init__(self, user_id, client):
        super().__init__(
            label="Confirm the trade request!",
            style=discord.ButtonStyle.green,
            custom_id=str(time.time_ns() + user_id) #custom_id is needed for persistent views and has to be unique. thanks discord lol
        )
        self.user_id = user_id
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        trade_request_status = check_trade_db(interaction.user.id, self.user_id, check=True)

        user1 = interaction.user.id
        user2 = self.user_id
        user = await discord.Bot.fetch_user(self.client, self.user_id)

        if trade_request_status == 0:
            embed = discord.Embed(
                title='Congratulations! :partying_face:',
                color=0x1abd46,
                description=f'Your trade with <@{user2}> has been confirmed! Both of your trade counts have been updated :)'
            )
            await interaction.response.send_message(embed=embed)

            embed = discord.Embed(
                title='Congratulations! :partying_face:',
                color=0x1abd46,
                description=f'Your trade with <@{user1}> has been confirmed! Both of your trade counts have been updated :)'
            )
            await user.send(embed=embed)
            confirmed_trade_modify_trade_count(user1, user2)

        elif trade_request_status == 1:
            embed = discord.Embed(
                color=0xd41c1c,
                title='Trade confirmation request has been rejected, or does not exist!',
                description=f"""The trade confirmation request with <@{user.id}> has either been rejected or does not exist."""
            )
            await interaction.response.send_message(embed=embed)


        elif trade_request_status == 2:
            embed = discord.Embed(
                color=0xd41c1c,
                title='Error: Trade request already sent to user',
                description=f"""You have already sent a trade request to <@{user.id}>.\
         Wait for the request to be completed before you send another one, or cancel the request with the command `/canceltrade user:@{user.name}`""")
            await interaction.response.send_message(embed=embed)
        await interaction.message.edit(view=None)

class RejectTradeConfirmation(discord.ui.Button):
    """Rejecct a trade request."""
    def __init__(self, user_id, client):
        super().__init__(
            label="Reject the trade request!",
            style=discord.ButtonStyle.red,
            custom_id=str(time.time_ns() + user_id + 1) #custom_id is needed for persistent views and has to be unique. thanks discord lol
        )
        self.user_id = user_id
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        user1 = interaction.user.id
        user2 = self.user_id
        user = await discord.Bot.fetch_user(self.client, self.user_id)

        status = reject_trade(user1, user2)
        if status is False:
            await interaction.response.send_message('**Error:** There is no trade confirmation request with the person specified.')
        else:
            await interaction.response.send_message('The trade confirmation request has been rejected.')
            await user.send(f'The trade confrimation request with <@{interaction.user.id}> has been cancelled.')


        await interaction.message.edit(view=None)

class TradeCount(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Confirm a trade with another user.")
    @option(
        "user",
        description="The user who you wish to confirm a trade with.",
        required=True,
    )
    async def confirmtrade(self, ctx, user: discord.Member):
        confirmed_trader_role = ctx.author.guild.get_role(confirmed_trader_role_id)

        #filter out common problems
        #author does not have confirmed trader role
        if confirmed_trader_role not in ctx.author.roles:
            await ctx.respond("""**Error:** You do not have a confirmed trader role.\
 If you recently traded with a user who has a confirmed trader role, please contact a moderator/admin so that we can give you a confirmed trader role.\
 In order for the role to be awarded, the trade must involve at least one user with a confirmed trader role, and both users must post a picture of their side of the trade.""")
            return

        #user author is trying to trade with is bot
        if user.bot:
            await ctx.respond('**Error:** Bots cannot trade!')
            return

        #user is self
        if user == ctx.author:
            await ctx.respond('**Error:** You can''t trade with yourself!')
            return

        #user author is trying to trade with does not have confirmed trader role
        if confirmed_trader_role not in user.roles:
            await ctx.respond("""**Error:** The user you are trying to trade with does not have a confirmed trader role.\
 If you recently traded with this user, please contact a moderator/admin so that we can give them a confirmed trader role.\
 In order for the role to be awarded, the trade must involve at least one user with a confirmed trader role, and both users must post a picture of their side of the trade.""")
            return

        user1 = ctx.author.id
        user2 = user.id
        trade_request_status = check_trade_db(user1, user2)

        #trade has been confirmed, tradecount to be updated
        if trade_request_status == 0:
            embed = discord.Embed(
                title='Congratulations! :partying_face:',
                color=0x1abd46,
                description=f'Your trade with <@{user2}> has been confirmed! Both of your trade counts have been updated :)'
            )
            await ctx.respond(embed=embed)

            embed = discord.Embed(
                title='Congratulations! :partying_face:',
                color=0x1abd46,
                description=f'Your trade with <@{user1}> has been confirmed! Both of your trade counts have been updated :)'
            )
            await user.send(embed=embed)
            confirmed_trade_modify_trade_count(user1, user2)

        elif trade_request_status == 1:
            embed = discord.Embed(
                color=0xFFCC00,
                title='Trade confirmation request sent!',
                description=f"""You have sent a trade confirmation request to <@{user.id}>."""
            )
            await ctx.respond(embed=embed)
            view = discord.ui.View(timeout=None)
            view.add_item(
                RejectTradeConfirmation(user_id=ctx.author.id, client=self.client)
            )
            view.add_item(
                ConfirmTradeConfirmation(user_id=ctx.author.id, client=self.client)
            )
            embed = discord.Embed(
                color=0xFFCC00,
                title='You have received a trade confirmation request!',
                description=f"""You have received a trade confirmation request from <@{ctx.author.id}>.
**Only accept this request if you have both received your trades!**

:white_check_mark: - To accept the request, press on the green button, or run the command `/confirmtrade user:@{ctx.author}` on the server.

:x: - To reject the reqeust, press on the red button, or run the command `/rejecttrade user:@{ctx.author}` on the server."""
            )
            await user.send(embed=embed, view=view)

        elif trade_request_status == 2:
            embed = discord.Embed(
                color=0xd41c1c,
                title='Error: Trade request already sent to user',
                description=f"""You have already sent a trade request to <@{user.id}>.\
 Wait for the request to be completed before you send another one, or cancel the request with the command `/canceltrade user:@{user.name}`""")
            await ctx.respond(embed=embed)

    @bot.command(description="Confirm a trade with another user.")
    @option(
        "user",
        description="The user who you wish to confirm a trade with.",
        required=True,
    )
    async def rejecttrade(self, ctx, user: discord.Member):
        status = reject_trade(ctx.author.id, user.id)
        if status is True:
            await ctx.respond('The trade confirmation request has been rejected.')
            user = await self.client.fetch_user(user.id)
            await user.send(f'The trade confrimation request with <@{ctx.author.id}> has been cancelled.')
        else:
            await ctx.respond('**Error:** There is no trade confirmation request with the person specified.')

    @bot.command(description='[MOD COMMAND] Modify another user''s tradecount.')
    @discord.commands.default_permissions(manage_messages=True)
    async def settradecount(self, ctx, user: discord.Member, tradecount: discord.Option(int, "The trade count you would like to set a user's total trades to", required=True)):
        conn = None
        db_file = "data/UserProfileDatabase.db"
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            conn.close()
            await ctx.respond('There has been an error, please contact the dev.', ephemeral=True)
            return
        finally:
            cur = conn.cursor()

        cur.execute(f"SELECT tradecount FROM userprofiledata WHERE ID = {user.id};")
        rows = cur.fetchone()
        if rows is None:
            await ctx.respond('The user does not have their own profile yet (run the command `/profile <user>` to make it)', ephemeral=True)
            return

        cur.execute(f"UPDATE userprofiledata SET tradecount = {tradecount} WHERE ID = {user.id}")
        conn.commit()
        conn.close()
        await ctx.respond('The user''s tradecount has been modified.', ephemeral=True)
        return



def setup(client):
    client.add_cog(TradeCount(client))
