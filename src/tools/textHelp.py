import logging
import re

from custom_types import CaseInsensitiveDict
from tools import findOfTheWeek

emote_id = findOfTheWeek.EMOTE_ID


def emojiReplacer(s: str) -> str:
    """
    Given a string will replace all !<country_code> with their respective emoji.  If there is no
    emoji present, it just returns the string.

    Input:  string
    Output: string
    """

    codeToEmote = CaseInsensitiveDict(
        {
            "!AD": "🇦🇩",
            "!AT": "🇦🇹",
            "!BE": "🇧🇪",
            "!CY": "🇨🇾",
            "!DE": "🇩🇪",
            "!EE": "🇪🇪",
            "!ES": "🇪🇸",
            "!EU": "🇪🇺",
            "!FI": "🇫🇮",
            "!FR": "🇫🇷",
            "!GR": "🇬🇷",
            "!HR": "🇭🇷",
            "!IE": "🇮🇪",
            "!IT": "🇮🇹",
            "!LT": "🇱🇹",
            "!LU": "🇱🇺",
            "!LV": "🇱🇻",
            "!MC": "🇲🇨",
            "!MT": "🇲🇹",
            "!NL": "🇳🇱",
            "!PT": "🇵🇹",
            "!SI": "🇸🇮",
            "!SK": "🇸🇰",
            "!SM": "🇸🇲",
            "!VA": "🇻🇦",
        }
    )

    for match in re.findall(r"!..", s):
        s = s.replace(match, codeToEmote.get(match, match))

    return s


def get_multiple_result_desc(processed_results: dict) -> str:
    """Given a processed result dict, returns the processed string for display in the discord multiple search results embed.
    Inputs:
    - processed_results (dict): returned from calling coinData.searchProcessor()
    Outputs:
    - desc (str): String to put in the search results embed desc, returns error msg if something went wrong"""
    # {'Status': '0', 'Issuer': '', 'Type': '', 'Year': ''}
    desc = ""
    if processed_results["Issuer"].lower() in country_to_french:
        french_country = country_to_french[processed_results["Issuer"].lower()]
        desc = f"{french_to_genitive[french_country].upper()} {french_to_emoji[french_country]}"
    elif processed_results["Issuer"].lower() in country_id_to_french:
        french_country = country_id_to_french[processed_results["Issuer"].lower()]
        desc = f"{french_to_genitive[french_country].upper()} {french_to_emoji[french_country]}"
    else:
        desc = "Error: Could not fetch country from textHelp"
        return desc

    if (
        processed_results["Type"] is not None
        and processed_results["Type"].lower() in to_type
    ):
        type = to_type[processed_results["Type"].lower()]
        desc = f"{desc} {type}"
    desc = f"{desc} Coins"

    if processed_results["Year"] is not None:
        desc = f"{desc} minted in {processed_results['Year']}"

    return desc


