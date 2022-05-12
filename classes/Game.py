#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .World import World
from .Camera import Camera
import pygame

class Game:
    """
    Main class managing the interface, world rendering and simulation
    """

    WIDTH = 800
    HEIGHT = 600

    MAX_FPS = 60

    def __init__(self):
        self.world = World(self)
        self.camera = Camera(self)

        pygame.init()
        self.window = pygame.display.set_mode([Game.WIDTH, Game.HEIGHT])
        self.clock = pygame.time.Clock()

    def mainloop(self):
        """Main game loop, calls the simulation and rendering functions"""

        while True:
            self.handle_events()
            self.physics()
            self.render()
    
    def handle_events(self):
        """Handle events triggered during this game loop"""

        pass

    def physics(self):
        """Processes physic simulation"""

        delta = 0
        self.world.physics(delta)
    
    def render(self):
        """Renders the game"""
        
        surface = self.window
        self.camera.render(surface)

        pygame.display.flip()
        self.clock.tick(self.MAX_FPS)