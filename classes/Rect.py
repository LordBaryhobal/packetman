#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Copyable import Copyable

class Rect(Copyable):
    """Simple rectangle class"""
    
    def __init__(self, x=0, y=0, w=0, h=0):
        """Initializes a Rect instance

        Keyword Arguments:
            x {float} -- x coordinate (default: {0})
            y {float} -- y coordinate (default: {0})
            w {float} -- width (default: {0})
            h {float} -- height (default: {0})
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def overlaps(self, r2):
        """Checks wether rectangles overlap

        Arguments:
            r2 {Rect} -- other rectangle to check overlapping with

        Returns:
            bool -- True if rectangles overlap, False otherwise
        """

        hor = not (r2.x >= self.x+self.w or self.x >= r2.x+r2.w)
        ver = not (r2.y >= self.y+self.h or self.y >= r2.y+r2.h)

        return hor and ver
    
    def from_vectors(self, topleft, bottomright):
        """Sets rectangle properties from corners

        Sets rectangle position and size from top-left and bottom-right corners

        Arguments:
            topleft {Vec} -- top-left coordinates
            bottomright {Vec} -- bottom-right coordinates
        """

        self.x = topleft.x
        self.y = topleft.y
        self.w = bottomright.x - topleft.x
        self.h = bottomright.y - topleft.y
    
    def render(self, surface, color, thickness=0):
        """Renders the rectangle

        Arguments:
            surface {pygame.Surface} -- surface to render the rectangle on
            color {tuple[int]} -- color of the rectangle

        Keyword Arguments:
            thickness {int} -- line thickness in pixels, 0 to fill (default: {0})
        """

        pygame.draw.rect(surface, color,(self.x, self.y, self.w, self.h), thickness)
    
    def __repr__(self):
        return f"Rect[{self.x}, {self.y}, {self.w}, {self.h}]"
    
    """The following methods make this class compatible with pygame"""

    def __getitem__(self, i):
        return [self.x, self.y, self.w, self.h][i]
    
    def __len__(self):
        return 4
    