#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

class Constraint:
    @property
    def val(self):
        return 0

class ConstantConstraint(Constraint):
    def __init__(self, val):
        super().__init__()
        self._val = val
    
    @property
    def val(self):
        return self._val

class RelativeConstraint(Constraint):
    def __init__(self, obj, attr, ratio):
        super().__init__()
        self.obj = obj
        self.attr = attr
        self.ratio = ratio
    
    @property
    def val(self):
        return self.ratio * getattr(self.obj, self.attr)