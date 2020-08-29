from modules.logging import Logging
Logger = None


class PlayerSystem:

    def __init__(self, events, server, settings):
        global Logger
        Logger = Logging(events, "Players")
        self.Events = events
        self.on = events.on
        self.Server = server
        self.players = {}
        self.settings = settings

    def initPlayer(self, username):
        self.players[username] = {
            "color": "green",
            "resources": self.settings.getStartingResources(),
            "ships": self.settings.getStartingShips()
        }

    def getPlayers(self):
        return self.players

    def getPlayer(self, username):
        if self.playerExists(username):
            return self.players[username]
        return False

    def playerExists(self, username):
        return username in self.players
