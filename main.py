from calcul_vectoriel import *
import api

DATA_DIR = "./data/json/"
RELATIONS_FILES_NAME = {"Agent":"24",
                        "AuteurCréateur":"54",
                        "Caractérisation":"23",
                        "Conséquence":"41",
                        "Despiction":"172",
                        "Holonymie":"10",
                        "LienSocial":"113",
                        "Lieu":"28",
                        "Matière":"50",
                        "Origine":"171",
                        "Quantification":"58",
                        "Topic":"142",
                        "Instrument":"25",
                        "Patient":"14",
                        "Possession" : "121"}
if __name__ == "__main__":
    generateVector(DATA_DIR + "Agent" + ".json",RELATIONS_FILES_NAME["Agent"])
    
    
