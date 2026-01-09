import json, re
from os import listdir
from os.path import isfile, join

DATA_DIR = "./data/"
TSV_DIR = DATA_DIR+"data_tsv_txt/"
TXT_DIR = DATA_DIR+"data_txt/"
F_DIR = DATA_DIR+"data_f/"

DATA_DIRS = [TXT_DIR, TSV_DIR, F_DIR]
RESULT_DIR = "./data/json/"
      
      
def parse_txt_to_json(phrase : str) -> dict:
    dets = {"de" : 0, "d'un" : 0, "d'une" : 0, "d'" : 0,
            "de la" : 1, "du" : 1, "de l'" : 1,
            "des" : 2}
    formatJSON = {}
    pattern = r"(\sdu\s|\sdes\s|\sd'|\sde la\s|\sde l'|\sde\s)"
    phrase = phrase.replace("-" ,"").replace("’","'").replace("\n","")
    groups = re.search(pattern, phrase)
    if groups == None:
        print(phrase)
        return None
    phrase_coupe = phrase.split(groups[1])
    gauche = phrase_coupe[0].replace('"',"")
    gauche = re.sub(r"^(le\s|la\s|les\s|l'|un\s|une\s|des\s|mon\s|ton\s|son\s|notre\s|votre\s|nos\s|vos\s)", "", gauche, flags=re.IGNORECASE)
    centre = groups[1].strip()
    droite = phrase_coupe[1]
    if (droite == None): 
        droite = centre.replace("d\'", "")
        centre = "d'"
    droite = re.sub(r"^(le\s|la\s|les\s|l'|un\s|une\s|des\s|mon\s|ton\s|son\s|notre\s|votre\s|nos\s|vos\s)", "", droite, flags=re.IGNORECASE)
    formatJSON["n1"] = gauche.strip()
    formatJSON["n2"] = droite.strip()
    formatJSON["det"] = dets[centre]
    return formatJSON

def parse_all_files():
    c = 0
    for dir in DATA_DIRS:
        files = [f for f in listdir(dir) if isfile(join(dir, f))]
        for filename in files:
            result = []
            print(dir + filename)
            with open(dir+filename, "r" , encoding="utf8") as f:
                phrases = f.readlines()
                for phrase in phrases:
                    formatJSON = parse_txt_to_json(phrase)
                    if formatJSON:
                        result.append(formatJSON)
                f.close()
            if c != 0:
                with open(RESULT_DIR+filename.replace(".txt",".json"), "r", encoding="utf8") as f: 
                    already_in_data = json.load(f)
                    result = already_in_data + result
            with open(RESULT_DIR+filename.replace(".txt",".json"), "w", encoding="utf8") as f:
                json.dump(result,f, ensure_ascii=False, indent =4)
                f.close()
        c += 1
                
if __name__=="__main__":
    parse_all_files()
            
            