from modules.logging import Logging
from modules.settings import Settings
from modules.mudserver import MudServer
from modules.accounts import AccountsSystem
from modules.graphics import MudGraphics
from modules.game import GameLogic
from modules.commands import CommandsSystem
from modules.players import PlayerSystem
import telnetlib3
import time
Logger = None


class TelnetServer:
    def __init__(self, events):
        global Logger
        Logger = Logging(events, "Server")
        self.Server = MudServer()
        self.Events = events
        self.on = events.on
        self.clients = {}
        self.settings = Settings("./storage/settings.json")
        self.graphics = MudGraphics(events, self, self.settings)
        self.formatting = self.graphics.formatting
        self.playersSystem = PlayerSystem(events, self, self.settings)
        self.accounts = AccountsSystem(
            events, self, self.playersSystem, self.settings)
        self.game = GameLogic(events, self, self.graphics,
                              self.accounts, self.playersSystem, self.settings)
        self.commands = CommandsSystem(events, self, self.graphics,
                                       self.accounts, self.playersSystem, self.settings)

    def start(self):
        Logger.log("Starting server.", "purple")
        while True:
            self.tick()
            time.sleep(0.02)

    def tick(self):
        self.Server.update()
        for id in self.Server.get_new_players():
            Logger.log(f"User '{id}' connected!", "green")
            self.clients[id] = True
            self.Events.trigger("connect", id)

        for id in self.Server.get_disconnected_players():
            Logger.log(f"User '{id}' disconnected!", "red")
            self.Events.trigger("disconnect", id)
            del self.clients[id]

        for id, command, rest in self.Server.get_commands():
            Logger.log(f"Received command '{command}' from {id}.")
            self.Events.trigger("command", {
                "id": id,
                "command": command,
                "rest": rest,
                "params": rest.split(" ")
            })
        self.Events.trigger("tick", 0)

    def send(self, id, text):
        self.Server.send_message(id, text)

    def sendAll(self, text):
        for id in self.clients:
            if self.accounts.isLoggedIn(id):
                self.Server.send_message(id, text)

    def say(self, id, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["serverMessageColor"]]
        self.sendAll(
            f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}")

    def error(self, id, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["serverErrorColor"]]
        self.sendAll(
            f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}")

    def warning(self, id, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["serverWarningColor"]]
        self.sendAll(
            f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}")
