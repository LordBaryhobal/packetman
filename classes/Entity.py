#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Copyable import Copyable
from classes.Rect import Rect
from classes.Texture import Texture
from classes.Utility import import_class
from classes.Vec import Vec

ENTITIES = {
    "Bullet": "classes.entities.Bullet",
    "Drone": "classes.entities.Drone",
    "Hacker": "classes.entities.Hacker",
    "Player": "classes.Player",
    "Robot": "classes.entities.Robot",
    "Trigger": "classes.entities.Triggers",
    "PlayerTrigger": "classes.entities.Triggers",
    "TileTrigger": "classes.entities.Triggers"
}

class Entity(Copyable):
    """Non grid-locked entity, either alive or not
    
    Subject to physics
    """
    
    _no_save = ["type", "pos", "vel", "acc", "box", "highlight", "texture", "world", "interact_hint", "last_pos"]
    _ENTITIES = {
        0: None
    }
    I18N_KEY = ""
    
    HINT_SIZE = Vec(0.3,0.3)
    HINT_TEXTURE = None
    SIZE = Vec(0.5,0.5)
    
    force_render = False
    gravity = True
    interactive = False
    

    def __init__(self, pos=None, vel=None, acc=None, type_=None, highlight=False, world=None):
        """Initializes an Entity instance

        Keyword Arguments:
            pos {Vec} -- position of entity in world coordinates (default: {None})
            vel {Vec} -- velocity of entity in world units (default: {None})
            acc {Vec} -- acceleration of entity in world units (default: {None})
            type_ {int} -- entity type (default: {None})
            highlight {bool} -- whether to highlight the entity (default: {False})
            world {World} -- world the entity is in (default: {None})
        """

        if pos is None: pos = Vec()
        if vel is None: vel = Vec()
        if acc is None: acc = Vec()
        if type_ is None: type_ = 0

        self.pos = pos
        self.vel = vel
        self.acc = acc

        self.type = type_
        self.name = self._ENTITIES[self.type]
        self.texture = Texture(self.name, 0) if self.name else None

        self.box = Rect(self.pos.x, self.pos.y, self.SIZE.x, self.SIZE.y)

        self.on_ground = False
        
        self.highlight = highlight
        self.world = world
        self.last_pos = None

        self.interact_hint = False
        
        if Entity.HINT_TEXTURE is None:
            Entity.HINT_TEXTURE = Texture("interaction_hint", 0, width=64, height=64)
    
    def __del__(self, *args, **kwargs):
        pass

    def get_cls(cls):
        """Get class from class name

        Arguments:
            cls {str} -- class name

        Returns:
            class -- corresponding class
        """
        
        return import_class(ENTITIES, cls)

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

        if dimensions is None:
            dimensions = self.SIZE
        
        rect = (pos.x, pos.y-self.box.h*size, self.box.w*size, self.box.h*size)

        if self.texture:
            self.texture.render(surface, pos, size, dimensions, hasattr(self, "direction") and self.direction == -1)
        else:
            pygame.draw.rect(surface, (100,100,100), rect)
        
        if self.highlight:
            pygame.draw.rect(hud_surf, (255,255,255), rect, 2)
        
        if self.interact_hint:
            hintpos = pos + Vec((self.SIZE.x - self.HINT_SIZE.x)*size/2, self.HINT_SIZE.y*size)
            self.HINT_TEXTURE.render(hud_surf, hintpos, size, self.HINT_SIZE)
            self.interact_hint = False

    def physics(self, delta):
        """Simulates physics

        Arguments:
            delta {float} -- time elapsed in last frame in seconds
        """

        if self.gravity:
            self.acc = Vec(0, -20)

        self.pos += self.vel * delta
        self.vel += self.acc * delta
        
        self.pos = round(self.pos, 6)
        self.vel = round(self.vel, 6)
        self.acc = round(self.acc, 6)

        self.update()
    
    def update(self):
        """Updates the entity's hitbox"""
        
        self.box.x = self.pos.x
        self.box.y = self.pos.y
    
    def handle_events(self, events):
        """Handles events

        Arguments:
            events {list} -- list of events
        """
        pass
    
    def update_texture(self):
        """Updates the entity's texture"""
        
        self.name = self._ENTITIES[self.type]
        self.texture = Texture(self.name, 0) if self.name else None

    def get_i18n_key(self):
        if self.name:
            return "entity."+self.__class__.I18N_KEY
        
        return ""