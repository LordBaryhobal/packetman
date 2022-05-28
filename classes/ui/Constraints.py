#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Copyable import Copyable
from classes.Rect import Rect
from classes.Vec import Vec

class Manager(Copyable):
    """Constraints manager
    
    Holds Constraint objects for x, y, w and h values.
    """

    def __init__(self):
        """Initializes a Manager instance"""

        self.x = Absolute(0, "x")
        self.y = Absolute(0, "y")
        self.w = Absolute(0, "w")
        self.h = Absolute(0, "h")
    
    def set_x(self, constr):
        """Sets the x constraint

        Arguments:
            constr {Constraint} -- constraint to set

        Returns:
            Manager -- self, to make this method chainable
        """

        constr.set_type("x")
        self.x = constr
        return self
    
    def set_y(self, constr):
        """Sets the y constraint

        Arguments:
            constr {Constraint} -- constraint to set

        Returns:
            Manager -- self, to make this method chainable
        """
        
        constr.set_type("y")
        self.y = constr
        return self
    
    def set_w(self, constr):
        """Sets the w constraint

        Arguments:
            constr {Constraint} -- constraint to set

        Returns:
            Manager -- self, to make this method chainable
        """
        
        constr.set_type("w")
        self.w = constr
        return self
    
    def set_h(self, constr):
        """Sets the h constraint

        Arguments:
            constr {Constraint} -- constraint to set

        Returns:
            Manager -- self, to make this method chainable
        """
        
        constr.set_type("h")
        self.h = constr
        return self
    
    def get_x(self, parent):
        """Computes the x value

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            float -- computed value
        """

        val = self.x.get_val(self, parent)
        if not parent is None:
            val += parent.get_x()
        
        return val
    
    def get_y(self, parent):
        """Computes the y value

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            float -- computed value
        """
        
        val = self.y.get_val(self, parent)
        if not parent is None:
            val += parent.get_y()
        
        return val
    
    def get_w(self, parent):
        """Computes the w value

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            float -- computed value
        """
        
        return self.w.get_val(self, parent)
    
    def get_h(self, parent):
        """Computes the h value

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            float -- computed value
        """
        
        return self.h.get_val(self, parent)
    
    def get_pos(self, parent):
        """Computes the position (x,y)

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            Vec -- computed value
        """
        
        return Vec(self.get_x(parent), self.get_y(parent))
    
    def get_size(self, parent):
        """Computes the size (w,h)

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            Vec -- computed value
        """
        
        return Vec(self.get_w(parent), self.get_h(parent))
    
    def get_shape(self, parent):
        """Computes the bounding box (x,y,w,h)

        Arguments:
            parent {Component} -- this component's parent

        Returns:
            Rect -- computed value
        """
        
        return Rect(self.get_x(parent), self.get_y(parent), self.get_w(parent), self.get_h(parent))
    
    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.w}, {self.h}]"

class Constraint(Copyable):
    """Basic constraint class, parent of all constraint types"""

    def __init__(self, type_=None):
        """Initializes a Constraint instance

        Keyword Arguments:
            type_ {str} -- type of constraint, one of: "x", "y", "w", "h" (default: {None})
        """

        self.type = type_

    def set_type(self, type_):
        """Sets this constraint's type

        Arguments:
            type_ {str} -- new type (see `__init__` for possible values)
        """

        self.type = type_
    
    def __repr__(self):
        return f"<{self.__class__.__name__} Constraint>"

class Center(Constraint):
    """Centers the element on the given axis"""

    def get_val(self, manager, parent):
        """Computes the value

        Arguments:
            manager {Manager} -- manager to which this constraint belongs
            parent {Component} -- the component's parent

        Returns:
            float -- computed value
        """

        parent_size = parent.get_w() if self.type == "x" else parent.get_h()
        size = manager.get_w(parent) if self.type == "x" else manager.get_h(parent)

        return parent_size/2 - size/2

class Absolute(Constraint):
    """Returns a constant value"""

    def __init__(self, val=0, type_=None):
        """Initializes an Absolute instance

        Keyword Arguments:
            val {float} -- constant value (default: {0})
            type_ {str} -- type of constraint (see `Constraint.__init__` for possible values) (default: {None})
        """

        super().__init__(type_)
        self.val = val
    
    def get_val(self, manager, parent):
        """Computes the value

        Arguments:
            manager {Manager} -- manager to which this constraint belongs
            parent {Component} -- the component's parent

        Returns:
            float -- computed value
        """
        
        return self.val

class Relative(Constraint):
    """Returns a value proportional to a parent's value"""

    def __init__(self, val=1, rel_type=None, type_=None):
        """Initializes a Relative instance

        Keyword Arguments:
            val {float} -- ratio with parent's value (default: {1})
            rel_type {str} -- type of parent's value (see `type_` for possible values) (default: {None})
            type_ {str} -- type of constraint (see `Constraint.__init__` for possible values) (default: {None})
        """
        
        super().__init__(type_)
        self.val = val
        self.rel_type = rel_type
    
    def get_val(self, manager, parent):
        """Computes the value

        Arguments:
            manager {Manager} -- manager to which this constraint belongs
            parent {Component} -- the component's parent

        Returns:
            float -- computed value
        """
        
        rel_type = self.rel_type
        if rel_type is None:
            rel_type = self.type
        
        val = 0

        if rel_type == "x": val = parent.get_x()
        elif rel_type == "y": val = parent.get_y()
        elif rel_type == "w": val = parent.get_w()
        elif rel_type == "h": val = parent.get_h()
        
        return self.val * val

class Aspect(Constraint):
    """Returns a value proportional to it's complementary value (width / height)"""
    
    def __init__(self, val=1, type_=None):
        """Initializes a Relative instance

        Keyword Arguments:
            val {float} -- aspect ratio (default: {1})
            type_ {str} -- type of constraint (see `Constraint.__init__` for possible values) (default: {None})
        """
        
        super().__init__(type_)
        self.val = val
    
    def get_val(self, manager, parent):
        """Computes the value

        Arguments:
            manager {Manager} -- manager to which this constraint belongs
            parent {Component} -- the component's parent

        Returns:
            float -- computed value
        """
        
        val = manager.get_w(parent) if self.type == "h" else manager.get_h(parent)
        
        return self.val * val

class Math(Constraint):
    """Returns a value computed from two other constraints using an operator"""

    def __init__(self, val1=None, val2=None, op=""):
        """Initializes a Math instance

        Keyword Arguments:
            val1 {Constraint} -- first constraint (default: {None})
            val2 {Constraint} -- second constraint (default: {None})
            op {str} -- operation to apply between the two constraints (default: {""})
        """
        
        super().__init__()
        self.val1 = val1
        self.val2 = val2
        self.op = op
    
    def get_val(self, manager, parent):
        """Computes the value

        Arguments:
            manager {Manager} -- manager to which this constraint belongs
            parent {Component} -- the component's parent

        Returns:
            float -- computed value
        """

        if self.val1 is None or self.val2 is None or self.op == "":
            return 0
        
        v1 = self.val1.get_val(manager, parent)
        v2 = self.val2.get_val(manager, parent)

        if self.op == "+":
            return v1+v2
        
        if self.op == "-":
            return v1-v2
    
    def set_type(self, type_):
        """Sets this constraint's type

        Also sets the types of the child constraints

        Arguments:
            type_ {str} -- new type (see `__init__` for possible values)
        """

        super().set_type(type_)
        self.val1.set_type(type_)
        self.val2.set_type(type_)