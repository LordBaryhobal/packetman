#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.tiles.Terrain import Terrain

class Metal(Terrain):
    CONNECTED = False

class Aluminium(Metal):
    _TILES = {
        0: "aluminium"
    }

class Brass(Metal):
    _TILES = {
        0: "brass"
    }

class Copper(Metal):
    _TILES = {
        0: "copper"
    }

class Gold(Metal):
    _TILES = {
        0: "gold"
    }

class Iron(Metal):
    _TILES = {
        0: "iron"
    }

class Lead(Metal):
    _TILES = {
        0: "lead"
    }

class Zinc(Metal):
    _TILES = {
        0: "zinc"
    }