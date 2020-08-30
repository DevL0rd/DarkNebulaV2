from modules.logging import Logging
from modules.server import MudServer
from modules.events import Events
EventSystem = Events()
Logger = Logging(EventSystem, "Server")
Server = MudServer(EventSystem)
Server.start()
