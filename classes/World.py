#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from scipy import isin
import numpy as np
from .Tile import Tile
from .Entity import Entity
from .Vec import Vec
from .Rect import Rect
from .Player import Player
from math import floor

class World:
    """
    World class holding world tiles and entities. Also processes physics.
    """

    WIDTH = 8
    HEIGHT = 8
    

    def __init__(self):
        self.create_tilelist()
        self.entities = []
        self.player = Player(Vec(1,1))
        self.entities.append(self.player)

        self.entities.append(Entity(Vec(1.5,1), vel=Vec(1,5)))
        
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
            entity.on_ground = False
            
            if entity.vel.y <= 0:
                tiles_below = self.get_tiles_in_rect(
                    floor( entity.pos+Vec(0,-0.001) ),
                    floor( entity.pos+Vec(entity.box.w, -0.001) )
                ).flatten()

                tiles_below = list(filter(lambda t: t is not None and t.type != 0 and t.solid, tiles_below))
                
                if len(tiles_below) > 0:
                    entity.on_ground = True
                    entity.vel.x = 0
    
    def get_tile(self, pos):
        """Get tile at pos
        @param pos: coordinates of the tile as a Vec
        @return Tile instance, None if outside of the world
        """
        x, y = int(pos.x), int(pos.y)

        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return None
        
        return self.tiles[y, x]

    def get_tiles_in_rect(self, topleft, bottomright):
        self.modify_tilelistlen(bottomright.max(topleft))
        return self.tiles[bottomright.y:topleft.y+1, topleft.x:bottomright.x+1]
    
    def get_entities_in_rect(self, topleft, bottomright):
        rect = Rect(topleft.x, bottomright.y, bottomright.x-topleft.x, topleft.y-bottomright.y)

        return list(filter(lambda e: e.box.overlaps(rect), self.entities))
    
    def check_collisions(self, entity, delta):
        vel = entity.vel - entity.acc*delta
        v = vel.length

        tl = Vec( int(entity.pos.x), int(entity.pos.y+entity.box.h))
        br = Vec( int(entity.pos.x+entity.box.w), int(entity.pos.y))

        tiles = self.get_tiles_in_rect(tl,br).flatten()

        for tile in tiles:
            if tile.type != 0 and tile.solid and entity.box.overlaps(Rect(tile.pos.x,tile.pos.y,1,1)):
                dx, dy = 0, 0
                if vel.x < 0:
                    dx = tile.pos.x+1 - entity.pos.x

                elif vel.x > 0:
                    dx = tile.pos.x - (entity.pos.x+entity.box.w)
                
                if vel.y < 0:
                    dy = tile.pos.y+1 - entity.pos.y

                elif vel.y > 0:
                    dy = tile.pos.y - (entity.pos.y+entity.box.h)
                

                d1 = abs(v * dx / vel.x) if vel.x != 0 else 0
                d2 = abs(v * dy / vel.y) if vel.y != 0 else 0

                d = min(d1, d2) if d1*d2 != 0 else max(d1, d2)
                
                #entity.pos -= vel.normalize()*d
                
                if d != 0:
                    if d1 != 0 and (d2 == 0 or d1 < d2):
                        entity.vel.x = 0
                        entity.pos.x += dx
                    else:
                        entity.vel.y = 0
                        entity.pos.y += dy
                
                entity.update()
        
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
    
    def place_selection(self,selection,pos,place_empty=False):
        for y in range(len(selection)):
            for x in range(len(selection[0])):
                t = selection[y][x]
                if t.type == 0 and not place_empty:
                    continue
                t.pos.x = pos.x + x
                t.pos.y = pos.y + y
                self.tiles[pos.y+y][pos.x+x] = t