def tocoin_argument_processor(content: str) -> dict:
    """Processes a list of arguments"""

    arguments = {"Status": None, "Sigma": 1, "Intensity": 5, "NMD": 4}

    if content is None:  # base case, if no arguments were supplied
        return arguments

    content_list = content.split()
    already_sigma = False
    already_intensity = False
    already_NMD = False

    for index, value in enumerate(content_list):
        if (
            value.lower() == "-s" and already_sigma == False
        ):  # Try to fetch the sigma value
            try:
                sigma = float(content_list[index + 1])
                if sigma > 10 or sigma < 0:
                    sigma = 0.1
                arguments["Sigma"] = sigma
                already_sigma = True
            except ValueError:  # If -s is not int
                arguments[
                    "Status"
                ] = "Invalid sigma (-s) argument given [argument must be a number]"
                return arguments
            except IndexError:  # If -s was never given
                arguments["Status"] = "Flag (-s) was used, but no argument was given."
                return arguments
        elif value.lower() == "-s" and already_sigma == True:
            arguments["Status"] = "Flag (-s) was used more than once."
            return arguments

        elif (
            value.lower() == "-i" and already_intensity == False
        ):  # Try to fetch the intensity value
            try:
                intensity = float(content_list[index + 1])
                if intensity > 15 or intensity < 0:
                    intensity = 0.1
                arguments["Intensity"] = intensity
                already_intensity = True
            except ValueError:  # If -i is not int
                arguments[
                    "Status"
                ] = "Invalid intensity (-i) argument given [argument must be a number]"
                return arguments
            except IndexError:  # If -i was never given
                arguments["Status"] = "Flag (-i) was used, but no argument was given."
                return arguments
        elif value.lower() == "-i" and already_intensity == True:
            arguments["Status"] = "Flag (-i) was used more than once."
            return arguments

        elif (
            value.lower() == "-nmd" and already_NMD == False
        ):  # Try to fetch the NMD value
            try:
                nmd = float(content_list[index + 1])
                if nmd > 10 or nmd < 1:
                    nmd = 1.0
                arguments["NMD"] = nmd
                already_NMD = True
            except ValueError:  # If -i is not int
                arguments[
                    "Status"
                ] = "Invalid NMD (-nmd) argument given [argument must be a number]"
                return arguments
            except IndexError:  # If -i was never given
                arguments["Status"] = "Flag (-nmd) was used, but no argument was given."
                return arguments
        elif value.lower() == "-nmd" and already_NMD == True:
            arguments["Status"] = "Flag (-nmd) was used more than once."
            return arguments

    # Final check to ensure nothing weird was fed through this command
    if any([already_NMD, already_intensity, already_sigma]) != True:
        arguments[
            "Status"
        ] = "Invalid arguments given. Arguments must be: <-s>, <-i>, <-nmd>. Arguments may be optional."
        logging.info(f"{already_sigma}, {already_intensity}, {already_NMD}")
    else:
        arguments["Status"] = ""

    logging.info(f"!tocoin : Processed {content} as {arguments}")
    return arguments


euro_country_list_fr = [
    "allemagne",
    "autriche",
    "belgique",
    "espagne",
    "finlande",
    "france",
    "irlande",
    "italie",
    "luxembourg",
    "pays-bas",
    "portugal",
    "grece",
    "slovenie",
    "chypre",
    "malte",
    "slovaquie",
    "estonie",
    "lettonie",
    "lituanie",
    "monaco",
    "saint-marin",
    "andorre",
    "croatie",
    "vatican",
]

types = ["1c", "2c", "5c", "10c", "20c", "50c", "1", "2", "2cc"]

blacklist = ["pattern", "Pattern"]

long_types = [
    "1 Euro Cent",
    "2 Euro Cent",
    "5 Euro Cent",
    "10 Euro Cent",
    "20 Euro Cent",
    "50 Euro Cent",
    "1 Euro",
    "2 Euro",
]


to_type = {
    "1c": "1 Euro Cent",
    "2c": "2 Euro Cent",
    "5c": "5 Euro Cent",
    "10c": "10 Euro Cent",
    "20c": "20 Euro Cent",
    "50c": "50 Euro Cent",
    "1": "1 Euro",
    "2": "2 Euro",
    "2cc": "2 Euro Commemorative",  # Beware of additional checks one might need to run!!!
}

from_type = {
    "1 cent": "1c",
    "2 cents": "2c",
    "5 cents": "5c",
    "10 cents": "10c",
    "20 cents": "20c",
    "50 cents": "50c",
    "1 euro": "1",
    "2 euro": "2",
    "2 euro commemorative": "2cc",
}

country_to_french = {
    "Andorra": "andorre",
    "Austria": "autriche",
    "Belgium": "belgique",
    "Croatia": "croatie",
    "Cyprus": "chypre",
    "Estonia": "estonie",
    "Finland": "finlande",
    "France": "france",
    "Germany": "allemagne",
    "Greece": "grece",
    "Ireland": "irlande",
    "Italy": "italie",
    "Latvia": "lettonie",
    "Lithuania": "lituanie",
    "Luxembourg": "luxembourg",
    "Malta": "malte",
    "Monaco": "monaco",
    "Netherlands": "pays-bas",
    "Portugal": "portugal",
    "San Marino": "saint-marin",
    "Slovakia": "slovaquie",
    "Slovenia": "slovenie",
    "Spain": "espagne",
    "Vatican": "vatican",
}


