#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import threading

import pygame

from classes.Animation import Animation
from classes.Event import Event, listener, on

@listener
class Cutscene:
    #BARS_HEIGHT = 100
    BARS_RATIO = 2.4

    START = 0
    FADING_OUT = 1
    LOADING = 2
    LOADED = 3
    END = 4

    PLAYER_SPEED = 1
    FADE_DURATION = 3
    BARS_DURATION = 1

    def __init__(self, game, from_lvl, to_lvl):
        self.game = game
        self.from_lvl = from_lvl
        self.to_lvl = to_lvl

        self.BARS_HEIGHT = (self.game.HEIGHT - self.game.WIDTH/self.BARS_RATIO)/2

        self.state = None

        self.bars_height = 0 if from_lvl else self.BARS_HEIGHT
        self.black_opacity = 0 if from_lvl else 255

        self.load_thread = None

        self.overlay = pygame.Surface([self.game.WIDTH, self.game.HEIGHT], pygame.SRCALPHA)

        if self.from_lvl:
            self.start()
        else:
            self.start_load()
    
    def start(self):
        """Starts the cutscene (i.e. bars slide in)"""

        self.state = self.START

        a = Animation(self, "bars_height", 0, self.BARS_HEIGHT, self.BARS_DURATION)
        a.origin = "Cutscene"
        a.id = "slide_in"

    def stop(self):
        """Starts the end of cutscene (i.e. bars slide out)"""

        self.state = self.END

        a = Animation(self, "bars_height", self.BARS_HEIGHT, 0, self.BARS_DURATION)
        a.origin = "Cutscene"
        a.id = "slide_out"
    
    def start_fade(self):
        """Starts fade out"""

        self.state = self.FADING_OUT

        a = Animation(self, "black_opacity", 0, 255, self.FADE_DURATION)
        a.origin = "Cutscene"
        a.id = "fade_out"

    def start_load(self):
        """Starts level loading"""

        self.state = self.LOADING

        if self.to_lvl:
            self.load_thread = threading.Thread(target=self.load_thread_func)
            self.load_thread.start()
        
        else:
            self.game.set_paused(True)
            self.game.gui.switch_menu("main_menu")
            self.end_cutscene()
            
    
    def load_thread_func(self):
        """Loads level (executed in other thread)"""

        self.game.world.load(self.to_lvl)
        self.game.world.player.pos.x -= self.PLAYER_SPEED * (self.FADE_DURATION + self.BARS_DURATION)

    def end_load(self):
        """Starts fade in"""

        self.state = self.LOADED

        self.game.world.player.force_render = True
        self.game.camera.update_visible_tiles()
        self.game.camera.update_visible_entities()
        a = Animation(self, "black_opacity", 255, 0, self.FADE_DURATION)
        a.origin = "Cutscene"
        a.id = "fade_in"
    
    def end_cutscene(self):
        """Ends the cutscene and returns to normal mode"""

        self.game.world.player.force_render = False
        self.game.world.player.vel.x = 0
        self.game.world.player.vel.y = 0
        self.game.cutscene = None
        Cutscene._instances.remove(self)

    def mainloop(self):
        """Main game loop (overrides Game.mainloop)"""
        
        self.handle_events()

        if not self.game.cutscene:
            return
        
        self.physics()
        self.render()

    def handle_events(self):
        """Handle events triggered during this game loop"""

        # Pygame events
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                if self.game.quit():
                    return

        # Animations
        for animation in Animation.ANIMATIONS:
            if not animation.start_time is None and not animation.finished:
                animation.update()
            
            if animation.finished:
                event = Event(Event.ANIMATION_FINISH)
                event.animation = animation
                self.game.events.append(event)
        
        Animation.ANIMATIONS = list(filter(lambda a: not a.finished, Animation.ANIMATIONS))

        # Custom events
        events = self.game.events
        for event in events:
            event.dispatch()

        self.game.events = []

        if self.state != self.LOADING:
            self.game.camera.update()
    
    def physics(self):
        """Processes physic simulation"""
        
        self.game.world.player.vel.x = self.PLAYER_SPEED
        self.game.world.player.vel.y = 0

        delta = self.game.clock.get_time()/1000
        #self.game.world.physics(delta)
        """for entity in self.game.world.entities:
            entity.physics(delta)"""
        
        player = self.game.world.player
        player.pos += player.vel * delta
        #player.vel += player.acc * delta
        
        player.pos = round(player.pos, 6)
        #player.vel = round(player.vel, 6)
        #player.acc = round(player.acc, 6)

        player.update()
    
    def render(self):
        """Renders the game"""
        
        pygame.display.set_caption(f"Packetman - {self.game.clock.get_fps():.2f}fps")
        
        self.game.camera.render(self.game.world_surf, self.game.hud_surf, self.game.editor_surf)

        pygame.draw.rect(self.game.world_surf, (0,0,0), [0, 0, self.game.WIDTH, self.bars_height])
        pygame.draw.rect(self.game.world_surf, (0,0,0), [0, self.game.HEIGHT-self.bars_height+1, self.game.WIDTH, self.bars_height])

        #self.game.editor_surf.set_alpha(200)
        self.game.window.blit(self.game.world_surf, [0, 0])
        #self.game.window.blit(self.game.editor_surf, [0, 0])
        #self.game.window.blit(self.game.hud_surf, [0, 0])
        #self.game.window.blit(self.game.menu_surf, [0, 0])
        self.overlay.fill((0, 0, 0, self.black_opacity))
        self.game.window.blit(self.overlay, [0, 0])

        pygame.display.flip()
        self.game.clock.tick(self.game.MAX_FPS)
    
    @on(Event.WORLD_LOADED)
    def on_world_loaded(self, event):
        self.end_load()
    
    @on(Event.ANIMATION_FINISH)
    def on_animation_finish(self, event):
        anim = event.animation
        if hasattr(anim, "origin") and anim.origin == "Cutscene":
            if self.state == self.START and anim.id == "slide_in":
                self.start_fade()
            
            elif self.state == self.FADING_OUT and anim.id == "fade_out":
                self.start_load()
            
            elif self.state == self.LOADED and anim.id == "fade_in":
                self.stop()
            
            elif self.state == self.END and anim.id == "slide_out":
                self.end_cutscene()