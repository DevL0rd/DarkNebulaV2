from modules.logging import Logging
from modules.server import TelnetServer
from modules.events import Events
EventSystem = Events()
Server = TelnetServer(EventSystem)
Logger = Logging(EventSystem, "Server")
Server.start()
