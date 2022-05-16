#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
import pygame

class Button(Component):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
    
    def render(self, surface):
        pygame.draw.rect(surface, (255,150,50), [self.x, self.y, self.w, self.h])