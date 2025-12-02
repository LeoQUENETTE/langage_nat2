import re
import spacy

nlp = spacy.load("fr_core_news_sm")

def extract_gn_before(sentence_doc, match_token_idx):
    """Extrait le GN avant le match dans le contexte de la phrase"""
    gn = []
    types = []
    
    # Parcourir les tokens avant le match dans la phrase
    for tok in reversed(sentence_doc[:match_token_idx]):
        if tok.pos_ in ("DET", "ADJ", "ADV", "NOUN", "PROPN"):
            gn.insert(0, tok.text)
            types.insert(0, tok.pos_)
        else:
            break
    
    if "NOUN" in types or "PROPN" in types:
        return " ".join(gn)
    return None

def extract_gn_after(sentence_doc, match_token_idx):
    """Extrait le GN après le match dans le contexte de la phrase"""
    gn = []
    types = []
    
    # Parcourir les tokens après le match dans la phrase
    for tok in sentence_doc[match_token_idx + 1:]:
        if tok.pos_ in ("DET", "ADJ", "ADV", "NOUN", "PROPN"):
            gn.append(tok.text)
            types.append(tok.pos_)
        else:
            break
    
    if "NOUN" in types or "PROPN" in types:
        return " ".join(gn)
    return None

def get_sentence_for_token(doc, token_idx):
    """Trouve la phrase contenant le token et retourne (phrase_doc, position_dans_phrase)"""
    token = doc[token_idx]
    sentence = token.sent
    
    # Calculer la position du token dans sa phrase
    sentence_start = sentence.start
    position_in_sentence = token_idx - sentence_start
    
    return sentence, position_in_sentence

if __name__ == "__main__":
    path = "data/livres/"
    file_name = "test"
    pattern = r"\b(d'|de l'|de la|du|des|de)\b"
    
    try:
        with open(f"{path}{file_name}.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Nettoyer le texte
        clean_text = content.replace("\n", " ").replace("'", "'")
        
        # Analyser tout le texte avec spaCy
        doc = nlp(clean_text)
        
        valid_gn = []
        
        # Chercher tous les matchs du regex
        for match in re.finditer(pattern, clean_text, flags=re.IGNORECASE):
            match_text = match.group()
            char_start = match.start()
            
            # Trouver le token correspondant
            token_index = None
            for i, tok in enumerate(doc):
                if tok.idx == char_start:
                    token_index = i
                    break
            
            if token_index is None:
                continue
            
            # Obtenir la phrase contenant ce token
            sentence, pos_in_sentence = get_sentence_for_token(doc, token_index)
            
            # Extraire les GN avant et après dans le contexte de la phrase
            before_gn = extract_gn_before(sentence, pos_in_sentence)
            after_gn = extract_gn_after(sentence, pos_in_sentence)
            
            if before_gn and after_gn:
                # Nettoyer le GN après si nécessaire
                after_gn_clean = after_gn
                if after_gn.startswith("la "):
                    after_gn_clean = after_gn[3:]
                elif after_gn.startswith("l' "):
                    after_gn_clean = after_gn[3:]
                
                full_gn = f"{before_gn} {match_text} {after_gn_clean}"
                valid_gn.append(full_gn)
        
        # Afficher les résultats
        print(f"\n===== GN détectés [{len(valid_gn)}] =====\n")
        for gn in valid_gn:
            print(gn)
            
    except FileNotFoundError:
        print("Le fichier n'existe pas, vérifie le chemin ou le nom.")