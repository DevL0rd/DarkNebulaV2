from modules.logging import Logging
Logger = None


class MudGraphics:
    formatting = {
        "reset": '\033[0m',
        "bold": '\033[01m',
        "disable": '\033[02m',
        "underline": '\033[04m',
        "reverse": '\033[07m',
        "strikethrough": '\033[09m',
        "invisible": '\033[08m',
        "fg": {
            'white':    "\033[1;37m",
            'yellow':   "\033[1;33m",
            'green':    "\033[1;32m",
            'blue':     "\033[1;34m",
            'cyan':     "\033[1;36m",
            "pink": '\033[1;95m',
            'red':      "\033[1;31m",
            'purple':  "\033[1;35m",
            'grey':  "\033[0;37m",
            "darkGrey": '\033[1;90m',
            'darkYellow': "\033[0;33m",
            'darkGreen':  "\033[0;32m",
            'blue':   "\033[0;34m",
            'darkCyan':   "\033[0;36m",
            'darkRed':    "\033[0;31m",
            'darkPurple': "\033[0;35m",
            'black':  "\033[0;30m"
        },
        "bg": {
            "black": '\033[40m',
            "red": '\033[41m',
            "green": '\033[42m',
            "yellow": '\033[43m',
            "blue": '\033[44m',
            "purple": '\033[45m',
            "cyan": '\033[46m',
            "lightGrey": '\033[47m'
        }
    }

    def __init__(self, events, server, settings):
        global Logger
        Logger = Logging(events, "Graphics")
        self.Events = events
        self.on = events.on
        self.Server = server
        self.clients = {}
        self.players = {}
        self.settings = settings
        self.Events.on("connect", self.onConnect)

    def onConnect(self, id):
        self.splash(id)

    def seperator(self, id):
        self.Server.send(
            id, self.formatting["bold"]+"#**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**~**o**#"+self.formatting["reset"])

    def splash(self, id):
        self.seperator(id)
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"                  *                         *            .                   "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"   *    /$$    .                /$$               .                          "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"       | $$                    | $$                         *          *     "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"   /$$$$$$$  /$$$$$$   /$$$$$$ | $$   /$$     *    .            .            "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"  /$$__  $$ |____  $$ /$$__  $$| $$  /$$/                                    "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+" | $$  | $$  /$$$$$$$| $$  \__/| $$$$$$/            *                 *      "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+" | $$  | $$ /$$__  $$| $$      | $$_  $$                                     "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+" |  $$$$$$$|  $$$$$$$| $$      | $$ \  $$          .         *               "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"  \_______/ \_______/|__/      |__/  \__/                                *   "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"           *                 *             /$$          *      /$$           "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"                      .                   | $$                | $$           "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+" *    *           *    /$$$$$$$   /$$$$$$ | $$$$$$$  /$$   /$$| $$  /$$$$$$  "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"             .        | $$__  $$ /$$__  $$| $$__  $$| $$  | $$| $$ |____  $$ "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"      *               | $$  \ $$| $$$$$$$$| $$  \ $$| $$  | $$| $$  /$$$$$$$ "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"           *          | $$  | $$| $$_____/| $$  | $$| $$  | $$| $$ /$$__  $$ "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+" *     .          *   | $$  | $$|  $$$$$$$| $$$$$$$/|  $$$$$$/| $$|  $$$$$$$ "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"                      |__/  |__/ \_______/|_______/  \______/ |__/ \_______/ "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.Server.send(
            id, self.formatting["bold"]+"#"+self.formatting["fg"]["blue"]+"             *            .                            *                .    "+self.formatting["reset"]+self.formatting["bold"]+"#"+self.formatting["reset"])
        self.seperator(id)
