# Structure de listeVecteur :
# [v1,v2,v3,....]
# v1 = [vecteur de "A", vecteur de "de B"] pour la phrase "A de B"
# vecteur de "A" = [[nomrel1, val1],[nomrel2, val2],[nomrel3, val3],...,[nomreln, valn]]
import math



# Class Arbre et fonctions asssociées

class Noeud:
    def __init__(self, valeur, nom=None):
        self.valeur = valeur
        self.nom = nom
        self.gauche = None
        self.droite = None


def creationNoeudDepart(listeVecteur): #1000 vecteurs de départs 
    noeuds = []
    for i, v in enumerate(listeVecteur): # i l'indice du vecteur et v le vecteur contenant le vecteur de A et de B
        noeuds.append(Noeud(v, nom=f"f{i}"))
    return noeuds


def fusionner(noeud1, noeud2, nomNoeud, valeur):
    parent = Noeud(valeur) 
    parent.nom = nomNoeud
    parent.gauche = noeud1
    parent.droite = noeud2
    return parent


def parcours_choix(noeud, cible, cpt=0): # noeud doit être égal à la racine, cpt est le nombre de boucle, cible est le vecteur normé à comparer
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


def moyenneArithmétique (a,b) :
    return (a+b)/2

def norme(vecteur):
    # Calcule la norme du vecteur
    norme = 0
    for elt in vecteur :
        norme += elt[1]*elt[1] # 2 case contient la valeur
    return math.sqrt(norme)

def vecteurNorme(vecteurdepart):
    # Norme le vecteur (les deux parties du vecteur)
    for v in range(len(vecteurdepart)):
        vecteur = vecteurdepart[v]
        normevecteur = norme(vecteur)
        if normevecteur == 0:
            normevecteur =1
        for i in range(len(vecteur)) :
            vecteur[i][1] = vecteur[i][1]/normevecteur
        vecteurdepart[v] = vecteur
    return vecteurdepart

def produitscalaire(vecteur1depart,vecteur2depart):  # Cosinus ici
    resultatfinal = 0
    for v in range(len(vecteur1depart)): # On traite chaque vecteur séparement
        v1 = vecteur1depart[v]
        v2 = vecteur2depart[v]
        multiplicationTerme = 0
        for i in v1:
            for j in v2:
                if i[0]==j[0]: # regarde si le nom des relations est le même 
                    multiplicationTerme += i[1]*j[1]
        normeTest = norme(v1)*norme(v2)
        if normeTest == 0:
            normeTest =1
        resultat = multiplicationTerme / normeTest # division sert à rien car en soit la norme est 1
        resultatfinal += resultat
    return resultatfinal

def matrice(listeVecteurs): # la donner normé
    # calcul la matrice des cosinus
    n = len(listeVecteurs)
    matrice = [[0 for _ in range(n)] for _ in range(n)]
    for i in range (len(listeVecteurs)):
        for j in range (len(listeVecteurs)):
            if i != j :
                matrice[i][j] = produitscalaire(listeVecteurs[i],listeVecteurs[j])
            else :
                matrice[i][j] = 0  # Pour ne pas perturber le max
    return matrice
        
def maxMatriceIndices(matrice):
    max_val = float('-inf')
    indice_i, indice_j = -1, -1

    n = len(matrice)
    for i in range(n):
        for j in range(n):
            if i != j and matrice[i][j] > max_val:
                max_val = matrice[i][j]
                indice_i, indice_j = i, j

    return max_val, indice_i, indice_j

def fusionVecteur(v1depart,v2depart):
    # Renvoie la fusion norme des deux vecteurs
    Vcree = []
    for v in range(len(v1depart)):
        v1 = v1depart[v]
        v2 = v2depart[v]
        VcreePart = []
        listeTestV2 = []
        for i in v1:
            cpt = 0 # Pour tester si on trouve ou pas un vecteur correspondant
            for j in v2:
                if i[0]==j[0]: # regarde si le nom des relations est le même 
                    cpt = 1
                    VcreePart.append([i[0],moyenneArithmétique(i[1],j[1])])
                    listeTestV2.append(j)
            if cpt == 0 :
                VcreePart.append([i[0],i[1]/2])
        for j in v2:
            if j not in listeTestV2:
                VcreePart.append([j[0],j[1]/2])
        Vcree.append(VcreePart)
    Vcree = vecteurNorme(Vcree)
    return Vcree

def enlever_indices(matrice, indices):
    """
    Supprime les lignes et colonnes correspondant aux indices donnés.
    indices : liste d'indices à supprimer (ex : [i,j])
    """
    # On garde uniquement les lignes dont l'index n'est pas dans indices
    matrice_filtrée = [
        [val for k, val in enumerate(ligne) if k not in indices]
        for l, ligne in enumerate(matrice) if l not in indices
    ]
    return matrice_filtrée

def ajouter_ligne_colonne_zero(matrice):
    n = len(matrice)
    # Ajouter 0 à la fin de chaque ligne existante
    for ligne in matrice:
        ligne.append(0)
    # Ajouter une nouvelle ligne de zéros
    nouvelle_ligne = [0] * (n + 1) # Création d'une liste de taille n + 1 rempli de 0
    matrice.append(nouvelle_ligne)
    return matrice

def CalculDernierLigneColonneMatrice(matrice,listeVecteurs):
    #On ajoute la ligne et la colonne correspondant au vecteur rajouté. 
    matrice = ajouter_ligne_colonne_zero(matrice)
    n = len(listeVecteurs)  # taille après ajout du nouveau vecteur
    # Dernier vecteur ajouté
    dernier_vecteur = listeVecteurs[-1]
    for i in range(n - 1):  # on met à jour les valeurs avec tous les autres vecteurs
        valeur = produitscalaire(dernier_vecteur, listeVecteurs[i])
        matrice[i][n - 1] = valeur  # dernière colonne
        matrice[n - 1][i] = valeur  # dernière ligne
    # diagonale = 0
    matrice[n - 1][n - 1] = 0
    return matrice

def constructionArbre(listeVecteurs) :
    cptNomNoeud = len(listeVecteurs)
    NoeudEnCours = creationNoeudDepart(listeVecteurs)
    for i in range(len(listeVecteurs)) :
        listeVecteurs[i] = vecteurNorme(listeVecteurs[i])
    matriceCosinus = matrice(listeVecteurs)
    while len(listeVecteurs)>1:
        _, v1, v2 = maxMatriceIndices(matriceCosinus) # on récupère les vecteurs les plus similaires
        v3 = fusionVecteur(listeVecteurs[v1], listeVecteurs[v2])
        NoeudEnCours.append(fusionner(NoeudEnCours[v1], NoeudEnCours[v2], f"f{cptNomNoeud}", v3))
        cptNomNoeud +=1
        # Remplacement dans listeVecteurs : enlever v1 et v2 et ajouter v3
        # On enlève d'abord les indices les plus grands pour ne pas perturber l'index
        # de même avec la liste de noeuds
        for idx in sorted([v1, v2], reverse=True):
            del listeVecteurs[idx]
            del NoeudEnCours[idx]
        # On supprime mtn les lignes dans la matrice :
        matriceCosinus = enlever_indices(matriceCosinus, [v1, v2])
        listeVecteurs.append(v3)
        matriceCosinus = CalculDernierLigneColonneMatrice(matriceCosinus, listeVecteurs)
    return NoeudEnCours[0] # Renvoie la racine