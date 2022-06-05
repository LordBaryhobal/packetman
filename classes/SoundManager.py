#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame
import os
from random import randint
from json import loads

from classes.Path import Path

class SoundManager:
    """Static class managing sound effects"""

    _cache = {}
    volume = 1

    def __init__(self):
        """Initializes pygame's sound module"""

        pygame.mixer.init()

    def load(sound):
        """Loads a sound

        Arguments:
            sound {str} -- sound id

        Returns:
            pygame.mixed.Sound -- sound object
        """
        
        elmts = sound.split(".")
        path = Path("assets", "sounds", *elmts)
        
        if os.path.exists(path+".json"):
            with open(path+".json", "r") as f:
                sound_property = loads(f.read())
            sound_list = []
            p = Path("assets", "sounds", *sound_property["path"].split("."))
            for i in range(sound_property["nb_of_sound"]):
                sound_list.append(pygame.mixer.Sound(p+str(i)+".wav"))
            return sound_list
        
        
        return pygame.mixer.Sound(path+".wav")

    def play(sound):
        """Plays the given sound

        Arguments:
            sound {str} -- sound id
        """
        
        if not sound in SoundManager._cache:
            SoundManager._cache[sound] = SoundManager.load(sound)
        
        if type(SoundManager._cache[sound]) == list:
            n = randint(0, len(SoundManager._cache[sound])-1)
            print(SoundManager._cache[sound][n])
            SoundManager._cache[sound][n].play().set_volume(SoundManager.volume)
        else:
            SoundManager._cache[sound].play().set_volume(SoundManager.volume)
    
    def set_volume(volume):
        """Sets playback volume

        Arguments:
            volume {float} -- new volume
        """

        SoundManager.volume = volume