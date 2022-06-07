#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import copysign

import pygame

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.SoundManager import SoundManager
from classes.Texture import Texture
from classes.Vec import Vec
from classes.Event import Event, listener, on
from classes.tiles.DetectionTile import DetectionTile

@listener
class Player(Entity):
    """Player class, extends Entity.
    
    Holds player-specific information and manages interactions
    """

    _ENTITIES = {
        0: "player"
    }
    I18N_KEY = "player"
    
    JUMP_SPEED = 7
    SIZE = Vec(0.8,0.8)
    
    speed = 4
    
    HB_LOGO = None
    HB_LOGO_SIZE = Vec(1,1)
    MAX_HEALTH = 10
    HB_SIZE = Vec(3, 1/4)
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.finishing_level = False
        self.health = self.MAX_HEALTH
        if Player.HB_LOGO is None:
            Player.HB_LOGO = Texture("health_bar_logo")
        self.direction = 1 # 1 if facing right, -1 if facing left
    
    def jump(self):
        """Makes the player jump if on the ground"""

        if self.on_ground:
            self.vel.y = self.JUMP_SPEED
            SoundManager.play("entity.player.jump")
    
    def move(self, direction):
        """Moves the player horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """

        self.vel.x = copysign(self.speed, direction)
    
    def handle_events(self, events):
        """Handles events for the player

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.move(1)
            self.direction = 1
        
        if keys[pygame.K_a]:
            self.move(-1)
            self.direction = -1
    
    @on(Event.ENTER_TILE)
    def on_enter_tile(self, event):
        if event.entity is self:
            for tile in event.tiles:
                if isinstance(tile, DetectionTile):
                    if self.on_ground:
                        self.world.game.finish_level()
                    else:
                        self.finishing_level = True
                    break
    
    @on(Event.HIT_GROUND)
    def on_hit_ground(self, event):
        if event.entity is self:
            SoundManager.play("entity.player.hit_ground")
            if self.finishing_level:
                self.finishing_level = False
                self.world.game.finish_level()

    def render(self, surface, hud_surf, pos, size, dimensions=None):
        """Renders the entity

        Renders the entity on a given surface at a given position and scale

        Arguments:
            surface {pygame.Surface} -- surface to render the entity on
            hud_surf {pygame.Surface} -- surface to render the hud elements on
            pos {Vec} -- pixel coordinates where to render on the surface
            size {int} -- size of a tile in pixels
            dimension {Vec} -- dimensions of the object in tiles (default: {None})
        """

        super().render(surface, hud_surf, pos, size, dimensions)
        if not self.world.game.config["edition"]:
            self.draw_healt_bar(hud_surf, size)
        
    def draw_healt_bar(self, surf, size):
        self.HB_LOGO.render(surf, Vec(0,self.HB_LOGO_SIZE.y*size), size, self.HB_LOGO_SIZE)
        color = (255, 0, 0) if self.health <= 3 else (0, 0, 255)
        pygame.draw.rect(surf, (100, 100, 100), (self.HB_LOGO_SIZE.x*size, self.HB_LOGO_SIZE.y*size*(1-self.HB_SIZE.y)/2, \
            size*self.HB_SIZE.x, self.HB_LOGO_SIZE.y*size*self.HB_SIZE.y), 0)
        
        pygame.draw.rect(surf, color, (self.HB_LOGO_SIZE.x*size, self.HB_LOGO_SIZE.y*size*(1-self.HB_SIZE.y)/2, \
            (self.MAX_HEALTH-self.health)/self.MAX_HEALTH*size*self.HB_SIZE.x, self.HB_LOGO_SIZE.y*size*self.HB_SIZE.y), 0)
    
    def get_hit(self, damage):
        """Reduces the player's health by a given amount

        Arguments:
            damage {int} -- amount of damage to deal to the player
        """

        self.health = max(self.health - damage, 0)
        if self.health <= 0:
            self.die()
    
    def die(self):
        """Kills the player"""

        self.world.load(self.world.level_file)