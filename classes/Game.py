#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.World import World
from classes.Camera import Camera
from classes.Logger import Logger
from classes.Event import Event
from classes.Animation import Animation
import pygame, json
from .Vec import Vec

class classproperty(property):
    """Utility class for annotating class properties. Parallel to `@property`"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


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

        self.logger = Logger()

        with open("./config.json", "r") as f:
            self.config = json.loads(f.read())
        
        self.logger.level = self.config["loglevel"]

        self.world = World()
        self.camera = Camera(self)

        self.running = True
        pygame.init()
        self.window = pygame.display.set_mode([Game.WIDTH, Game.HEIGHT])
        self.clock = pygame.time.Clock()

        self.events = []
        self.animations = []
    
    @classproperty
    def instance(cls):
        """Returns the unique Game instance, initializing one if none already exists"""
        if cls._instance is None:
            cls._instance = Game()

        return cls._instance

    def mainloop(self):
        """Main game loop, calls the simulation and rendering functions"""

        while self.running:
            self.handle_events()
            self.physics()
            self.render()
        
        pygame.display.quit()
        pygame.quit()
    
    def handle_events(self):
        """Handle events triggered during this game loop"""

        #Pygame events
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                if self.quit():
                    return

        for animation in self.animations:
            animation.update()
        
        self.animations = list(filter(lambda a: not a.finished, self.animations))

        #Custom events
        events = self.events

        for event in events:
            if event.type == Event.NONE:
                pass
            
            elif event.type == Event.UPDATED:
                if hasattr(event.obj) and hasattr(event.callback):
                    getattr(event.obj, event.callback).__call__(event)

        self.events = []

    def physics(self):
        """Processes physic simulation"""

        delta = self.clock.get_time()/1000
        self.world.physics(delta)
    
    def render(self):
        """Renders the game"""
        
        pygame.display.set_caption(f"Packetman - {self.clock.get_fps():.2f}fps")

        surface = self.window
        self.camera.render(surface)

        pygame.display.flip()
        self.clock.tick(self.MAX_FPS)
    
    def quit(self):
        self.running = False
    
    def animate(self, obj, attr_, val_a, val_b, duration, start=True, loop=None, type_=Animation.FLOAT):
        self.animations.append(Animation(obj, attr_, val_a, val_b, duration, start, loop, type_))