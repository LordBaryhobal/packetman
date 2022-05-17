#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.World import World
from classes.Camera import Camera
from classes.Logger import Logger
from classes.Event import Event
from classes.Animation import Animation
from classes.Editor import Editor
import pygame, json
from classes.ui.GUI import GUI
from classes.ui.Button import Button
from classes.ui.Constraints import *
from classes.ui.Component import Component
from classes.ui.Label import Label

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

        with open("./config.json", "r") as f:
            self.config = json.loads(f.read())
            
        if self.config["edition"]:
            self.editor = Editor(self)
        
        Logger.level = self.config["loglevel"]

        self.world = World(self)
        self.camera = Camera(self)

        self.running = True
        pygame.init()
        self.window = pygame.display.set_mode([Game.WIDTH, Game.HEIGHT])
        self.menu_surf, self.editor_surf, self.hud_surf, self.world_surf = [pygame.Surface([Game.WIDTH, Game.HEIGHT], pygame.SRCALPHA) for i in range(4)]
        self.clock = pygame.time.Clock()

        self.events = []

        self.gui = GUI(self)
        self.init_gui()

        #Test
        """self.gui.add(
            Button(
                ConstantConstraint(50),
                ConstantConstraint(50),
                RelativeConstraint(self, "WIDTH", 0.25),
                RelativeConstraint(self, "HEIGHT", 0.1),
                text="Button 1",
                callback=lambda *args, **kwargs: print("Clicked button 1") or True
            )
        )"""

        if not self.config["edition"]:
            self.world.load("level1")
    
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

            if not self.config["edition"]:
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
            
            elif event.type == pygame.KEYDOWN:
                if not self.config["edition"]:
                    if event.key == pygame.K_SPACE:
                        self.world.player.jump()
            
        keys = pygame.key.get_pressed()

        self.gui.handle_events(events)
        events = list(filter(lambda e: not (hasattr(e, "handled") and e.handled), events))

        if not self.config["edition"]:
            if keys[pygame.K_d]:
                self.world.player.move(1)
            
            if keys[pygame.K_a]:
                self.world.player.move(-1)

        if self.config["edition"]:
            self.editor.handle_events(events)

        for animation in Animation.animations:
            if not animation.start_time is None and not animation.finished:
                animation.update()
        
        Animation.animations = list(filter(lambda a: not a.finished, Animation.animations))

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

        self.menu_surf.fill((0,0,0,0))
        self.camera.render(self.world_surf, self.hud_surf, self.editor_surf)

        self.gui.render(self.menu_surf)

        #self.editor_surf.set_alpha(200)
        self.window.blit(self.world_surf, [0,0])
        self.window.blit(self.editor_surf, [0,0])
        self.window.blit(self.hud_surf, [0,0])
        self.window.blit(self.menu_surf, [0,0])

        pygame.display.flip()
        self.clock.tick(self.MAX_FPS)
    
    def quit(self):
        self.running = False
    
    def animate(self, obj, attr_, val_a, val_b, duration, start=True, loop=None, type_=Animation.FLOAT):
        Animation.animations.append(Animation(obj, attr_, val_a, val_b, duration, start, loop, type_))
    
    def init_gui(self):
        Const, Rel = ConstantConstraint, RelativeConstraint
        main = Component(Const(0), Const(0), Const(self.WIDTH), Const(self.HEIGHT)).add(
            Label(Const(0), Const(0), Const(self.WIDTH), Rel(self, "HEIGHT", 0.1), "Menu")
        )
        main.visible = False


        self.gui.add(main)