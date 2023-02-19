import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Union

import requests
from dotenv import load_dotenv

from tools import textHelp

# Parameters
endpoint = "https://api.numista.com/api/v3"
load_dotenv()
api_key = os.getenv("API_KEY")
client_id = os.getenv("CLIENT_ID")


def refreshFiles() -> None:
    """Refreshes all the JSON files in \json_data\ by calling the numista API for euro coins, specifically.
    This uses A LOT of API requests (30!). DO NOT RUN THIS AUTOMATICALLY, let the admins do it RARELY!!!!
    Inputs:
    - none
    Outputs:
    - none.
    """

    resultcount = 350  # The number of results to ask numista for
    countries = textHelp.euro_country_list_fr
    path = "data/json_data"

    logging.info("Refreshing API files...")
    for country in countries:
        search_query = "euro"
        response = requests.get(
            endpoint + "/types",
            params={
                "q": search_query,
                "page": 1,
                "count": resultcount,
                "lang": "en",
                "issuer": f"{country}",
                "category": "coin",
            },
            headers={"Numista-API-Key": api_key},
        )
        search_results = json.dumps(response.json(), indent=4)
        finalpath = path + f"\{country}.json"
        try:
            with open(finalpath, "w") as country_json:
                country_json.truncate(0)
                country_json.write(search_results)
                logging.info(f"Refreshed API for: {country}")
        except FileNotFoundError:
            logging.info(f"JSON file for {country} does not exist, creating one ...")
            try:
                with open(finalpath, "x") as country_json:
                    country_json.write(search_results)
                logging.info(f"Refreshed API for: {country}")
            except Exception as error:
                logging.error(
                    f"JSON file for {country} could not be created because of {error}, skipping..."
                )

    logging.info("API Refresh complete")


def searchProcessor(arglist: list[str]) -> dict:
    """Input a list of 1-3 arguments, returns a dict with said parameters.
    Inputs:
    - arglist (list[str]): A list of arguments (MAX 3)
    Outputs:
    - dict: A dict with all the formats. The dict is structured like so:
    "status" : 0 if no problems. If there are a problems, an error message would show up here.
    "issuer" : The issuer to look for, 0 if one was not listed.
    "type" : The coin type to look for, 0 if one was not listed.
    "year": The coin year to look for, 0 if one was not listed."""
    already_type = False
    already_country = False
    already_year = False

    final_dict = {"Status": None, "Issuer": None, "Type": None, "Year": None}

    # Check list length
    if len(arglist) > 3:
        final_dict[
            "Status"
        ] = "There are too many arguments in the given argument list!"
        return final_dict

    for i in arglist:

        if i is None:
            continue

        if i.lower() in textHelp.types:  # Check if argument is a type
            if (
                already_type == True
            ):  # If a type has already been found, then multiple types were supplied
                final_dict["Status"] = "Multiple types have been supplied!"
                return final_dict

            elif already_type == False:
                final_dict["Type"] = i
                already_type = True

        elif (
            i.lower() in textHelp.country_to_french
            or i.lower() in textHelp.country_id_to_french
        ):  # Check if argument is a country name
            if (
                already_country == True
            ):  # If a country name has already been supplied, then multiple country names were supplied
                final_dict["Status"] = "Multiple countries were supplied!"
                return final_dict

            elif already_country == False:
                final_dict["Issuer"] = i
                already_country = True

        else:  # idk how to do this part at all. Check if the argument is a year.
            try:
                year = int(i)
                if year >= 1999:
                    if (
                        already_year == True
                    ):  # If this is true then there has already been a year supplied.
                        final_dict["Status"] = "Multiple years were supplied!"
                        return final_dict
                    final_dict["Year"] = str(year)
                    already_year = True
                else
                    final_dict["Status"] = "Year is out of bounds"
                    return final_dict
            except ValueError:
                # If it reaches this far this MUST be an invalid argument.
                final_dict["Status"] = f"Invalid argument {i}"
                return final_dict

    if already_country == False:
        final_dict["Status"] = "You must return a country!"
    else:
        final_dict["Status"] = "0"

    return final_dict


