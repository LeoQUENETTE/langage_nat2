import os, json

data_dir = "./json/"
file_name_list = [
    "Agent","AuteurCréateur","Caractérisation","Conséquence","Despiction",
    "Holonymie","LienSocial","Lieu","Matière","Origine","Quantification","Topic"
]

os.makedirs(data_dir, exist_ok=True)

for file in file_name_list:
    file_pwd = os.path.join(data_dir, file + ".json")
    
    if not os.path.isfile(file_pwd):
        print(f"Fichier introuvable : {file_pwd}")
        continue
    
    with open(file_pwd, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(file + " : " + str(len(data)))