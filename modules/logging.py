# Authors: DevL0rd
# -*- coding: utf-8 -*-
from time import gmtime, strftime
import ctypes
import asyncio
import os
import sys
import codecs


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


class Logging:
    namesSpace = "No Namespace"
    namesSpaceColor = "purple"
    timeColor = "blue"
    useColor = True
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
            'darkBlue':   "\033[0;34m",
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

    def getColoredTimeString(self):
        timeString = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return self.formatting['fg']["white"] + \
            "[" + self.formatting['fg'][self.timeColor] + \
            timeString + self.formatting['fg']["white"] + "]"

    def getColoredNamespaceString(self):
        return self.formatting['fg']["white"] + \
            "[" + self.formatting['fg'][self.namesSpaceColor] + \
            self.nameSpace + self.formatting['fg']["white"] + "]"

    def getColoredLogPrefixes(self):
        timeStringColored = self.getColoredTimeString()
        nameSpaceString = self.getColoredNamespaceString()
        return timeStringColored + " " + nameSpaceString + ": "

    def reColorQuotedStrings(self, text, textColor, highlightColor="blue"):
        stringMatched = find_between(text, "'", "'")
        if stringMatched:
            stringMatched = "'" + stringMatched + "'"
            newString = self.formatting['fg'][highlightColor] + \
                stringMatched + self.formatting['fg'][textColor]
            text = text.replace(
                stringMatched, newString, 1)
        return text

    def formatAndColorLogText(self, text, color):
        text = self.formatting['fg'][color] + text + self.formatting['reset']
        coloredLogPrefixes = self.getColoredLogPrefixes()
        formatedLogText = self.reColorQuotedStrings(text, color)
        return coloredLogPrefixes + formatedLogText

    def getTimeString(self):
        timeString = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return "[" + timeString + "]"

    def getNamespaceString(self):
        return "[" + self.nameSpace + "]"

    def getLogPrefixes(self):
        return self.getTimeString() + " " + self.getNamespaceString() + ": "

    def formatLogText(self, text):
        return self.getLogPrefixes() + text

    def log(self, text, color="white"):
        colorText = self.formatAndColorLogText(text, color)
        normalText = self.formatLogText(text)
        if self.useColor:
            print(colorText)
        else:
            print(normalText)
        self.Events.trigger("log", normalText)
        self.Events.trigger("logColor", colorText)
        self.Events.trigger("logRaw", text)

    def warn(self, text, color="darkYellow"):
        colorText = self.formatAndColorLogText(text, color)
        normalText = self.formatLogText(text)
        if self.useColor:
            print(colorText)
        else:
            print(normalText)
        self.Events.trigger("warn", normalText)
        self.Events.trigger("warnColor", colorText)
        self.Events.trigger("warnRaw", text)

    def error(self, text, color="red"):
        colorText = self.formatAndColorLogText(text, color)
        normalText = self.formatLogText(text)
        if self.useColor:
            print(colorText)
        else:
            print(normalText)
        self.Events.trigger("error", normalText)
        self.Events.trigger("errorColor", colorText)
        self.Events.trigger("errorRaw", text)

    def exception(self, text, color="red"):
        colorText = self.formatAndColorLogText(text, color)
        normalText = self.formatLogText(text)
        if self.useColor:
            print(colorText)
        else:
            print(normalText)
        self.Events.trigger("exception", normalText)
        self.Events.trigger("exceptionColor", colorText)
        self.Events.trigger("exceptionRaw", text)

    def setNamespaceColor(self, color):
        self.nameSpaceColor = color

    def setNamespace(self, nameSpace, color="default"):
        self.nameSpace = nameSpace
        if not color == "default":
            self.setNamespaceColor(color)

    def setColorMode(self, useColor):
        self.useColor = useColor

    def __init__(self, Events, nameSpace="No Namespace"):
        self.Events = Events
        self.on = self.Events.on
        self.setNamespace(nameSpace)
        if os.name == 'nt':  # If windows then enable color support in console
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        sys.stdout.reconfigure(encoding='utf-8')
