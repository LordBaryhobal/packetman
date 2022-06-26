#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import glob
import os
import pygame
from random import choice

from classes.Logger import Logger
from classes.Path import Path

class SoundManager:
    """Static class managing sound effects"""

    _cache = {}
    TOTAL = 0
    LOADED = 0
    volume = 1

    def __init__(self):
        """Initializes pygame's sound module"""

        pygame.mixer.init()

    def load_all(game):
        SoundManager.TOTAL = len(glob.glob(Path("assets", "sounds", "**", "*.wav"), recursive=True))
        SoundManager.LOADED = 0
        SoundManager.load_walk(game, Path("assets", "sounds"))
    
    def load_walk(game, path, name="", variants=False):
        content = os.listdir(path)

        for f in content:
            p = Path(path, f)

            if os.path.isdir(p):
                n = name
                if n: n += "."
                n += f

                if os.path.exists(Path(p, ".variants")):
                    SoundManager._cache[n] = []
                    SoundManager.load_walk(game, p, n, True)

                else:
                    SoundManager.load_walk(game, p, n)
            
            elif os.path.splitext(f)[1] == ".wav":
                if variants:
                    SoundManager._cache[name].append(pygame.mixer.Sound(p))
                
                else:
                    n = name
                    if n: n += "."
                    n += os.path.splitext(f)[0]
                    SoundManager._cache[n] = pygame.mixer.Sound(p)
                
                SoundManager.LOADED += 1

    def load(sound):
        """Loads a sound

        Arguments:
            sound {str} -- sound id

        Returns:
            pygame.mixed.Sound -- sound object
        """
        
        elmts = sound.split(".")
        path = Path("assets", "sounds", *elmts)
        
        if os.path.exists(path) and os.path.isdir(path):
            sound_files = os.listdir(path)
            sound_list = []
            for f in sound_files:
                sound_list.append(pygame.mixer.Sound(os.path.join(path, f)))
            return sound_list
        
        
        return pygame.mixer.Sound(path+".wav")

    def play(sound):
        """Plays the given sound

        Arguments:
            sound {str} -- sound id
        """
        
        if not sound in SoundManager._cache:
            #SoundManager._cache[sound] = SoundManager.load(sound)
            Logger.error(f"Sound {sound} not loaded")
        
        if isinstance(SoundManager._cache[sound], list):
            s = choice(SoundManager._cache[sound])
            s.play().set_volume(SoundManager.volume)
        else:
            s = SoundManager._cache[sound].play()
            if s:
                s.set_volume(SoundManager.volume)
    
    def set_volume(volume):
        """Sets playback volume

        Arguments:
            volume {float} -- new volume
        """

        SoundManager.volume = volume