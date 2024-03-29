import logging
import os
from os import path

import discord
from discord import bot
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands

from tools import designer, textHelp


class ToCoin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.s = 1.0
        self.i = 5.0
        self.nmd = 4.0
        self.using_tocoin = False

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    tocoin = SlashCommandGroup("tocoin", "Change tocoin settings")

    @tocoin.command(description="Change tocoin's image settings")
    async def settings(
        self,
        ctx,
        sigma=Option(
            float,
            "Modifies how sharp image appears on coin.",
            required=False,
            default=1,
        ),
        intensity=Option(
            float,
            "Modifies how visible image appears on coin.",
            required=False,
            default=5,
        ),
        nmd=Option(
            float,
            "How much dark areas of the coin pop out. Changing this doesn't do much - best to leave at 1-4",
            required=False,
            default=4,
        ),
    ):
        self.s = float(sigma)
        self.i = float(intensity)
        self.nmd = float(nmd)

        if not 0 <= self.f <= 20:
            await ctx.respond("Sigma must be between 0 and 20")
            return
        elif not 0 <= self.i <= 20:
            await ctx.respond("Intensity must be between 0 and 20")
            return
        elif not 1 <= self.nmd <= 10:
            await ctx.respond("nmd must be between 1 and 10")
            return
        await ctx.respond(
            f"CoinDesigner options changed to:\n**sigma**: {self.s}\n**intensity**: {self.i}\n**nmd**: {self.nmd}"
        )

    @tocoin.command(description="Reset tocoin's image settings to their default")
    async def reset(self, ctx):
        self.s = 1
        self.i = 5
        self.nmd = 4
        await ctx.respond(
            f"Reset CoinDesigner to default settings:\n**sigma**: {self.s}\n**intensity**: {self.i}\n**nmd**: {self.nmd}"
        )

    @commands.message_command()
    async def Convert(self, ctx, msg: discord.Message):
        """Processes an image using Frakkur's image to 2-euro coin program."""

        # Check to make sure this command isn’t currently being used.  Otherwise file deletion
        # becomes a bit screwed up.
        if self.using_tocoin:
            await ctx.respond(
                "This command is currently in use. Please wait a few seconds before running it.",
                ephemeral=True,
            )
            return
        self.using_tocoin = True
        await ctx.defer()
        response = False

        if not msg.attachments:
            await ctx.respond(
                "There are no attachments on this message!", ephemeral=True
            )
            self.using_tocoin = False
            return

        for file in msg.attachments:
            if file.filename.endswith(".jpg") or file.filename.endswith(".png"):
                attachment = msg.attachments[0]
                response = designer.euro_designer(
                    attachment.url,
                    self.s,
                    self.i,
                    self.nmd,
                )
            else:
                await ctx.respond(
                    "The attachment on this image is invalid!", ephemeral=True
                )
                self.using_tocoin = False
                return

        # If the response is true then conversion was successful.  Get the file, send in embed, and
        # then delete the file.
        if response:
            file = discord.File("data/outputs/output.png", filename="image.png")
            embed = discord.Embed(
                title=f"Sigma = {self.s}, Intensity = {self.i}, NMD = {self.nmd}"
            )
            embed.set_image(url="attachment://image.png")
            embed.set_footer(
                text="CoinDesigner by <@!273393211156856832> — https://github.com/joaoperfig — Use `/tocoin help` for help with changing settings"
            )
            await ctx.respond(file=file, embed=embed)
            os.remove("data/outputs/output.png")
        else:
            await ctx.respond(
                "There was an error processing the image. Please contact an admin!",
                ephemeral=True,
            )

        self.using_tocoin = False


def setup(client):
    client.add_cog(ToCoin(client))
