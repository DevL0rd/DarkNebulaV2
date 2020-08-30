from modules.logging import Logging
Logger = None


class PlayerSystem:

    def __init__(self, events, server, settings):
        global Logger
        Logger = Logging(events, "Players")
        self.Events = events
        self.on = events.on
        self.server = server
        self.players = {}
        self.settings = settings

    def initPlayer(self, username, password):
        self.players[username] = {
            "password": password,
            "color": "green",
            "resources": self.settings.getStartingResources(),
            "ships": self.settings.getStartingShips(),
            "op": True,  # TODO, change to false by default. After testing.
            "friends": []
        }

    def addFriend(self, username, friendName):
        self.players[username]["friends"].append(friendName)

    def removeFriend(self, username, friendName):
        self.players[username]["friends"].remove(friendName)

    def isFriend(self, username, friendName):
        return friendName in self.players[username]["friends"]

    def getFriends(self, username):
        return self.players[username]["friends"]

    def playerExists(self, username):
        return username in self.players

    def isOp(self, username):
        return self.players[username]["op"]

    def getPlayers(self):
        return self.players

    def getPlayer(self, username):
        if self.playerExists(username):
            return self.players[username]
        return False
