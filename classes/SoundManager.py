#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

from classes.Path import Path

class SoundManager:
    _cache = {}

    def __init__(self):
        pygame.mixer.init()

    def load(sound):
        elmts = sound.split(".")
        path = Path("assets", "sounds", *elmts)+".ogg"

        return pygame.mixer.Sound(path)

    def play(sound):
        if not sound in SoundManager._cache:
            SoundManager._cache[sound] = SoundManager.load(sound)
        
        SoundManager._cache[sound].play()