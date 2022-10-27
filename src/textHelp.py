import logging
import re


def concat(*args: str) -> str:
    return "\n".join(args)


def emojiReplacer(s: str) -> str:
    """Given a string will replace all !<country_code> with their respective emoji. If there is no
    emoji present, it just returns the string.
    DO NOT LOWERCASE TEXT BEFORE PUTTING INTO FUNCTION!
    Yes I know this can be more efficient but I am too lazy to do it! Let me improve it later
    Input: string
    Output: string"""

    final = s
    codeToEmote = {
        "AN": "🇦🇩",
        "AT": "🇦🇹",
        "BE": "🇧🇪",
        "CY": "🇨🇾",
        "EE": "🇪🇪",
        "FI": "🇫🇮",
        "FR": "🇫🇷",
        "DE": "🇩🇪",
        "GR": "🇬🇷",
        "IE": "🇮🇪",
        "IT": "🇮🇹",
        "LV": "🇱🇻",
        "LT": "🇱🇹",
        "LU": "🇱🇺",
        "MT": "🇲🇹",
        "NL": "🇳🇱",
        "PT": "🇵🇹",
        "SK": "🇸🇰",
        "SI": "🇸🇮",
        "ES": "🇪🇸",
        "EU": "🇪🇺",
        "HR": "🇭🇷",
        "MC": "🇲🇨",
        "VA": "🇻🇦",
        "SM": "🇸🇲",
    }

    for match in re.finditer(r"!(..)", s):
        if (code := match.group(1)) in codeToEmote:
            final = final.replace(match.group(0), codeToEmote[code])

    return final


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

    arguments = {"Status": None, "Sigma": 0.1, "Intensity": 2.0, "NMD": 1.5}

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

country_to_french = {
    "germany": "allemagne",
    "austria": "autriche",
    "belgium": "belgique",
    "spain": "espagne",
    "finland": "finlande",
    "france": "france",
    "ireland": "irlande",
    "italy": "italie",
    "luxembourg": "luxembourg",
    "netherlands": "pays-bas",
    "portugal": "portugal",
    "greece": "grece",
    "slovenia": "slovenie",
    "cyprus": "chypre",
    "malta": "malte",
    "slovakia": "slovaquie",
    "estonia": "estonie",
    "latvia": "lettonie",
    "lithuania": "lituanie",
    "monaco": "monaco",
    "san-marino": "saint-marin",
    "sanmarino": "saint-marin",
    "andorra": "andorre",
    "vaticancity": "vatican",
    "vatican-city": "vatican",
    "vatican": "vatican",
}

country_id_to_french = {
    "de": "allemagne",
    "at": "autriche",
    "be": "belgique",
    "es": "espagne",
    "fi": "finlande",
    "fr": "france",
    "ie": "irlande",
    "it": "italie",
    "lu": "luxembourg",
    "nl": "pays-bas",
    "pt": "portugal",
    "gr": "grece",
    "si": "slovenie",
    "cy": "chypre",
    "mt": "malte",
    "sk": "slovaquie",
    "ee": "estonie",
    "lv": "lettonie",
    "lt": "lituanie",
    "mc": "monaco",
    "sm": "saint-marin",
    "ad": "andorre",
    "va": "vatican",
}

french_to_emoji = {
    "allemagne": "🇩🇪",
    "autriche": "🇦🇹",
    "belgique": "🇧🇪",
    "espagne": "🇪🇸",
    "finlande": "🇫🇮",
    "france": "🇫🇷",
    "irlande": "🇮🇪",
    "italie": "🇮🇹",
    "luxembourg": "🇱🇺",
    "pays-bas": "🇳🇱",
    "portugal": "🇵🇹",
    "grece": "🇬🇷",
    "slovenie": "🇸🇮",
    "chypre": "🇨🇾",
    "malte": "🇲🇹",
    "slovaquie": "🇸🇰",
    "estonie": "🇪🇪",
    "lettonie": "🇱🇻",
    "lituanie": "🇱🇹",
    "monaco": "🇲🇨",
    "saint-marin": "🇸🇲",
    "andorre": "🇦🇩",
    "vatican": "🇻🇦",
}