country_id_to_french = {
    "ad": "andorre",
    "at": "autriche",
    "be": "belgique",
    "cy": "chypre",
    "de": "allemagne",
    "ee": "estonie",
    "es": "espagne",
    "fi": "finlande",
    "fr": "france",
    "gr": "grece",
    "ie": "irlande",
    "it": "italie",
    "lt": "lituanie",
    "lu": "luxembourg",
    "lv": "lettonie",
    "mc": "monaco",
    "mt": "malte",
    "nl": "pays-bas",
    "pt": "portugal",
    "si": "slovenie",
    "sk": "slovaquie",
    "sm": "saint-marin",
    "va": "vatican",
}

french_to_emoji = {
    "allemagne": "🇩🇪",
    "andorre": "🇦🇩",
    "autriche": "🇦🇹",
    "belgique": "🇧🇪",
    "chypre": "🇨🇾",
    "croatie": "🇭🇷",
    "espagne": "🇪🇸",
    "estonie": "🇪🇪",
    "finlande": "🇫🇮",
    "france": "🇫🇷",
    "grece": "🇬🇷",
    "irlande": "🇮🇪",
    "italie": "🇮🇹",
    "lettonie": "🇱🇻",
    "lituanie": "🇱🇹",
    "luxembourg": "🇱🇺",
    "malte": "🇲🇹",
    "monaco": "🇲🇨",
    "pays-bas": "🇳🇱",
    "portugal": "🇵🇹",
    "saint-marin": "🇸🇲",
    "slovaquie": "🇸🇰",
    "slovenie": "🇸🇮",
    "vatican": "🇻🇦",
}

french_to_genitive = {
    "allemagne": "German",
    "andorre": "Andorran",
    "autriche": "Austrian",
    "belgique": "Belgian",
    "chypre": "Cypriot",
    "espagne": "Spanish",
    "estonie": "Estonian",
    "finlande": "Finnish",
    "france": "French",
    "grece": "Greek",
    "ireland": "Irish",
    "irlande": "Irish",
    "italie": "Italian",
    "lettonie": "Latvian",
    "lituanie": "Lithuanian",
    "luxembourg": "Luxembourgish",
    "malte": "Maltese",
    "monaco": "Monégasque",
    "pays-bas": "Dutch",
    "portugal": "Portuguese",
    "saint-marin": "Sammarinese",
    "slovaquie": "Slovak",
    "slovenie": "Slovene",
    "vatican": "Vatican",
}


default_year = [i for i in range(1999, 2031)]
default_types = types

crh_info = """**What is Coin Roll Hunting?**
- __Coin Roll Hunting (CRH)__ is a hobby which many users on this server participate in regularly. The idea is to go to a bank, purchase coin rolls, then to look through the rolls for any special coins you don't have or may want to keep for trading. The regular coins you don't need anymore you deposit back into the bank. It's a cheap way to quickly expand your collection by only looking through circulated coins.

**How do I get started with Coin Roll Hunting?**    
- To get started with CRH, go to your local bank and ask to purchase coin rolls. In some banks, this process is even automated with machines. Sometimes you need to have a bank account with the bank, sometimes you don't, and sometimes purchasing rolls costs a little over face value. The exact process varies by country. To receive detailed information by country, select a country from the dropdown option below. 

**What do I do when I am done with the hunt?**   
- When you're done and you've looked through the rolls, you can go back and deposit your coins by using a coin counting machine. __It is generally not recommended to go back to the same branch you used to purchase the coins__, and to have separate branches dedicated to purchasing and depositing coins. Otherwise you run the risk of searching through rolls of coins you've already searched through. This depends on the country, however, as some banks may ship their deposited coins to a central coin wrapping place instead, and you wouldn't need to worry about depositing your coins in a different branch.
  
- Lastly, our community is very interested in live coin roll hunts! If you plan on hunting and don't mind livestreaming your hunt in a vc, don't hesitate to let people know in #coin-hunts!"""

