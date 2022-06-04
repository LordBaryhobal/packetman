#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import pygame

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
        path = Path("assets", "sounds", *elmts)+".wav"
        return pygame.mixer.Sound(path)

    def play(sound):
        """Plays the given sound

        Arguments:
            sound {str} -- sound id
        """
        
        if not sound in SoundManager._cache:
            SoundManager._cache[sound] = SoundManager.load(sound)
        
        SoundManager._cache[sound].play().set_volume(SoundManager.volume)
    
    def set_volume(volume):
        """Sets playback volume

        Arguments:
            volume {float} -- new volume
        """

        SoundManager.volume = volume