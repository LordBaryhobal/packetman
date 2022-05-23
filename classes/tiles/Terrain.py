#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Tile import Tile

class Terrain(Tile):
    solid = True

    _tiles = {
        0: "metal"
    }