tocoin_help_menu = f"""___***COINDESIGNER HELP***___
With CoinDesigner, you can convert any coin design you want into a 2 euro coin! However, the command may be a bit tricky to figure out how to use.

First, create an image. The image should be square (otherwise itll be squished!) and ideally black and white. Lighter areas will stand out more in the final design.
Here are a few good example images you can use to test out the program: https://imgur.com/a/4PcuMoA

Next, select the image options by running the command ``/tocoin settings``. To reset to default settings run the command ``/tocoin default``.
<:emote:{emote_id}> ``sigma`` modifies how blurry (or sharp) the coin will appear to be. Higher ``sigma`` = more blurriness. 
<:emote:{emote_id}> ``intensity`` modifies how big the fields of the coin will be. Higher ``intensity`` = more noticeable fields.
<:emote:{emote_id}> ``nmd`` modifies how much dark areas of the coin pop out. Higher ``nmd`` = more noticeable dark areas. This is hard to tell, however, so it is recommended to keep this at 1.5 - 5.
Fool around with these numbers until you feel like the coin looks good enough!

To convert the image, select the message with the image, and go into message options (hold message on mobile, click on the three dots on PC) and go to Apps -> Convert. The bot will then post your converted coin in the chat! It may take a few seconds to do so.
"""

country_id_help_menu = """**TWO-LETTER COUNTRY IDENTIFICATION CODES**
AD = Andorra | AT = Austria | BE = Belgium | CY = Cyprus | DE = Germany | EE = Estonia | ES = Spain | FI = Finland | FR = France | GR = Greece | HR = Croatia
IE = Ireland | IT = Italy | LT = Lithuania | LU = Luxembourg | LV = Latvia | MC = Monaco | MT = Malta | NL = Netherlands | PT = Portugal | SI = Slovenia | 
SK = Slovakia | SM = San Marino | VA = Vatican 
"""

info_unknown_text = """\
No information available. If you have any information that could be added here, let the bot developers know!\
"""

slashcommands_notice = """\
EuroBot 1.1 was released on **November 20th, 2022**. With it, we have officially switched to _slash commands_.

Slash commands offer better syntax, more concise arguments, and allow us to add buttons and other cool features to embeds. The old `eur!` and `€!` have thus been replaced.

To execute a slash command, simply use the `/` prefix instead. Most commands in v1.1 still operate the same as they did pre-slash commads, but if you need help, feel free to issue `/help`.\
"""

help_text = f"""\
**General Help**

EuroBot is the discord bot for the /r/EuroCoins discord server. It provides various commands and tools to help improve the server experience.

In the following list of commands, command options in `[square brackets]` are optional while command options in `<angle brackets>` are required.

<:emote:{emote_id}> **Commands:**

`/banknote <serial>`: Identify a euro banknote and validate its’ serial number.

`/demintmark <year>`: Show the location of the mintmark on German commemorative coins from the year `year`.

`/help [command]`: Display help for the command `command`. If no command is specified, this help message is displayed.

`/info <subject>`: Display information about the subject `subject`.

`/search coin <country> [year] [type]`: Display information about the euro coin(s) from the country `country`. An optional `year` and `type` may be specified to narrow the search.
`/search id <id>`: Display information about the euro coin with the numista ID `id`.

`/tocoin settings [sigma] [intensity] [nmd]`: Set your default CoinDesigner settings.
`/tocoin reset`: Reset your CoinDesigner settings to their defaults.\
"""

help_banknote_text = """\
**SYNOPSIS**
`/banknote <serial>`

**DESCRIPTION**
The `/banknote` command takes the serial number specified by `serial` and identifies the country the banknote originates from and the series the banknote is a part of. If the banknote is a Europa series banknote then it also identifies the printer where the banknote was printed. Additionally, the serial number is validated.

Here is the location of the euro banknote serials for both series 1 (top) and series 2 (bottom): https://imgur.com/u3IraLz

**EXAMPLES**
Get information about a banknote: `/banknote [serial|Y04760833015]`
Find out where a banknote comes from by supplying just the country code: `/banknote [serial|Y]`\
"""

help_demintmark_text = """\
**SYNOPSIS**
`/demintmark <year>`

**DESCRIPTION**
The `/demintmark` command displays the location of the mintmark on the German €2 commemorative coin(s) from the specified year. For more information on the different German mintmarks, run the `/info mintmarks` command.

**EXAMPLES**
Locate the mintmarks on the German 2022 €2 commemoratives: `/demintmark 2022`\
"""

help_help_text = """\
**SYNOPSIS**
`/help [command]`

**DESCRIPTION**
The `/help` command displays a help page (like this one!) describing how a command works. A help
page is typically broken up into three sections, the synopsis, the description, and the examples.

The synopsis describes the command name and options the command takes. The description describes how
the command actually works. The examples shows various examples of how you might use the command.

**EXAMPLES**
Get help on how to use `/help`: `/help help`
Get help on how to use `/info`: `/help info`\
"""

