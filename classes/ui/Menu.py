#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .Component import Component
from .Constraints import *

class Menu(Component):
    def __init__(self, game, name=None):
        """Initializes a Menu instance

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
        
        self.visible = False
        self.bg_color = (0,0,0)
    
    def on_click(self, event):
        """Callback (can be overwritten by subclasses)

        Called when this component's pressed state changes to True
        Always returns True to catch events

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONDOWN event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

        return True
    
    def on_release(self, event):
        """Callback (can be overwritten by subclasses)

        Called when this component's pressed state changes to False
        Always returns True to catch events

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONUP event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

        return True
    
    def on_mouse_down(self, event):
        """Callback (can be overwritten by subclasses)

        Called when a mouse button is pressed down on the component
        Always returns True to catch events

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONDOWN event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

        return True
    
    def on_mouse_up(self, event):
        """Callback (can be overwritten by subclasses)

        Called when a mouse button is released on the component
        Always returns True to catch events

        Arguments:
            event {pygame.Event} -- MOUSEBUTTONUP event

        Returns:
            bool -- wether this event has been handled and shouldn't be passed further
        """

        return True