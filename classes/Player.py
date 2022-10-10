#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from math import copysign

import pygame
from time import time

from classes.Entity import Entity
from classes.Event import Event, listener, on
from classes.SoundManager import SoundManager
from classes.Texture import Texture
from classes.Vec import Vec
from classes.tiles.DetectionTile import DetectionTile
from classes.entities.Bullet import Bullet

@listener
class Player(Entity):
    """Player class, extends Entity.
    
    Holds player-specific information and manages interactions
    """

    _ENTITIES = {
        0: "player"
    }
    I18N_KEY = "player"
    
    JUMP_SPEED = 14
    SIZE = Vec(0.75,1.5)
    
    speed = 5
    TIME_STEP = 0.3
    
    HB_LOGO = None
    HB_LOGO_SIZE = Vec(1,1)
    MAX_HEALTH = 3
    HB_SIZE = Vec(3, 1/4)
    HIT_SOUND = "entity.player.hit"
    BULLET_SPEED = 10
    RELOAD_TIME = 1  # in seconds

    mass = 1.5
    
    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        super().__init__(pos, vel, acc, type_, highlight, world)
        self.finishing_level = False
        self.last_step = time()
        if Player.HB_LOGO is None:
            Player.HB_LOGO = Texture("health_bar_logo")
        self.direction = Vec(1,0) # 1 if facing right, -1 if facing left
        self.last_shot = time()
    
    def move(self, direction):
        """Moves the player horizontally

        Arguments:
            direction {int} -- negative if moving left, positive if moving right
        """
        if direction.x == 0:
            self.direction.x = 0
            self.vel.x = 0
        else:
            self.vel.x = copysign(self.speed, direction.x)
            self.direction.x = direction.x
        
        if direction.y == 0:
            self.direction.y = 0
            self.vel.y = 0
        else:
            self.vel.y = copysign(self.speed, direction.y)
            self.direction.y = direction.y
        self.vel.y = copysign(self.speed, direction.y)
    
    def handle_events(self, events):
        """Handles events for the player

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """

        """for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if time() - self.last_shot > self.RELOAD_TIME:
                        self.shoot()"""
        
        if pygame.mouse.get_pressed()[0]:
            if time() - self.last_shot > self.RELOAD_TIME:
                self.shoot()
                
    
        move_vec = Vec()
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            move_vec.x += 1
        
        if keys[pygame.K_a]:
            move_vec.x -= 1
        
        if keys[pygame.K_w]:
            move_vec.y -= 1
    
        if keys[pygame.K_s]:
            move_vec.y += 1
        
        self.move(move_vec)
    
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
    
    def play_step(self, material=""):
        newtime = time()
        if newtime - self.last_step > self.TIME_STEP:
            SoundManager.play("entity.player.step_" + material)
            self.last_step = newtime

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
    
    def die(self):
        """Kills the player"""
        SoundManager.play("entity.player.death")
        self.world.load(self.world.level_file)
    
    def shoot(self):
        """Shoots a bullet"""
        pos = self.world.game.camera.screen_to_world(Vec(*pygame.mouse.get_pos()), round_ = False) - Bullet.SIZE/2
        SoundManager.play("entity.player.shoot")
        bullet_pos = (self.pos + self.SIZE/2) - Bullet.SIZE/2
        bullet_vel = (pos - bullet_pos).normalize() * self.BULLET_SPEED
        self.world.add_entity(Bullet(bullet_pos, bullet_vel, owner=self))
        self.last_shot = time()
