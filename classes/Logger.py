#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import time

class Logger:
    """
    Utility class used for logging info to the console.
    """

    INFO = 1
    WARN = 2
    ERROR = 4
    DEBUG = 8

    DEFAULT = INFO|WARN|ERROR
    ALL = INFO|WARN|ERROR|DEBUG

    def __init__(self, level=DEFAULT):
        """
        @param level: Either Logger.ALL or a combination of Logger.INFO, Logger.WARN,
                      Logger.ERROR, Logger.DEBUG
                      Indicates which messages should be logged.
        """

        self.level = level
    
    def log(self, msg, level=INFO):
        if level & self.level == 0:
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

    def info(self, msg):
        self.log(msg, Logger.INFO)
    
    def warn(self, msg):
        self.log(msg, Logger.WARN)
    
    def error(self, msg):
        self.log(msg, Logger.ERROR)

    def debug(self, msg):
        self.log(msg, Logger.DEBUG)

if __name__ == "__main__":
    log = Logger(Logger.ALL)
    log.info("Test info")
    log.warn("Test warn")
    log.error("Test error")
    log.debug("Test debug")
