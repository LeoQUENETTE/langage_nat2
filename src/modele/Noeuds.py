from .Vecteur import *
import pickle
class Noeud:
    __slots__ = ("valeur", "nom", "gauche", "droite")
    def __init__(self, valeur : list[tuple[str, float]], nom : str = None):
        self.valeur : list[list] = valeur
        self.nom : str = nom
        self.gauche : Noeud = None
        self.droite : Noeud = None
    def encode(self, filename : str):
        with open(filename+".pkcl", "wb") as f:
            pickle.dump(self, f)
    

def fusionnerNoeuds(noeud1 : Noeud, noeud2 : Noeud, nomNoeud : str, valeur : tuple[int, float]) -> Noeud:
    '''
    fusionner : Fonction créant un nouveau noeud avec deux feuilles, une à gauche et une à droite.
    '''
    parent = Noeud(valeur) 
    parent.nom = nomNoeud
    parent.gauche = noeud1
    parent.droite = noeud2
    return parent

def creationNoeudDepart(listeVecteur : list) -> list[Noeud]:
    '''
    creationNoeudDepart : Fonction permettant de créer une liste de noeuds à partir de la liste des vecteurs de relations
    ''' 
    noeuds = []
    for i, v in enumerate(listeVecteur): # i l'indice du vecteur et v le vecteur contenant le vecteur de A et de B
        noeuds.append(Noeud(v, nom=f"f{i}"))
    return noeuds



def parcours_choix(noeud : Noeud, cible : Noeud, cpt : int = 0) -> float: # noeud doit être égal à la racine, cpt est le nombre de boucle, cible est le vecteur normé à comparer
    # TODO fonction récursive, problème potentielle de pile, faire attention
    '''
    parcours_choix : Fonction récursive parcourant l'arbre des noeuds afin de rechercher le noeuds ayant la valeur la plus proche de celle du noeud cible.
    '''
    if noeud is None:
        return None
    
    # Valeurs actuelles
    val_actuelle = produitscalaire(noeud.valeur, cible)
    
    if cpt == 0 and val_actuelle<0.1: # On est donc à la racine ici
        return None
    
    val_gauche = produitscalaire(noeud.gauche.valeur,cible) if noeud.gauche else float('-inf') 
    val_droite = produitscalaire(noeud.droite.valeur,cible) if noeud.droite else float('-inf')

    # On cherche la valeur max parmi les trois
    max_val = max(val_actuelle, val_gauche, val_droite)

    # Décision
    if max_val == val_actuelle:
        # On garde ce noeud
        return val_actuelle
    elif max_val == val_gauche:
        # On descend à gauche
        return parcours_choix(noeud.gauche, cible,cpt+1)
    else:
        # On descend à droite
        return parcours_choix(noeud.droite, cible,cpt+1)

# Formules mathématiques
# cosinus et matrice
# On prend le vecteur le plus petit
# On fait produit scalaire divisé par produit des normes des trucs en commun A de B et C de D 
# Cosinus de A avec C et de B avec D
# Matrice pour chaque correspondance
# moyenne arithmétique et on renorme et on met à jour la matrice.