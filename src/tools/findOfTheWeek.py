import logging
import os
from shutil import copyfile
from time import time as unixtime

import discord
from discord.ext import commands
from dotenv import load_dotenv

from tools import textHelp

load_dotenv()
CHANNEL_ID = os.getenv('FOTW_CHANNEL_ID_1')
CHANNEL_ID_1 = os.getenv("FOTW_CHANNEL_ID_1")
CHANNEL_ID_2 = os.getenv("FOTW_CHANNEL_ID_2")
EMOTE_ID = os.getenv("FOTW_EMOTE_ID")
EMOTE_NAME = os.getenv("FOTW_EMOTE_NAME")
TRADER_ROLE_ID = os.getenv("VERIFIED_TRADER_GROUP_ID")


class findOfTheWeek:
    def __init__(self):
        self.msgList = []
        try:
            with open("tools/FOTW.txt", "r") as FOTWFile:
                for line in FOTWFile:
                    self.msgList.append(line[:-1])
        except FileNotFoundError:
            with open("tools/FOTW.txt", "x") as FOTWFile:
                self.msgList = []

    def getList(self):
        """Returns the list of messages, mostly for debugging
        Inputs: none
        Outputs: np.array([list of message ids])"""
        return self.msgList

    def addMsg(self, msg: int) -> bool:
        """Adds a message ID to the end of the list.
        Inputs:
        - msg (int): The message ID to add
        Outputs:
        - bool: True if task was successful or if message already in msgList, False if it wasn't successful."""
        try:
            if str(msg) in self.msgList:
                return True
            else:
                self.msgList.append(str(msg))
                with open("tools/FOTW.txt", "a") as FOTWFile:
                    FOTWFile.write(str(msg) + "\n")
                return True
        except Exception:
            return False

    def subtractMessage(self, msg: int) -> bool:
        """Removes a message ID from the end of the list.
        Inputs:
        - msg (int): The message ID to remove
        Outputs:
        - bool: True if task was successful OR if message ID was not present. False if it wasn't"""
        try:
            if str(msg) not in self.msgList:
                return True
            elif str(msg) in self.msgList:
                self.msgList.remove(str(msg))
                # print(self.msgList)
                with open("tools/FOTW.txt", "a") as FOTWFile:
                    FOTWFile.truncate(0)
                    for msg_id in self.msgList:
                        FOTWFile.write(msg_id + "\n")
                return True
        except Exception:
            return False

    def refreshList(self) -> bool:
        """Refreshes the list, intended to be run on Sundays.
        WARNING: Only run this command after checking all messages for emotes!"""
        current_dir = os.getcwd()
        # Make a copy of the current FOTW file
        try:
            os.mkdir(current_dir + "/data/FOTW_BACKUPS/")
        except FileExistsError:
            pass

        time = unixtime()
        try:
            copyfile("tools/FOTW.txt", current_dir + f"/data/FOTW_BACKUPS/{time}.txt")
        except Exception:
            pass  # log error here

        try:
            with open("tools/FOTW.txt", "a") as FOTWFile:
                FOTWFile.truncate(0)
            self.msgList = []
            return True
        except Exception:
            return False


fotw = findOfTheWeek()
