#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import json
from math import ceil
import os
import struct
from time import time

import pygame

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Cutscene import Cutscene
from classes.Editor import Editor
from classes.Event import Event
from classes.Logger import Logger
from classes.Path import Path
from classes.Settings import Settings
from classes.SoundManager import SoundManager
from classes.TextManager import TextManager
from classes.Texture import Texture
from classes.World import World
from classes.entities.Triggers import Trigger
from classes.ui.Constraints import *
from classes.ui.GUI import GUI
from classes.ui.Parser import Parser

class classproperty(property):
    """Utility class for annotating class properties. Parallel to `@property`"""

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Game:
    """Singleton class managing the interface, world rendering and simulation"""

    WIDTH = 800
    HEIGHT = 600

    MAX_FPS = 60
    RESIZE_COOLDOWN = 1

    PROGRESS_VER = 0

    _instance = None

    def __init__(self):
        """Initializes a Game instance. Should not be called manually"""

        with open(Path("config.json"), "r") as f:
            self.config = json.loads(f.read())
            
        Logger.level = self.config["loglevel"]

        self.settings = Settings(self)

        pygame.init()
        pygame.display.set_icon(pygame.image.load(Path("logo.png")))
        self.window = pygame.display.set_mode([self.WIDTH, self.HEIGHT], pygame.RESIZABLE)

        Texture.load_all(self)
        SoundManager()
        SoundManager.set_volume(self.settings.get("volume"))
        SoundManager.load_all(self)
        TextManager(self)
        TextManager.load_all(self)

        self.camera = Camera(self)
        self.world = World(self)
        self.camera.update_visible_tiles()
        self.camera.update_visible_entities()
        
        if self.config["edition"]:
            self.camera.follow_player = False

        if self.config["edition"]:
            self.editor = Editor(self)
        
        self.running = True
        self.paused = True

        self.menu_surf, self.editor_surf, self.hud_surf, self.entity_surf = [
            pygame.Surface([self.WIDTH, self.HEIGHT], pygame.SRCALPHA) for _ in range(4)
        ]
        self.world_surf = pygame.Surface([self.world.WIDTH*self.camera.tilesize, self.world.HEIGHT*self.camera.tilesize], pygame.SRCALPHA)
        self.world_surf.fill((40,40,40))
        self.clock = pygame.time.Clock()

        self.events = []

        self.gui = GUI(self)
        self.init_gui()

        self.cutscene = False

        self.cur_lvl = 0
        self.load_progress()
        self.start_resizing = None
        self.resize_font = pygame.font.SysFont("Arial", 40)
    
    @classproperty
    def instance(cls):
        """Returns the unique Game instance, initializing one if none already exists"""

        if cls._instance is None:
            cls._instance = Game()

        return cls._instance

    def mainloop(self):
        """Main game loop, calls the simulation and rendering functions"""

        while self.running:
            if self.cutscene:
                self.cutscene.mainloop()
            
            else:
                self.handle_events()

                if self.cutscene:
                    continue

                if not self.config["edition"] and not self.paused:
                    self.physics()
                
                self.render()
        
        pygame.display.quit()
        pygame.quit()
    
    def handle_events(self):
        """Handle events triggered during this game loop"""

        # Pygame events
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                if self.quit():
                    return
            
            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.size
                self.start_resizing = time()

            elif event.type == pygame.KEYDOWN:
                if not self.config["edition"]:
                    if event.key == pygame.K_c:
                        self.cutscene = Cutscene(self, "level", "test_tiles")
                    
                    elif event.key == pygame.K_DOLLAR:
                        self.cur_lvl = int(input("new cur_lvl: "))
                    
                    elif event.key == pygame.K_f:
                        self.finish_level()
        
        # Entities and World
        if not self.config["edition"] and not self.paused and not self.cutscene:
            for entity in self.world.entities:
                entity.handle_events(events)
            self.world.handle_events(events)

        # GUI
        self.gui.handle_events(events)
        events = list(filter(lambda e: not (hasattr(e, "handled") and e.handled), events))

        if not self.paused:
            # Editor
            if self.config["edition"]:
                self.editor.handle_events(events)
            
            # Animations
            for animation in Animation.ANIMATIONS:
                if not animation.start_time is None and not animation.finished:
                    animation.update()
                
                if animation.finished:
                    event = Event(Event.ANIMATION_FINISH)
                    event.animation = animation
                    self.events.append(event)
            
            Animation.ANIMATIONS = list(filter(lambda a: not a.finished, Animation.ANIMATIONS))

        # Custom events
        events = self.events

        for event in events:
            event.dispatch()

        self.events = []
        #self.world.circuit.current_circuit = set() # used when circuit are limited to one update per tile
        self.world.circuit.counter = 0
        if not self.config["edition"]:
            self.camera.update()

    def physics(self):
        """Processes physic simulation"""
        
        delta = self.clock.get_time()/1000
        self.world.physics(delta)
    
    def render(self):
        """Renders the game"""
        
        pygame.display.set_caption(f"Packetman - {self.clock.get_fps():.2f}fps")

        if self.start_resizing:
            if time() - self.start_resizing > self.RESIZE_COOLDOWN:
                self.start_resizing = None
                self.update_resize()
            
            else:
                self.window.fill((0, 0, 0))
                txt = self.resize_font.render(f"{self.WIDTH}x{self.HEIGHT}", True, (255, 255, 255))
                self.window.blit(txt, [self.WIDTH/2 - txt.get_width()/2, self.HEIGHT/2 - txt.get_height()/2])
                pygame.display.flip()
                self.clock.tick(self.MAX_FPS)
                return
        
        self.camera.render(self.world_surf, self.entity_surf, self.hud_surf, self.editor_surf)
        TextManager.render(self.hud_surf)

        if self.gui.changed:
            self.menu_surf.fill((0,0,0,0))
            self.gui.render(self.menu_surf)

        #self.editor_surf.set_alpha(200)
        #self.window.blit(self.world_surf, [-self.camera.pos.x, self.camera.pos.y])
        self.window.blit(self.world_surf, [0, 0], [
            self.camera.pos.x,
            self.world_surf.get_height()-self.camera.pos.y-self.HEIGHT,
            self.WIDTH, self.HEIGHT
        ])
        self.window.blit(self.entity_surf, [0, 0])

        if self.config["edition"]:
            self.window.blit(self.editor_surf, [0, 0])
        
        self.window.blit(self.hud_surf, [0, 0])

        if any(map(lambda c: c.visible, self.gui.children)):
            self.window.blit(self.menu_surf, [0, 0])

        pygame.display.flip()
        self.clock.tick(self.MAX_FPS)
    
    def set_paused(self, paused=True):
        """Sets paused state

        Keyword Arguments:
            paused {bool} -- new paused state (default: {True})
        """

        if self.paused != paused:
            if paused:
                Animation.pause_all()

            else:
                Animation.resume_all()
            
            self.paused = paused
    
    def update_resize(self):
        """Updates window dependent objects after a window resize"""

        self.camera.tilesize = self.HEIGHT//self.config["number_of_tiles"]
        self.menu_surf, self.editor_surf, self.hud_surf, self.entity_surf = [
            pygame.Surface([self.WIDTH, self.HEIGHT], pygame.SRCALPHA) for _ in range(4)
        ]
        #self.world_surf = pygame.Surface([self.world.WIDTH*self.camera.tilesize, self.world.HEIGHT*self.camera.tilesize], pygame.SRCALPHA)
        #self.world_surf.fill((40,40,40))
        self.update_world_surf()
        self.gui.cm.w.val = self.WIDTH
        self.gui.cm.h.val = self.HEIGHT
        self.camera.update_visible_tiles()
        self.camera.update_visible_entities()
        self.gui.set_changed(2)
        Texture.load_all(self)
        list(map(lambda t: t.on_update(), self.world.tiles.flatten()))

    def update_world_surf(self):
        world_surf = self.world_surf if hasattr(self, "world_surf") else pygame.Surface([0,0],pygame.SRCALPHA)
        w = ceil(self.world.WIDTH/32)*32*self.camera.tilesize
        h = ceil(self.world.HEIGHT/32)*32*self.camera.tilesize

        if (w, h) != world_surf.get_size():
            self.world_surf = pygame.Surface([w, h], pygame.SRCALPHA)
            self.world_surf.fill((40,40,40))
            self.world_surf.blit(world_surf, [0, self.world_surf.get_height()-world_surf.get_height()])

    def quit(self):
        """Stops the game"""

        self.running = False
        self.save_progress()
    
    def animate(self, obj, attr_, val_a, val_b, duration, start=True, loop=None, type_=Animation.FLOAT):
        """Initializes an Animation instance and adds it to the list of ANIMATIONS

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

        Animation.ANIMATIONS.append(Animation(obj, attr_, val_a, val_b, duration, start, loop, type_))
    
    def init_gui(self):
        """Loads and initializes the GUI"""

        self.parser = Parser(self)
        self.main_menu = self.parser.parse("main")
        self.pause_menu = self.parser.parse("pause")
        self.settings_menu = self.parser.parse("settings")
        self.levels_menu = self.parser.parse("levels")
        self.level_comp = self.parser.parse("level")
        self.entity_menu = self.parser.parse("entity")
        self.trigger_menu = self.parser.parse("trigger")
        self.save_menu = self.parser.parse("save")

        #self.main_menu.set_visible(True)
        #self.entity_menu.set_visible(False)

        self.pause_menu.bg_color = (100,100,100,200)
        self.entity_menu.bg_color = (100,150,100)
        self.trigger_menu.bg_color = (100,150,100)

        self.gui.add(self.main_menu)
        self.gui.add(self.pause_menu)
        self.gui.add(self.settings_menu)
        self.gui.add(self.levels_menu)
        self.gui.add(self.entity_menu)
        self.gui.add(self.trigger_menu)
        self.gui.add(self.save_menu)

        self.gui.switch_menu("main_menu")
    
    def resume(self, *args, **kwargs):
        """Closes pause menu and resumes the game"""

        self.gui.close_menu()
        self.set_paused(False)
    
    def pause(self):
        """Pauses the game and opens pause menu"""

        self.set_paused(True)
        self.gui.switch_menu("pause_menu")
    
    def cb_quit(self, button):
        self.quit()
        return True

    def cb_choose_lvl(self, button):
        levels = self.get_levels()
        
        container = self.levels_menu.get_by_name("levels")
        container.children = []

        if self.config["edition"]:
            level = self.level_comp.copy()
            level.args = ("new", )
            level.text = "New Level"
            container.add(level)

        if not (self.config["edition"] or self.config["bypass_progress"]):
            levels = levels[:self.cur_lvl+1]
        
        for l in levels:
            level = self.level_comp.copy()
            level.args = (l["level"], )
            level.text = l["name"]
            container.add(level)

        self.gui.switch_menu("levels_menu")
        return True
    
    def cb_lvl(self, button, path):
        Logger.debug(f"Selected level {path}")
        
        if path == "new":
            self.world.reset()
        
        else:
            if self.config["edition"]:
                self.world.load(path)
            else:
                self.cutscene = Cutscene(self, None, path)
        
        #self.camera.update_visible_tiles()
        #self.camera.update_visible_entities()
        
        self.gui.close_menu()
        self.set_paused(False)
        return True

    def cb_settings(self, button):
        self.settings.load()
        self.gui.switch_menu("settings_menu")
        return True
    
    def cb_exit_settings(self, button):
        self.settings.save()
        SoundManager.set_volume(self.settings.get("volume"))
        self.gui.switch_menu("main_menu")
        return True
    
    def cb_test(self, checkbox, *args, **kwargs):
        return True

    def cb_exit_entity_settings(self, button):
        self.save_entity_settings()
        self.gui.close_menu()
        return True
    
    def open_entity_settings(self, single_entity=False):
        self.single_entity = single_entity
        entity = self.editor.selected_entity
        
        if self.single_entity and isinstance(entity, Trigger):
            self.trigger_menu.get_by_name("text_id").set_value(entity.text_id)
            self.gui.switch_menu("trigger_menu")

        else:
            if self.single_entity:
                self.entity_menu.get_by_name("x_velocity").set_value(entity.vel.x)
                self.entity_menu.get_by_name("y_velocity").set_value(entity.vel.y)
                self.entity_menu.get_by_name("type").set_value(entity.type)
            self.gui.switch_menu("entity_menu")
        
    def save_entity_settings(self):
        if self.single_entity:
            entities = [self.editor.selected_entity]
        else:
            entities = self.editor.selected_entities
        
        vel = Vec(
            self.entity_menu.get_by_name("x_velocity").value,
            self.entity_menu.get_by_name("y_velocity").value
        )
        
        value = self.entity_menu.get_by_name("type").value
        for entity in entities:
            entity.vel = vel.copy()
            if value in entity._ENTITIES:
                entity.type = value
                entity.update_texture()

    def cb_entity_menu(self, slider, value, label_name, *args, **kwargs):
        label = self.entity_menu.get_by_name(label_name)
        current_text = label.text
        new_text = current_text.split(":")[0] + ":" + str(round(value,1))
        label.set_text(new_text)
        return True
    
    def cb_save_lvl(self, button):
        level_name = self.save_menu.get_by_name("level_name").value
        self.world.save(level_name)
        self.gui.close_menu()
        return True
    
    def cb_exit_trigger_settings(self, button):
        text_id = self.trigger_menu.get_by_name("text_id").get_value()
        self.editor.selected_entity.text_id = text_id
        self.gui.close_menu()
        return True
    
    def get_user_path(self):
        home = os.path.expanduser("~")
        dir_ = os.path.join(home, ".packetman")
        
        if not os.path.exists(dir_):
            os.mkdir(dir_)
        
        return dir_
    
    def get_levels(self):
        """Returns the list of levels

        Returns:
            list[dict] -- list of levels with name and filename
        """

        levels = []

        with open(Path("levels.json"), "r") as f:
            levels = json.loads(f.read())
        
        return levels
    
    def load_progress(self):
        """Loads current progress from progress file"""

        path = self.get_user_path()
        path = os.path.join(path, "progress.dat")
        
        if not os.path.exists(path):
            self.save_progress()
            return
        
        with open(path, "rb") as f:
            ver = struct.unpack(">H", f.read(2))[0]

            if ver != self.PROGRESS_VER:
                Logger.error(f"Progress file of version {ver} cannot be loaded with current version set to {self.PROGRESS_VER}")
            self.cur_lvl = struct.unpack(">H", f.read(2))[0]
    
    def save_progress(self):
        """Saves current progress to progress file"""

        path = self.get_user_path()
        path = os.path.join(path, "progress.dat")
        
        with open(path, "wb") as f:
            f.write(struct.pack(">H", self.PROGRESS_VER))
            f.write(struct.pack(">H", self.cur_lvl))
    
    def finish_level(self):
        """Completes the current level

        Updates current progress and triggers cutscene
        """

        levels = self.get_levels()
        for i, l in enumerate(levels):
            if l["level"] == self.world.level_file:
                self.cur_lvl = max(i+1, self.cur_lvl)
                break
        
        if i+1 >= len(levels):
            Logger.info("Congratulations, you finished the game !")
            self.save_progress()
            self.cutscene = Cutscene(self, self.world.level_file, None)
            return
        
        self.save_progress()
        self.cutscene = Cutscene(self, self.world.level_file, levels[i+1]["level"])