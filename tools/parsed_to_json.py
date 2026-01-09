from pathlib import Path
import re

JSON_DIR :str = "./tools/parsed_json/"
PARSED_DIR : str = "./tools/parsed/"

def convert_txt_json(file_path : str, file_name : str):
    lines : list[str] = []
    pattern = r"^(.+?)\s+((?:du|de|des|d\'\w+))(?:\s+(.+))?$"
    with open(file_path, "r", encoding="utf8") as f:
        lines = f.readlines()
    taille = len(lines)
    c = 0
    with open(JSON_DIR+file_name+".json", "w", encoding="utf8") as f:
        f.write("[\n")
        for l in lines:
            c+=1
            l = l.replace("-" ,"")
            groups = re.match(pattern, l)
            if groups == None:print(l);continue
            partie_gauche = groups[1].replace('"',"")
            centre = groups[2]
            partie_droite = groups[3]
            if (partie_droite == None): partie_droite = centre.replace("d\'", ""); centre = "d'"
            f.write("\t{" + f'"n1" : "{partie_gauche}", "det" : "{centre}" ,"n2" : "{partie_droite}"' + "}")
            if c < taille:
                f.write(",\n")
        f.write("\n]")
            

if __name__ == "__main__":
    parsed_folder = Path(PARSED_DIR)
    for f in parsed_folder.glob("*.txt"):
        convert_txt_json(f, f.name.replace(".txt",""))