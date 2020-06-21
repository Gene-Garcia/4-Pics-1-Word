from Parser import Parser
import os.path
from os import path

class Game:

    MAX_LEVEL = 50
    PASS_COST = 10
    HINT_COST = 2

    def __init__(self):
        self.__pictures = Parser.readList()
        self.__user = Parser.readUserInfo()

    def moveLevel(self):
        # after moving to the next level, call parser to record the users data.
        # kaya pagkatapos kasi, baka hindi na niya matapos sagutan at i exit na ang program.
        # atleast naka record na kung saan siya tumugil

        self.__user["level"] += 1
        Parser.rewriteUserInfo(self.__user)


    def getCurrentLevel(self):
        return self.__user["level"]

    def getLevelImage(self):
        loc = "pics\\" + str(self.__pictures[self.__user["level"]]) + ".png"

        if path.exists(loc):
            return loc
        return False

    def getLevelWord(self):
        return self.__pictures[self.__user["level"]].upper().strip()

    def getUserCoins(self):
        return self.__user["coins"]

    def incrementUserCoins(self):
        self.__user["coins"] = self.__user["coins"] + 10

    def decreaseUserCoins(self, type):
        # hint, pass
        if type.lower() == "hint":
            self.__user["coins"] -= 2
        elif type.lower() == "pass":
            self.__user["coins"] -= 10
