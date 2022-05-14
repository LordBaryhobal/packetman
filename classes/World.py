#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np
from .Tile import Tile
from .Entity import Entity
from .Vec import Vec
from .Rect import Rect

class World:
    """
    World class holding world tiles and entities. Also processes physics.
    """

    WIDTH = 20
    HEIGHT = 20
    

    def __init__(self):
        self.create_tilelist()
        self.entities = []

        self.entities.append(Entity(Vec(5,5)))
        
    def create_tilelist(self):
        arr = np.random.randint(0,8,(self.HEIGHT,self.WIDTH))
        self.tiles = np.empty([self.HEIGHT,self.WIDTH], dtype='object')
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self.tiles[y][x] = Tile(x,y,arr[y][x])
    
    def physics(self, delta):
        pass
    
    def get_tiles_in_rect(self, topleft, bottomright):
        return self.tiles[bottomright.y:topleft.y+1, topleft.x:bottomright.x+1]
    
    def get_entities_in_rect(self, topleft, bottomright):
        rect = Rect(topleft.x, bottomright.y, bottomright.x-topleft.x, topleft.y-bottomright.y)

        return list(filter(lambda e: e.box.overlaps(rect), self.entities))