from calcul_vectoriel import *

DATA_DIR = "./data/json/"
RELATIONS_FILES_NAME = {"Agent":"24",
                        "AuteurCréateur":"",
                        "Caractérisation":"23",
                        "Conséquence":"41",
                        "Despiction":"",
                        "Holonymie":"10",
                        "LienSocial":"",
                        "Lieu":"28",
                        "Matière":"50",
                        "Origine":"",
                        "Quantification":"",
                        "Topic":"",
                        "Instrument":"25",
                        "Patient":"14",
                        "Possession" : "121"}
if __name__ == "__main__":
    generateVector(DATA_DIR + "Agent" + ".json",RELATIONS_FILES_NAME["Agent"])
    
    