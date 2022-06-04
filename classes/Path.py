#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import os

class Path(str):
    """Subclass of str which builds paths relative to game directory"""
    
    def __new__(cls, *elmts):
        path = os.path.join(os.getcwd(), *elmts)
        return str.__new__(cls, path)