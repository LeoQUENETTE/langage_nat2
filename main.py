from calcul_vectoriel import *

DATA_DIR = "./data/"
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


if __name__ == "__main__":
    generateVector(DATA_DIR + "dataset2" + ".json")
