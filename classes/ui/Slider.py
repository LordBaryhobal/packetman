#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Logger import Logger
from classes.ui.Component import Component

def round_step(val, step, min_, max_):
    """Rounds a value to nearest step

    Arguments:
        val {float} -- current value
        step {float} -- step size
        min_ {float} -- minimum value
        max_ {float} -- maximum value

    Returns:
        flaot -- rounded value
    """

    if step == 0:
        return min(max_, max(min_, val))
    
    return min(max_, max(min_, round(val/step)*step ))

class Slider(Component):
    """Tweakable slider component"""

    def __init__(self, min_, max_, step=1, callback=lambda *args, **kwargs: True, args=(), name=None):
        """Initializes a Slider instance

        Arguments:
            min_ {float} -- minimum value
            max_ {float} -- maximum value

        Keyword Arguments:
            step {float} -- step size (default: {1})
            callback {function} -- callback to call when value is updated (default: {nop})
            args {tuple} -- arguments to pass to callback (default: {()})
            name {str} -- component's name (default: {None})
        """

        super().__init__(name)
        
        self.callback = callback
        self.args = args

        self.min = min_
        self.max = max_
        self.step = step
        self.range = (self.max-self.min)

        self.thumb = 0.5
        self.value = round_step((min_+max_)/2, self.step, self.min, self.max)
    
    def render(self, surface):
        x, y, w, h = self.get_shape()
        X = x+w*self.thumb

        pygame.draw.rect(surface, (200,200,200), [x, y+h*0.25, w, h*0.5])
        pygame.draw.rect(surface, (100,100,100), [X-10, y, 20, h])

        super().render(surface)

    def get_value(self):
        return self.value

    def set_value(self, value):
        """Sets the slider's value

        Arguments:
            value {float} -- new value
        """
        
        value = round_step(value, self.step, self.min, self.max)
        if self.value != value:
            if self.on_change(value):
                self.value = value
        self.thumb = (self.value-self.min)/self.range
    
    def on_click(self, event):
        self.on_mouse_move(event)
        return True

    def on_mouse_move(self, event):
        if self.pressed:
            self.thumb = (event.pos[0]-self.get_x())/self.get_w()
            value = self.min + self.thumb*self.range
            
            self.set_value(value)

    def on_change(self, value):
        self.set_changed(1)
        return self.callback(self, value, *self.args)