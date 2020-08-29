class Settings:
    def __init__(self, settingsPath="./storage/settings.json"):
        self.settings = self.loadSettings("./storage/settings.json")

    def loadSettings(self, settingsPath):
        return {
            "currencyName": "SpaceBucks",
            "currencyAbbr": "SB",
            "chat": {
                "sayMessageColor": "cyan",
                "sayTagColor": "blue",
                "pmMessageColor": "lime",
                "pmTagColor": "green",
                "serverMessageColor": "purple",
                "serverTagColor": "red",
                "serverErrorColor": "red",
                "serverWarningColor": "yellow"
            },
            "startingResources": {
                "money": 500,
                "heavyMetal": 5,
                "heavyMetal_max": 20,
                "energy": 10,
                "processingModules": 0
            },
            "startingShips": [
                {
                    "name": "Starter Probe",
                    "type": "probe",
                    "fuel": 100,
                    "fuel_max": 100,
                    "hp": 100,
                    "hp_max": 100
                },
                {
                    "name": "Starter Miner",
                    "type": "miner",
                    "fuel": 100,
                    "fuel_max": 100,
                    "hp": 100,
                    "hp_max": 100
                }
            ]
        }

    def getSettings(self):
        return self.settings

    def getChatSettings(self):
        return self.settings["chat"]

    def getStartingResources(self):
        return self.settings["startingResources"]

    def getStartingShips(self):
        return self.settings["startingShips"]
