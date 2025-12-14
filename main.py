from calcul_vectoriel import *
import api

DATA_DIR = "./data/json/"
RELATIONS_FILES_NAME = {"Agent":"70",
                        "AuteurCréateur":"54",
                        "Caractérisation":"173",
                        "Conséquence":"42",
                        "Despiction":"172",
                        "Holonymie":"10",
                        "LienSocial":"113",
                        "Lieu":"15",
                        "Matière":"50",
                        "Origine":"171",
                        "Quantification":"58",
                        "Topic":"142",
                        "Instrument":"139",
                        "Patient":"76",
                        "Possession" : "122"}
if __name__ == "__main__":
    # api.getNodeById("465544042")
    generateVector(DATA_DIR + "Agent" + ".json")
    
    