french_to_genitive = {
    "allemagne": "German",
    "autriche": "Austrian",
    "belgique": "Belgian",
    "espagne": "Spanish",
    "finlande": "Finnish",
    "france": "French",
    "ireland": "Irish",
    "italie": "Italian",
    "luxembourg": "Luxembourgish",
    "pays-bas": "Dutch",
    "portugal": "Portuguese",
    "grece": "Greek",
    "slovenie": "Slovene",
    "chypre": "Cypriot",
    "malte": "Maltese",
    "slovaquie": "Slovak",
    "estonie": "Estonian",
    "lettonie": "Latvian",
    "lituanie": "Lithuanian",
    "irlande": "Irish",
    "monaco": "Monégasque",
    "saint-marin": "Sammarinese",
    "andorre": "Andorran",
    "vatican": "Vatican",
}


default_year = [i for i in range(1999, 2031)]
default_types = types

clean_msg = """In general, **you should never clean coins.** This is because most cleaning methods can remove tarnishing or luster on coins which naturally develops over time, and may also leave scratch marks on the coin. Even lightly polishing it with a cloth may significantly impact a coins surface! To most collectors, this damage is noticeable and _significantly_ impacts the value of a coin.
    
The above advice is mostly meant towards older coins (usually pre-euro). Since euro coins are rarely worth a significant amount over face value (especially when found in circulation), cleaning them won''t significantly lower their value. However, it is _still not recommended to clean them_ if you intend on trading coins or intend on your collection increasing in value in the future.
    
If your coins are physically dirty (i.e. due to dirt), __there are safe methods of removing it__. Soak the coin in distilled water or __100%__ acetone [see below], rinse with a fresh portion of the same liquid, and allow the coin to air-dry. When in doubt, feel free to ask members on the server for help!
    
(Use only pure acetone. Do not use acetone-containing products (i.e. nail polish remover). When using acetone, do not use plastic containers, and use it in a well-ventilated area. You can purchase pure acetone in most hardware stores.)
"""

storage_msg_1 = """There are many safe methods of storing coins. The most common methods are to use 2x2 flips, capsules, or special albums. 
    
2x2 flips are small cardboard flips with holes cut in which are covered by film. You put the coin inside and fold the flips shut. Depending on the flip, the flip will either glue itself shut, or you will need to staple it shut. If you need to staple the flip shut, make sure that your stapler does not contact the coin inside the flip, otherwise it may leave a mark on the coin! Once inside the coin is protected from the outside environment. You still need to be careful with how you store your coins, though. There are special albums which can store 2x2 flips. The downside is that the flips can be quite big and you will need a lot of album space to store them. Lots of people also prefer to store flips in special boxes. There's lots of space on the flip to write information about the coin, or alternatively you can download flip tags made by chris24o1#9608 which you can glue onto coin flips here: https://discordapp.com/channels/555331630206681108/555333655866769418/930114755027402792
    
Capsules are small plastic covers which you can put your coin in. The advantage is that because they are hard surfaces, its less likely for the coin to be defaced by contact with another flip. The disadvantage is that they can be slightly more expensive and harder to store.
"""

storage_msg_2 = """There are many types of albums to store your coin in. __The only advice you need to follow is to ensure that the albums do not contain PVC.__ PVC is a chemical which leaves ugly green marks on a coin over time! PVC damage can be removed safely, but it is a nuisance to do so. It's best to avoid albums with the chemical for long-term storage.
    
Lighthouse/Leuchtturm is a very reliable brand for purchasing coin supplies. Your LCS should have a supply of storage materials for your coins. Alternatively, department stores are also a good place to check!
    
If you have any other questions about storing coins, feel free to inquire the community - we will be more than willing to help!"""

