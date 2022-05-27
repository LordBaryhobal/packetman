#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np
from .Tile import Tile
from .Vec import Vec
from .Rect import Rect
from .Entity import Entity
from .Player import Player
from .Logger import Logger
from math import floor, copysign
import struct, pickle
import pygame
from .entities.Bullet import Bullet
from .entities.Hacker import Hacker
from .entities.Robot import Robot
from .entities.Drone import Drone

from .tiles.Bit import Bit
from .tiles.Terrain import *
from .tiles.Components import *
from .tiles.Metals import *
from .Event import Event

class World:
    """
    World class holding world tiles and entities. Also processes physics.
    """

    WIDTH = 1
    HEIGHT = 1
    

    def __init__(self, game):
        """Initializes a World instance

        Arguments:
            game {Game} -- Game instance
        """

        self.game = game
        self.tiles = np.array([[Tile()]], dtype='object')
        self.entities = []
        self.player = Player(Vec(1,1),world=self)
        self.entities.append(self.player)
    
    def physics(self, delta):
        """Simulates physics

        Arguments:
            delta {float} -- time elapsed in last frame in seconds
        """

        count = len(self.entities)
        for i, entity in enumerate(self.entities):
            entity.physics(delta)

            self.check_collisions(entity, delta)
            entity.on_ground = False
            
            if entity.vel.y <= 0:
                tiles_below = self.get_tiles_in_rect(
                    floor( entity.pos+Vec(0,-0.001) ),
                    floor( entity.pos+Vec(entity.box.w-0.001, -0.001) )
                ).flatten()

                tiles_below = list(filter(lambda t: t is not None and ((t.name and t.solid) or t.type == -1), tiles_below))
                
                if len(tiles_below) > 0 or entity.pos.y < 0.001:
                    entity.on_ground = True
                    entity.vel.x = 0
            
            if isinstance(entity, Player):
                entity.vel.x *= 0.95
            

            if i != count-1:
                for entity2 in self.entities[i+1:]:
                    if entity.box.overlaps(entity2.box):
                        event = Event(Event.COLLISION_ENTITY)
                        event.entities = [entity, entity2]
                        self.game.events.append(event)
    
    def get_tile(self, pos):
        """Returns the tile at a given position

        Arguments:
            pos {Vec} -- world coordinates of the tile

        Returns:
            Tile -- tile if pos is in the world, None otherwise
        """
        
        x, y = int(pos.x), int(pos.y)

        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return None
        
        return self.tiles[y, x]
    
    def set_tile(self, tile, pos):
        """Sets the tile at a given pos

        Arguments:
            tile {Tile} -- tile to set
            pos {Vec} -- world coordinates of the tile
        """

        if pos.x >= self.WIDTH or pos.y >= self.HEIGHT:
            self.modify_tilelistlen(pos)

        tile.pos = pos.copy()
        self.tiles[pos.y, pos.x] = tile
        self.update_tile(pos)

    def get_tiles_in_rect(self, topleft, bottomright):
        """Get tiles overlapping with rectangle

        Returns a 2D numpy array of tiles which overlap with the rectangle
        delimited by its top-left and bottom-right corners

        Arguments:
            topleft {Vec} -- top-left world coordinates of the rectangle
            bottomright {Vec} -- bottom-right world coordinates of the rectangle

        Returns:
            np.array[Tile] -- 2D array of tiles
        """

        topleft = floor(topleft)
        bottomright = floor(bottomright)
        self.modify_tilelistlen(bottomright.max(topleft))

        return self.tiles[bottomright.y:topleft.y+1, topleft.x:bottomright.x+1]
    
    def get_entities_in_rect(self, topleft, bottomright):
        """Get entities overlapping with rectangle

        Returns a list of entities which overlap with the rectangle
        delimited by its top-left and bottom-right corners

        Arguments:
            topleft {Vec} -- top-left world coordinates of the rectangle
            bottomright {Vec} -- bottom-right world coordinates of the rectangle

        Returns:
            list[Entity] -- array of entities
        """

        rect = Rect(topleft.x, bottomright.y, bottomright.x-topleft.x, topleft.y-bottomright.y)

        return list(filter(lambda e: e.box.overlaps(rect), self.entities))
    
    def check_collisions(self, entity, delta):
        """Checks and handles collisions for a given entity

        Arguments:
            entity {Entity} -- entity to process
            delta {float} -- time elapsed in last frame in seconds
        """

        collided = False
        collided_with = []

        vel = entity.vel - entity.acc*delta
        v = vel.length

        tl = Vec( int(entity.pos.x), int(entity.pos.y+entity.box.h))
        br = Vec( int(entity.pos.x+entity.box.w), int(entity.pos.y))

        tiles = self.get_tiles_in_rect(tl, br).flatten()

        if entity.pos.x < 0:
            tiles = np.append(tiles, Tile(floor(entity.pos.x), floor(entity.pos.y-1), -1))
            tiles = np.append(tiles, Tile(floor(entity.pos.x), floor(entity.pos.y), -1))
            tiles = np.append(tiles, Tile(floor(entity.pos.x), floor(entity.pos.y+1), -1))
        
        if entity.pos.y < 0:
            tiles = np.append(tiles, Tile(floor(entity.pos.x-1), floor(entity.pos.y), -1))
            tiles = np.append(tiles, Tile(floor(entity.pos.x), floor(entity.pos.y), -1))
            tiles = np.append(tiles, Tile(floor(entity.pos.x+1), floor(entity.pos.y), -1))
        
        # order according to speed -> going right = sort from left to right
        #                             going up = sort from botton to top
        tiles = sorted(tiles, key=lambda t: copysign(t.pos.x,vel.x)+copysign(t.pos.y,vel.y))

        for tile in tiles:
            if ((tile.name and tile.solid) or tile.type == -1) and entity.box.overlaps(Rect(tile.pos.x, tile.pos.y,1,1)):
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
                    
                    collided = True
                    collided_with.append(tile)

                entity.update()
        
        if collided:
            event = Event(Event.COLLISION_WORLD)
            event.entity = entity
            event.tiles = collided_with
            self.game.events.append(event)
        
    def modify_tilelistlen(self, pos):
        """Updates world size to include a given position

        Arguments:
            pos {Vec} -- world coordinates of position to include
        """

        xpad, ypad = 0,0
        pos = floor(pos)
        
        if pos.x >= self.WIDTH:
            xpad = pos.x - self.WIDTH + 1
            self.WIDTH = pos.x + 1
        
        if pos.y >= self.HEIGHT:
            ypad = pos.y - self.HEIGHT + 1
            self.HEIGHT = pos.y + 1
        
        if xpad != 0 or ypad != 0:
            self.tiles = np.pad(self.tiles, ((0, ypad),(0, xpad)), "constant", constant_values=0)
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    if self.tiles[y][x] == 0:
                        self.tiles[y][x] = Tile(x, y, 0)
    
    def save(self, filename):
        """Saves the current level

        Arguments:
            filename {str} -- level name
        """

        Logger.info(f"Saving as '{filename}'")
        buf_tiles = bytearray()
        buf_entities = bytearray()

        max_x, max_y = 0, 0

        Logger.info("Saving tiles")
        tiles = self.tiles.flatten()
        for tile in tiles:
            if not tile.name:
                continue
            
            buf_tile = bytearray()
            buf_tile.extend(struct.pack(">H", tile.type))
            buf_tile.extend(struct.pack(">H", tile.pos.x))
            buf_tile.extend(struct.pack(">H", tile.pos.y))
            buf_tile.extend(bytearray(tile.__class__.__qualname__, "utf-8"))
            buf_tile.append(0)
            attrs = tile.__dict__.copy()

            if hasattr(tile, "_no_save"):
                for a in tile._no_save:
                    del attrs[a]
            
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

            if hasattr(entity, "_no_save"):
                for a in entity._no_save:
                    del attrs[a]
            
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
        """Loads a level

        Arguments:
            filename {str} -- level name
        """

        Logger.info(f"Loading level '{filename}'")

        with open(f"./levels/{filename}.dat", "rb") as f:
            size_tiles = struct.unpack(">I", f.read(4))[0]
            size_entities = struct.unpack(">I", f.read(4))[0]
            self.WIDTH = struct.unpack(">H", f.read(2))[0]
            self.HEIGHT = struct.unpack(">H", f.read(2))[0]
            
            self.tiles = np.empty([self.HEIGHT, self.WIDTH], dtype='object')
            self.entities = []

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
                    if self.tiles[y, x] is None:
                        self.tiles[y, x] = Tile(x, y)
            
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
                entity = cls(pos=Vec(x, y), vel=Vec(vx, vy), type_=type_)

                for k, v in attrs.items():
                    setattr(entity, k, v)
                
                self.add_entity(entity)
                if cls == Player:
                    self.player = entity
        
        Logger.info("Level loaded successfully (maybe)")

        self.game.camera.update()
        self.game.camera.update_visible_tiles()
        self.game.camera.update_visible_entities()

        #Call twice to have correct physics
        self.game.clock.tick()
        self.game.clock.tick()
    
    def place_selection(self, selection, pos, place_empty=False):
        """Places tiles from a selection in the world

        Arguments:
            selection {np.array[Tile]} -- 2D array of tiles to place
            pos {Vec} -- bottom-left corner's world coordinates

        Keyword Arguments:
            place_empty {bool} -- wether to override if placing empty tiles (default: {False})
        """

        self.modify_tilelistlen(pos+Vec(len(selection[0]), len(selection)))

        for y in range(len(selection)):
            for x in range(len(selection[0])):
                t = selection[y][x]
                if not t.name and not place_empty:
                    continue
                
                self.set_tile(t, pos+Vec(x, y))
    
    def update_tile(self, pos):
        """Updates a tile

        Updates the tile's neighbor count and of neighboring tiles

        Arguments:
            pos {Vec} -- world coordinates of the tile to update
        """
        
        tile = self.get_tile(pos)
        offsets = [Vec(0,1), Vec(1,0), Vec(0,-1), Vec(-1,0)]
        
        for i, off in enumerate(offsets):
            bit, bit2 = 2**i, 2**((i+2)%4)
            tile2 = self.get_tile(pos+off)

            t = not tile or tile.name
            t2 = not tile2 or tile2.name

            if t:
                if t2:
                    if tile2:
                        tile2.neighbors |= bit2
                    
                    if tile:
                        tile.neighbors |= bit
                elif tile:
                    tile.neighbors &= ~bit
            elif tile2:
                tile2.neighbors &= ~bit2
            
            if tile2:
                tile2.on_update()
        
        if tile:
            tile.on_update()
    
    def remove_entity(self, entity):
        """Removes an entity

        Arguments:
            entity {Entity} -- entity to remove
        """
        
        self.entities.remove(entity)
        del entity
        self.game.camera.update_visible_entities()
    
    def add_entity(self, entity):
        """Adds an entity

        Arguments:
            entity {Entity} -- entity to add
        """
        
        entity.world = self
        self.entities.append(entity)
        self.game.camera.update_visible_entities()
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not self.game.config["edition"] and not self.game.paused:
                    #get the tile around the player
                    player = self.player
                    player_pos = player.pos + player.SIZE/2
                    tiles = self.get_tiles_in_rect(player_pos+Vec(-1,1), player_pos + Vec(1,-1))
                    interactive_tiles = list(filter(lambda t: t.INTERACTIVE, list(tiles.flatten())))
                    
                    entities = self.get_entities_in_rect(player_pos+Vec(-1,1), player_pos + Vec(1,-1))
                    interactive_entities = list(filter(lambda e: e.INTERACTIVE, entities))
                    if len(interactive_entities) > 0 or len(interactive_tiles)>0:
                        event = Event(Event.INTERACTION)
                        event.tiles = interactive_tiles
                        event.entities = interactive_entities
                        self.game.events.append(event)