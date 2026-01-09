import json, re
from os import listdir
from os.path import isfile, join


data_dir = "./data/json/"
result_dir = "./data/json/"
onlyfiles = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]



for file in onlyfiles:
    
    occurrences : list[dict] = []
    suprrimes : int = 0
    with open(data_dir+file, "r", encoding="utf-8") as f:
        phrases : list[dict[str,any]]= json.load(f)
        for p in phrases:
            n1 : str = p["n1"]
            det : int = p["det"]
            n2 : str = p["n2"]
            present = False
            for d in occurrences:
                if n1 == d["n1"] and n2 == d["n2"] and det == d["det"]:
                    present = True
                    suprrimes += 1
            if not present:
                occurrences.append(p)
    print(str(file)+ " " + str(suprrimes) + " lignes supprimes")
    with open(result_dir+file, "w", encoding="utf-8") as f:
        json.dump(occurrences, f, ensure_ascii=False, indent=4)