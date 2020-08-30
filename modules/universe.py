import random
from modules.logging import Logging
Logger = None


class UniverseSystem:
    def __init__(self, events, server, graphics, accounts, playersSystem, settings):
        global Logger
        Logger = Logging(events, "Universe")
        self.Events = events
        self.on = events.on
        self.server = server
        self.accounts = accounts
        self.playersSystem = playersSystem
        self.settings = settings
        self.graphics = graphics
        self.formatting = graphics.formatting
        self.mapObjects = [
            {
                "name": "Red Giant",
                "fuelRate": 1.5,
                "energyRate": 1.5,
                "char": "O",
                "color": "red",
                "rarity": 10
            },
            {
                "name": "White Dwarf Star",
                "fuelRate": 0.5,
                "energyRate": 0.5,
                "char": "o",
                "color": "white",
                "rarity": 15
            },
            {
                "name": "Red Dwarf Star",
                "fuelRate": 0.2,
                "energyRate": 0.2,
                "char": "o",
                "color": "red",
                "rarity": 22
            },
            {
                "name": "Main Sequence Star",
                "fuelRate": 1,
                "energyRate": 1,
                "char": "O",
                "color": "yellow",
                "rarity": 95
            },
            {
                "name": "Neutron Star",
                "massRate": 100,
                "char": "x",
                "color": "purple",
                "rarity": 3
            },
            {
                "name": "Supergiant",
                "fuelRate": 10,
                "energyRate": 10,
                "char": "S",
                "color": "blue",
                "rarity": 12
            },
            {
                "name": "Quasar",
                "char": "*",
                "energyRate": 100,
                "color": "white",
                "rarity": 3
            },
            {
                "name": "Pulsar",
                "fuelRate": 0,
                "energyRate": 50,
                "char": "*",
                "color": "purple",
                "rarity": 2
            },
            {
                # stay away
                "name": "Black Hole",
                "fuelRate": 0,
                "char": "X",
                "color": "purple",
                "rarity": 4
            },
            {
                "name": "Kugelblitz",
                "fuelRate": 0,
                "energyRate": 1000,
                "char": "K",
                "color": "white",
                "rarity": 1
            }
            # {
            #     "type": "water",
            #     "atmosphere": "nitrogen"
            # },
            # {
            #     "type": "rocky"
            # },
            # {
            #     "type": "gas giant"
            # },
            # {
            #     "type": "goldilocks"
            # },
            # {
            #     "type": "frozen"
            # },
            # {
            #     "type": "lava"
            # },
            # {
            #     "type": "moon"
            # },
            # {
            #     "type": "barren",
            #     "atmosphere": None
            # }
        ]
        # lambda function to sort by rarity
        self.mapObjects = sorted(
            self.mapObjects, key=lambda k: k['rarity'], reverse=True)
        self.universe = self.generateUniverse()

    def generateUniverse(self):
        universe = {}
        universeSettings = self.settings.getUniverseSettings()
        x = 0
        y = 0
        Logger.log("Generating universe...")
        while y < universeSettings["height"]:
            while x < universeSettings["width"]:
                decision = random.randrange(0, 100)
                if decision <= universeSettings["spawnChance"]:
                    newMapTile = self.getRandomMapTile()
                    if newMapTile:
                        if not x in universe:
                            universe[x] = {}
                        universe[x][y] = newMapTile
                x += 1
            x = 0
            y += 1
        Logger.log("Universe generated!")
        return universe

    def getRandomMapTile(self):
        decision = random.randrange(0, 100)
        possibleSpawns = []
        for mapObject in self.mapObjects:
            # TODO make more complex generation later
            if decision <= mapObject["rarity"]:
                possibleSpawns.append(mapObject)
            else:
                break
        if len(possibleSpawns) > 0:
            if len(possibleSpawns) == 1:
                return possibleSpawns[0]
            else:
                return possibleSpawns[random.randrange(0, len(possibleSpawns) - 1)]
        return False

#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#
    def renderMap(self, id, startX, startY):
        x = startX
        y = startY
        width = x + 79
        height = y + 20
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        self.graphics.seperator(id)
        while y < height:
            textRow = ""
            while x < width:
                if x in self.universe and y in self.universe[x]:
                    mapTile = self.universe[x][y]
                    char = mapTile["char"]
                    color = self.formatting["fg"][mapTile["color"]]
                    textRow += f"{bold}{color}{char}{reset}"
                else:
                    textRow += " "
                x += 1
            x = startX
            y += 1
            self.server.send(id, textRow)
        self.graphics.seperator(id)
