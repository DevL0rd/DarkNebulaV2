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
        ]
        self.resources = {
            "hydrogen": {
                "name": "Hydrogen",
                "rarity": 70
            },
            "water": {
                "name": "Water",
                "rarity": 30
            },
            "carbon": {
                "name": "Carbon",
                "rarity": 55
            },
            "iron": {
                "name": "Iron",
                "rarity": 40
            },
            "silica": {
                "name": "Silica",
                "rarity": 10
            },
            "darkMatter": {
                "name": "Dark Matter",
                "rarity": 0
            },
            "antiMatter": {
                "name": "Anti Matter",
                "rarity": 0
            },
            "gold": {
                "name": "Gold",
                "rarity": 15
            },
            "copper": {
                "name": "Copper",
                "rarity": 30
            },
            "diamond": {
                "name": "Diamond",
                "rarity": 5
            },
            "unobtanium": {
                "name": "Unobtanium",
                "rarity": 0
            }
        }
        # https://en.wikipedia.org/wiki/List_of_planet_types
        # read by composition
        self.planets = [
            {
                "name": "Silicate planet",
                "canLand": True,
                "habitable": True,
                "isGas": False,
                "resources": [
                    self.resources["silica"]
                ],
                "rarity": 75
            },
            {
                "name": "Carbon planet",
                "canLand": True,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["carbon"],
                    self.resources["diamond"]
                ],
                "rarity": 15
            },
            {
                "name": "Desert planet",
                "canLand": True,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["silica"]
                ],
                "rarity": 26
            },
            {
                "name": "Gas giant",
                "canLand": True,
                "habitable": False,
                "isGas": True,
                "resources": [
                    self.resources["hydrogen"]
                ],
                "rarity": 50
            },
            {
                "name": "Ice giant",
                "canLand": True,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["hydrogen"],
                    self.resources["water"]
                ],
                "rarity": 60
            },
            {
                "name": "Lava planet",
                "canLand": False,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["carbon"],
                    self.resources["iron"]
                ],
                "rarity": 20
            },
            {
                "name": "Ocean planet",
                "canLand": True,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["hydrogen"],
                    self.resources["water"]
                ],
                "rarity": 58
            },
            {
                "name": "Protoplanet",
                "canLand": True,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["iron"],
                ],
                "rarity": 70
            },
            {
                "name": "Puffy planet",
                "canLand": False,
                "habitable": False,
                "isGas": True,
                "resources": [
                    self.resources["hydrogen"],
                ],
                "rarity": 30
            },
            {
                "name": "Terrestrial planet",
                "canLand": True,
                "habitable": True,
                "isGas": False,
                "resources": [
                    self.resources["iron"],
                    self.resources["hydrogen"],
                    self.resources["water"]
                ],
                "rarity": 30
            },
            {
                "name": "Ancient Religious Civilization",
                "canLand": True,
                "habitable": True,
                "isGas": False,
                "resources": [
                    self.resources["copper"],
                    self.resources["carbon"],
                    self.resources["iron"],
                    self.resources["water"],
                    self.resources["hydrogen"]
                ],
                "rarity": 13
            },
            {
                "name": "Ancient Technological Civilization",
                "canLand": True,
                "habitable": True,
                "isGas": False,
                "resources": [
                    self.resources["copper"],
                    self.resources["gold"],
                    self.resources["carbon"],
                    self.resources["iron"],
                    self.resources["water"],
                    self.resources["hydrogen"],
                    self.resources["silica"],
                    self.resources["diamond"]
                ],
                "rarity": 9
            },
            {
                "name": "Ancient Super Civilization",
                "canLand": True,
                "habitable": True,
                "isGas": False,
                "resources": [
                    self.resources["copper"],
                    self.resources["carbon"],
                    self.resources["gold"],
                    self.resources["iron"],
                    self.resources["water"],
                    self.resources["hydrogen"],
                    self.resources["silica"],
                    self.resources["diamond"],
                    self.resources["unobtanium"]
                ],
                "rarity": 2
            },
            {
                "name": "Inhabited Planet",
                "canLand": True,
                "habitable": True,
                "isGas": False,
                "resources": [
                    self.resources["iron"],
                    self.resources["water"],
                    self.resources["hydrogen"]
                ],
                "rarity": 25
            }
        ]
        self.asteroidBelts = [
            {
                "name": "Ice Belt",
                "canLand": False,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["water"],
                    self.resources["hydrogen"]
                ],
                "rarity": 25
            },
            {
                "name": "Carbon Belt",
                "canLand": False,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["carbon"]
                ],
                "rarity": 25
            },
            {
                "name": "Iron Belt",
                "canLand": False,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["iron"]
                ],
                "rarity": 25
            },
            {
                "name": "Silica Belt",
                "canLand": False,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["silica"]
                ],
                "rarity": 25
            },
            {
                "name": "Gold Belt",
                "canLand": False,
                "habitable": False,
                "isGas": False,
                "resources": [
                    self.resources["gold"]
                ],
                "rarity": 25
            }
        ]
        # lambda function to sort by rarity
        self.mapObjects = sorted(
            self.mapObjects, key=lambda k: k['rarity'], reverse=True)
        self.planets = sorted(
            self.planets, key=lambda k: k['rarity'], reverse=True)
        self.asteroidBelts = sorted(
            self.asteroidBelts, key=lambda k: k['rarity'], reverse=True)
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
            return self.generateObjectsForBody(random.choice(possibleSpawns))
        return False

    def generateObjectsForBody(self, body):
        body["objects"] = []
        planetCount = random.randrange(3, 10)
        decision = random.randrange(0, 100)
        possibleSpawns = []
        for planet in self.planets:
            if decision <= planet["rarity"]:
                possibleSpawns.append(planet)
            else:
                break
        while planetCount > 0:
            if len(possibleSpawns) > 0:
                obj = random.choice(possibleSpawns)
                possibleResources = []
                for resKey in self.resources:
                    resource = self.resources[resKey]
                    if decision <= resource["rarity"]:
                        possibleResources.append(resource)
                    else:
                        break
                if len(possibleResources) > 0:
                    resourceCount = random.randrange(1, 4)
                    while resourceCount > 0:
                        selectedResource = random.choice(possibleResources)
                        if not selectedResource in obj["resources"]:
                            obj["resources"].append(selectedResource)
                        resourceCount -= 1
                body["objects"].append(obj)
            planetCount -= 1

        decision = random.randrange(0, 100)
        possibleSpawns = []
        for belt in self.asteroidBelts:
            if decision <= belt["rarity"]:
                possibleSpawns.append(belt)
            else:
                break
        if len(possibleSpawns) > 0:
            body["objects"].append(random.choice(possibleSpawns))

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

    # def renderSystem(self, id, startX, startY):
    #     x = startX
    #     y = startY
    #     width = x + 79
    #     height = y + 20
    #     bold = self.formatting['bold']
    #     reset = self.formatting['reset']
    #     self.graphics.seperator(id)
    #     while y < height:
    #         textRow = ""
    #         while x < width:
    #             if x in self.universe and y in self.universe[x]:
    #                 mapTile = self.universe[x][y]
    #                 char = mapTile["char"]
    #                 color = self.formatting["fg"][mapTile["color"]]
    #                 textRow += f"{bold}{color}{char}{reset}"
    #             else:
    #                 textRow += " "
    #             x += 1
    #         x = startX
    #         y += 1
    #         self.server.send(id, textRow)
    #     self.graphics.seperator(id)
