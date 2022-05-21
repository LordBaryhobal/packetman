#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
from .Constraints import *

class Component:
    """Basic UI component extend by all other UI elements"""

    def __init__(self, name):
        """Initializes a Component instance

        Arguments:
            name {str} -- component's name
        """

        self.cm = Manager() # Constraints manager
        self.name = name

        self.parent = None
        self.children = []

        self.bg_color = None

        self.pressed = False
        self.hover = False
        self.visible = True

    def copy(self):
        """Creates a new copy this component

        Keeps class and all properties

        Returns:
            Component -- deepcopy of this component
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
        """Prints a tree-like representation of this element and its children recursively

        Keyword Arguments:
            level {int} -- indentation level of this element (default: {0})
        """

        print("| "*level + "+-+" + str(self))
        for child in self.children:
            child.print_tree(level+1)

    def render(self, surface):
        """Renders the component

        Arguments:
            surface {pygame.Surface} -- surface to render the component on
        """

        if self.visible:
            tmp_surf = surface.copy()

            if not self.bg_color is None:
                pygame.draw.rect(tmp_surf, self.bg_color, self.get_shape())
            
            for child in self.children:
                child.render(tmp_surf)
            
            x, y, w, h = self.get_shape()
            surface.blit(tmp_surf, [x,y], [x,y,w,h])

    def get_shape(self):
        """Returns the shape of this component

        Returns:
            Rect -- delimiting rectangle of this component
        """

        return self.cm.get_shape(self.parent)
    
    def get_x(self):
        """Returns the x position of this component

        Returns:
            float -- x coordinate
        """

        return self.cm.get_x(self.parent)
    
    def get_y(self):
        """Returns the y position of this component

        Returns:
            float -- y coordinate
        """
        
        return self.cm.get_y(self.parent)
    
    def get_w(self):
        """Returns the width of this component

        Returns:
            float -- width
        """
        
        return self.cm.get_w(self.parent)
    
    def get_h(self):
        """Returns the height of this component

        Returns:
            float -- height
        """
        
        return self.cm.get_h(self.parent)

    def get_by_name(self, name):
        """Gets an element by its name

        This method is called recursively for each child until it finds the element or has checked the whole tree

        Arguments:
            name {str} -- name of the element to get

        Returns:
            Component -- the component if it was found, None otherwise
        """

        if self.name == name:
            return self
        
        elmt = None
        for child in self.children:
            elmt = child.get_by_name(name)
            if elmt:
                break
        
        return elmt
    
    def add(self, child):
        """Adds a child to this component

        Arguments:
            child {Component} -- child to add

        Returns:
            Component -- self, to make this method chainable
        """

        child.parent = self
        self.children.append(child)
        return self
    
    def handle_event(self, event):
        """Processes a mouse or keyboard event

        This method first passes the event to its children recursively

        Arguments:
            event {pygame.Event} -- event to process

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

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
        """Callback (can be overwritten by subclasses)

        Called when this component's pressed state changes to True

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONDOWN event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

        return False
    
    def on_release(self, event):
        """Callback (can be overwritten by subclasses)

        Called when this component's pressed state changes to False

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONUP event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        return False
    
    def on_enter(self, event):
        """Callback (can be overwritten by subclasses)

        Called when the mouse cursor enters this component's bounding box

        Arguments:
            event {pygame.Event} -- MOUSEMOTION event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        return False
    
    def on_exit(self, event):
        """Callback (can be overwritten by subclasses)

        Called when the mouse cursor exits this component's bounding box

        Arguments:
            event {pygame.Event} -- MOUSEMOTION event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        return False
    
    def on_mouse_down(self, event):
        """Callback (can be overwritten by subclasses)

        Called when a mouse button is pressed down on the component

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONDOWN event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        return False
    
    def on_mouse_up(self, event):
        """Callback (can be overwritten by subclasses)

        Called when a mouse button is released on the component

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONUP event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        return False
    
    def on_mouse_move(self, event):
        """Callback (can be overwritten by subclasses)

        Called when the mouse cursor moves in this component's bounding box

        Arguments:
            event {pygame.Event} -- MOUSEMOTION event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """
        
        return False