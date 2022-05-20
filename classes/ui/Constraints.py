#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Vec import Vec
from classes.Rect import Rect

class Manager:
    def __init__(self):
        self.x = None
        self.y = None
        self.w = None
        self.h = None
    
    def set_x(self, constr):
        constr.setType("x")
        self.x = constr
    
    def set_y(self, constr):
        constr.setType("y")
        self.y = constr
    
    def set_w(self, constr):
        constr.setType("w")
        self.w = constr
    
    def set_h(self, constr):
        constr.setType("h")
        self.h = constr
    
    def get_x(self, parent):
        val = self.x.get_val(self, parent)
        if not parent is None:
            val += parent.get_x()
        
        return val
    
    def get_y(self, parent):
        val = self.y.get_val(self, parent)
        if not parent is None:
            val += parent.get_y()
        
        return val
    
    def get_w(self, parent):
        return self.w.get_val(self, parent)
    
    def get_h(self, parent):
        return self.h.get_val(self, parent)
    
    def get_pos(self, parent):
        return Vec(self.get_x(parent), self.get_y(parent))
    
    def get_size(self, parent):
        return Vec(self.get_w(parent), self.get_h(parent))
    
    def get_shape(self, parent):
        return Rect(self.get_x(parent), self.get_y(parent), self.get_w(parent), self.get_h(parent))


class Constraint:
    def __init__(self, type_):
        self.type = type_

    def set_type(self, type_):
        self.type = type_

class Center(Constraint):
    def get_val(self, manager, parent):
        parent_size = parent.get_w() if self.type == "x" else parent.get_h()
        size = manager.get_w(parent) if self.type == "x" else manager.get_h(parent)

        return parent_size/2 - size/2

class Absolute(Constraint):
    def __init__(self, val, type_=None):
        super().__init__(type_)
        self.val = val
    
    def get_val(self, manager, parent):
        return self.val

class Relative(Constraint):
    def __init__(self, val, rel_type=None, type_=None):
        super().__init__(type_)
        self.val = val
        self.rel_type = rel_type
    
    def get_val(self, manager, parent):
        rel_type = self.rel_type
        if rel_type is None:
            rel_type = self.type
        
        val = 0

        if rel_type == "x":
            val = parent.get_x()
        elif rel_type == "y":
            val = parent.get_y()
        elif rel_type == "w":
            val = parent.get_w()
        elif rel_type == "h":
            val = parent.get_h()
        
        return self.val * val

class Aspect(Constraint):
    def __init__(self, val, type_):
        super().__init__(type_)
        self.val = val
    
    def get_val(self, manager, parent):
        val = manager.get_w(parent) if self.type == "h" else manager.get_h(parent)
        
        return self.val * val

class Math(Constraint):
    def __init__(self, val1, val2, op):
        super().__init__()
        self.val1 = val1
        self.val2 = val2
        self.op = op
    
    def get_val(self, manager, parent):
        v1 = self.val1.get_val(manager, parent)
        v2 = self.val2.get_val(manager, parent)

        if self.op == "+":
            return v1+v2
        
        if self.op == "-":
            return v1-v2
    
    def set_type(self, type_):
        super().set_type(type_)
        self.val1.set_type(type_)
        self.val2.set_type(type_)