#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Terrain import Terrain

class Metal(Terrain):
    connected = False

class Aluminium(Metal):
    _tiles = {
        0: "aluminium"
    }
class Brass(Metal):
    _tiles = {
        0: "brass"
    }
class Copper(Metal):
    _tiles = {
        0: "copper"
    }
class Gold(Metal):
    _tiles = {
        0: "gold"
    }
class Iron(Metal):
    _tiles = {
        0: "iron"
    }
class Lead(Metal):
    _tiles = {
        0: "lead"
    }
class Zinc(Metal):
    _tiles = {
        0: "zinc"
    }