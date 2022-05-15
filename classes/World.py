#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np
from .Tile import Tile
from .Vec import Vec
from .Rect import Rect
from .Player import Player
from .Logger import Logger
from math import floor
import struct, pickle

class World:
    """
    World class holding world tiles and entities. Also processes physics.
    """

    WIDTH = 1
    HEIGHT = 1
    

    def __init__(self):
        self.tiles = np.array([[Tile()]], dtype='object')
        self.entities = []
        self.player = Player(Vec(1,1))
        self.entities.append(self.player)
    
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
        Logger.info(f"Saving as '{filename}'")
        buf_tiles = bytearray()
        buf_entities = bytearray()

        max_x, max_y = 0, 0

        Logger.info("Saving tiles")
        tiles = self.tiles.flatten()
        for tile in tiles:
            if tile.type == 0:
                continue
            
            buf_tile = bytearray()
            buf_tile.extend(struct.pack(">H", tile.type))
            buf_tile.extend(struct.pack(">H", tile.pos.x))
            buf_tile.extend(struct.pack(">H", tile.pos.y))
            buf_tile.extend(bytearray(tile.__class__.__qualname__, "utf-8"))
            buf_tile.append(0)
            attrs = tile.__dict__.copy()
            del attrs["type"]
            del attrs["pos"]
            attrs = pickle.dumps(attrs)
            buf_tile.extend(attrs)

            buf_tiles.extend(struct.pack(">H", len(buf_tile)))
            buf_tiles += buf_tile

            max_x = max(max_x, tile.pos.x)
            max_y = max(max_y, tile.pos.y)
        
        entities = self.entities

        Logger.info("Saving entities")
        for entity in entities:
            buf_entity = bytearray()
            buf_entity.extend(struct.pack(">H", entity.type))
            buf_entity.extend(struct.pack(">f", entity.pos.x))
            buf_entity.extend(struct.pack(">f", entity.pos.y))
            buf_entity.extend(struct.pack(">f", entity.vel.x))
            buf_entity.extend(struct.pack(">f", entity.vel.y))
            buf_entity.extend(bytearray(entity.__class__.__qualname__, "utf-8"))
            buf_entity.append(0)
            attrs = entity.__dict__.copy()
            del attrs["type"]
            del attrs["pos"]
            del attrs["vel"]
            del attrs["acc"]
            del attrs["box"]
            attrs = pickle.dumps(attrs)
            buf_entity.extend(attrs)

            buf_entities.extend(struct.pack(">H", len(buf_entity)))
            buf_entities += buf_entity
        
        Logger.info("Writing to file")
        with open("./levels/"+filename+".dat", "wb") as f:
            f.write(struct.pack(">I", len(buf_tiles) ))
            f.write(struct.pack(">I", len(buf_entities) ))
            f.write(struct.pack(">H", max_x+1))
            f.write(struct.pack(">H", max_y+1))
            f.write(buf_tiles)
            f.write(buf_entities)
        
        Logger.info("Level saved successfully (maybe)")

    def load(self, filename):
        Logger.info(f"Loading level '{filename}'")

        with open(f"./levels/{filename}.dat", "rb") as f:
            size_tiles = struct.unpack(">I", f.read(4))[0]
            size_entities = struct.unpack(">I", f.read(4))[0]
            self.WIDTH = struct.unpack(">H", f.read(2))[0]
            self.HEIGHT = struct.unpack(">H", f.read(2))[0]
            
            self.tiles = np.empty([self.HEIGHT,self.WIDTH], dtype='object')

            Logger.info("Loading tiles")
            while f.tell() < size_tiles+12:
                size = struct.unpack(">H", f.read(2))[0]
                type_ = struct.unpack(">H", f.read(2))[0]
                x = struct.unpack(">H", f.read(2))[0]
                y = struct.unpack(">H", f.read(2))[0]

                cls = b""

                while True:
                    c = f.read(1)
                    if c == b"\0": break
                    cls += c

                attrs = pickle.loads(f.read(size - len(cls) - 7))

                cls = globals()[str(cls, "utf-8")]
                tile = cls(x, y, type_)
                for k, v in attrs.items():
                    setattr(tile, k, v)
                
                self.tiles[y, x] = tile
            
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if self.tiles[y,x] is None:
                        self.tiles[y,x] = Tile(x, y)
            
            Logger.info("Loading entities")
            while f.tell() < size_entities+size_tiles+12:
                size = struct.unpack(">H", f.read(2))[0]
                type_ = struct.unpack(">H", f.read(2))[0]
                x = struct.unpack(">f", f.read(4))[0]
                y = struct.unpack(">f", f.read(4))[0]
                vx = struct.unpack(">f", f.read(4))[0]
                vy = struct.unpack(">f", f.read(4))[0]

                cls = b""

                while True:
                    c = f.read(1)
                    if c == b"\0": break
                    cls += c
                
                attrs = pickle.loads(f.read(size - len(cls) - 19))

                cls = globals()[str(cls, "utf-8")]
                entity = cls(pos=Vec(x,y), vel=Vec(vx, vy), type_=type_)

                for k, v in attrs.items():
                    setattr(entity, k, v)
                
                self.entities.append(entity)
                if cls == Player:
                    self.player = entity
        
        Logger.info("Level loaded successfully (maybe)")
    
    def place_selection(self,selection,pos,place_empty=False):
        self.modify_tilelistlen(pos+Vec(len(selection[0]),len(selection)))
        for y in range(len(selection)):
            for x in range(len(selection[0])):
                t = selection[y][x]
                if t.type == 0 and not place_empty:
                    continue
                t.pos.x = pos.x + x
                t.pos.y = pos.y + y
                self.tiles[pos.y+y][pos.x+x] = t
