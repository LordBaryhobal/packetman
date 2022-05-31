#!/usr/bin/env python3

#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

from classes.Game import Game

if __name__ == "__main__":
    print("Packetman  Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY")
    Game.instance.mainloop()