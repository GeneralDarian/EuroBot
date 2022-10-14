import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ID = os.getenv("FOTW_CHANNEL_ID")
EMOTE_ID = os.getenv("FOTW_EMOTE_ID")


class findOfTheWeek:
    def __init__(self):
        self.msgList = []
        try:
            with open('FOTW.txt', 'r') as FOTWFile:
                for line in FOTWFile:
                    self.msgList.append(line[:-1])
        except FileNotFoundError:
            with open('FOTW.txt', 'x') as FOTWFile:
                self.msgList = []

    def getList(self):
        """Returns the list of messages, mostly for debugging
        Inputs: none
        Outputs: np.array([list of message ids])"""
        return self.msgList

    def isInList(self, msg: int) -> bool:
        """Returns if message ID is in current FOTW list.
        Inputs:
        - msg (int): The message ID to check
        Outputs:
        - bool: True if the message ID is present, False if it isn't"""
        if str(msg) in self.msgList:
            return True
        else:
            return False

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
                with open('FOTW.txt', 'a') as FOTWFile:
                    FOTWFile.write(str(msg) + '\n')
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
                print(self.msgList)
                with open('FOTW.txt', 'a') as FOTWFile:
                    FOTWFile.truncate(0)
                    for j in self.msgList:
                        FOTWFile.write(j + '\n')
                return True
        except Exception:
            return False

    def refreshList(self) -> bool:
        """Refreshes the list, intended to be run on Sundays.
        WARNING: Only run this command after checking all messages for emotes!"""
        try:
            with open('FOTW.txt', 'a') as FOTWFile:
                FOTWFile.truncate(0)
            self.msgList = []
            return True
        except Exception:
            return False


fotw = findOfTheWeek()
