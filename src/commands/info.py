import logging
from os import path

import discord
from discord import SelectOption, bot
from discord.commands import option
from discord.ext import commands
from discord.ext.pages import Page, Paginator

from custom_types import CaseInsensitiveDict
from tools import textHelp

pages = CaseInsensitiveDict(
    {
        "cleaning": textHelp.info_cleaning_text,
        "coin roll hunting": {
            "placeholder": "Select a country for specific information",
            "entries": {
                "Andorra": {
                    "emoji": "!AD",
                    "description": textHelp.info_crh_andorra_text,
                },
                "Austria": {
                    "emoji": "!AT",
                    "description": textHelp.info_crh_austria_text,
                },
                "Belgium": {
                    "emoji": "!BE",
                    "description": textHelp.info_crh_belgium_text,
                },
                "Croatia": {
                    "emoji": "!HR",
                    "description": textHelp.info_crh_croatia_text,
                },
                "Cyprus": {
                    "emoji": "!CY",
                    "description": textHelp.info_crh_cyprus_text,
                },
                "Estonia": {
                    "emoji": "!EE",
                    "description": textHelp.info_crh_estonia_text,
                },
                "Finland": {
                    "emoji": "!FI",
                    "description": textHelp.info_crh_finland_text,
                },
                "France": {
                    "emoji": "!FR",
                    "description": textHelp.info_crh_france_text,
                },
                "Germany": {
                    "emoji": "!DE",
                    "description": textHelp.info_crh_germany_text,
                },
                "Greece": {
                    "emoji": "!GR",
                    "description": textHelp.info_crh_greece_text,
                },
                "Ireland": {
                    "emoji": "!IE",
                    "description": textHelp.info_crh_ireland_text,
                },
                "Italy": {
                    "emoji": "!IT",
                    "description": textHelp.info_crh_italy_text,
                },
                "Latvia": {
                    "emoji": "!LV",
                    "description": textHelp.info_crh_latvia_text,
                },
                "Lithuania": {
                    "emoji": "!LT",
                    "description": textHelp.info_crh_lithuania_text,
                },
                "Luxembourg": {
                    "emoji": "!LU",
                    "description": textHelp.info_crh_luxembourg_text,
                },
                "Malta": {
                    "emoji": "!MT",
                    "description": textHelp.info_crh_malta_text,
                },
                "Monaco": {
                    "emoji": "!MC",
                    "description": textHelp.info_crh_monaco_text,
                },
                "Netherlands": {
                    "emoji": "!NL",
                    "description": textHelp.info_crh_netherlands_text,
                },
                "Portugal": {
                    "emoji": "!PT",
                    "description": textHelp.info_crh_portugal_text,
                },
                "San Marino": {
                    "emoji": "!SM",
                    "description": textHelp.info_crh_san_marino_text,
                },
                "Slovakia": {
                    "emoji": "!SK",
                    "description": textHelp.info_crh_slovakia_text,
                },
                "Slovenia": {
                    "emoji": "!SI",
                    "description": textHelp.info_crh_slovenia_text,
                },
                "Spain": {
                    "emoji": "!ES",
                    "description": textHelp.info_crh_spain_text,
                },
                "Vatican City": {
                    "emoji": "!VA",
                    "description": textHelp.info_crh_vatican_city_text,
                },
            },
        },
        "find of the week": textHelp.info_find_of_the_week_text,
        "lists": textHelp.list_info,
        "mintmarks": textHelp.info_mintmarks_text,
        "rare coins": textHelp.info_rare_coins_text,
        "storage": (
            textHelp.info_storage_text_opener,
            textHelp.info_storage_text_albums,
            textHelp.info_storage_text_boxes,
            textHelp.info_storage_text_capsules,
            textHelp.info_storage_text_flips,
        ),
    }
)


class InfoCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(
            f"Cog {path.basename(__file__).removesuffix('.py')} loaded successfully"
        )

    @bot.command(description="Get help for various bot commands")
    @option(
        name="topic",
        description="Topic to get information on",
        autocomplete=discord.utils.basic_autocomplete(pages.keys()),
        required=True,
        default=None,
    )
    async def info(self, ctx, topic: str):
        if topic is None:
            embed = discord.Embed(
                title=f"Invalid `/info` Usage",
                description="No topic was provided! For help using the `/info` command, try `/help info`.",
                color=0xFFCC00,
            )
            embed.add_default_footer()
            await ctx.respond(embed=embed)

        data = pages.get(topic, f"No information found for the topic “{topic}”")

        if type(data) is str:
            embed = discord.Embed(
                title=f"“{topic.title()}” Info Page",
                description=data,
                color=0xFFCC00,
            )
            embed.add_default_footer()
            await ctx.respond(embed=embed)
        elif type(data) is tuple:
            numpages = len(data)
            builtpages = []
            for i in range(numpages):
                embed = discord.Embed(
                    title=f"“{topic.title()}” Info Page [{i + 1} / {numpages}]",
                    description=data[i],
                    color=0xFFCC00,
                )
                embed.add_default_footer()
                builtpages.append(Page(embeds=[embed]))
            await Paginator(pages=builtpages, show_disabled=False).respond(
                ctx.interaction, ephemeral=False
            )
        elif type(data) is dict:

            class Dropdown(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=60)

                @discord.ui.select(
                    placeholder=data["placeholder"],
                    min_values=1,
                    max_values=1,
                    options=[
                        SelectOption(
                            label=key.title(),
                            emoji=textHelp.emojiReplacer(data["entries"][key]["emoji"]),
                        )
                        for key in data["entries"]
                    ],
                )
                async def select_callback(self, select, interaction):
                    value = select.values[0]
                    embed = discord.Embed(
                        title=f"“{topic.title()}” Info Page [{value.title()}]",
                        description=data["entries"][value]["description"],
                        color=0xFFCC00,
                    )
                    embed.add_default_footer()

                    await interaction.message.edit(content=None, embed=embed)
                    await interaction.response.defer(ephemeral=True)

                async def on_timeout(self):
                    for child in self.children:
                        child.disabled = True
                    await self.message.edit(content=None, view=self)

            embed = discord.Embed(
                title=f"“{topic.title()}” Info Page",
                description=textHelp.crh_info,
                color=0xFFCC00,
            )
            embed.add_default_footer()
            await ctx.respond(embed=embed, view=Dropdown())
        else:
            embed = discord.Embed(
                title="Error!",
                description="Something went horribly wrong… please contact a bot admin.",
                color=0xFF0000,
            )
            embed.add_default_footer()
            await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(InfoCommand(client))
