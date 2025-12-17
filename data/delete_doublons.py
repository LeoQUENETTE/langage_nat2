import os, json

data_dir = "./json/"
file_name_list = [
    "Agent","AuteurCréateur","Caractérisation","Conséquence","Despiction",
    "Holonymie","LienSocial","Lieu","Matière","Origine","Quantification","Topic"
]

os.makedirs(data_dir, exist_ok=True)

for file in file_name_list:
    file_pwd = os.path.join(data_dir, file + ".json")
    
    print("")
    print(f"=============== {file} ===============")
    print("")
    if not os.path.isfile(file_pwd):
        print(f"Fichier introuvable : {file_pwd}")
        continue
    
    one_occurence : list = []
    with open(file_pwd, "r", encoding="utf-8") as f:
        data = json.load(f)
        for object in data:
            for k,v in object.items():
                object[k] = v.lower()
            n = 0
            not_found = True
            while n < len(one_occurence) and not_found:
                if one_occurence[n] == object:
                    not_found = False
                n+= 1
            if not_found == True:
                one_occurence.append(object)
                
                
    with open(file_pwd, "w", encoding="utf-8") as f:
        print(str(len(one_occurence)) + " lignes crées")
        json.dump(one_occurence, f, ensure_ascii=False, indent=4)