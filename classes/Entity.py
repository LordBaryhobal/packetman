#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from typing import Type
from Vec import Vec
import pygame

class Entity:
    """
    Non grid-locked entity, either alive or not
    Subject to physics
    """

    def __init__(self) -> None:
        self.pos = Vec()
        self.vel = Vec()
        self.acc = Vec()
    
    """
    Renders the entity on a given surface at a given position and scale
    @param surface: pygame.Surface to render on
    @param pos: Vec containing the relative position of the entity on the surface
    """
    def render(self, surface: Type[pygame.Surface], pos: Type[Vec]) -> None:
        pass
