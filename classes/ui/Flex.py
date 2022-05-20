#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.ui.Constraints import Absolute
from .Component import Component
from classes.Logger import Logger
import pygame

class Flex(Component):
    def __init__(self, name=None, dir_="col", justify="space-evenly"):
        super().__init__(name)
        
        self.dir = dir_
        self.justify = justify
    
    def render(self, surface):
        if self.visible:
            if not self.bg_color is None:
                pygame.draw.rect(surface, self.bg_color, self.get_shape())
            
            current = 0

            if self.dir == "col":
                min_size = sum([child.get_h() for child in self.children])
                remainder = self.get_h()-min_size
            else:
                min_size = sum([child.get_w() for child in self.children])
                remainder = self.get_w()-min_size
            
            if remainder < 0:
                Logger.warn("Flex overflow")
            
            if self.justify == "space-between":
                gap = remainder / (len(self.children)-1)
            
            elif self.justify == "space-around":
                gap = remainder / len(self.children)
                current += gap/2
            
            elif self.justify == "space-evenly":
                gap = remainder / (len(self.children)+1)
                current += gap

            for child in self.children:
                constr = Absolute(current)
                constr._automatic = True

                if self.dir == "col":
                    child.cm.set_y(constr)
                else:
                    child.cm.set_x(constr)
                
                child.render(surface)

                if self.dir == "col":
                    current += child.get_h()
                else:
                    current += child.get_w()
                
                current += gap