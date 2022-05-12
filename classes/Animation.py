#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import time

class Animation:
    """
    Class used to animate attribute values of a particular object.
    Examples of use:
    - camera movement
    - color transition
    - tile movements
    """

    FLOAT = 0
    INT = 1

    FORWARDS = 0
    ALTERNATE = 1

    def __init__(self, obj, attr_, val_a, val_b, duration, start=True, loop=None, type_=FLOAT):
        """Initializes an Animation object
        @param obj: object to animate
        @param attr_: name of the attribute to animate
        @param val_a: value at the start of the animation
        @param val_b: value at the end of the animation
        @param duration: duration in seconds of the animation
        @param start: (default: True) True if animation should start automatically
        @param loop: (default: None) type of looping. One of:
            - None: no loop
            - Animation.FORWARDS: loops back to beginning when reaching the end
            - Animation.ALTERNATE: loops back and forth
        @param type_: (default: Animation.FLOAT) type of the animated value. One of:
            - Animation.FLOAT
            - Animation.INT
        """

        self.obj = obj
        self.attr = attr_
        self.val_a = val_a
        self.val_b = val_b
        self.duration = duration
        self.loop = loop
        self.type = type_
        self.start_time = None
        self.finished = False

        if start:
            self.start()
    
    def start(self):
        """Starts the animation. Returns True if successful, False otherwise"""

        if self.start_time is None:
            self.finished = False
            self.start_time = time.time()
            return True
        
        return False
    
    def update(self):
        """
        Updates the value at the current time,
        stopping the animation if completed
        """

        t = time.time()
        ratio = (t-self.start_time)/self.duration

        if ratio > 1:
            if self.loop is None:
                self.finished = True
                return
            
            elif self.loop == Animation.FORWARDS:
                ratio %= 1
            
            elif self.loop == Animation.ALTERNATE:
                ratio = 1 - abs((ratio%2) - 1)
        
        val = ratio

        if self.type == Animation.FLOAT:
            val = ratio*(self.val_b - self.val_a) + self.val_a

        elif self.type == Animation.INT:
            val = int( ratio*(self.val_b - self.val_a) + self.val_a)
        
        setattr(self.obj, self.attr, val)