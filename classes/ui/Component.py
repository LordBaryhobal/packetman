#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from .Constraints import *

class Component:
    """Basic UI component extend by all other UI elements"""

    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

        self.parent = None
        self.children = []

        self.pressed = False
        self.hover = False
        self.visible = True

    def render(self, surface, x, y, w, h):
        if self.visible:
            for child in self.children:
                child.render(surface, x+child.x, y+child.y, child.w, child.h)
    
    @property
    def x(self):
        return self._x.val
    
    @property
    def y(self):
        return self._y.val
    
    @property
    def w(self):
        return self._w.val
    
    @property
    def h(self):
        return self._h.val
    
    def add(self, child):
        child.parent = self
        self.children.append(child)
        return self
    
    def handle_event(self, event):
        if not self.visible:
            return False
        
        x, y = self.x, self.y
        w, h = self.w, self.h

        handled = False

        for child in self.children:
            if handled:
                break
            
            handled = child.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= event.pos[0] < x+w and y <= event.pos[1] < y+h:
                if self.on_clicked(event.button):
                    handled = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed:
                self.pressed = False
                self.on_release(event.button)
        
        elif event.type == pygame.MOUSEMOTION:
            if x <= event.pos[0] < x+w and y <= event.pos[1] < y+h:
                if not self.hover:
                    self.hover = True
                    self.on_enter()
            elif self.hover:
                self.hover = False
                self.on_exit()

        return handled
    
    def on_clicked(self, button):
        return False
    
    def on_release(self, button):
        return False
    
    def on_enter(self):
        return False
    
    def on_exit(self):
        return False