def searchEngine(params: dict) -> list[dict]:
    """Given dictionary with arguments will look through json_data and return results.
    Inputs:
    - params (dict): A dictionary in the type which is supplied via searchProcessor
    Outputs:
    - list[dict]: A list of all "hits" to the search. main.py will process this."""
    search_results = []

    # Get issuer
    if params["Issuer"] is not None:
        if params["Issuer"].title() in textHelp.country_to_french:
            issuer = textHelp.country_to_french[params["Issuer"].title()]
        if params["Issuer"].lower() in textHelp.country_id_to_french:
            issuer = textHelp.country_id_to_french[params["Issuer"].lower()]

    # Get year
    if params["Year"] is not None:
        year = params["Year"]
    else:
        year = None

    # Get deno
    if params["Type"] is not None:
        type = params["Type"]
    else:
        type = None

    if type is None and year is None and issuer is None:
        raise ValueError("All three of type, year, issuer are none!")

    # return [issuer, year, type]
    if issuer is not None:
        path = Path(f"data/json_data/{issuer}.json")
        with open(path, "r") as country_json:
            json_dict = json.load(country_json)

        for entry in json_dict["types"]:  # Loop thru json_dict

            if (
                year is not None
            ):  # If the year is none this part gets skipped, and max_year and min_year are irrelevant
                if int(entry["min_year"]) > int(year) or int(entry["max_year"]) < int(
                    year
                ):  # If year not in (minyear, maxyear) then proceed to next count
                    continue

            if (
                any(
                    [
                        (entry["title"].startswith(title_check))
                        for title_check in textHelp.long_types
                    ]
                )
                == False
            ):  # Broadly filter out non-euro coins (i.e. 1 1/2 euro, 3 euro, etc.)
                continue
            if (
                any(
                    [
                        blacklistword in entry["title"]
                        for blacklistword in textHelp.blacklist
                    ]
                )
                == True
            ):
                continue

            if type is not None:
                formaltype = type

                if "c" in type and not (
                    "cc" in type
                ):  # If this is a euro cent and not a 2cc, add "X Euro Cent" to the end, check if title begins with it. if it does congrats! its a result!
                    formaltype = formaltype.replace("c", " Euro Cent")
                    if not (
                        entry["title"].startswith(formaltype)
                    ):  # If it doesn't, proceed to next count
                        continue
                    else:
                        search_results.append(
                            entry
                        )  # Otherwise append to search results and proceed to next count
                        continue

                elif type == "1":
                    formaltype += " Euro"
                    if not (entry["title"].startswith(formaltype)) or entry[
                        "title"
                    ].startswith("1 Euro Cent"):
                        continue
                    else:
                        search_results.append(entry)
                        continue

                elif type == "2":  # For 2 the process is a bit different
                    if not (entry["title"].startswith("2 Euro")) or entry[
                        "title"
                    ].startswith("2 Euro Cent"):
                        continue
                    if "(" in entry["title"]:  # Check if the coin has a bracket
                        if (
                            ("1st map" in entry["title"])
                            or ("2nd map" in entry["title"])
                            and not ("(Pattern)" in entry["title"])
                        ):  # If it does check if its a part of (1st map) or (2nd map)
                            search_results.append(
                                entry
                            )  # If it does, its definitely not a 2cc.
                            continue
                        else:
                            continue  # If it does not its definitely a 2cc and must be skipped.
                    else:
                        search_results.append(entry)
                        continue

                elif type == "2cc":  # For 2cc the process is a bit different
                    formaltype = "2 Euro"
                    if not (entry["title"].startswith(formaltype)) or entry[
                        "title"
                    ].startswith("2 Euro Cent"):
                        continue
                    if "(" in entry["title"]:  # Check if the coin has a bracket
                        if (
                            "1st map" in entry["title"]
                            or "2nd map" in entry["title"]
                            or "(Pattern)" in entry["title"]
                        ):  # If it does check if its a part of (1st map) or (2nd map)
                            continue
                        else:
                            search_results.append(
                                entry
                            )  # If it does, its definitely a 2cc.
                            continue  # If it does not its definitely not a 2cc and must be skipped.
                    else:
                        continue  # if it does not have a bracket its not a 2cc and must be skipped
            else:
                search_results.append(entry)

        return search_results


