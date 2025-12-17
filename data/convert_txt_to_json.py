import os
import json
import re

data_dir = "./data_txt"
file_name_list = [
    "Agent","AuteurCréateur","Caractérisation","Conséquence","Despiction",
    "Holonymie","LienSocial","Lieu","Matière","Origine","Quantification","Topic"
]
target_dir = "json/"

os.makedirs(target_dir, exist_ok=True)

def parse_phrase(phrase: str):
    """
    Parse une phrase du type :
    "Entraînement du sportif"
    et renvoie {"n1": "...", "det": "...", "n2": "..."}
    
    Gère les déterminants : du, de la, de l', des, d', de, d'un, de l', etc.
    """
    # Liste des déterminants possibles (triés par longueur décroissante)
    determiners = [
        "de la", "de l'", "de le", "de les", "d'un", "du", "des", "d'", "de", 
        "à la", "à l'", "au", "aux", "à", "par", "pour"
    ]
    
    # Cherche le premier déterminant qui apparaît dans la phrase
    found_det = None
    det_start = -1
    
    for det in determiners:
        # Pour "d'" on cherche le motif " d'"
        if det == "d'":
            pattern = r'\sd\''
        else:
            pattern = r'\s' + re.escape(det) + r'\s'
        
        match = re.search(pattern, ' ' + phrase + ' ', re.IGNORECASE)
        if match:
            found_det = det
            det_start = match.start()
            break
    
    if found_det is None:
        # Si aucun déterminant n'est trouvé, essaye une approche par défaut
        parts = phrase.split()
        if len(parts) >= 3:
            # Prend le dernier mot comme n2, l'avant-dernier comme det, et le reste comme n1
            n2 = parts[-1]
            det = parts[-2]
            n1 = " ".join(parts[:-2])
            return {"n1": n1, "det": det, "n2": n2}
        return None
    
    # Extrait les parties de la phrase
    n1_part = phrase[:det_start].strip()
    n2_part = phrase[det_start + len(found_det):].strip()
    
    # Nettoie n1_part pour enlever les déterminants initiaux (le, la, l', les, un, une, des)
    n1_clean = re.sub(r'^(le |la |l\'|les |un |une |des )', '', n1_part, flags=re.IGNORECASE)
    
    # Si n1_clean est vide, utilise n1_part
    if not n1_clean:
        n1_clean = n1_part
    
    # Pour le déterminant "d'", on nettoie n2_part pour enlever l'apostrophe initiale si présente
    if found_det == "d'" and n2_part.startswith("'"):
        n2_part = n2_part[1:]
    
    return {"n1": n1_clean, "det": found_det, "n2": n2_part}

for file in file_name_list:
    file_pwd = os.path.join(data_dir, file + ".txt")
    
    if not os.path.isfile(file_pwd):
        print(f"Fichier introuvable : {file_pwd}")
        continue
    
    results = []
    with open(file_pwd, "r", encoding="utf-8") as f:
        for line in f:
            phrase = line.strip()
            if not phrase:
                continue

            parsed = parse_phrase(phrase)
            if parsed:
                results.append(parsed)
    
    # Sauvegarde en JSON
    out_path = os.path.join(target_dir, file + ".json")
    with open(out_path, "w", encoding="utf-8") as jf:
        json.dump(results, jf, ensure_ascii=False, indent=4)
    
    print(f"JSON créé : {out_path} ({len(results)} entrées)")