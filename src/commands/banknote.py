import logging
from os import path

from discord import bot
from discord.commands import Option
from discord.ext import commands

from tools import banknote as cmdBanknote
from tools import textHelp


class Banknote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Get information about a banknote")
    async def banknote(
        self,
        ctx,
        serial=Option(
            str,
            "Enter the serial number or type 'help' for help",
            required=False,
            default="help",
        ),
    ):
        if serial is None or serial.lower() == "help":
            await ctx.respond(
                f"""**/BANKNOTE HELP**
Use ``eur!banknote <ID>`` to get banknote information, where <ID> is the banknote serial. Do not add printer identification codes or vertical serial numbers.
Here is the location of the euro banknote serials for both Series 1 (top) and Series 2 (bottom): https://imgur.com/u3IraLz"""
            )
            return

        # Get banknote info
        banknoteInfo = cmdBanknote.checkSumValidator(serial)
        # Was there an error when getting banknote information?
        if banknoteInfo[0] == 0:
            if len(banknoteInfo) <= 1:
                await ctx.respond("Something went wrong... please contact an admin!")
                logging.error("Executing banknote command returned len <= 1.")
            else:
                await ctx.send(f"**Error:** {banknoteInfo[1]}")
            return

        # Display banknote information
        if banknoteInfo[0] == 1:
            await ctx.respond(
                f"💶 **Banknote information for serial** ``{serial}``\n**SERIES:** 1\n**ISSUER:** {textHelp.emojiReplacer(banknoteInfo[1].upper())}\n**VALID:** {banknoteInfo[2]}"
            )
        else:
            await ctx.respond(
                f"💶 **Banknote information for serial** ``{serial}``\n**SERIES:** 2\n**PRINTER:** {textHelp.emojiReplacer(banknoteInfo[1].upper())}\n**VALID:** {banknoteInfo[2]}"
            )


def setup(client):
    client.add_cog(Banknote(client))
