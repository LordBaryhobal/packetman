#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.ui.Constraints import *
from classes.ui.Component import Component
from classes.ui.Menu import Menu
from classes.ui.Label import Label
from classes.ui.Button import Button
from classes.ui.Checkbox import Checkbox
from classes.ui.Slider import Slider
from classes.ui.Flex import Flex
from classes.ui.Input import Input
from classes.Logger import Logger
import json

class Parser:
    def __init__(self, game):
        """Initializes a Parser instance

        Arguments:
            game {Game} -- game instance
        """

        self.game = game
    
    def parse(self, name):
        """Parses a gui file

        Arguments:
            name {str} -- gui name

        Returns:
            Component -- parsed component
        """

        with open("./guis/"+name+".json", "r") as f:
            desc = json.loads(f.read())
        
        return self.parse_child(desc)

    def parse_child(self, desc, parent=None):
        """Parses a component's child

        Arguments:
            desc {dict} -- dictionary of properties

        Keyword Arguments:
            parent {Component} -- parent component (default: {None})

        Returns:
            Component -- parsed component
        """

        cls = desc["class"]

        params = desc["params"]

        args = []
        kwargs = {}

        for param in params:
            if isinstance(param, dict) and "name" in param.keys():
                val = self.parse_param(param["val"], parent)
                kwargs[param["name"]] = val
            else:
                val = self.parse_param(param, parent)
                args.append(val)

        comp = globals()[cls](*args, **kwargs)
        comp.parent = parent

        for c in ["x","y","w","h"]:
            if c in desc:
                getattr(comp.cm, f"set_{c}")(self.parse_param(desc[c], parent))

        if "children" in desc.keys():
            for child in desc["children"]:
                comp.children.append(self.parse_child(child, comp))
        
        return comp
    
    def parse_param(self, param, parent):
        """Parses a value

        Arguments:
            param {Any} -- value to parse
            parent {Component} -- parent component

        Returns:
            Any -- parsed value
        """
        
        if isinstance(param, str):
            if param.startswith("${>") and param.endswith("}"):
                menu = param[3:-1]
                return lambda *a, **kwa: self.game.gui.switch_menu(menu)
            
            elif param == "${#}":
                return lambda *a, **kwa: self.game.gui.close_menu()

            elif param.startswith("${") and param.endswith("}"):
                path = param[2:-1].split(".")

                obj = None
                root = path.pop(0)
                if root == "parent":
                    obj = parent
                elif root == "game":
                    obj = self.game
                
                for p in path:
                    if hasattr(obj, p):
                        obj = getattr(obj, p)

                return obj
            
            return param

        elif isinstance(param, (int, float, bool)):
            return param
        
        elif isinstance(param, list):
            return [self.parse_param(p, parent) for p in param]
        
        elif isinstance(param, dict):
            keys = param.keys()
            if "type" in keys:
                cls = param["type"]
                args = list(param.values())
                args.remove(cls)

                constr = globals()[cls](*[self.parse_param(p, parent) for p in args])
                
                return constr
            
            else:
                d = {}
                for k,v in param.items():
                    d[k] = self.parse_param(v, parent)
                
                return d
            

if __name__ == "__main__":
    #p = Parser(None)
    #m = p.parse("")
    pass