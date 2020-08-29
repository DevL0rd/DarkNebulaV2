from modules.logging import Logging
from modules.server import MudServer
from modules.events import Events
EventSystem = Events()
Server = MudServer(EventSystem)
Logger = Logging(EventSystem, "Server")
Server.start()
