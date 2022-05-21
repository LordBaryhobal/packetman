#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Label import Label
from classes.Logger import Logger
import pygame

class Checkbox(Label):
    def __init__(self, text="", callback=lambda *args, **kwargs: None, args=(), halign="center", valign="center", font_size=30, name=None):
        super().__init__(text, halign, valign, font_size, name)
        self.callback = callback
        self.args = args
        Logger.debug(f"Args: {args}")

        self.checked = False
    
    def render(self, surface):
        x, y, w, h = self.get_shape()
        h12 = h/12
        
        pts = [
            (x+3*h12, y+2*h12),
            (x+6*h12, y+5*h12),
            (x+9*h12, y+2*h12),
            (x+10*h12, y+3*h12),
            (x+7*h12, y+6*h12),
            (x+10*h12, y+9*h12),
            (x+9*h12, y+10*h12),
            (x+6*h12, y+7*h12),
            (x+3*h12, y+10*h12),
            (x+2*h12, y+9*h12),
            (x+5*h12, y+6*h12),
            (x+2*h12, y+3*h12)
        ]

        pygame.draw.rect(surface, (100,100,100), [x,y,h,h])
        pygame.draw.rect(surface, (200,200,200), [x+h*0.1,y+h*0.1,h*0.8,h*0.8])

        if self.checked:
            pygame.draw.polygon(surface, (0,0,0), pts)
        
        super().render(surface)
    
    def on_release(self, event):
        if event.button == 1:
            self.checked = not self.checked
            return self.callback(self, *self.args)
        
        return False