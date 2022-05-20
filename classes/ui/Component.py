#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from .Constraints import *

class Component:
    """Basic UI component extend by all other UI elements"""

    def __init__(self, name):
        self.cm = Manager() # Constraints manager
        self.name = name

        self.parent = None
        self.children = []

        self.bg_color = None

        self.pressed = False
        self.hover = False
        self.visible = True

    def copy(self):
        """
        Creates a new copy of this component. Keeps class and all properties
        """
        cls = self.__class__
        new = cls(self.name)

        for k,v in self.__dict__.items():
            if hasattr(v, "copy"):
                v = v.copy()
            setattr(new, k, v)
        
        return new
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} \"{self.name}\" {self.cm}>"
    
    def print_tree(self, level=0):
        print("| "*level + "+-+" + str(self))
        for child in self.children:
            child.print_tree(level+1)

    def render(self, surface):
        if self.visible:
            if not self.bg_color is None:
                pygame.draw.rect(surface, self.bg_color, self.get_shape())
            
            for child in self.children:
                child.render(surface)

    def get_shape(self):
        return self.cm.get_shape(self.parent)
    
    def get_x(self):
        return self.cm.get_x(self.parent)
    
    def get_y(self):
        return self.cm.get_y(self.parent)
    
    def get_w(self):
        return self.cm.get_w(self.parent)
    
    def get_h(self):
        return self.cm.get_h(self.parent)

    def get_by_name(self, name):
        if self.name == name:
            return self
        
        elmt = None
        for child in self.children:
            elmt = child.get_by_name(name)
            if elmt:
                break
        
        return elmt
    
    def add(self, child):
        child.parent = self
        self.children.append(child)
        return self
    
    def handle_event(self, event):
        if not self.visible:
            return False
        
        x, y, w, h = self.get_shape()

        handled = False

        for child in self.children:
            if handled:
                break
            
            handled = child.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x <= event.pos[0] < x+w and y <= event.pos[1] < y+h:
                self.pressed = True

                if self.on_click(event):
                    handled = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.on_mouse_up(event):
                handled = True

            if self.pressed:
                self.pressed = False
                if self.on_release(event):
                    handled = True
        
        elif event.type == pygame.MOUSEMOTION:
            if self.on_mouse_move(event):
                handled = True

            if x <= event.pos[0] < x+w and y <= event.pos[1] < y+h:
                if not self.hover:
                    self.hover = True
                    if self.on_enter(event):
                        handled = True
                    
            elif self.hover:
                self.hover = False
                if self.on_exit(event):
                    handled = True

        return handled
    
    def on_click(self, event):
        return False
    
    def on_release(self, event):
        return False
    
    def on_enter(self, event):
        return False
    
    def on_exit(self, event):
        return False
    
    def on_mouse_down(self, event):
        return False
    
    def on_mouse_up(self, event):
        return False
    
    def on_mouse_move(self, event):
        return False