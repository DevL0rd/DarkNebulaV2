from modules.logging import Logging
from modules.settings import Settings
from modules.telnet import TelnetServer
from modules.accounts import AccountsSystem
from modules.graphics import MudGraphics
from modules.game import GameLogic
from modules.commands import CommandsSystem
from modules.players import PlayerSystem
from modules.universe import UniverseSystem
import telnetlib3
import time
Logger = None


class MudServer:
    def __init__(self, events):
        global Logger
        Logger = Logging(events, "Server")
        self.server = TelnetServer()
        self.Events = events
        self.on = events.on
        self.clients = {}
        self.settings = Settings("./storage/settings.json")
        self.graphics = MudGraphics(events, self, self.settings)
        self.formatting = self.graphics.formatting
        self.playersSystem = PlayerSystem(events, self, self.settings)
        self.accounts = AccountsSystem(
            events, self, self.playersSystem, self.settings)
        self.universe = UniverseSystem(events, self, self.graphics,
                                       self.accounts, self.playersSystem, self.settings)
        self.game = GameLogic(events, self, self.graphics,
                              self.accounts, self.playersSystem, self.universe, self.settings)
        self.commands = CommandsSystem(events, self, self.graphics,
                                       self.accounts, self.playersSystem, self.universe, self.settings)

    def start(self):
        Logger.log("Starting server.", "purple")
        while True:
            self.tick()
            time.sleep(0.02)

    def tick(self):
        self.server.update()
        for id in self.server.get_new_players():
            self.clients[id] = True
            self.Events.trigger("connect", id)
            playerCount = str(self.accounts.getOnlineUsersCount())
            Logger.log(
                f"Client '{id}' connected! {playerCount} players online.", "green")

        for id in self.server.get_disconnected_players():
            self.Events.trigger("disconnect", id)
            del self.clients[id]
            playerCount = str(self.accounts.getOnlineUsersCount())
            Logger.log(
                f"Client '{id}' disconnected! {playerCount} players online.", "red")

        for id, command, rest in self.server.get_commands():
            self.Events.trigger("command", {
                "id": id,
                "command": command,
                "rest": rest,
                "params": rest.split(" ")
            })
        self.Events.trigger("tick", 0)

    def send(self, id, text, logIt=False):
        self.server.send_message(id, text)
        if logIt:
            receiverName = self.accounts.getUsername(id)
            player = self.playersSystem.getPlayer(receiverName)
            if not player:
                print(text)
            else:
                playerColor = player["color"]
                bold = self.formatting['bold']
                reset = self.formatting['reset']
                print(f"{bold}{playerColor}{receiverName}{reset}<-{text}")

    def sendAll(self, text, logIt=False):
        for id in self.clients:
            if self.accounts.isLoggedIn(id):
                self.server.send_message(id, text)
        if logIt:
            print(text)

    def say(self, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["serverMessageColor"]]
        self.sendAll(
            f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}", True)

    def pm(self, id, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["pmMessageColor"]]
        self.send(id,
                  f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}", True)

    def error(self, id, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["serverErrorColor"]]
        self.send(id,
                  f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}", True)

    def warning(self, id, message):
        chatSettings = self.settings.getChatSettings()
        bold = self.formatting['bold']
        reset = self.formatting['reset']
        tagColor = self.formatting['fg'][chatSettings["serverTagColor"]]
        msgColor = self.formatting['fg'][chatSettings["serverWarningColor"]]
        self.send(
            id, f"{bold}[{tagColor}SERVER{reset}{bold}]{reset}: {msgColor}{message}{reset}", True)
