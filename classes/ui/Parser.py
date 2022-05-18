#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.ui.Constraints import ConstantConstraint, RelativeConstraint
from classes.ui.Component import Component
from classes.ui.Menu import Menu
from classes.ui.Label import Label
from classes.ui.Button import Button
from classes.Logger import Logger
import json

class Parser:
    def __init__(self, game):
        self.game = game
    
    def parse(self, name):
        with open("./guis/"+name+".json", "r") as f:
            desc = json.loads(f.read())
        
        return self.parse_child(desc)

    def parse_child(self, desc, parent=None):
        Logger.debug(f"Parsing child: parent={parent} | child={desc}")
        cls = desc["class"]

        params = desc["params"]

        args = []
        kwargs = {}

        for param in params:
            val = self.parse_param(param, parent)
            Logger.debug(f"Param: {param} | val: {val}")

            if isinstance(param, dict) and "name" in param.keys():
                kwargs[param["name"]] = val
            else:
                args.append(val)

        comp = globals()[cls](*args, **kwargs)
        comp.parent = parent

        if "children" in desc.keys():
            for child in desc["children"]:
                comp.children.append(self.parse_child(child, comp))
        
        return comp
    
    def parse_param(self, param, parent):
        if isinstance(param, str):
            if param.startswith("${") and param.endswith("}"):
                path = param[2:-1].split(".")
                
                Logger.debug(f"path: {path}")

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
        
        elif isinstance(param, dict):
            keys = param.keys()
            if "constraint" in keys:
                if param["constraint"] == "const":
                    return ConstantConstraint(self.parse_param(param["val"], parent))

                elif param["constraint"] == "rel":
                    return RelativeConstraint(
                        self.parse_param(param["obj"], parent),
                        self.parse_param(param["attr"], parent),
                        self.parse_param(param["ratio"], parent)
                    )
            

if __name__ == "__main__":
    #p = Parser(None)
    #m = p.parse("")
    pass