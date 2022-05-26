#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Entity import Entity
from .Tile import Tile
from .Vec import Vec
from .Logger import Logger
from .Animation import Animation
import pygame

from .tiles.Bit import Bit
from .tiles.Terrain import *
from .tiles.Components import *
from .tiles.Metals import *

from .entities.Bullet import Bullet
from .entities.Hacker import Hacker
from .entities.Robot import Robot

class Hud:
    """Class to display editor hud"""

    MARGIN = 20
    SLOT_COL = (150,150,150)
    SLOT_INDICATOR_COL = (200,80,80)

    def __init__(self, game):
        """Initializes a Hud instance

        Arguments:
            game {Game} -- game instance
        """

        self.game = game
        self.slot = 0
        self.hotbar = 0
        self.hotbars = [
            #[Tile(type_=1), Tile(type_=2), Tile(type_=3), Tile(type_=4), Tile(type_=5), Tile(type_=7), Tile(type_=8)]
            #[Terrain(type_=0), Bit(type_=0), Bit(type_=0)]
            [Aluminium(), Brass(), Copper(), Gold(), Iron(), Lead(), Zinc()],
            [Insulator(), Plastic(), ThermalConductor(), Plate(), Button(), Wire(), Gate()],
            [Entity(type_=0),Bullet(type_=0),Hacker(type_=0),Robot(type_=0)]
        ]
        #self.hotbars[0][2].value = 1
        #self.hotbars[0][2].on_update()

        self.sb_opacity_anim = None
        self.sb_opacity = 0
    
    def get_type(self):
        """Returns the selected tile/entity type

        Returns:
            class -- class of selected type
            int -- selected type
        """

        if self.hotbar < len(self.hotbars) and self.slot < len(self.hotbars[self.hotbar]):
            selected = self.hotbars[self.hotbar][self.slot]
            return (selected.__class__, selected.type, selected)
        
        return (Tile, 0, Tile(type_=0))

    def render(self, surface):
        """Renders the hud

        Arguments:
            surface {pygame.Surface} -- surface to render the hud on
        """

        # Hotbar
        hotbar_pos = self.game.config["gui"]["editor"]["hotbar_pos"]

        WIDTH, HEIGHT = surface.get_width(), surface.get_height()
        hotbar_length = 0.5*WIDTH
        slot_size = 0.1*hotbar_length

        if hotbar_pos == 0:
            ox, oy = WIDTH/2 - hotbar_length/2, HEIGHT-slot_size-self.MARGIN
        else:
            ox, oy = self.MARGIN, HEIGHT/2 - hotbar_length/2
        
        gap = (hotbar_length-9*slot_size)/10
        margin = slot_size*0.1

        for i in range(9):
            if hotbar_pos == 0:
                x, y = ox + gap + i*(slot_size+gap), oy
            else:
                x, y = ox, oy + gap + i*(slot_size+gap)
            
            pygame.draw.rect(surface, self.SLOT_COL, [x, y, slot_size, slot_size])

            if self.hotbar < len(self.hotbars) and i < len(self.hotbars[self.hotbar]):
                #dimension = Vec(1,1) because we want the entity to be scaled at 1x1 tile
                self.hotbars[self.hotbar][i].render(surface, Vec(x+margin, y+slot_size-margin), slot_size*0.8, dimensions=Vec(1,1))
        
        if hotbar_pos == 0:
            w, h = slot_size*0.75, self.MARGIN/4
            pygame.draw.rect(surface, self.SLOT_INDICATOR_COL, [ox + gap + self.slot*(slot_size+gap) + slot_size*0.5 - w/2, HEIGHT-self.MARGIN*0.75, w, h])
        
        else:
            w, h = self.MARGIN/4, slot_size*0.75
            pygame.draw.rect(surface, self.SLOT_INDICATOR_COL, [self.MARGIN*0.75-w, oy + gap + self.slot*(slot_size+gap) + slot_size*0.5 - h/2, w, h])


        # Scrollbars
        if self.game.config["gui"]["editor"]["scrollbars"]:
            world_w = self.game.world.WIDTH*self.game.camera.tilesize
            world_h = self.game.world.HEIGHT*self.game.camera.tilesize

            pos_x, pos_y = self.game.camera.pos.x, self.game.camera.pos.y
            
            rx = pos_x/(world_w - self.game.WIDTH)
            ry = pos_y/(world_h - self.game.HEIGHT)
            rx, ry = max(0, min(1, rx)), max(0, min(1, ry))
            
            x_thumb_w = min(1, self.game.WIDTH/world_w) * self.game.WIDTH
            y_thumb_h = min(1, self.game.HEIGHT/world_h) * self.game.HEIGHT

            x = rx*(self.game.WIDTH-x_thumb_w)
            y = (1-ry)*(self.game.HEIGHT-y_thumb_h)

            pygame.draw.rect(surface, (255,255,255, self.sb_opacity), [x, HEIGHT-5, x_thumb_w,5])
            pygame.draw.rect(surface, (255,255,255, self.sb_opacity), [0, y, 5, y_thumb_h])
    
    def set_hotbar(self, i):
        """Sets which hotbar is currently selected

        Arguments:
            i {int} -- index of the hotbar to select
        """
        
        if i < len(self.hotbars):
            self.hotbar = i
        
        else:
            Logger.warn(f"Tried to set hotbar of index {i} but only {len(self.hotbars)} are defined")
    
    def show_scrollbars(self):
        """Shows the panning scrollbars"""

        if not self.sb_opacity_anim is None:
            self.sb_opacity_anim.finished = True
        
        self.sb_opacity_anim = None
        self.sb_opacity = 255
    
    def hide_scrollbars(self):
        """Hides the panning scrollbars"""

        if not self.sb_opacity_anim is None:
            self.sb_opacity_anim.finished = True
        
        self.sb_opacity_anim = Animation(self, "sb_opacity", 255, 0, 1, type_=Animation.INT)
        Animation.animations.append(self.sb_opacity_anim)