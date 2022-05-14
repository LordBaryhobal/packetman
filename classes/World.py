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

    WIDTH = 8
    HEIGHT = 8
    

    def __init__(self):
        self.create_tilelist()
        self.entities = []

        self.entities.append(Entity(Vec(1.5,5), vel=Vec(1)))
        
    def create_tilelist(self):
        #arr = np.random.randint(0,8,(self.HEIGHT,self.WIDTH))
        arr = np.array([
            [1,2,1,2,1,2,1,2],
            [3,0,0,0,0,0,0,0],
            [4,0,0,0,0,0,0,0],
            [3,0,0,0,0,0,0,0],
            [4,0,0,0,0,0,0,0],
            [3,0,0,0,0,0,0,0],
            [4,0,0,0,0,0,0,0],
            [3,0,0,0,0,0,0,0]
        ])

        self.tiles = np.empty([self.HEIGHT,self.WIDTH], dtype='object')
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self.tiles[y][x] = Tile(x,y,arr[y][x])
    
    def physics(self, delta):
        for entity in self.entities:
            entity.physics(delta)

            self.check_collisions(entity, delta)
    
    def get_tiles_in_rect(self, topleft, bottomright):
        self.modify_tilelistlen(bottomright.max(topleft))
        return self.tiles[bottomright.y:topleft.y+1, topleft.x:bottomright.x+1]
    
    def get_entities_in_rect(self, topleft, bottomright):
        rect = Rect(topleft.x, bottomright.y, bottomright.x-topleft.x, topleft.y-bottomright.y)

        return list(filter(lambda e: e.box.overlaps(rect), self.entities))
    
    def check_collisions(self, entity, delta):
        v = entity.vel.length

        tl = Vec( int(entity.pos.x), int(entity.pos.y+entity.box.h))
        br = Vec( int(entity.pos.x+entity.box.w), int(entity.pos.y))

        tiles = self.get_tiles_in_rect(tl,br).flatten()

        for tile in tiles:
            if tile.type != 0 and tile.solid:
                print(tile.coo)
                dx, dy = 0, 0
                if entity.vel.x < 0:
                    dx = tile.coo.x - entity.pos.x
                elif entity.vel.x > 0:
                    dx = entity.pos.x+entity.box.w - tile.coo.x
                
                if entity.vel.y < 0:
                    dy = tile.coo.y - entity.pos.y + entity.box.h
                elif entity.vel.y > 0:
                    dy = entity.pos.y - tile.coo.y + 1

                d1 = -v * dx / entity.vel.x if entity.vel.x != 0 else 0
                d2 = -v * dy / entity.vel.y if entity.vel.y != 0 else 0
                print(d1, d2)
                print(entity.vel)

                d = min(d1, d2) if d1*d2 != 0 else max(d1, d2)
                
                entity.pos -= entity.vel.normalize()*d
                
                if d != 0:
                    if d1 < d2:
                        entity.vel.x = 0
                    else:
                        entity.vel.y = 0
                #input()
        
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
