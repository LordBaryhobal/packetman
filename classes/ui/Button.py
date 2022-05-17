#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Label import Label
import pygame

class Button(Label):
    def __init__(self, x, y, w, h, text="", callback=lambda *args, **kwargs: None, halign="center", valign="center", font_size=30):
        super().__init__(x, y, w, h, text, halign, valign, font_size)
        self.callback = callback
    
    def render(self, surface, x, y, w, h):
        pygame.draw.rect(surface, (255,150,50), [x, y, w, h])
        super().render(surface, x, y, w, h)
    
    def click(self):
        self.callback(self)