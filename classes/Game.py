#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from .World import World
from .Camera import Camera
import pygame

class Game:
    """
    Singleton class managing the interface, world rendering and simulation
    """

    WIDTH = 800
    HEIGHT = 600

    MAX_FPS = 60

    _instance = None

    def __init__(self):
        """Initializes a Game instance. Should not be called manually"""

        self.world = World()
        self.camera = Camera()

        pygame.init()
        self.window = pygame.display.set_mode([Game.WIDTH, Game.HEIGHT])
        self.clock = pygame.time.Clock()
    
    @property
    def instance():
        """Returns the unique Game instance, initializing one if none already exists"""
        if Game._instance is None:
            Game._instance = Game()

        return Game._instance

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