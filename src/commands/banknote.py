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

PRINTERS = CaseInsensitiveDict(
    {
        "d": "!FI SETEC",
        "e": "!FR Oberthur",
        "f": "!AT Österreichische Banknoten‐ und Sicherheitsdruck GmbH",
        "g": "!NL Koninklĳke Joh. Enschedé",
        "h": "!UK Thomas de la Rue",
        "j": "!IT Banca d’Italia",
        "k": "!IE Central Bank of Ireland",
        "l": "!FR Banque de France",
        "m": "!ES Fábrica Nacional de Moneda y Timbre",
        "n": "!GR Bank of Greece",
        "p": "!DE Giesecke & Devrient",
        "r": "!DE Bundesdruckerei Berlin",
        "t": "!BE National Bank of Belgium",
        "u": "!PT Valora",
    }
)


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
            "s": ("!IT Italy", 7),
            "t": ("!IE Ireland", 6),
            "u": ("!FR France", 5),
            "v": ("!ES Spain", 4),
            "x": ("!DE Germany", 2),
            "y": ("!GR Greece", 1),
            "z": ("!BE Belgium", 9),
        }
    )

    # series2_checksums[input] = (printer, checksum)
    series2_checksums = CaseInsensitiveDict(
        {
            "e": ("!FR Oberthur", 3),
            "f": ("!BG Oberthur Fiduciaire AD", 2),
            "m": ("!PT Valora", 4),
            "n": (
                "!AT Österreichische Banknoten‐ und Sicherheitsdruck GmbH",
                3,
            ),
            "p": ("!NL Koninklĳke Joh. Enschedé", 1),
            "r": ("!DE Bundesdruckerei Berlin", 8),
            "s": ("!IT Banca d’Italia", 7),
            "t": ("!IE Central Bank of Ireland", 6),
            "u": ("!FR Banque de France", 5),
            "v": ("!ES Fábrica Nacional de Moneda y Timbre", 4),
            "w": ("!DE Giesecke & Devrient Leipzig", 3),
            "x": ("!DE Giesecke & Devrient Munich", 2),
            "y": ("!GR Bank of Greece", 1),
            "z": ("!BE National Bank of Belgium", 9),
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
        raise ValueError(f"Printer code ‘{serial[0]}’ doesn’t exist")

    if banknote.series == Series.SERIES_1:
        banknote.country, _ = series1_checksums[serial[0]]
    else:
        banknote.printer, _ = series2_checksums[serial[0]]

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
        serial=Option(str, "Your banknote’s serial number", required=True),
        printer_code=Option(
            str, "Your banknote’s printer code (series 1 only)", required=False
        ),
    ):
        try:
            banknote_info = checksum_validator(serial)
        except ValueError as err:
            await ctx.respond(f"**Error:** {err}")

        match banknote_info.series:
            case Series.SERIES_1:
                if type(printer_code) is str:
                    if len(printer_code) == 0:
                        await ctx.respond("**Error:** Empty printer code provided")
                        return
                    if (c := printer_code[0]) not in PRINTERS:
                        await ctx.respond(f"**Error:** Printer ‘{c}’ doesn’t exist")
                        return
                    printer = textHelp.emojiReplacer(PRINTERS[c])
                else:
                    printer = "Unknown"

                description = (
                    f"**Series:** {banknote_info.series.value}\n"
                    + f"**Country:** {textHelp.emojiReplacer(banknote_info.country)}\n"
                    + f"**Printer**: {printer}\n"
                    + f"**Valid:** {banknote_info.valid}"
                )
            case Series.SERIES_2:
                description = (
                    f"**Series:** {banknote_info.series.value}\n"
                    + f"**Printer:** {textHelp.emojiReplacer(banknote_info.printer)}\n"
                    + f"**Valid:** {banknote_info.valid}"
                )

        embed = discord.Embed(
            title=f"Banknote Information for Serial `{serial}`",
            description=description,
            color=0xFFCC00,
        )
        embed.add_default_footer()
        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(Banknote(client))
