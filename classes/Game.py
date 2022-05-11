#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

class Game:
    """
    Main class managing the interface, world rendering and simulation
    """

    def __init__(self):
        pass

    def mainloop(self):
        """Main game loop, calls the simulation and rendering functions"""

        while True:
            self.handle_events()
            self.physics()
            self.render()
    
    def handle_events(self):
        """Handle events triggered during this game loop"""

        pass

    def physics(self):
        """Processes physic simulation"""

        pass
    
    def render(self):
        """Renders the game"""
        
        pass