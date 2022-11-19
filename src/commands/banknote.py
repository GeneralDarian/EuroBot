from discord.ext import commands
from discord.commands import Option
from discord import bot
import logging
from tools import banknote as cmdBanknote
from tools import textHelp

class Banknote(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command(description="Get information about a banknote")
    async def banknote(self, ctx, serial=Option(str, "Enter the serial number or type 'help' for help", required = False, default = 'help')):  # eur!banknote command
        # display help info if arg1 is not set or if arg1 == "help"
        arg1 = serial
        if arg1 is None or arg1.lower() == "help":
            await ctx.respond(
                f"""**/BANKNOTE HELP**
Use ``eur!banknote <ID>`` to get banknote information, where <ID> is the banknote serial. Do not add printer identification codes or vertical serial numbers.
Here is the location of the euro banknote serials for both Series 1 (top) and Series 2 (bottom): https://imgur.com/u3IraLz"""
            )
            return
        elif "`" in arg1:
            await ctx.respond(f"Error: Invalid input")
            return

        # Get banknote info
        banknoteInfo = cmdBanknote.checkSumValidator(str(arg1))
        # Was there an error when getting banknote information?
        if banknoteInfo[0] == 0:
            if len(banknoteInfo) <= 1:
                await ctx.respond("Something went wrong... please contact an admin!")
                logging.error("Executing banknote command returned len <= 1.")
                return
            else:
                await ctx.send(f"**Error:** {banknoteInfo[1]}")
                return

        # Display banknote information
        if banknoteInfo[0] == 1:
            await ctx.respond(
                f"💶 **Banknote information for serial** ``{arg1}``\n**SERIES:** 1\n**ISSUER:** {textHelp.emojiReplacer(banknoteInfo[1].upper())}\n**VALID:** {banknoteInfo[2]}"
            )
        else:
            await ctx.respond(
                f"💶 **Banknote information for serial** ``{arg1}``\n**SERIES:** 2\n**PRINTER:** {textHelp.emojiReplacer(banknoteInfo[1].upper())}\n**VALID:** {banknoteInfo[2]}"
            )
        return

def setup(client):
    client.add_cog(Banknote(client))
