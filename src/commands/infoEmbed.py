import discord
import datetime
from discord.ext import commands
from discord.commands import Option
from discord import bot
import logging, time
from tools import findOfTheWeek

class InfoEmbed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Cog info loaded successfully")

    @bot.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="/r/EuroCoins - Server and Bot Information",
            url="https://github.com/GeneralDarian/EuroBot",
            color=0xffcc00
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/555331630206681108/ce006b24f0d5fb90fbbcfc53c17ab4a2"
        )
        embed.add_field(
            name="Server Members",
            value=len([user for user in self.client.users if not user.bot]),
            inline=True,
        )
        traders_role = ctx.guild.get_role(int(findOfTheWeek.TRADER_ROLE_ID))
        embed.add_field(name="Verified Traders", value=len(traders_role.members))
        guild_creation_time = ctx.guild.created_at
        guild_diff = (
            datetime.datetime.now(datetime.timezone.utc) - guild_creation_time
        ).days
        guild_creation_value = f"{guild_diff} days old\nCreated {guild_creation_time.strftime('%d. %B %Y')}"
        embed.add_field(
            name="Server is currently...",
            value=guild_creation_value,
        )
        embed.add_field(
            name="Bot version:",
            value="1.1 [Released 2022.11.20]",
        )
        embed.add_field(
            name="EuroBot Discord:",
            value="https://discord.gg/ev53PnSaXV",
        )
        embed.set_footer(
            text="EuroBot is an open source project created by @General Darian ✓ᵛᵉʳᶦᶠᶦᵉᵈ#8498 and @Mango Man#0669. Click on the embed title to visit the bot's github!",
            icon_url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        )
        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(InfoEmbed(client))