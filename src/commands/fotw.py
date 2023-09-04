import logging
import time
import datetime
from os import path

import discord
from discord import bot
from discord.ext import commands, tasks

from tools import findOfTheWeek


class Fotw(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )



    @commands.Cog.listener()
    async def on_message(self, message):  # FindOfTheWeek
        pass
        if message.author.bot:  # is message from bot?
            return

        channel_id_1 = findOfTheWeek.CHANNEL_ID_1
        channel_id_2 = findOfTheWeek.CHANNEL_ID_2
        if (str(message.channel.id) != channel_id_1) and (str(message.channel.id) != channel_id_2):  # is message sent in right channel?
            # await self.client.process_commands(message)
            return

        if len(message.attachments) > 0:
            for file in message.attachments:
                if file.filename.endswith("jpg") \
                        or file.filename.endswith("png") \
                        or file.filename.endswith("JPG") \
                        or file.filename.endswith("PNG"):  # Checks if message has attachments .png or .jpg
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

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        findOfTheWeek.fotw.subtractMessage(str(message.id))

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def getwinners(self, ctx):
        if ctx.author.id != 228069568222855169:
            user = await self.client.fetch_user("228069568222855169")
            await user.send(
                f"Someone tried to run /getwinners without your permission. The name of the user is {ctx.author} with id {ctx.author.id}"
            )
            return
        try:
            await self.getFOTWWinner(findOfTheWeek.fotw.getList())
        except Exception as error:
            logging.error(
                f"getWinners : encountered an error with getFOTWWinner: {error}"
            )
        try:
            findOfTheWeek.fotw.refreshList()
        except Exception as error:
            logging.error(f"getWinners: encountered an error with refresh: {error}")

    async def getFOTWWinner(self, message_id_list: list) -> None:
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
        emote_name = findOfTheWeek.EMOTE_NAME
        channel = self.client.get_channel(
            int(findOfTheWeek.CHANNEL_ID)
        )  # Gets CHANNEL_ID which is defined in findOfTheWeek
        first = []  # The list of winners
        second = [] #The list of second place finds
        third = [] #The list of third place finds

        first_count = 0 #The emote count for first place
        second_count = 0 #The emote count for second place
        third_count = 0 #The emote count for third place

        for msgID in message_id_list:
            try:
                msg = await channel.fetch_message(msgID)
            except Exception:
                continue
            if (
                isinstance(msg, discord.NotFound)
                or isinstance(msg, discord.Forbidden)
                or isinstance(msg, discord.HTTPException)
            ):
                continue
            logging.info(f"Logging message {msgID}")

            reaction_count = msg.reactions
            for reaction in reaction_count:
                if str(reaction.emoji) == f"<:{emote_name}:{emote_id}>":
                    print("HIT:")
                    print(str(reaction.emoji) == f"<:{emote_name}:{emote_id}>")
                    print(f"{reaction.count} REACTIONS")

                    if (
                        reaction.count == None
                    ):  # If the message doesn't even have any reactions lol
                        continue

                    elif (
                        reaction.count < third_count
                    ):  # If the message has less reactions than third_count, it cannot be a winner.
                        continue

                    elif (
                        reaction.count == third_count
                    ) and (
                        len(second) == 1
                    ): # If the message has the same reactions as third_count, it is added to third place.
                        third.append(msg)
                        continue

                    elif (
                        reaction.count > third_count and reaction.count < second_count
                    ): # If it is between third_count and second_count then this message is the new third place.
                        third = [msg]
                        third_count = reaction.count
                        continue

                    elif (
                        reaction.count == second_count
                    ): # If it equal to second_count it is added to second place.
                        second.append(msg)
                        continue

                    elif (
                        reaction.count > second_count and reaction.count < first_count
                    ): # If it is between second_count and first_count then this message is the new second place.
                        third = second
                        second = [msg]
                        third_count = second_count
                        second_count = reaction.count

                    elif (
                        reaction.count == first_count
                    ): # If it is equal to first_count then this message is tied first.
                        first.append(msg)

                    else: #This message is the new first place
                        third = second
                        second = first
                        first = [msg]
                        third_count = second_count
                        second_count = first_count
                        first_count = reaction.count








        # ASSEMBLE WIN EMBED DESC
        if len(first) == 0:
            embed = discord.Embed(
                title=f"FIND OF THE WEEK - <t:{int(time.time())}:D>",
                description=f"It appears as if there aren't any winners for this week's Find Of The Week :/\nRemember: React to a message with <:emote:{int(emote_id)}> to enter someone's find into next week's FOTW!",
                color=0xFFCC00,
            )
            await channel.send(embed=embed)
            return

        embed_desc = f"<:emote:{int(emote_id)}> **FIRST PLACE**\n"
        if len(first) != 1:
            embed_desc += "This week, multiple people scored first place!\n\n"
        for message in first:
            embed_desc += f"Congratulations <@{message.author.id}> for winning this week's FOTW competition!\nSubmission: https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}\n\n"

        if len(first) >= 3 or len(second) == 0:
            pass
        else:
            embed_desc += f"<:emote:{int(emote_id)}> **SECOND PLACE**\n"
            if len(second) != 1:
                embed_desc += "This week, multiple people scored second place!\n\n"
            for message in second:
                embed_desc += f"Congratulations <@{message.author.id}> for second place!\nSubmission: https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}\n\n"

        if len(first) > 1 or len(second) > 1 or len(third) == 0:
            pass
        else:
            embed_desc += f"<:emote:{int(emote_id)}> **THIRD PLACE**\n"
            if len(third) != 1:
                embed_desc += "This week, multiple people scored third place!\n\n"
            for message in third:
                embed_desc += f"Congratulations <@{message.author.id}> for third place!\nSubmission: https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}\n\n"

        embed_desc += f"""\n\nRemember: React to a message with <:emote:{int(emote_id)}> to enter someone's find into next week's FOTW!\nThe member with the most <:emote:{int(emote_id)}> reactions will win!"""
        embed = discord.Embed(
            title=f"FIND OF THE WEEK - <t:{int(time.time())}:D>",
            description=embed_desc,
            color=0xFFCC00,
        )
        await channel.send(embed=embed)
        print(first)
        print(second)
        print(third)


def setup(client):
    client.add_cog(Fotw(client))
