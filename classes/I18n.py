#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import json
import os

from classes.Path import Path

DICT = {}

def load_locale(lang="en"):
    global DICT

    path = Path("assets", "i18n", lang+".json")
    if not os.path.exists(path):
        path = Path("assets", "i18n", "en.json")
    
    with open(path, "r") as f:
        DICT = json.load(f)

def i18n(key):
    if not key:
        return ""
    
    # Literal
    if key.startswith("{") and key.endswith("}"):
        return key[1:-1]
    
    if key in DICT:
        return DICT[key]
    
    return f"[{key}]"