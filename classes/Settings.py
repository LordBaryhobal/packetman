#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import json
import os

from classes.ui.Checkbox import Checkbox
from classes.ui.Input import Input
from classes.ui.Slider import Slider

class Settings:
    """Utility class to manage settings"""

    DEFAULTS = {
        "volume": 0.5,
        "rtx_mode": False,
        "fullscreen": False,
        "lang": "en",
        "interaction_hint": True
    }

    def __init__(self, game):
        """Initializes a Settings instance

        Arguments:
            game {Game} -- game instance
        """

        self.game = game
        self.settings = {}
        self.load()
    
    def load(self):
        """Loads settings from settings file"""

        path = self.game.get_user_path()
        path = os.path.join(path, "settings.json")
        
        if not os.path.exists(path):
            self.save()
            return

        settings = self.DEFAULTS.copy()
        
        with open(path, "r") as f:
            settings.update(json.loads(f.read()))
        
        self.settings = settings
        
        if hasattr(self.game, "gui"):
            for k,v in self.settings.items():
                elmt = self.game.settings_menu.get_by_name(k)
                
                if elmt:
                    elmt.set_value(v)
    
    def save(self):
        """Saves settings to settings file"""

        path = self.game.get_user_path()
        path = os.path.join(path, "settings.json")

        if hasattr(self.game, "gui"):
            for k,v in self.DEFAULTS.items():
                elmt = self.game.settings_menu.get_by_name(k)
                
                if elmt:
                    self.settings[k] = elmt.get_value()

        settings = self.DEFAULTS.copy()
        settings.update(self.settings)
        
        with open(path, "w") as f:
            f.write(json.dumps(settings, indent=4))
    
    def get(self, key):
        """Gets a setting value

        Arguments:
            key {str} -- setting id

        Returns:
            Any -- setting value
        """

        return self.settings[key]
    
    def set(self, key, val):
        """Sets a setting value

        Arguments:
            key {str} -- setting id
            val {Any} -- setting value
        """

        self.settings[key] = val