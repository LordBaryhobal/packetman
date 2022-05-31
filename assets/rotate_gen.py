#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import numpy as np
from PIL import Image

name = input("name: ")
img = Image.open(f"./textures/{name}.png")
a = np.array(img)

for y in range(2):
    for i in range(1,4):
        a[y*32:y*32+32,i*32:i*32+32] = np.rot90(a[y*32:y*32+32,0:32], -i)

img.close()
img = Image.fromarray(a)
img.save(f"./textures/{name}.png")