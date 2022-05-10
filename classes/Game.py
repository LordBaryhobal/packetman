#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

class Game:
    """
    Main class managing the interface, world rendering and simulation
    """

    def __init__(self) -> None:
        pass

    #Main game loop, calls the simulation and rendering functions
    def mainloop(self) -> None:
        while True:
            self.handle_events()
            self.physics()
            self.render()
    
    #Handle events triggered during this game loop
    def handle_events(self) -> None:
        pass

    #Processes physic simulation
    def physics(self) -> None:
        pass
    
    #Renders the game
    def render(self) -> None:
        pass