help_info_text = """\
**SYNOPSIS**
`/info <topic>`

**DESCRIPTION**
The `/info` command displays information about the topic `topic`. The `topic` option is case-insensitive.

**EXAMPLES**
Get information on cleaning coins: `/info cleaning`
Get information on mintmarks in coins: `/info mintmarks`\
"""

help_serverinfo_text = """\
**SYNOPSIS**
`/serverinfo`

**DESCRIPTION**
The `/serverinfo` command displays information about the current server. It displays the following:
  - Number of server members
  - Number of confirmed traders in the server
  - Age of the server
  - Link to the EuroBot discord server

**EXAMPLES**
Get information about the current server: `/serverinfo`\
"""

info_cleaning_text = """\
In general, **you should never clean coins.** This is because most cleaning methods can remove tarnishing or luster on coins which naturally develops over time, and may also leave scratch marks on the coin. Even lightly polishing it with a cloth may significantly impact a coins surface! To most collectors, this damage is noticeable and _significantly_ impacts the value of a coin.

The above advice is mostly meant towards older coins (usually pre-euro). Since euro coins are rarely worth a significant amount over face value (especially when found in circulation), cleaning them won’t significantly lower their value. However, it is _still not recommended to clean them_ if you intend on trading coins or intend on your collection increasing in value in the future.

If your coins are physically dirty (i.e. due to dirt), __there are safe methods of removing it__. Soak the coin in distilled water or __100%__ acetone[see below], rinse with a fresh portion of the same liquid, and allow the coin to air-dry. When in doubt, feel free to ask members on the server for help!

*Use only pure acetone. Do not use acetone-containing products (i.e. nail polish remover). When using acetone, do not use plastic containers, and use it in a well-ventilated area. You can purchase pure acetone in most hardware stores.\
"""

info_crh_andorra_text = """\
Coin rolls can be obtained from the banks Andbank, Crèdit Andorrà, and MoraBanc. All three banks require you to be a customer to get rolls.

Information regarding fees for getting rolls is unknown.\
"""

info_crh_austria_text = """\
Availability varies by bank.

**Austrian National Bank**
Does not distribute circulated rolls but sells rolls of commemorative coins at face value on release as well as uncirculated rolls for all denominations.

**Bank Austria**
There is a fee of €0.20 per roll. Rolls can be purchased with cash at machines (available to everyone, but not in all branches. Look for the filter option “Münzrollengeber” at https://filialen.bankaustria.at/de/).

**Erste Bank**
There is a fee of €0.10 per roll. You must be a customer and pay with a card at machines. Free when purchased at counters (but counters will redirect you to machines if they work); counters accept cash.

Depositing coins is free for up to €100 a day, at which point you pay 1% for anything over €100. You must also be a customer.

**Raiffeisenbank**
There is a fee of €1 per roll if you aren’t a customer, and €0.30 otherwise. Coin deposits are free if you’re a customer.

**Volksbank**
Reportedly fee-less with no need of being a customer, needs to be confirmed.\
"""

info_crh_belgium_text = """\
There are no ATMs with coin rolls.

**Argenta**
€1.50 processing fee, but no limit on rolls.

**Belgian Central Bank**
You can visit the European/Belgium Central Bank in Brussels as an EU citizen. You can order coin rolls for no fee up to €2000 in value (see https://www.youtube.com/watch?v=I4gwrpsl2Bk). They seem to distribute uncirculated, standard coins.

**KBC**
Free for customers but getting coin rolls is still difficult sometimes. Non-customers cannot get rolls.\
"""

info_crh_croatia_text = info_unknown_text

info_crh_cyprus_text = info_unknown_text

info_crh_estonia_text = """\
It is very difficult to obtain coin rolls in Estonia.

**All Banks**
Coin rolls are very expensive and you must make an appointment first (customers only).

**Central Bank of Estonia Museum (Tallinn)**
You can purchase commemorative coins (even those released years ago) at face value. Also an interesting museum in general.\
"""

info_crh_finland_text = """\
Finland has no coin roll machines, but you can find vending machines or coin exchange machines (albeit they are rare).

**Aktia**
Coin rolls can be obtained with no fee.

**Bank of Finland**
It is probably not possible to obtain coin rolls, but this is not confirmed.\
"""

