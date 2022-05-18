#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Label import Label
import pygame

class Button(Label):
    def __init__(self, x, y, w, h, text="", callback=lambda *args, **kwargs: None, args=(), halign="center", valign="center", font_size=30, name=None):
        super().__init__(x, y, w, h, text, halign, valign, font_size, name)
        self.callback = callback
        self.args = args
    
    def render(self, surface, x, y, w, h):
        color = (255,150,50) if self.hover else (200, 100, 0)
        pygame.draw.rect(surface, color, [x, y, w, h])
        super().render(surface, x, y, w, h)
    
    def on_release(self, event):
        if event.button == 1:
            return self.callback(self, *self.args)
        
        return False