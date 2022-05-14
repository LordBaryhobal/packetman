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

    WIDTH = 1
    HEIGHT = 1
    

    def __init__(self):
        self.create_tilelist()
        self.entities = []

        #self.entities.append(Entity(Vec(5,5)))
        
    def create_tilelist(self):
        arr = np.zeros((self.HEIGHT,self.WIDTH))
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
    
    def set_tile(self, pos, type_):
        if pos.x >= self.WIDTH or pos.y >= self.HEIGHT:
            self.modify_tilelistlen(pos)
        self.tiles[pos.y][pos.x] = Tile(pos.x,pos.y,type_)
        
    def modify_tilelistlen(self,pos):
        xpad,ypad = 0,0
        
        if pos.x >= self.WIDTH:
            xpad = pos.x - self.WIDTH + 1
            self.WIDTH = pos.x + 1
        if pos.y >= self.HEIGHT:
            ypad = pos.y - self.HEIGHT + 1
            self.HEIGHT = pos.y + 1
        if xpad != 0 or ypad != 0:
            self.tiles = np.pad(self.tiles, ((0,ypad),(0,xpad)), "constant", constant_values=0)
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    if self.tiles[y][x] == 0:
                        self.tiles[y][x] = Tile(x,y,0)
    
    def save(self, filename):
        pass
