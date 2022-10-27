import logging
from enum import Enum
from typing import NamedTuple

from discord import app_commands

import textHelp
from bot import EuroBot

logger = logging.getLogger(f"{EuroBot.name}.{__name__}")

SERIES_1_CHECKSUMS = {
    "D": ("Estonia !EE", 4),
    "E": ("Slovakia !SK", 3),
    "F": ("Malta !MT", 2),
    "G": ("Cyprus !CY", 1),
    "H": ("Slovenia !SI", 9),
    "L": ("Finland !FI", 5),
    "M": ("Portugal !PT", 4),
    "N": ("Austria !AT", 3),
    "P": ("Netherlands !NL", 1),
    "R": ("Luxembourg !LX", 8),
    "S": ("Italy !IT", 7),
    "T": ("Ireland !IE", 6),
    "U": ("France !FR", 5),
    "V": ("Spain !ES", 4),
    "X": ("Germany !DE", 2),
    "Y": ("Greece !GR", 1),
    "Z": ("Belgium !BE", 9),
}

SERIES_2_CHECKSUMS = {
    "D": ("Polska Wytwórnia Papierów Wartościowych !PL", 4),
    "E": ("Oberthur !FR", 3),
    "F": ("Oberthur Fiduciaire AD Bulgaria !BG", 2),
    "H": ("De La Rue Loughton !UK", 9),
    "J": ("De La Rue Gateshead !UK", 7),
    "M": ("Valora !PT", 4),
    "N": ("Österreichische Banknoten‐ und Sicherheitsdruck GmbH !AT", 3),
    "P": ("Koninklĳke Joh. Enschedé !NL", 1),
    "R": ("Bundesdruckerei !DE", 8),
    "S": ("Banca d'Italia !IT", 7),
    "T": ("Central Bank of Ireland !IE", 6),
    "U": ("Banque de France !FR", 5),
    "V": ("FNMT-RCM !ES", 4),
    "W": ("Giesecke+Devrient (Leipzig) !DE", 3),
    "X": ("Giesecke+Devrient (Munich) !DE", 2),
    "Y": ("Bank of Greece !GR", 1),
    "Z": ("National Bank of Belgium !BE", 9),
}


class BanknoteSeries(Enum):
    Series1 = "The Ages and Styles of Europe"
    Series2 = "Europa Series"

    # TODO: Remove these methods when we upgrade to Python3.11
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()


class Banknote(NamedTuple):
    issuer: str
    series: BanknoteSeries
    isValid: bool


def init(client):
    @client.tree.command(
        name="banknote",
        description="Find out where a banknote is from, and validate the serial number",
    )
    @app_commands.describe(serial="Your banknotes serial number")
    async def banknote(interaction, serial: str):
        try:
            banknote = parseSerial(serial)
        except (LookupError, ValueError) as err:
            logger.debug(err)
            await client.send(interaction, err)
        except Exception as err:
            logger.error(err)
            await client.send(interaction, "Something bad happened… Contact an admin.")
        else:
            logger.debug(f"Serial number “{serial}” parsed: {banknote}")
            await client.send(
                interaction,
                textHelp.concat(
                    f"💶 **Banknote information for serial** ``{serial}``",
                    f"**SERIES:** {banknote.series}",
                    f"**ISSUER:** {textHelp.emojiReplacer(banknote.issuer)}",
                    f"**VALID:** {banknote.isValid}",
                ),
            )


def parseSerial(serial: str) -> Banknote:
    """
    Parse a banknotes serial number and determine the series, issuer, etc.  The banknote serial
    number is also validated.

    serial => The banknote serial number
    return => A Banknote
    """
    # In theory, this is impossible, but better safe than sorry.
    if len(serial) == 0:
        raise ValueError("Serial number cannot be empty")
    if not serial[0].isalpha():
        raise ValueError("Serial number must begin with a letter")

    # Ensures that no ValueError arises if input is just letters.
    serial = serial.upper() + "0"
    series = BanknoteSeries.Series2 if serial[1].isalpha() else BanknoteSeries.Series1
    prefix = serial[0]

    try:
        if series == BanknoteSeries.Series1:
            issuer, root = SERIES_1_CHECKSUMS[prefix]
            checksum = int(serial[1:])
        else:
            issuer, root = SERIES_2_CHECKSUMS[prefix]
            checksum = int(serial[2:]) * 100 + ord(serial[1])
    except KeyError:
        raise LookupError(f"Issuer/Printer code ‘{prefix}’ doesn’t exist")
    except ValueError:
        isValid = False
    else:
        isValid = (checksum - 1) % 9 + 1 == root and len(serial) == 13
    return Banknote(issuer, series, isValid)
