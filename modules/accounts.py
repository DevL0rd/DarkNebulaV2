from modules.logging import Logging
Logger = None


class AccountsSystem:

    def __init__(self, events, server, playersSystem, settings):
        global Logger
        Logger = Logging(events, "Accounts")
        self.Events = events
        self.on = events.on
        self.Server = server
        self.clients = {}
        self.playersSystem = playersSystem
        self.settings = settings
        self.Server.on("connect", self.onConnect)
        self.Server.on("disconnect", self.onDisconnect)
        self.Server.on("command", self.onCommand)

    def onConnect(self, id):
        self.clients[id] = {
            "loggedIn": False
        }
        self.Server.send(id, "Username: ")

    def onDisconnect(self, id):
        if self.isLoggedIn(id):
            username = self.clients[id]["username"]
            self.Server.sendAll(
                f"User {username} has disconnected from the server.")
        del self.clients[id]

    def onCommand(self, data):
        id = data["id"]
        command = data["command"]
        if not self.isLoggedIn(id):
            if not "username" in self.clients[id]:
                username = command
                self.clients[id]["username"] = username
                if self.playersSystem.playerExists(username):
                    self.Server.send(id, "Password: ")
                else:
                    self.Server.send(id,
                                     "Please type a password for your new account.")
                    self.Server.send(id, "Password: ")
            else:
                password = command
                username = self.clients[id]["username"]
                self.login(id, password)
        else:
            return False  # todo add logout commands
        return True  # stop event system from triggering the rest of the listeners

    def getId(self, username):
        for id in self.clients:
            if self.isLoggedIn(id) and username == self.getUsername(id):
                return id
        return False

    def isLoggedIn(self, id):
        if id in self.clients:
            return self.clients[id]["loggedIn"]
        return False

    def getOnlineUsers(self):
        onlineUsers = []
        for id in self.clients:
            if self.isLoggedIn(id):
                onlineUsers.append(self.getUsername(id))
        return onlineUsers

    def getOnlineUsersCount(self):
        return len(self.getOnlineUsers())

    def getUsername(self, id):
        if self.isLoggedIn(id):
            return self.clients[id]["username"]
        return False

    def login(self, id, password):
        username = self.clients[id]["username"]
        if username in self.playersSystem.players:
            if password == self.playersSystem.players[username]["password"]:
                self.clients[id]["loggedIn"] = True
                Logger.log(f"User '{username}'' has logged in!")
                self.Server.send(id, f"Welcome back {username}!")
                self.Events.trigger("login", id)
            else:
                Logger.log(
                    f"Invalid login attempt on account {username}!", "red")
                self.Server.send(id, f"Invalid password!")
        else:
            Logger.log(f"User '{username}' has logged in!")
            self.Server.send(id, f"Welcome to Dark Nebula {username}!")
            self.playersSystem.initPlayer(username)
            self.clients[id]["loggedIn"] = True
            self.Events.trigger("firstLogin", id)
            self.Server.sendAll(f"Welcome {username} to the server!")