def getCoinInfo(coin_id: str) -> dict:
    """Given numista coin ID will return with statistics "worthy" of being listed on EuroBOT. (incl. mintages).
    Inputs:
    - coin_id (str): the Numista ID of the coin
    Outputs:
    - dict: Information about the coin
    status (str): 0 if successful, if anything else yields in an error message
    title (str): title of the coin
    issuer (str): issuer of the coin
    cc (bool): True if commem, False if not
    obversepic (str): picture of the obverse
    reversepic (str): picture of the reverse
    designinfo (str): information on the design
    min_year (str): first year coin was minted
    max_year (str): last year coin was minted
    mintage (dict): Information about the coin's mintage"""

    coin_info = {
        "status": None,
        "title": None,
        "issuer": None,
        "cc": None,
        "obverse_pic": None,
        "reverse_pic": None,
        "design_info": None,
        "mintage_list": [],
        "min_year": None,
        "max_year": None,
        "mintage": None,
    }

    # os.path.exists()
    try:
        path = Path(f"data/coin_data/{coin_id}.json")
        with open(path, "r") as country_json:
            search_results = json.load(country_json)
    except FileNotFoundError:
        coin_info["status"] = "ERROR: No coin with given ID in database"
        return coin_info

    # if search_results["value"]["currency"]["id"] != 9007:
    #    coin_info["status"] = f"invalid currency {search_results['value']['currency']['id']}"
    #    return coin_info

    coin_info["title"] = search_results["title"]
    if search_results["issuer"]["code"] in textHelp.french_to_emoji:
        coin_info["title"] = (
            search_results["title"]
            + " "
            + textHelp.french_to_emoji[search_results["issuer"]["code"]]
        )
    coin_info["issuer"] = search_results["issuer"]["code"]

    if (
        search_results["type"] == "Circulating commemorative coin"
        or search_results["type"] == "Non-circulating coin"
    ):
        coin_info["cc"] = True
        coin_info["title"] = coin_info["title"] + " " + "⭐"
    else:
        coin_info["cc"] = False

    if "picture" not in search_results["obverse"]:
        coin_info[
            "obverse_pic"
        ] = "https://en.numista.com/catalogue/no-obverse-coin-en.png"
    else:
        coin_info["obverse_pic"] = search_results["obverse"]["picture"]

    if "picture" not in search_results["reverse"]:
        coin_info[
            "reverse_pic"
        ] = "https://en.numista.com/catalogue/no-obverse-coin-en.png"
    else:
        coin_info["reverse_pic"] = search_results["reverse"]["picture"]

    try:
        if sys.getsizeof(search_results["obverse"]["description"]) > 1023:
            coin_info[
                "design_info"
            ] = "The design info is too large to be displayed here! Click on the blue link of this embed to learn more about this coin's design."
        else:
            coin_info["design_info"] = search_results["obverse"]["description"]
    except KeyError:
        coin_info["design_info"] = "None Specified"
    coin_info["max_year"] = search_results["max_year"]
    coin_info["min_year"] = search_results["min_year"]
    coin_info["status"] = "0"
    coin_info["mintage"] = getCoinMintage(
        coin_id, coin_info["max_year"], coin_info["min_year"]
    )
    return coin_info


def getCoinMintage(coin_id: str, max_year: int, min_year: int) -> dict:
    mintages: dict[Any, Union[list[str], Any]] = {}

    path = Path(f"data/coin_mintages/{coin_id}.json")
    with open(path, "r") as country_json:
        years = json.load(country_json)

    for i in years:
        line_value = ""
        try:  # First look at the year
            if i["year"] not in mintages:
                year_data = []
                mintages[i["year"]] = year_data
            else:
                year_data = mintages[i["year"]]
        except KeyError:
            continue

        try:  # Then look at the mintage and begin to assemble the data value
            line_value = f"{i['mintage']:,}"
        except KeyError:
            line_value = "NO SPECIFIED MINTAGE"

        try:
            line_value = f"{line_value} ({i['mint_letter']}, {i['comment']})"
        except KeyError:
            try:
                line_value = f"{line_value} ({i['mint_letter']})"
            except KeyError:
                try:
                    line_value = f"{line_value} ({i['comment']})"
                except KeyError:
                    line_value = line_value

        year_data.append(line_value)
        mintages[i["year"]] = year_data

    return mintages
