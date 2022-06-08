#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.tiles.Terrain import Terrain

class Metal(Terrain):
    CONNECTED = False

class Aluminium(Metal):
    _TILES = {
        0: "aluminium"
    }
    I18N_KEY = "aluminium"

class Brass(Metal):
    _TILES = {
        0: "brass"
    }
    I18N_KEY = "brass"

class Copper(Metal):
    _TILES = {
        0: "copper"
    }
    I18N_KEY = "copper"

class Gold(Metal):
    _TILES = {
        0: "gold"
    }
    I18N_KEY = "gold"

class Iron(Metal):
    _TILES = {
        0: "iron"
    }
    I18N_KEY = "iron"

class Lead(Metal):
    _TILES = {
        0: "lead"
    }
    I18N_KEY = "lead"

class Zinc(Metal):
    _TILES = {
        0: "zinc"
    }
    I18N_KEY = "zinc"