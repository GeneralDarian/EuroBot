import logging

def checkSumValidator(n: str) -> list:
    """Displays information about a euro banknote checksum
    Input: The banknote
    Output: A list containing information.
    List[0] = 0 if this is an invalid banknote, 1 if this is a series 1 banknote, 2 if this is a series 2 banknote
    """
    final = []

    # Check for both valid input and if its a S1 or S2 input
    letters = "abcdefghijklmnopqrstuvwxyz"
    if n[0].lower() not in letters:  # Check valid input
        final.append(0)
        final.append("Input must begin with letter")
        return final

    n = n + "0"  # ensures that no valueerror arises if input is just letters.

    if n[1].lower() in letters:  # If the second digit is a letter it is a S2 banknote
        final.append(2)
        series = 2
    else:  # Else this is a S1 banknote
        final.append(1)
        series = 1

    # series1checksums[input] = [countryname, checksum]
    series1checksums = {
        "d": ["Estonia !EE", 4],
        "e": ["Slovakia !SK", 3],
        "f": ["Malta !MT", 2],
        "g": ["Cyprus !CY", 1],
        "h": ["Slovenia !SV", 9],
        "l": ["Finland !FI", 5],
        "m": ["Portugal !PT", 4],
        "n": ["Austria !AT", 3],
        "p": ["Netherlands !NL", 1],
        "r": ["Luxembourg !LX", 8],
        "s": ["Italy !IT", 7],
        "t": ["Ireland !IE", 6],
        "u": ["France !FR", 5],
        "v": ["Spain !ES", 4],
        "x": ["Germany !DE", 2],
        "y": ["Greece !GR", 1],
        "z": ["Belgium !BE", 9],
    }

    # series2checksums[input] = [printername, checksum]
    series2checksums = {
        "d": ["Polska Wytwórnia Papierów Wartościowych !PL", 4],
        "e": ["Oberthur !FR", 3],
        "f": ["	Oberthur Fiduciaire AD Bulgaria !BG", 2],
        "h": ["De La Rue Loughton !UK", 9],
        "j": ["De La Rue Gateshead !UK", 7],
        "m": ["Valora !PT", 4],
        "n": ["Österreichische Banknoten‐ und Sicherheitsdruck GmbH !AT", 3],
        "p": ["Koninklijke Joh. Enschedé !NL", 1],
        "r": ["Bundesdruckerei !DE", 8],
        "s": ["Banca d'Italia !IT", 7],
        "t": ["Central Bank of Ireland !IE", 6],
        "u": ["Banque de France !FR", 5],
        "v": ["FNMT-RCM !ES", 4],
        "w": ["Giesecke+Devrient (Leipzig) !DE", 3],
        "x": ["Giesecke+Devrient (Munich) !DE", 2],
        "y": ["Bank of Greece !GR", 1],
        "z": ["National Bank of Belgium !BE", 9],
    }

    # Pick the right series dictionary to look through
    # Also, this is the step which will check for any stray letters which may have wandered their way into the serial number
    # due to user misinput.
    try:
        if series == 1:
            serieschecksums = series1checksums
            checksum = int(n[1:])
        else:
            serieschecksums = series2checksums
            # It has to append the ASCII value of the second letter here to the end of the number
            checksum = int(n[2:]) * 100 + ord(n[1])
    except ValueError:
        final.append(0)
        final.append("Misinput")
        return final
    except Exception as error:
        logging.error(f"Function checkSumValidator encountered an error: {error}")
        final.append("Something went wrong... please contact an admin!")
        return final

    # Is the first letter in the series checksum? If not the note may have not been entered properly.
    if not n[0].lower() in serieschecksums:
        final[0] = 0
        final.append("Issue/Printer doesnt exist")
        return final
    else:
        final.append(serieschecksums[n[0].lower()][0])

    # Calculates the digital root, compares it to checksum, and also ensures that the length is correct
    try:
        if (int(checksum) - 1) % 9 + 1 == serieschecksums[n[0].lower()][1] and len(n) == 13:
            final.append(True)
        else:
            final.append(False)
    except Exception as error:
        logging.error(f"!banknote : Function checkSumValidator encountered an error: {error}")


    return final
