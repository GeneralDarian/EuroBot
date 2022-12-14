import logging
import string
from enum import Enum
from os import path

import discord
from discord import bot
from discord.commands import Option
from discord.ext import commands

from custom_types import CaseInsensitiveDict
from tools import textHelp


class Series(Enum):
    SERIES_1 = "The Ages and Styles of Europe"
    SERIES_2 = "Europa Series"


class BanknoteInfo:
    def __init__(self):
        self.valid = False
        self.series = None
        self.country = None
        self.printer = None


def checksum_validator(serial: str) -> list:
    banknote = BanknoteInfo()

    if serial[0] not in string.ascii_letters:
        raise ValueError("Banknote serial number must begin with a letter")

    # Ensure that no ValueError arises if input is just letters.
    serial += "0"

    banknote.series = (
        Series.SERIES_2 if serial[1] in string.ascii_letters else Series.SERIES_1
    )

    # series1_checksums[input] = (country, checksum)
    series1_checksums = CaseInsensitiveDict(
        {
            "d": ("!EE Estonia", 4),
            "e": ("!SK Slovakia", 3),
            "f": ("!MT Malta", 2),
            "g": ("!CY Cyprus", 1),
            "h": ("!SV Slovenia", 9),
            "l": ("!FI Finland", 5),
            "m": ("!PT Portugal", 4),
            "n": ("!AT Austria", 3),
            "p": ("!NL Netherlands", 1),
            "r": ("!LX Luxembourg", 8),
            "s": ("!IT Italy", 7),
            "t": ("!IE Ireland", 6),
            "u": ("!FR France", 5),
            "v": ("!ES Spain", 4),
            "x": ("!DE Germany", 2),
            "y": ("!GR Greece", 1),
            "z": ("!BE Belgium", 9),
        }
    )

    # series2_checksums[input] = (country, printer, checksum)
    series2_checksums = CaseInsensitiveDict(
        {
            "d": ("!PL Poland", "Polska Wytwórnia Papierów Wartościowych", 4),
            "e": ("!FR France", "Oberthur", 3),
            "f": ("!BG Bulgaria", "Oberthur Fiduciaire AD Bulgaria", 2),
            "h": ("!UK United Kingdom", "De La Rue Loughton", 9),
            "j": ("!UK United Kingdom", "De La Rue Gateshead", 7),
            "m": ("!PT Portugal", "Valora", 4),
            "n": (
                "!AT Austria",
                "Österreichische Banknoten‐ und Sicherheitsdruck GmbH",
                3,
            ),
            "p": ("!NL Netherlands", "Koninklĳke Joh. Enschedé", 1),
            "r": ("!DE Germany", "Bundesdruckerei", 8),
            "s": ("!IT Italy", "Banca d'Italia", 7),
            "t": ("!IE Ireland", "Central Bank of Ireland", 6),
            "u": ("!FR France", "Banque de France", 5),
            "v": ("!ES Spain", "FNMT-RCM", 4),
            "w": ("!DE Germany", "Giesecke+Devrient (Leipzig)", 3),
            "x": ("!DE Germany", "Giesecke+Devrient (Munich)", 2),
            "y": ("!GR Greece", "Bank of Greece", 1),
            "z": ("!BE Belgium", "National Bank of Belgium", 9),
        }
    )

    # Pick the right series dictionary to look through.  Also, this is the step which will check for
    # any stray letters which may have wandered their way into the serial number due to user
    # misinput.
    try:
        if banknote.series == Series.SERIES_1:
            series_checksums = series1_checksums
            checksum = int(serial[1:]) if serial[1:] != "" else None
        else:
            series_checksums = series2_checksums
            # It has to append the ASCII value of the second letter here to the end of the number
            checksum = (
                int(serial[2:]) * 100 + ord(serial[1].upper())
                if serial[2:] != ""
                else None
            )
    except ValueError:
        raise ValueError("Given serial number follows an invalid format")

    # Is the first letter in the series checksum?  If not the note may have not been entered
    # properly.
    if not serial[0] in series_checksums:
        raise ValueError(f"Country/Printer code ‘{serial[0]}’ doesn’t exist")

    if banknote.series == Series.SERIES_1:
        banknote.country, _ = series1_checksums[serial[0]]
    else:
        banknote.country, banknote.printer, _ = series2_checksums[serial[0]]

    # Calculates the digital root, compares it to checksum, and also ensures that the length is
    # correct
    banknote.valid = (
        checksum is not None
        and (checksum - 1) % 9 + 1 == series_checksums[serial[0].lower()][-1]
        and len(serial) == 13
    )

    return banknote


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
        serial=Option(str, "Your banknotes’ serial number", required=True),
    ):
        try:
            banknote_info = checksum_validator(serial)
        except ValueError as err:
            await ctx.respond(f"**Error:** {err}")

        match banknote_info.series:
            case Series.SERIES_1:
                description = (
                    f"**Series:** {banknote_info.series.value}\n"
                    + f"**Country:** {textHelp.emojiReplacer(banknote_info.country)}\n"
                    + f"**Valid:** {banknote_info.valid}"
                )
            case Series.SERIES_2:
                description = (
                    f"**Series:** {banknote_info.series.value}\n"
                    + f"**Country:** {textHelp.emojiReplacer(banknote_info.country)}\n"
                    + f"**Printer:** {banknote_info.printer}\n"
                    + f"**Valid:** {banknote_info.valid}"
                )

        embed = discord.Embed(
            title=f"Banknote Information for Serial `{serial}`",
            description=description,
            color=0xFFCC00,
        )
        embed.set_footer(text=self.client.version)
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Banknote(client))
