import datetime
import logging
from os import path

import discord
from discord import bot
from discord.ext import commands

from tools import findOfTheWeek


class ServerInfoCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Get information about the current server")
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            title="/r/EuroCoins — Server and Bot Information",
            url="https://github.com/GeneralDarian/EuroBot",
            description="EuroBot is an open source project created by <@!228069568222855169> and <@!280428276810383370>. Click on the embed title to visit the bot's github!",
            color=0xFFCC00,
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
            name="Server is currently…",
            value=guild_creation_value,
        )
        embed.add_field(
            name="EuroBot Discord:",
            value="https://discord.gg/ev53PnSaXV",
        )
        embed.set_footer(text=self.client.version)
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(ServerInfoCommand(client))
