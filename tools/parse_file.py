from pathlib import Path
import spacy, re
import spacy

LIVRE_PATH = "./data/livres/"
RESULT_PATH = "./tools/parsed/"


def extraire_groupes_nominaux(texte):
    """
    Extrait tous les groupes nominaux d'un texte en français.
    
    Args:
        texte (str): Le texte à analyser
    
    Returns:
        list: Liste des groupes nominaux trouvés
    """
    # Charger le modèle français de spaCy
    try:
        nlp = spacy.load("fr_core_news_sm")
    except OSError:
        print("Le modèle français n'est pas installé.")
        print("Installez-le avec: python -m spacy download fr_core_news_sm")
        return []
    
    # Analyser le texte
    doc = nlp(texte)
    
    groupes_nominaux = []
    
    # Extraire les chunks nominaux
    for chunk in doc.noun_chunks:
        groupes_nominaux.append({
            'texte': chunk.text,
            'racine': chunk.root.text,
            'pos': chunk.root.pos_,
            'debut': chunk.start_char,
            'fin': chunk.end_char
        })
    
    return groupes_nominaux


def afficher_groupes_nominaux(groupes_nominaux):
    """
    Affiche les groupes nominaux de manière formatée.
    
    Args:
        groupes_nominaux (list): Liste des groupes nominaux
    """
    if not groupes_nominaux:
        print("Aucun groupe nominal trouvé.")
        return
    
    print(f"\n{'='*60}")
    print(f"GROUPES NOMINAUX TROUVÉS ({len(groupes_nominaux)})")
    print(f"{'='*60}\n")
    
    for i, gn in enumerate(groupes_nominaux, 1):
        print(f"{i}. '{gn['texte']}'")
        print(f"   → Racine: {gn['racine']} ({gn['pos']})")
        print(f"   → Position: {gn['debut']}-{gn['fin']}\n")

def convert_txt_into_str(file_path : str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8")  as f:
            return f.read().replace("“", '"').replace("”", '"').replace("\n", " ").replace("’", "'")
    except FileNotFoundError:
        print("Le fichier est introuvable")
        
def enregistrer_resultat(book_path : str, book_name : str):
    texte = convert_txt_into_str(book_path)
    results = find_pattern_in_texte(texte)
    with open(RESULT_PATH+book_name, "w", encoding="utf8") as f :
        for ligne in results:
            f.write(ligne)
def find_pattern_in_texte(texte : str) -> set[str]:
    pattern = r"^(de|du|des|d\')$"
    groupes_nominaux = extraire_groupes_nominaux(texte)
    res_set : set[str] = set()
    for i, gn in enumerate(groupes_nominaux, 0):
        if i + 1 >= len(groupes_nominaux): return res_set
        
        entre_deux_gn_str = texte[gn['fin']:groupes_nominaux[i + 1]['debut']]
        entre_deux_gn = entre_deux_gn_str.split(" ")
        entre_deux_gn = [x for x in entre_deux_gn if x != '']
        if len(entre_deux_gn) != 1: continue
        
        mot  = entre_deux_gn[0]
        if re.match(pattern, mot, re.IGNORECASE) == None: continue
        
        res_set.add(f"{gn['texte']}{entre_deux_gn_str}{groupes_nominaux[i + 1]['texte']}\n")
    return res_set

if __name__ == "__main__":
    livre_dossier = Path(LIVRE_PATH)
    for f in livre_dossier.glob("*.txt"):
        enregistrer_resultat(f, f.name)