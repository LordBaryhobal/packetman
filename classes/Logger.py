#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import time

class Logger:
    """
    Utility static class used for logging info to the console.
    """

    INFO = 1
    WARN = 2
    ERROR = 4
    DEBUG = 8

    DEFAULT = INFO|WARN|ERROR
    ALL = INFO|WARN|ERROR|DEBUG

    _instance = None

    level = DEFAULT
    
    def log(msg, level=INFO):
        """Logs a message with a given log level

        Arguments:
            msg {str} -- message to log

        Keyword Arguments:
            level {int} -- level of logging (default: {INFO})
        """

        if level & Logger.level == 0:
            return

        print(time.strftime("[%Y-%m-%d %H:%M:%S] "), end="")

        if level == Logger.INFO:
            print("[INFO] ", end="")
        elif level == Logger.WARN:
            print("\033[33m[WARN]\033[0m ", end="")
        elif level == Logger.ERROR:
            print("\033[38;2;170;0;0m\033[1m[ERROR]\033[0m ", end="")
        elif level == Logger.DEBUG:
            print("\033[35m[DEBUG]\033[0m ", end="")
        
        print(msg)

    def info(msg):
        """Logs a message with level INFO

        Arguments:
            msg {str} -- message to log
        """

        Logger.log(msg, Logger.INFO)
    
    def warn(msg):
        """Logs a message with level WARN

        Arguments:
            msg {str} -- message to log
        """
        
        Logger.log(msg, Logger.WARN)
    
    def error(msg):
        """Logs a message with level ERROR

        Arguments:
            msg {str} -- message to log
        """
        
        Logger.log(msg, Logger.ERROR)

    def debug(msg):
        """Logs a message with level DEBUG

        Arguments:
            msg {str} -- message to log
        """
        
        Logger.log(msg, Logger.DEBUG)

if __name__ == "__main__":
    Logger.level = Logger.ALL
    Logger.info("Test info")
    Logger.warn("Test warn")
    Logger.error("Test error")
    Logger.debug("Test debug")
