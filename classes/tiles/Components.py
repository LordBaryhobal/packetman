#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Tile import Tile

class Electrical(Tile):
    pass

class Input(Electrical):
    _tiles = {
        0: "input"
    }

class Output(Electrical):
    _tiles = {
        0: "output"
    }

class Plate(Input):
    _tiles = {
        0: "plate"
    }

class Button(Input):
    _tiles = {
        0: "button"
    }

class Wire(Electrical):
    _tiles = {
        0: "wire"
    }
    connected = True
    connect_strict = True

class Gate(Electrical):
    _tiles = {
        0: "gate"
    }