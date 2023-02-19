import logging
import time
from os import path

import discord
from discord import bot
from discord.ext import commands

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
        if message.author.bot:  # is message from bot?
            return

        channel_id = findOfTheWeek.CHANNEL_ID
        if str(message.channel.id) != channel_id:  # is message sent in right channel?
            # await self.client.process_commands(message)
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
        winners = []  # The list of winners
        count = 1  # The emote count

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
                        logging.info(f"New list of winners is: {winners}\n")
                        continue
                    elif (
                        reaction.count < count
                    ):  # If message has less reactions than count, it is not a winner.
                        logging.info(f"New list of winners is: {winners}\n")
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
                    logging.info(f"New list of winners is: {winners}\n")

        # ASSEMBLE WIN MESSAGE
        logging.info(f"{winners}")
        if len(winners) < 1:  # No victors
            logging.info(f"NO WINNERS.")
            vMsg = f"""**FIND OF THE WEEK:** <t:{int(time.time())}:D>
It appears as if there aren't any winners for this week's find of the week :/
Remember: React to a message with <:emote:{int(emote_id)}> to enter someone's find into next week's FOTW!
The member with the most <:emote:{int(emote_id)}> reactions will win!
            """

        elif (
            len(winners) == 1
        ):  # One victor. Returns immediately to not tamper with the FOTW class any further.
            logging.info(
                f"ONE WINNER. {winners[0].author.id} LINK: https://discordapp.com/channels/{winners[0].guild.id}/{winners[0].channel.id}/{winners[0].id}"
            )
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


def setup(client):
    client.add_cog(Fotw(client))
