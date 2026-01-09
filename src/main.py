from modele.Matrice import *
import re,os
from api import *

DATA_DIR = "./data/json/"
TRAIN_DIR = "./saved_trainings/"
RELATIONS_FILES_NAME = {"Agent":"70",           #r_processus>agent
                        "AuteurCréateur":"54",  #r_product_of
                        "Caractérisation":"173",#r_has_prop-1
                        "Conséquence":"42",     #r_has_causatif
                        "Despiction":"172",     #r_depict
                        "Holonymie":"10",       #r_holo
                        "LienSocial":"113",     #r_has_social_ties_with
                        "Lieu":"15",            #r_lieu
                        "Matière":"50",         #r_object>mater
                        "Origine":"171",        #r_lieu>origin
                        "Quantification":"174", #r_quantificateur-1
                        "Topic":"142",          #r_has_topic
                        "Instrument":"139",     #r_processus>instr-1
                        "Patient":"76",         #r_processus>agent
                        "Possession" : "122"}   #r_own-1



def train(filename : str): 
    # Je crois que je peux pas réentrainer à partir d'un arbre déjà existant car les données json sur lesquel le premier arbre à été créer 
    # sont aussi présentes dans les nouvelles données 
    
    # ancienne_racine = decode(train_dir+filename)
    # print(ancienne_racine)
    
    vecteurs = generateAllVectorsFromFile(str(DATA_DIR) + filename)
    racine : Noeud = constructionArbre(vecteurs)
    racine.encode(TRAIN_DIR+filename.replace(".json",""))
def decode(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)
def parse_txt_to_json(phrase : str) -> dict:
    dets = {"de" : 0, "d'un" : 0, "d'une" : 0, "d'" : 0,
            "de la" : 1, "du" : 1, "de l'" : 1,
            "des" : 2}
    formatJSON = {}
    pattern = r"(du\s|des\s|d'|de la\s|de l'|de\s)"
    phrase = phrase.replace("-" ,"").replace("’","'").replace("\n","")
    groups = re.search(pattern, phrase)
    if groups == None:
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
    formatJSON["n1"] = gauche
    formatJSON["n2"] = droite
    formatJSON["det"] = dets[centre]
    return formatJSON
def prediction(phrase : str):
    parsed_phrase = parse_txt_to_json(phrase)
    
    print(parsed_phrase["n1"],end=" ")
    print(parsed_phrase["det"],end=" ")
    print(parsed_phrase["n2"])
    
    vector = generateVector(parsed_phrase)
    
    files = [f for f in os.listdir(TRAIN_DIR) if os.path.isfile(os.path.join(TRAIN_DIR, f))]
    for f in files:
        racine : Noeud = decode(TRAIN_DIR+f)
        print(f"{f} : {produitscalaire(vector, racine.valeur)}")
        
if __name__ == "__main__":
    prediction("vitesse du guépard") 
    # train("Caractérisation.json")
    
    # files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    # for filename in files:
    #     with open(DATA_DIR+filename,"r",encoding="utf8") as f:
    #         train(f)