info_crh_france_text = """\
Coin roll machines are uncommon, only some banks have them and you need to be a customer. You may also need to order them in advance.

**Caisse d’Épargne**
Coin rolls can be obtained with no fee. You must be a customer.

**CIC**
Coin rolls can be obtained with no fee. You must be a customer.

**Crédit Agricole**
Coin rolls can be obtained with no fee. You must be a customer.

**Le Crédit Lyonnais (LCL)**
There are coin roll machines but it is not yet known if you need to be a customer or if there are fees.\
"""

info_crh_germany_text = """\
Coin roll availability may vary across banks and branches, as well as the price. You must be a customer to purchase coin rolls unless specified otherwise.

**Deutsche Bundesbank**
You can obtain commemorative coins for face value including €5, €10, and €20 coins. You do not need to be a customer although depending on your branch you may need to make an appointment.

**Deutsche Post**
Hand-rolled coin rolls can be obtained with no additional fees.

**Sparkasse**
Coin rolls can be obtained for a fee of €0.50 – €1.50 per roll. The amount varies per branch.

**Volksbank**
Coin rolls can be obtained for a fee of €0.25 per roll.\
"""

info_crh_greece_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**Bank of Greece (Τράπεζα της Ελλάδος)**
Fee-less coin rolls for everyone (you need to show an ID card). The latest €2 commemoratives are also sold for face value.\
"""

info_crh_ireland_text = """\
Coin rolls are available at banks with a fee of €1 per roll; rolls could potentially have no fee if you only need a few.\
"""

info_crh_italy_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**Banca Cambiano**
There are coin roll machines but it is unknown if you need to be a customer or if there are additional fees.

**Bank of Italy**
Coin rolls are sold to everyone.\
"""

info_crh_latvia_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**In General**
Coin rolls are sold with a fee of €0.60 per roll.\
"""

info_crh_lithuania_text = info_unknown_text

info_crh_luxembourg_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**BCL**
No information known yet. Their webshop sells commemoratives at face value, whether this is for sale in person is not known.

**Dexia-Bank**
You should be able to get coin rolls with no additional fees.\
"""

info_crh_malta_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**Bank of Valletta and HSBC Bank Malta**
You can get rolls for a fee of €0.30 per roll. You must order coin rolls through their online platform, and you must be a customer.\
"""

info_crh_monaco_text = info_unknown_text

info_crh_netherlands_text = """\
Note that 1c and 2c coins are no longer used in the Netherlands and cannot be got from rolls.

**ABN AMRO, ING, and Rabobank**
You can get coin rolls from Geldmaat coin roll machines, which are located in some branches of GAMMA and Karwei. You must be a customer of one of these banks and you must pay with your bankcard.

