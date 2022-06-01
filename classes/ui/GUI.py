#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.ui.Component import Component
from classes.ui.Constraints import *

class GUI(Component):
    """Root component containing all menus which will be displayed"""

    def __init__(self, game, name=None):
        """Initializes a GUI instance

        Arguments:
            game {Game} -- game instance

        Keyword Arguments:
            name {str} -- component's name (default: {None})
        """

        self.game = game
        super().__init__(name)
        self.cm.set_x(Absolute(0))
        self.cm.set_y(Absolute(0))
        self.cm.set_w(Absolute(self.game.WIDTH))
        self.cm.set_h(Absolute(self.game.HEIGHT))
        self.current = None

    def render(self, surface):
        for child in self.children:
            child.render(surface)
    
    def handle_events(self, events):
        """Processes mouse and keyboard events

        Arguments:
            events {list[pygame.Event]} -- list of pygame events
        """
        
        for event in events:
            if self.handle_event(event):
                event.handled = True
    
    def handle_event(self, event, in_parent=True):
        handled = super().handle_event(event, in_parent)

        if not handled:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not self.game.paused:
                        self.game.pause()
                        handled = True
        
        return handled
    
    def close_menu(self):
        if self.current:
            self.current.set_visible(False)
            self.current = None
    
    def switch_menu(self, name):
        self.close_menu()
        self.current = self.get_by_name(name)
        self.current.set_visible(True)
            