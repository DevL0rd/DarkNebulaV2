import time
from modules.logging import Logging
Logger = None

# fancy logic


class CommandsSystem:
    def __init__(self, events, server, graphics, accounts, playersSystem, settings):
        global Logger
        Logger = Logging(events, "Commands")
        self.Events = events
        self.on = events.on
        self.Server = server
        self.accounts = accounts
        self.playersSystem = playersSystem
        self.settings = settings
        self.graphics = graphics
        self.formatting = graphics.formatting
        self.Events.on("command", self.onCommand)
        self.commands = {
            "help": {
                "exec": self.help,
                "usage": "help <command>",
                "description": "Shows this help page."
            },
            "pm": {
                "exec": self.pm,
                "usage": "pm [username] [message]",
                "description": "Send a user a private message."
            },
            "say": {
                "exec": self.say,
                "usage": "say [message]",
                "description": "Send a global message."
            }
        }

    def commandExists(self, command):
        return command in self.commands

    def sendCommandUsage(self, id, command):
        comData = self.commands[command]
        self.Server.send(comData["usage"])

    def onCommand(self, data):
        id = data["id"]
        if not self.accounts.isLoggedIn(id):
            return

        command = data["command"].lower()
        rest = data["rest"]
        params = data["params"]

        if self.commandExists(command):
            self.commands[command]["exec"](id, rest, params)
        else:
            self.Server.error(id, "The command '" + command + "' is invalid.")
    # -----commands start here-----

    def help(self, id, rest, params):
        self.graphics.seperator(id)
        for command in self.commands:
            comData = self.commands[command]
            usage = comData['usage']
            description = comData['description']
            self.Server.send(id, command)
            self.Server.send(id, f" Use: {usage}")
            self.Server.send(id, f" Description: " + description)
            self.Server.send(id, " ")
        self.graphics.seperator(id)

    # TODO, Finish this function by getting the player id by the first param, which should be username, then the rest is the message, and check if the reciever is online.
    def pm(self, id, message, params):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["pmTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["pmMessageColor"]]
        thisUsersName = self.accounts.getUsername(id)
        player = self.playersSystem.getPlayer(thisUsersName)
        userColor = self.formatting['fg'][player["color"]]
        self.Server.send(
            f"{bold}[{tagColor}MESSAGE{reset}{bold}]{bold}<{reset}{userColor}{thisUsersName}{reset}{bold}>{reset}: {msgColor}{message}{reset}")

    def say(self, id, message, params):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["sayTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["sayMessageColor"]]
        thisUsersName = self.accounts.getUsername(id)
        player = self.playersSystem.getPlayer(thisUsersName)
        userColor = self.formatting['fg'][player["color"]]
        self.Server.sendAll(
            f"{bold}[{tagColor}GLOBAL{reset}{bold}]{bold}<{reset}{userColor}{thisUsersName}{reset}{bold}>{reset}: {msgColor}{message}{reset}")