You can locate coin roll machines [using this link](https://www.locatiewijzer.geldmaat.nl/?fiver&functionality=Munten%20opnemen). [This video](https://www.youtube.com/watch?v=AcfeTg05a70) contains instructions on using the machines.

**ABN AMRO**
Rolls can be obtained for a fee of €0.30 per roll. You must withdrawal between 10 and 20 rolls at a time.

**De Nederlandsche Bank (DNB)**
The Dutch Central Bank does not do anything with coins.

**ING**
Rolls can be obtained for a fee of €7 + an additional €0.35 per roll.

**Rabobank:**
Rolls can be obtained for a fee of €7 + an additional €0.50 per roll.

TIP: The main train station in Delft (not Delft Campus!) has a burger fast-food place called “Smullers”. They have a coin exchange machine where you can exchange higher denominatoin coins for 10c, 20c, and 50c coins.

TIP: If you would like to get 1c and 2c coins, your best bet is likely to ask to exchange coins at a currency exchange office. You can find one of these at most train stations.\
"""

info_crh_portugal_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**Banco Comercial Português (Millenium BCP)**
Coin bags are sold with no fees to customers.

**Banco de Portugal (Lisbon)**
Coin bags are sold with no fees to everyone.\
"""

info_crh_san_marino_text = info_unknown_text

info_crh_slovakia_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**Tatra Banka**
You can get an unlimited number of rolls for a fee of €5. You must be a customer.

**National Bank of Slovakia (Národná banka Slovenska)**
You _may_ be able to get uncirculated rolls. This is not yet confirmed.\
"""

info_crh_slovenia_text = """\
This page may be incomplete. Feel free to contribute by letting bot devs know!

**In General**
€1.20 per roll.

**Bank of Slovenia**
You can purchase commemorative coins for face value.

**Slovenian National Bank**
Coin rolls are sold with no fees to everyone.\
"""

info_crh_spain_text = """\
**Banco Santander**
Coin rolls are free, but you must be customer.

**Bank of Spain**
You can purchase individual coins and commemorative coin rolls (even those of other countries).

**BBVA**
Alicante: Coin rolls have a fee of €2 for 5 rolls. Seems to vary by region.
Madrid: Coin rolls have no fees.

**La Caixa**
Coin rolls have no fees and can be purchased with cash. You do not need to be a customer.\
"""

info_crh_vatican_city_text = """\
Ask the Pope nicely and he’ll probably give you some Vatican coins for free.\
"""

info_find_of_the_week_text = f"""\
“Find of the Week” is a weekly competition where new coin finds are “ranked” by the commmunity. The best find wins this week’s Find of the Week!

For starters, post a picture of your find in <#{findOfTheWeek.CHANNEL_ID}>. Afterwards, other users can react to the picture with <:emote:{findOfTheWeek.EMOTE_ID}> emotes!

On Sundays, the find with the most emotes wins!\
"""

info_mintmarks_text = f"""\
Mintmarks (not to be confused with “Mint Master Marks”) are symbols (usually a letter), that feature on the design of a coin. They identify the location where a coin was minted. They are most well known for their prominence on German euro coins where the mint marks ‘A’, ‘D’, ‘F’, ‘G’, and ‘J’ can be found. For this reason many collectors like to collect 5 copies of each German euro coin, one for each mintmark.

If you would like to find the location of mintmarks on German CCs, you can use the `/demintmark` command.

The alphabetic mintmarks used in Euro coins are as follows:
    - Finland Fi (Vantaa, Finland)
    - Finland M (Vantaa, Finland)
    - Germany A (Berlin, Germany)
    - Germany D (Munich, Germany)
    - Germany F (Stuttgart, Germany)
    - Germany G (Karlsruhe, Germany)
    - Germany J (Hamburg, Germany)
    - Greece E (Madrid, Spain)
    - Greece F (Pessac, France)
    - Greece S (Vantaa, Finland)
    - Italy R (Rome, Italy)
    - Lithuania LMK (Vilnius, Lithuania)
    - Luxembourg F (Pessac, France)
    - Luxembourg S (Vantaa, Finland)
    - Malta F (Pessac, France)
    - Portugal INCM (Lisbon, Portugal)
    - San Marino R (Rome, Italy)
    - Slovenia Fi (Vantaa, Finland)
    - Spain M (Madrid, Spain)
    - Vatican City R (Rome, Italy)\
"""

info_rare_coins_text = """\
__Be sceptical of online listings of coins claiming that your coin is worth a lot of money__. People like to put up listings for very common circulation coins claiming they are worth thousands, when in reality they are probably worth face value. There are many factors which go into what makes a coin rare, and it's best to do more research by looking into mintage figures and sold ebay listings. When in doubt, you can also ask the community in the <#680408011751424039> channel to give their own opinion into the value of a coin.
    
__Greece 2002S is not a rare coin, nor is it a mintage error__. In 2002, Greece could not make enough 2 euro coins for the introduction of the euro, so they asked Finland to help them out by minting some 2 euro coins for them. Finland made approximately __70 million__ 2 euro coins for Greece and marked them with an “S” mintmark (S for “Suomi”). This is the most common coin listed on marketplaces for extremely high prices. For more information about mintmarks, see `/info mintmarks`.

Also keep in mind that a coin being rare does not make it __valuable__. Most “rare” or “low-mintage” coins are still worth close to around face value. Once again, feel free to ask in <#680408011751424039> if you find yourself being confused by a coins value.\
"""

info_storage_text_opener = """\
There are many safe methods of storing coins. The most common methods are to use coin albums, boxes, capsules, and/or flips.

The following pages discuss different coin storing methods.\
"""

info_storage_text_albums = """\
**Coin Albums**

Coin albums are one of the most popular ways of storing coins. Coin albums comprise of individual coin sheets which are plastic pages with slots where you place your coin for protection from an outside environment.

Many coins albums come with a set number of pages giving the albums a set number of coins that they can store, but you can also buy individual coin sheets which can often be inserted into your standard office binder.

IMPORTANT: If you choose to use a coin album or coin sheets, make sure that the sheets **do not** contain PVC plastics. Exposure to such plastics can damage coins over time.\
"""

info_storage_text_boxes = """\
**Coin Boxes**

TODO\
"""

info_storage_text_capsules = """\
**Coin Capsules**

Coin capsules work in much the same way as coin flips. The main difference is that instead of the coin being in a folded piece of cardboard with a plastic window, the coin is in an entirely plastic capsule. These capsules can be found in a variety of sizes, but you must make sure to get the right capsule size for your coins.

Capsules are typically more expensive than coin flips, but offer some aditional advantages. Since a capsule is entirely made out of plastic, you can see certain coin features like the edge engravings and such a lot better.

Capsules are also far more durable than flips, and can be opened and closed repeatedly allowing for them to be reused. This isn’t really possible with flips.\
"""

info_storage_text_flips = """\
**Coin Flips**

Coin flips, also known as 2x2 flips by Americans (since they are 2x2 inches in size typically) are small cardboard flips with a plastic covered hole in the middle for viewing. There are two main types of coin flips, those being “standard” coin flips and “glued” coin flips.

Standard coin flips are typically the cheaper of the two options. To use these you place your coin inside of the flip and use a stapler to staple the flip shut. Visually these are not as nice as glued flips since you have staples in your flip. Glued coin flips are typically more expensive than the standard flips and feature a small amount of glue around the inner border of the flip. To use these flips you simply place your coin in the flip and close it; the glue will keep the flip shut on its own.

Coin flips allow you to securely protect your coins from the outside environment. They also have a relatively small space profile (although they are larger than capsules) and they can be easily stacked in boxes for compact coin storage. It is also common for collectors to write notes about a coin on the flip itself, such as the price or mintage of the coin.

There are also special coin album sheets you can purchase that can house coin flips, but keep in mind that putting coins into a coin sheet without flips will allow you to fit many more coins per sheet.

<@!632122927734718474> created a collection of country flags in DOCX, DWG, PNG, and PDF formats which can be printed out and glued/taped to your flips. You can find them here: https://discordapp.com/channels/555331630206681108/555333655866769418/930114755027402792.\
"""

search_help = f"""

EuroBot's search functionality allows you to quickly search through Numista's database for all euro coins. Note that this only includes regular issue (i.e. 1c - 2 euro) coins, although it does include NIFC ones. EuroBot will also display the mintages for each coin.

<:emote:{int(emote_id)}> **Generic Search:**
`/search coin` is the command to execute a generic search. You will notice that there are three requirements - country, year, and type - of which only one (country) is mandatory. Additionally, the bot autocompletes a list of arguments you can include for each query. 

The search will yield a picture of the coin, some text describing the design, and mintage figures, as well as a direct link to the coin's Numista page. 

Sometimes the search yields multiple results. If that's the case, you can either use the buttons to select a result, or run the command `/search id [id] {{year}}` to select one via its numista ID. You can add {{year}} to narrow down the mintages if there are lots of them displayed.

<:emote:{int(emote_id)}> **Fast Search (fsearch):**
In a hurry? With `/fsearch [query]` you can execute a search much more quickly. The query consists of the required two letter TLD of the country (i.e. "de" for germany, "at" for austria, "si" for slovenia), the optional denomination (must be of the type "1c", "2c", "5c", "10c", "20c", "50c", "1", "2", "2cc", where those with "c" refer to cents, "1" and "2" refer to 1- and 2-euro coins, and "2cc" to 2-euro commemoratives), as well as the optional year. These arguments can be in any order.

For example, `/fsearch query: 10c at 2006` returns the mintage of the Austrian 10c coin in 2006, and `/fsearch query: ad 2cc` returns a list of all Andorran 2-euro commemoratives.

If you used EuroBot 1.0: `/fsearch` is used the exact same way as `eur!search`, except for the additional `query:` (which gets automatically added by discord)

<:emote:{int(emote_id)}> **Note about new coins:**
The database which EuroBot uses is remotely downloaded from Numista and requires updating sometimes by the developers. If you notice that a coin is missing, let the developers know.

"""