crh_info = """__Coin Roll Hunting (CRH)__ is a hobby which many users on this server participate in regularly. The idea is to go to a bank, purchase coin rolls, then to look through the rolls for any special coins you don't have or may want to keep for trading. The regular coins you don't need anymore you deposit back into the bank. It's a cheap way to quickly expand your collection by only looking through circulated coins.
    
To get started with CRH, go to your local bank and ask to purchase coin rolls. In some banks, this process is even automated with machines. Sometimes you need to have a bank account with the bank, sometimes you don't, and sometimes purchasing rolls costs a little over face value. The exact process varies by country. To receive detailed information by country, run the command ``eur!crh <country>``. 
    
When you're done and you've looked through the rolls, you can go back and deposit your coins by using a coin counting machine. __It is generally not recommended to go back to the same branch you used to purchase the coins__, and to have separate branches dedicated to purchasing and depositing coins. Otherwise you run the risk of searching through rolls of coins you've already searched through. This depends on the country, however, as some banks may ship their deposited coins to a central coin wrapping place instead, and you wouldn't need to worry about depositing your coins in a different branch.
    
Lastly, our community is very interested in live coin roll hunts! If you plan on hunting and don't mind livestreaming your hunt in a vc, don't hesitate to let people know in #coin-hunts!"""

rare_coins = """__Be sceptical of online listings of coins claiming that your coin is worth a lot of money.__ People like to put up listings for very common circulation coins claiming they are worth thousands, when in reality they are probably worth face value. There are many factors which go into what makes a coin rare, and it's best to do more research by looking into mintage figures and sold ebay listings. When in doubt, you can also ask the community in the #values channel to give their own opinion into the value of a coin.
    
__Greece 2002S is not a rare coin, nor is it a mintage error.__ In 2002, Greece could not make enough 2 euro coins for the introduction of the euro, so they asked Finland to help them out by minting some 2 euro coins for them. Finland made approximately __70 million__ 2 euro coins for Greece and marked them with an "S" mintmark (S for "Suomi"). This is the most common coin listed on marketplaces for extremely high prices. """

tocoin_help_menu = """___***EUR!TOCOIN HELP***___
With ``eur!tocoin``, you can convert any coin design you want into a 2 euro coin! However, the command may be a bit tricky to figure out how to use.

First, you must either add an image to your command, or reply to an already existing message with an image. Due to technical limitations __linked images will not work__. In order for the program to work properly, it is _recommended_ that your image is square (otherwise the program will squish it into one).

It is also recommended that your image is _black and white_. The larger the contrast between two areas, the more it will show up on the coin design. Here are a few examples of designs which will look good on the coin: https://imgur.com/a/4PcuMoA
(You can use a program like Photoshop, Gimp, or even Paint to make a design for the coin.)

Lastly, running ``eur!tocoin`` returns the same as running ``eur!tocoin -s 0.1 -i 2.0 -nmd 1.5`` does. 
``-s`` modifies how blurry (or sharp) the coin will appear to be. Higher ``-s`` = more blurriness. 
``-i`` modifies how big the fields of the coin will be. Higher ``-i`` = more noticeable fields.
``-nmd`` modifies how much dark areas of the coin pop out. Higher ``-nmd`` = more noticeable dark areas. This is hard to tell, however, so it is recommended to keep this at 1.5 - 5.
Fool around with these numbers until you feel like the coin looks good enough!
"""

country_id_help_menu = """**TWO-LETTER COUNTRY IDENTIFICATION CODES**
AD = Andorra | AT = Austria | BE = Belgium | CY = Cyprus | DE = Germany | EE = Estonia | ES = Spain | FI = Finland | FR = France | GR = Greece | HR = Croatia
IE = Ireland | IT = Italy | LT = Lithuania | LU = Luxembourg | LV = Latvia | MC = Monaco | MT = Malta | NL = Netherlands | PT = Portugal | SI = Slovenia | 
SK = Slovakia | SM = San Marino | VA = Vatican 
"""
