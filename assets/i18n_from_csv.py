#Packetman is a small game created in the scope of a school project
#Copyright (C) 2022  Louis HEREDERO & Mathéo BENEY

import csv
import json
import os

path = os.path.join("assets", "translations.csv")

flat = True

with open(path, "r") as f:
    reader = csv.reader(f)
    headers = next(reader)
    langs = [{} for _ in range(len(headers)-2)]

    for row in reader:
        elmts = row[1].split(".")
        
        for i in range(len(langs)):
            if flat:
                langs[i][row[1]] = row[i+2]
            
            else:
                d = langs[i]
                for e in elmts[:-1]:
                    if not e in d:
                        d[e] = {}
                
                    d = d[e]
            
                d[elmts[-1]] = row[i+2]
    
    for l, lang in enumerate(headers[2:]):
        with open(os.path.join("assets", "i18n", lang+".json"), "w") as lang_file:
            json.dump(langs[l], lang_file, indent=4)