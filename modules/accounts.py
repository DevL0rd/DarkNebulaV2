from modules.logging import Logging
Logger = None


class AccountsSystem:

    def __init__(self, events, server, playersSystem, settings):
        global Logger
        Logger = Logging(events, "Accounts")
        self.Events = events
        self.on = events.on
        self.server = server
        self.clients = {}
        self.playersSystem = playersSystem
        self.settings = settings
        self.server.on("connect", self.onConnect)
        self.server.on("disconnect", self.onDisconnect)
        self.server.on("command", self.onCommand)

    def onConnect(self, id):
        self.clients[id] = {
            "loggedIn": False
        }
        self.server.send(id, "Username: ")

    def onDisconnect(self, id):
        if self.isLoggedIn(id):
            username = self.clients[id]["username"]
            self.server.say(
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
                    self.server.send(id, "Password: ")
                else:
                    self.server.send(id,
                                     "Please type a password for your new account.")
                    self.server.send(id, "Password: ")
            else:
                password = command
                username = self.clients[id]["username"]
                if not self.isOnline(username):
                    self.login(id, password)
                else:
                    self.server.send(
                        id, "This account is already logged in, from another location.")
                    del self.clients[id]["username"]
                    self.server.send(id, "Username: ")
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

    def isOnline(self, username):
        for id in self.clients:
            if self.isLoggedIn(id):
                if username == self.getUsername(id):
                    return True
        return False

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
                self.server.pm(id, f"Welcome back {username}!")
                self.Events.trigger("login", id)
            else:
                Logger.log(
                    f"Invalid login attempt on account {username}!", "red")
                self.server.send(id, f"Invalid password!")
        else:
            Logger.log(f"User '{username}' has logged in!")
            self.server.pm(id, f"Welcome to Dark Nebula {username}!")
            self.playersSystem.initPlayer(username, password)
            self.clients[id]["loggedIn"] = True
            self.Events.trigger("firstLogin", id)
            self.server.say(f"Welcome {username} to the server!")
