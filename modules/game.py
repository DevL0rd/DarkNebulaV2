import time
from modules.logging import Logging
Logger = None

# fancy logic


class GameLogic:
    def __init__(self, events, server, graphics, accounts, playersSystem, universeSystem, settings):
        global Logger
        Logger = Logging(events, "GameLogic")
        self.Events = events
        self.on = events.on
        self.server = server
        self.accounts = accounts
        self.playersSystem = playersSystem
        self.universe = universeSystem
        self.settings = settings
        self.Events.on("tick", self.onGameTick)
        self.Events.on("login", self.onLogin)
        self.Events.on("firstLogin", self.onFirstLogin)

    def onLogin(self, id):
        return

    def onFirstLogin(self, id):
        return

    def onGameTick(self, delta):
        self.updateResources(delta)

    def updateResources(self, delta):
        players = self.playersSystem.getPlayers()
        # some logic here
        for player in players:
            for ship in player.ships:
                if ship["type"] == "miner":
                    player.resources

        # ships that you can build
self.ships = {
    "probe": {
        "cost": 100,
        "energy": 10,
        "heavyMetal": 1,
        "processingModules": 0,
        "initialProperties": {
            "name": "New Probe",
            "type": "probe",
            "fuel": 100,
            "fuel_max": 100,
            "hp": 100,
            "hp_max": 100,
            "size": "small"
        }
    },
    "miner": {
        "cost": 100,
        "energy": 10,
        "heavyMetal": 1,
        "processingModules": 0,
        "initialProperties": {
            "name": "New Miner",
            "type": "miner",
            "fuel": 100,
            "fuel_max": 100,
            "hp": 100,
            "hp_max": 100,
            "size": "small"
        }
    },
    "colonizer": {
        "cost": 300,
        "energy": 30,
        "heavyMetal": 3,
        "processingModules": 0,
        "initialProperties": {
            "name": "New Colonizer",
            "type": "colonizer",
            "fuel": 300,
            "fuel_max": 300,
            "hp": 200,
            "hp_max": 200,
            "size": "medium"
        }
    },
    "fighter": {
        "cost": 200,
        "energy": 20,
        "heavyMetal": 2,
        "processingModules": 0,
        "initialProperties": {
            "name": "New Fighter",
            "type": "fighter",
            "fuel": 300,
            "fuel_max": 300,
            "hp": 300,
            "hp_max": 300,
            "size": "small"
        }
    },
    "capitalship": {
        "cost": 500,
        "energy": 50,
        "heavyMetal": 5,
        "processingModules": 5,
        "initialProperties": {
            "name": "New Capital Ship",
            "type": "capitalship",
            "fuel": 1000,
            "fuel_max": 1000,
            "hp": 1000,
            "hp_max": 1000,
            "bay_type": "medium",
            "secondaryBay_type": "small",
            "bay_amount": 3,
            "secondaryBay_amount": 5
        }
    },
    "mothership": {
        "cost": 1000,
        "energy": 100,
        "heavyMetal": 10,
        "processingModules": 10,
        "initialProperties": {
            "name": "New Mothership",
            "type": "mothership",
            "fuel": 2000,
            "fuel_max": 2000,
            "hp": 2500,
            "hp_max": 2500,
            "bay_type": "large",
            "bay_amount": 10
        }
    },
    "titanship": {
        "cost": 10000,
        "energy": 1000,
        "heavyMetal": 100,
        "processingModules": 100,
        "initialProperties": {
            "name": "New Titanship",
            "type": "titanship",
            "fuel": 10000,
            "fuel_max": 10000,
            "hp": 10000,
            "hp_max": 10000,
            "size": "your mom"
        }
    },
    "frigate": {
        "cost": 300,
        "energy": 30,
        "heavyMetal": 3,
        "processingModules": 3,
        "initialProperties": {
            "name": "New Frigate",
            "type": "frigate",
            "fuel": 500,
            "fuel_max": 500,
            "hp": 500,
            "hp_max": 500,
            "size": "medium"
        }
    },
    "carrier": {
        "cost": 500,
        "energy": 50,
        "heavyMetal": 5,
        "processingModules": 5,
        "initialProperties": {
            "name": "New Carrier",
            "type": "carrier",
            "fuel": 1000,
            "fuel_max": 1000,
            "hp": 1000,
            "hp_max": 1000,
            "size": "large",
            "bay_type": "small",
            "bay_amount": 20
        }
    }
}
