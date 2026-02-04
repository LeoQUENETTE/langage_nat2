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
    
    vector = generateVector(parsed_phrase)
    
    files = [f for f in os.listdir(TRAIN_DIR) if os.path.isfile(os.path.join(TRAIN_DIR, f))]
    answers = {}
    for f in files:
        racine : Noeud = decode(TRAIN_DIR+f)
        val = produitscalaire(vector, racine.valeur)
        answers[val] = f"{f} : {val}"

    for _, v in dict(sorted(answers.items(), reverse=True)).items():
        print(v)
        
if __name__ == "__main__":
    
    phrase ="juge des enfants"
    print(f"\nPhrase choisie : {phrase}\n")
    prediction(phrase)
    
    
    
    # #train("Agent.json") 
    # train("AuteurCréateur.json")
    # #train("Caractérisation.json")
    # train("Conséquence.json")
    # train("Despiction.json")
    # train("Holonymie.json")
    # #train("Instrument.json")
    # train("LienSocial.json")
    # train("Lieu.json")
    # train("Matière.json")
    # train("Origine.json")
    # train("Patient.json")
    # train("Possession.json")
    # train("Quantification.json")
    # train("Topic.json")
    
    # files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    # for filename in files:
    #     with open(DATA_DIR+filename,"r",encoding="utf8") as f:
    #         train(f)
