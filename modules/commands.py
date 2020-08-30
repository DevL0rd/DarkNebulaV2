import time
from modules.logging import Logging
Logger = None

# fancy logic


class CommandsSystem:
    def __init__(self, events, server, graphics, accounts, playersSystem, universeSystem, settings):
        global Logger
        Logger = Logging(events, "Commands")
        self.Events = events
        self.on = events.on
        self.server = server
        self.accounts = accounts
        self.playersSystem = playersSystem
        self.universe = universeSystem
        self.settings = settings
        self.graphics = graphics
        self.formatting = graphics.formatting
        self.Events.on("command", self.onCommand)
        self.commands = {
            "help": {
                "exec": self.help,
                "usage": "help <command>",
                "description": "Shows this help page.",
                "requiresOp": False
            },
            "pm": {
                "exec": self.pm,
                "usage": "pm [username] [message]",
                "description": "Send a user a private message.",
                "requiresOp": False
            },
            "say": {
                "exec": self.say,
                "usage": "say [message]",
                "description": "Send a global message.",
                "requiresOp": False
            },
            "op": {
                "exec": self.op,
                "usage": "op [username]",
                "description": "Makes a player a operator.",
                "requiresOp": True
            },
            "friend": {
                "exec": self.friend,
                "usage": "friend <list/add/del/rem> [username]",
                "description": "Manage your friends.",
                "requiresOp": False
            },
            "shipshop": {
                "exec": self.shipShop,
                "usage": "shipshop <list, buy, sell, inspect> <shiptype>",
                "description": "Displays ships in the shop, allows you to buy/sell and inspect the ship shop's wares.",
                "requiresOp": False
            },
            "map": {
                "exec": self.map,
                "usage": "map <ship/planet> or <x> <y>",
                "description": "Displays ships in the shop, allows you to buy/sell and inspect the ship shop's wares.",
                "requiresOp": False
            }
        }

    def commandExists(self, command):
        return command in self.commands

    def sendCommandUsage(self, id, command):
        comData = self.commands[command]
        self.server.send(comData["usage"])

    def onCommand(self, data):
        id = data["id"]
        if not self.accounts.isLoggedIn(id):
            return

        command = data["command"].lower()
        rest = data["rest"]
        params = data["params"]

        if self.commandExists(command):
            if self.commands[command]["requiresOp"]:
                username = self.accounts.getUsername(id)
                isOp = self.playersSystem.isOp(username)
                if isOp:
                    self.commands[command]["exec"](id, rest, params)
                else:
                    self.server.error(
                        id, f"You don't have permission to use this command.")
            else:
                self.commands[command]["exec"](id, rest, params)
        else:
            self.server.error(id, f"The command '{command}' is invalid.")

    # -----commands start here-----
    def map(self, id, rest, params):
        self.universe.renderMap(id, 25, 25)

    def shipShop(self, id, rest, params):
        return

    def op(self, id, rest, params):
        return

    def help(self, id, rest, params):
        self.graphics.seperator(id)
        username = self.accounts.getUsername(id)
        isOp = self.playersSystem.isOp(username)
        for command in self.commands:
            comData = self.commands[command]
            if comData["requiresOp"] and not isOp:
                continue
            usage = comData['usage']
            description = comData['description']
            self.server.send(id, command)
            self.server.send(id, f" Use: {usage}")
            self.server.send(id, f" Description: " + description)
            self.server.send(id, " ")
        self.graphics.seperator(id)

    # TODO, Finish this function by getting the player id by the first param, which should be username, then the rest is the message, and check if the reciever is online.
    def pm(self, id, message, params):
        if len(params) == 0:
            self.server.error(id, self.commands["pm"]["usage"])
            return
        userToMessage = params[0]
        if self.playersSystem.playerExists(userToMessage):
            if self.accounts.isOnline(userToMessage):
                message = " ".join(params[1:len(params)])
                chatSettings = self.settings.getChatSettings()
                bold = self.formatting['bold']
                reset = self.formatting['reset']
                tagColor = self.formatting['fg'][chatSettings["pmTagColor"]]
                msgColor = self.formatting['fg'][chatSettings["pmMessageColor"]]
                thisUsersName = self.accounts.getUsername(id)
                player = self.playersSystem.getPlayer(thisUsersName)
                userColor = self.formatting['fg'][player["color"]]
                receiverID = self.accounts.getId(userToMessage)
                self.server.send(receiverID,
                                 f"{bold}[{tagColor}MESSAGE{reset}{bold}]{bold}<{reset}{userColor}{thisUsersName}{reset}{bold}>{reset}: {msgColor}{message}{reset}", True)
            else:
                self.server.error(
                    id, f"{userToMessage} is not online.")
        else:
            self.server.error(
                id, f"{userToMessage} is not a real player you git!")

    def say(self, id, message, params):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["sayTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["sayMessageColor"]]
        thisUsersName = self.accounts.getUsername(id)
        player = self.playersSystem.getPlayer(thisUsersName)
        userColor = self.formatting['fg'][player["color"]]
        self.server.sendAll(
            f"{bold}[{tagColor}GLOBAL{reset}{bold}]{bold}<{reset}{userColor}{thisUsersName}{reset}{bold}>{reset}: {msgColor}{message}{reset}", True)

    def friend(self, id, rest, params):
        if len(params) == 0:
            self.server.error(id, self.commands["friend"]["usage"])
            return

        thisUsername = self.accounts.getUsername(id)
        if params[0] == "list":
            friendsList = self.playersSystem.getFriends(thisUsername)
            self.graphics.seperator(id)
            for friend in friendsList:
                self.server.send(id, friend)
            self.graphics.seperator(id)
        elif params[0] == "add" and len(params) == 2:
            friendToAdd = params[1]
            if not friendToAdd == thisUsername:
                if self.playersSystem.playerExists(friendToAdd):
                    if not self.playersSystem.isFriend(thisUsername, friendToAdd):
                        # add the friend
                        self.playersSystem.addFriend(thisUsername, friendToAdd)
                        self.server.pm(id, f"{friendToAdd} has been added")
                    else:  # already in friends list
                        self.server.error(
                            id, f"{friendToAdd} is already a friend.")
                else:  # player does not exist
                    self.server.error(
                        id, f"{friendToAdd} is not a real player you git!")
            else:
                self.server.error(id, f"Really...? Thats sad..")
        elif params[0] == "del" or params[0] == "rem" and len(params) == 2:
            friendToDel = params[1]
            if self.playersSystem.isFriend(thisUsername, friendToDel):
                self.playersSystem.removeFriend(thisUsername, friendToDel)
                self.server.pm(id, f"{friendToDel} has been removed.")
            else:
                self.server.error(id, f"{friendToDel} isn't ya friend.")
        else:  # if invalid use, send usage
            self.server.error(id, self.commands["friend"]["usage"])

        # self.server.pm(id, "Messagehere")
        # self.server.error(id, "error message")
        # self.playersSystem.playerExists(thisUsersName)
        # self.playersSystem.getFriends(thisUsersName)
        # self.playersSystem.isFriend(thisUsersName, friendName)
        # self.playersSystem.removeFriend(thisUsersName, friendName)
        # self.playersSystem.addFriend(thisUsersName, friendName)
