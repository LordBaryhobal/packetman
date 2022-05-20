#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
from classes.Logger import Logger
import pygame

def round_step(val, step, min_, max_):
    if step == 0:
        return min(max_, max(min_, val))
    
    return min(max_, max(min_, round(val/step)*step ))

class Slider(Component):
    def __init__(self, x, y, w, h, min_, max_, step=1, callback=lambda *args, **kwargs: None, args=(), name=None):
        super().__init__(x, y, w, h, name)
        
        self.callback = callback
        self.args = args

        self.min = min_
        self.max = max_
        self.step = step
        self.range = (self.max-self.min)

        self.thumb = 0.5
        self.value = round_step((min_+max_)/2, self.step, self.min, self.max)
    
    def render(self, surface, x, y, w, h):
        X = x+w*self.thumb

        pygame.draw.rect(surface, (200,200,200), [x, y+h*0.25, w, h*0.5])
        pygame.draw.rect(surface, (100,100,100), [X-10, y, 20, h])

        super().render(surface, x, y, w, h)

    def on_click(self, event):
        self.on_mouse_move(event)
        
        return True

    def on_mouse_move(self, event):
        if self.pressed:
            self.thumb = (event.pos[0]-self.x)/self.w
            value = round_step(self.min + self.thumb*self.range, self.step, self.min, self.max)
            
            if self.value != value:
                if self.on_change(value):
                    self.value = value

            self.thumb = (self.value-self.min)/self.range

    def on_change(self, value):
        return True