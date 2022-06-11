#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import glob
import os
import pygame
from random import choice

from classes.Logger import Logger
from classes.Path import Path

class MusicManager:
    """Static class managing musics"""

    musics = []
    volume = 1

    def __init__(self):
        """Initializes pygame's sound module"""

        pygame.mixer.init()
        folder = Path("assets", "musics")
        musics = glob.glob(Path(folder, "**", "*.wav"), recursive=True)

        for i, music in enumerate(musics):
            elmts = os.path.splitext(os.path.relpath(music, folder))[0].split(os.path.sep)
            musics[i] = ".".join(elmts)
        
        MusicManager.musics = musics
    
    def play(music=None):
        """Plays the given music

        Keyword Arguments:
            music {str} -- music id, if None, chooses a random music (default: {None})
        """
        
        if music is None:
            music = choice(MusicManager.musics)
        
        elmts = music.split(".")
        path = Path("assets", "musics", *elmts)+".wav"
        Logger.info(f"Now playing {music}")
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(MusicManager.volume)
        pygame.mixer.music.set_endevent(pygame.USEREVENT+8)
    
    def set_volume(volume):
        """Sets playback volume

        Arguments:
            volume {float} -- new volume
        """

        MusicManager.volume = volume