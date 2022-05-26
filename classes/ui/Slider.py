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
        """Renders the component

        Arguments:
            surface {pygame.Surface} -- surface to render the component on
        """

        x, y, w, h = self.get_shape()
        X = x+w*self.thumb

        pygame.draw.rect(surface, (200,200,200), [x, y+h*0.25, w, h*0.5])
        pygame.draw.rect(surface, (100,100,100), [X-10, y, 20, h])

        super().render(surface)

    def on_click(self, event):
        """Callback (can be overwritten by subclasses)

        Called when this component's pressed state changes to True
        Always returns True to catch events

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONDOWN event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

        self.on_mouse_move(event)
        
        return True

    def on_mouse_move(self, event):
        """Callback (can be overwritten by subclasses)

        Called when the mouse cursor moves in this component's bounding box

        Arguments:
            event {pygame.Event} -- MOUSEMOTION event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        if self.pressed:
            self.thumb = (event.pos[0]-self.get_x())/self.get_w()
            value = self.min + self.thumb*self.range
            
            self.set_value(value)

    def on_change(self, value):
        """Callback (can be overwritten by subclasses)

        Called when the slider's value is changed

        Arguments:
            value {float} -- new value

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        self.set_changed(1)
        return self.callback(self, value, *self.args)
        #return True
    
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