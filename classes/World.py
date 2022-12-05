#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import floor, copysign
import os
import tempfile

import numpy as np
import pygame

from classes.Circuit import Circuit
from classes.Event import Event
from classes.Logger import Logger
from classes.Path import Path
from classes.Player import Player
from classes.Rect import Rect
from classes.SaveFile import SaveFile
from classes.Tile import Tile
from classes.Vec import Vec
from classes.tiles.Components import Electrical


AUTOSAVE_PATH = os.path.join(tempfile.gettempdir(), "packetman_autosave.dat")

class World:
    """World class holding world tiles and entities. Also processes physics."""

    WIDTH = 1
    HEIGHT = 1

    def __init__(self, game):
        """Initializes a World instance

        Arguments:
            game {Game} -- Game instance
        """

        self.game = game
        self.level_file = ""
        self.tiles = np.array([[Tile(world=self)]], dtype='object')
        self.entities = []
        self.player = Player(Vec(1, 1), world=self)
        self.entities.append(self.player)
        self.circuit = Circuit(self)
        self.chunks = {}
        self.default_ground_tile = Tile()
        self.file = None
    
    def physics(self, delta):
        """Simulates physics

        Arguments:
            delta {float} -- time elapsed in last frame in seconds
        """

        count = len(self.entities)
        for i, entity in enumerate(self.entities):
            entity.physics(delta)

            self.check_collisions(entity, delta)
            was_on_ground = entity.on_ground
            entity.on_ground = False
            
            # Check tiles a little bit below to see if entity is on the ground
            # TODO: refaire
            """
            if entity.vel.y <= 0:
                tiles_below = self.get_tiles_in_rect(
                    floor( entity.pos + Vec(0, -0.001) ),
                    floor( entity.pos + Vec(entity.box.w-0.001, -0.001) )
                ).flatten()

                tiles_below = list(filter(lambda t: t is not None and ((t.name and t.solid) or t.type == -1), tiles_below))
                
                if len(tiles_below) > 0 or entity.pos.y < 0.001:
                    if tiles_below and isinstance(entity, Player):
                        if entity.vel.x != 0:
                            if isinstance(tiles_below[0], Metal):
                                entity.play_step(material="metal")
                            else:
                                entity.play_step(material="not_metal")
                    entity.on_ground = True
                    entity.vel.x = 0"""
            
            if isinstance(entity, Player):
                entity.vel.x *= 0.95
                entity.vel.y *= 0.95
            
            # Check entity/entity collisions
            if i != count-1:
                for entity2 in self.entities[i+1:]:
                    if entity.box.overlaps(entity2.box):
                        event = Event(Event.COLLISION_ENTITY)
                        event.entities = [entity, entity2]
                        self.game.events.append(event)
            
            # Store current top-left and bottom-right corners
            # .copy() is very very important (read with indian accent)
            current_pos = [entity.pos.copy(), entity.pos + entity.SIZE]

            if entity.last_pos is None:
                entity.last_pos = current_pos
                in_tiles = self.get_tiles_in_rect(*current_pos).flatten()
                in_tiles = list(filter(lambda t: t.name, in_tiles))

                if in_tiles:
                    event = Event(Event.ENTER_TILE)
                    event.tiles = in_tiles
                    event.entity = entity
                    self.game.events.append(event)
            else:
                if floor(entity.last_pos[0]) == floor(current_pos[0]) and floor(entity.last_pos[1]) == floor(current_pos[1]):
                    entity.last_pos = current_pos
                    continue
                
                last_tiles = self.get_tiles_in_rect(*entity.last_pos).flatten()
                new_tiles = self.get_tiles_in_rect(*current_pos).flatten()
                enter_tiles = list(filter(lambda t: t not in last_tiles and t.name, new_tiles))
                exit_tiles = list(filter(lambda t: t not in new_tiles and t.name, last_tiles))

                if enter_tiles:
                    event = Event(Event.ENTER_TILE)
                    event.tiles = enter_tiles
                    event.entity = entity
                    self.game.events.append(event)
                
                if exit_tiles:
                    event = Event(Event.EXIT_TILE)
                    event.tiles = exit_tiles
                    event.entity = entity
                    self.game.events.append(event)
                
                entity.last_pos = current_pos
                    
    def get_tile(self, pos):
        """Returns the tile at a given position

        Arguments:
            pos {Vec} -- world coordinates of the tile

        Returns:
            Tile -- tile if pos is in the world, None otherwise
        """
        
        pos = floor(pos)
        
        c =self.get_chunk(pos//16)

        return c if c is None else c.get_tile(pos%16)
    
    def set_tile(self, tile, pos, ground=False):
        """Sets the tile at a given pos

        Arguments:
            tile {Tile} -- tile to set
            pos {Vec} -- world coordinates of the tile
        """
        reset_circuit = False
        
        pos = floor(pos)
        cpos = pos//16

        c = self.get_chunk(cpos.x, cpos.y, create=True)
        

        tile.pos = pos.copy()
        if not ground:
            if isinstance(self.get_tile(pos), Electrical) or isinstance(tile, Electrical):
                reset_circuit = True
            tile.world = self
        c.set_tile(tile, pos%16, ground)
        if not ground:
            self.update_tile(tile)
            if reset_circuit:
                self.game.editor.init_circuit_reset(tile)
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
        
        rtiles = []
        for y in range(topleft.y//16, bottomright.y//16 + 1):
            tilerow = None         
            for x in range(topleft.x//16, bottomright.x//16 + 1):
                relativetopleft = (max(topleft.x-x*16, 0), max(topleft.y-y*16,0))
                relativebottomright = (min(bottomright.x-x*16, 16), min(bottomright.y-y*16,16))
                c = self.get_chunk(x,y)
                if c is None:
                    s = (relativetopleft.x -relativebottomright.x,\
                        relativetopleft.y -relativebottomright.y)
                    tiles = np.full(shape=s, fill_value=None, dtype="object")
                else:
                    tiles = c.get_tiles_in_rect(relativetopleft, relativebottomright)
                tilerow.append(tiles)
            rtiles.append(np.concatenate(tilerow, axis=1))
        
        return np.concatenate(rtiles, axis =0)
    
    def get_entities_in_rect(self, topleft, bottomright, with_force_render=False):
        """Get entities overlapping with rectangle

        Returns a list of entities which overlap with the rectangle
        delimited by its top-left and bottom-right corners

        Arguments:
            topleft {Vec} -- top-left world coordinates of the rectangle
            bottomright {Vec} -- bottom-right world coordinates of the rectangle

        Keyword Arguments:
            with_force_render {bool} -- include entities with force_render=True

        Returns:
            list[Entity] -- array of entities
        """

        rect = Rect(topleft.x, topleft.y, bottomright.x-topleft.x, bottomright.y-topleft.y)

        return list(filter(lambda e: e.box.overlaps(rect) \
            or (with_force_render and e.force_render), self.entities))
    
    def check_collisions(self, entity, delta):
        """Checks and handles collisions for a given entity

        Arguments:
            entity {Entity} -- entity to process
            delta {float} -- time elapsed in last frame in seconds
        """

        collided = False
        collided_with = []

        #vel = entity.vel - entity.acc*delta
        if entity.last_pos is None: return
        vel = Vec(entity.pos.x-entity.last_pos[0].x, entity.pos.y-entity.last_pos[0].y)/delta
        v = vel.length

        #tl = Vec( int(entity.pos.x), int(entity.pos.y+entity.box.h))
        #br = Vec( int(entity.pos.x+entity.box.w), int(entity.pos.y))
        tl = Vec(int(entity.pos.x), int(entity.pos.y))
        br = Vec(int(entity.pos.x+entity.box.w), int(entity.pos.y+entity.box.h))

        tiles = self.get_tiles_in_rect(tl, br).flatten()
        
        # Order according to speed -> going right = sort from left to right
        #                             going down = sort from top to bottom
        tiles = sorted(tiles, key=lambda t: copysign(t.pos.x,vel.x)+copysign(t.pos.y,vel.y))

        for tile in tiles:
            solid_tile = ((tile.name and tile.solid) or tile.type == -1)
            overlaps = entity.box.overlaps(Rect(tile.pos.x, tile.pos.y, 1, 1))

            if solid_tile and overlaps:
                dx, dy = 0, 0
                if vel.x < 0:
                    dx = tile.pos.x+1 - entity.pos.x

                elif vel.x > 0:
                    dx = tile.pos.x - (entity.pos.x+entity.box.w)
                
                if vel.y < 0:
                    dy = tile.pos.y+1 - entity.pos.y

                elif vel.y > 0:
                    dy = tile.pos.y - (entity.pos.y+entity.box.h)
                

                d1 = abs(dx / vel.x) if vel.x != 0 else 0
                d2 = abs(dy / vel.y) if vel.y != 0 else 0

                d = min(d1, d2) if d1*d2 != 0 else max(d1, d2)
                
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
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if self.tiles[y, x] == 0:
                        self.tiles[y, x] = Tile(x, y, 0)
    
    def save(self, filename, autosave=False):
        """Saves the current level

        Arguments:
            filename {str} -- level name
        
        Keyword Arguments:
            autosave {bool} -- if True, world is saved in temporary folder (default: {False})
        """

        Logger.info(f"Saving as '{filename}'")
        
        if autosave:
            path = AUTOSAVE_PATH
        
        else:
            path = Path("levels", filename+".dat")
            
            if os.path.isfile(AUTOSAVE_PATH):
                os.remove(AUTOSAVE_PATH)

        self.file = SaveFile(path, self)
        self.file.save()
        
        Logger.info("Level saved successfully (maybe)")
        if not autosave:
            self.level_file = filename
            pygame.time.set_timer(pygame.USEREVENT+1, self.game.AUTOSAVE_FREQ*1000)

        self.game.events.append(Event(Event.WORLD_SAVED))

    def load(self, filename, autosave=False):
        """Loads a level

        Arguments:
            filename {str} -- level name
        
        Keyword Arguments:
            autosave {bool} -- wether to load from temporary autosave file (default: {False})
        """

        Logger.info(f"Loading level '{filename}'")
        
        if autosave:
            path = AUTOSAVE_PATH
        
        else:
            path = Path("levels", filename+".dat")
            
        self.file = SaveFile(path, self)
        self.file.load()
        
        Logger.info("Level loaded successfully (maybe)")
        self.level_file = filename

        self.game.camera.update()
        self.game.camera.update_visible_tiles()
        self.game.camera.update_visible_entities()

        self.game.events.append(Event(Event.WORLD_LOADED))

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

        self.modify_tilelistlen(pos + Vec(selection.shape[1], selection.shape[0]))

        for y in range(selection.shape[0]):
            for x in range(selection.shape[1]):
                t = selection[y, x]
                if not t.name and not place_empty:
                    continue
                newpos = pos + Vec(x, y)
                if newpos.x < 0 or newpos.y < 0:
                    continue
                self.set_tile(t, newpos)
    
    def update_tile(self, tile):
        """Updates a tile

        Updates the tile's neighbor count and of neighboring tiles

        Arguments:
            pos {Vec} -- world coordinates of the tile to update
        """
        
        offsets = [Vec(0, -1), Vec(1, 0), Vec(0, 1), Vec(-1, 0)]
        
        for i, off in enumerate(offsets):
            bit, bit2 = 2**i, 2**((i+2)%4)
            tile2 = self.get_tile(tile.pos+off)
            
            # t --> does tile want to connect to tile2?
            # t2 --> does tile2 want to connect to tile?
            
            # Verify that tile2 is not None
            t, t2 = False, False
            
            if not tile2:
                t2 = False
                if tile.CONNECTED:
                    t = True
            
            else:
                t = False
                if tile.CONNECT_TO:
                    t = tile.CONNECTED and isinstance(tile2, tile.CONNECT_TO)
                
                t2 = False
                if tile2.CONNECT_TO:
                    t2 = tile2.CONNECTED and isinstance(tile, tile2.CONNECT_TO)
            
            if t:
                tile.neighbors |= bit
            elif tile and tile.CONNECTED:
                tile.neighbors &= ~bit
            
            if t2:
                tile2.neighbors |= bit2
            elif tile2 and tile2.CONNECTED:
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
        entity.__del__()
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
        """Handle pygame events

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """
        interactive_tiles, interactive_entities = [], []
        if not self.game.config["edition"] and not self.game.paused:
            # Get the tiles around the player
            player = self.player
            
            pos1 = player.pos + Vec(-0.25, -0.25)
            pos2 = player.pos + player.SIZE + Vec(0.25, 0.25)
            
            tiles = self.get_tiles_in_rect(pos1, pos2)
            interactive_tiles = list(filter(lambda t: t.interactive, list(tiles.flatten())))
            entities = self.get_entities_in_rect(pos1, pos2)
            interactive_entities = list(filter(lambda e: e.interactive, entities))
            
            if self.game.settings.get("interaction_hint"):
                for entity in interactive_entities:
                    entity.interact_hint = True
                
                for tile in interactive_tiles:
                    tile.interact_hint = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if interactive_entities or interactive_tiles:
                        event = Event(Event.INTERACTION)
                        event.tiles = [interactive_tiles[0]] if interactive_tiles else []
                        event.entities = [interactive_entities[0]] if interactive_entities else []
                        self.game.events.append(event)
    
    def reset(self):
        """Resets the world"""
        
        for tile in self.tiles.flatten():
            tile.__del__()
        
        for entity in self.entities:
            entity.__del__()
        
        self.tiles = np.array([[Tile(world=self)]], dtype='object')
        self.entities = []
        self.player = Player(Vec(1, 1), world=self)
        self.entities.append(self.player)
        self.WIDTH = 1
        self.HEIGHT = 1
        self.game.camera.update_visible_tiles()
        self.game.camera.update_visible_entities()