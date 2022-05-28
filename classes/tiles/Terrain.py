#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Tile import Tile

class Terrain(Tile):
    """Static tile used for world building and decoration"""

    _TILES = {
        0: "metal"
    }
    CONNECTED = False

    solid = True
    

class Insulator(Terrain):
    _TILES = {
        0: "insulator"
    }

class Plastic(Terrain):
    _TILES = {
        0: "plastic"
    }

class ThermalConductor(Terrain):
    _TILES = {
        0: "thermal_conductor"
    }