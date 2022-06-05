#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Animation import Animation
from classes.Event import Event, listener, on
from classes.Path import Path

@listener
class TextManager:
    """Singleton class managing story texts used like a static class"""

    DELAY_PER_CHAR = 0.2
    FADE_DURATION = 0.5
    MARGIN = 10
    TIME_BAR = 2

    def __init__(self, game):
        """Initializes a TextManager instance

        Arguments:
            game {Game} -- game instance
        """

        self.game = game
        TextManager._instance = self
        TextManager.font = pygame.font.SysFont("Arial", 20)
        
        self.lines = []
        self.delay = 0
        self.opacity = 0
        self.displaying = False

    def show(id_):
        TM = TextManager._instance
        
        with open(Path("assets", "texts", id_+".txt"), "r") as f:
            TM.lines += f.read().strip().split("\n\n")
        
        if not TM.displaying:
            TextManager.next_line()
    
    def next_line(*args, **kwargs):
        TM = TextManager._instance
        TM.displaying = True
        if len(TM.lines) > 0:
            a = Animation(TM, "opacity", 0, 255, TM.FADE_DURATION)
            a.origin = "TextManager"
            a.id = "fade_in"
            TM.delay = 0
        
        else:
            TM.displaying = False

    def render(surface):
        TM = TextManager._instance
        W, H = TM.game.WIDTH, TM.game.HEIGHT

        if len(TM.lines) > 0:
            # Add empty line to leave space
            lines = TM.lines[0].split("\n")[::-1]

            s2 = pygame.Surface([W, H], pygame.SRCALPHA)

            y = H - TM.MARGIN
            max_w = 0
            
            for l in lines:
                txt = TM.font.render(l, True, (255, 255, 255))
                y -= txt.get_height()
                s2.blit(txt, [W/2 - txt.get_width()/2, y])
                max_w = max(max_w, txt.get_width())

            s2.set_alpha(TM.opacity)

            w = max_w + TM.MARGIN*2
            h_bg = H - y + TM.MARGIN
            x = W/2 - w/2
            
            # Background
            pygame.draw.rect(surface, (0, 0, 0, TM.opacity), [
                x, y - TM.MARGIN, w, h_bg])
            
            # Time bar
            pygame.draw.rect(surface, (150, 150, 150, TM.opacity), [
                x, H - TM.TIME_BAR, w*TM.delay, TM.TIME_BAR])

            surface.blit(s2, [0, 0])
    
    @on(Event.WORLD_LOADED)
    def clear(self, *args, **kwargs):
        """Clears all currently display texts"""

        self.lines = []
        self.delay = 0
        self.opacity = 0
        self.displaying = False

        Animation.ANIMATIONS = list(filter(
            lambda a: not hasattr(a, "origin") or a.origin != "TextManager",
            Animation.ANIMATIONS
        ))

    @on(Event.ANIMATION_FINISH)
    def on_anim_finish(self, event):
        anim = event.animation
        if hasattr(anim, "origin") and anim.origin == "TextManager":
            if anim.id == "fade_in":
                a = Animation(self, "delay", 0, 1, self.DELAY_PER_CHAR*len(self.lines[0]))
                a.origin = "TextManager"
                a.id = "delay"
            
            elif anim.id == "delay":
                a = Animation(self, "opacity", 255, 0, self.FADE_DURATION)
                a.origin = "TextManager"
                a.id = "fade_out"
            
            elif anim.id == "fade_out":
                self.lines.pop(0)
                self.next_line()