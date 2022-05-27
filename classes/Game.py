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
from classes.ui.Menu import Menu
from classes.ui.Label import Label
from classes.ui.Parser import Parser
import os

from classes.tiles.Bit import Bit
from classes.tiles.Components import Button as ButtonTile

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
        self.paused = True
        pygame.init()
        pygame.display.set_icon(pygame.image.load("./logo.png"))
        self.window = pygame.display.set_mode([Game.WIDTH, Game.HEIGHT])
        self.menu_surf, self.editor_surf, self.hud_surf, self.world_surf = [pygame.Surface([Game.WIDTH, Game.HEIGHT], pygame.SRCALPHA) for i in range(4)]
        self.clock = pygame.time.Clock()

        self.events = []

        self.gui = GUI(self)
        self.init_gui()
    
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

            if not self.config["edition"] and not self.paused:
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
                if event.key == pygame.K_ESCAPE:
                    if self.paused and self.pause_menu.visible:
                        self.resume()
                    elif not self.paused:
                        self.pause()
                    
                    elif self.levels_menu.visible:
                        self.cb_exit_levels(None)
                    
                    elif self.settings_menu.visible:
                        #self.cb_exit_settings(None)
                        pass

        if not self.config["edition"]:
            for entity in self.world.entities:
                entity.handle_events(events)
            self.world.handle_events(events)
                    

            
        keys = pygame.key.get_pressed()

        self.gui.handle_events(events)
        events = list(filter(lambda e: not (hasattr(e, "handled") and e.handled), events))

        if not self.paused:
            if self.config["edition"]:
                self.editor.handle_events(events)

            
            for animation in Animation.animations:
                if not animation.start_time is None and not animation.finished:
                    animation.update()
            
            Animation.animations = list(filter(lambda a: not a.finished, Animation.animations))

        #Custom events
        events = self.events

        for event in events:
            """
            if event.type == Event.NONE:
                pass
            
            elif event.type == Event.UPDATED:
                if hasattr(event.obj) and hasattr(event.callback):
                    getattr(event.obj, event.callback).__call__(event)"""
            event.dispatch()

        self.events = []
        if not self.config["edition"]:
            self.camera.update()

    def physics(self):
        """Processes physic simulation"""
        
        delta = self.clock.get_time()/1000
        self.world.physics(delta)
    
    def render(self):
        """Renders the game"""
        
        pygame.display.set_caption(f"Packetman - {self.clock.get_fps():.2f}fps")

        self.camera.render(self.world_surf, self.hud_surf, self.editor_surf)

        if self.gui.changed:
            self.menu_surf.fill((0,0,0,0))
            self.gui.render(self.menu_surf)

        #self.editor_surf.set_alpha(200)
        self.window.blit(self.world_surf, [0,0])
        self.window.blit(self.editor_surf, [0,0])
        self.window.blit(self.hud_surf, [0,0])
        self.window.blit(self.menu_surf, [0,0])

        pygame.display.flip()
        self.clock.tick(self.MAX_FPS)
    
    def quit(self):
        """Stops the game"""

        self.running = False
    
    def animate(self, obj, attr_, val_a, val_b, duration, start=True, loop=None, type_=Animation.FLOAT):
        """Initializes an Animation instance and adds it to the list of animations

        Arguments:
            obj {object} -- object to animate
            attr_ {str} -- name of the attribute to animate
            val_a {float} -- value at the start of the animation
            val_b {float} -- value at the end of the animation
            duration {float} -- duration in seconds of the animation

        Keyword Arguments:
            start {bool} -- True if animation should start automatically (default: {True})
            loop {int} -- type of looping (default: {None})
                          One of: None, Animation.FORWARDS, Animation.ALTERNATE
            type_ {int} -- type of the animated value (default: {FLOAT})
                           One of: Animation.FLOAT, Animation.INT
        """

        Animation.animations.append(Animation(obj, attr_, val_a, val_b, duration, start, loop, type_))
    
    def init_gui(self):
        """Loads and initializes the GUI"""

        self.parser = Parser(self)
        self.main_menu = self.parser.parse("main")
        self.pause_menu = self.parser.parse("pause")
        self.settings_menu = self.parser.parse("settings")
        self.levels_menu = self.parser.parse("levels")
        self.level_comp = self.parser.parse("level")
        self.entity_menu = self.parser.parse("entity")

        self.main_menu.set_visible(True)
        self.entity_menu.set_visible(False)

        self.pause_menu.bg_color = (100,100,100,200)
        self.entity_menu.bg_color = (100,150,100)

        self.gui.add(self.main_menu)
        self.gui.add(self.pause_menu)
        self.gui.add(self.settings_menu)
        self.gui.add(self.levels_menu)
        self.gui.add(self.entity_menu)
    
    def resume(self):
        """Closes pause menu and resumes the game"""

        self.pause_menu.set_visible(False)
        self.paused = False
    
    def pause(self):
        """Pauses the game and opens pause menu"""

        self.paused = True
        self.pause_menu.set_visible(True)
        self.entity_menu.set_visible(False)
    
    def load_settings(self):
        #menu = self.settings_menu
        #menu.get_by_name("")
        pass

    def save_settings(self):
        #self.config[""]
        pass

    def cb_resume(self, button):
        self.resume()
    
    def cb_quit(self, button):
        self.quit()

    def cb_choose_lvl(self, button):
        levels = os.listdir("./levels")
        container = self.levels_menu.get_by_name("levels")
        container.children = []

        if self.config["edition"]:
            level = self.level_comp.copy()
            level.args = ("new", )
            level.text = "New Level"
            container.add(level)

        for l in levels:
            if l.endswith(".dat"):
                level = self.level_comp.copy()
                level.args = (l[:-4], )
                level.text = l[:-4]
                container.add(level)

        self.levels_menu.set_visible(True)
        self.main_menu.set_visible(False)
    
    def cb_lvl(self, button, path):
        Logger.debug(f"Selected level {path}")
        
        #TODO: empty world if new
        if path != "new":
            self.world.load(path)
        
        self.camera.update_visible_tiles()
        self.camera.update_visible_entities()
        
        self.levels_menu.set_visible(False)
        self.paused = False

    def cb_settings(self, button):
        self.load_settings()
        self.main_menu.set_visible(False)
        self.settings_menu.set_visible(True)
    
    def cb_exit_pause(self, button):
        self.main_menu.set_visible(True)
        self.pause_menu.set_visible(False)
    
    def cb_exit_settings(self, button):
        self.save_settings()
        self.main_menu.set_visible(True)
        self.settings_menu.set_visible(False)
    
    def cb_exit_levels(self, button):
        self.main_menu.set_visible(True)
        self.levels_menu.set_visible(False)
    
    def cb_checkbox(self, checkbox, *args, **kwargs):
        pass

    def cb_exit_entity_settings(self, button):
        self.save_entity_settings()
        self.entity_menu.set_visible(False)
    
    def open_entity_settings(self, single_entity=False):
        self.single_entity = single_entity
        self.entity_menu.set_visible(True)
        
    def save_entity_settings(self):   
        if self.single_entity:
            entities = [self.editor.selected_entity]
        else:
            entities = self.editor.selected_entities
        
        vel = Vec(self.entity_menu.get_by_name("x_velocity").value,self.entity_menu.get_by_name("y_velocity").value)
        
        value = self.entity_menu.get_by_name("type").value
        for entity in entities:
            entity.vel = vel.copy()
            if value in entity._entity:
                entity.type = value
                entity.update_texture()
        return True

    def cb_entity_menu(self, slider, value, label_name, *args, **kwargs):
        label = self.entity_menu.get_by_name(label_name)
        current_text = label.text
        new_text = current_text.split(":")[0] + ":" + str(round(value,1))
        label.set_text(new_text)
        return True