from dataclasses import dataclass
from enum import Enum

from discord import app_commands

import textHelp

SERIES_1_CHECKSUMS = {
    "D": ("Estonia !EE", 4),
    "E": ("Slovakia !SK", 3),
    "F": ("Malta !MT", 2),
    "G": ("Cyprus !CY", 1),
    "H": ("Slovenia !SV", 9),
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


@dataclass
class Banknote:
    issuer: str
    series: BanknoteSeries
    valid: bool


def init(client):
    @client.tree.command(
        name="banknote",
        description="Find out where a banknote is from, and validate the serial number",
    )
    @app_commands.describe(serial="Your banknotes serial number")
    async def banknote(interaction, serial: str):
        try:
            banknote = validateChecksum(client, serial)
        except Exception as err:
            print(err)
            await client.send(interaction, "Something bad happened… Contact an admin.")
        else:
            client.logger.debug(f"Banknote with serial {serial} validated: {banknote}")
            await client.send(
                interaction,
                textHelp.concat(
                    f"💶 **Banknote information for serial** ``{serial}``",
                    f"**SERIES:** {banknote.series}",
                    f"**ISSUER:** {textHelp.emojiReplacer(banknote.issuer)}",
                    f"**VALID:** {banknote.valid}",
                ),
            )


def validateChecksum(client, n: str) -> Banknote:
    """Displays information about a euro banknote checksum
    Input: The banknote
    Output: A list containing information.
    List[0] = 0 if this is an invalid banknote, 1 if this is a series 1 banknote, 2 if this is a series 2 banknote
    """
    # Check for both valid input and if its a S1 or S2 input
    if not n[0].isalpha():
        raise Exception("Input must begin with letter")

    # Ensures that no ValueError arises if input is just letters.
    n = n.upper() + "0"

    series = BanknoteSeries.Series2 if n[1].isalpha() else BanknoteSeries.Series1

    try:
        if series == BanknoteSeries.Series1:
            seriesChecksums = SERIES_1_CHECKSUMS
            checksum = int(n[1:])
        else:
            seriesChecksums = SERIES_2_CHECKSUMS
            # It has to append the ASCII value of the second letter here to the end of the number
            checksum = int(n[2:]) * 100 + ord(n[1])
    except ValueError:
        raise Exception("Invalid serial number format")
    except Exception as err:
        client.logger.error(f"Function validateChecksum encountered an error: {err}")
        raise Exception("Something went wrong… please contact an admin!")

    # Is the first letter in the series checksum?  If not the note may have not been entered properly.
    if not n[0] in seriesChecksums:
        raise Exception("Issuer/Printer doesnt exist")
    else:
        issuer = seriesChecksums[n[0]][0]

    # Calculates the digital root, compares it to checksum, and also ensures that the length is correct
    try:
        valid = (int(checksum) - 1) % 9 + 1 == seriesChecksums[n[0]][1] and len(n) == 13
    except Exception as err:
        client.logger.error(
            f"/banknote: Function validateChecksum encountered an error: {err}"
        )

    return Banknote(issuer, series, valid)
