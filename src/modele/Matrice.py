# Structure de listeVecteur :
# [v1,v2,v3,....]
# v1 = [vecteur de "A", vecteur de "de B"] pour la phrase "A de B"
# vecteur de "A" = [[nomrel1, val1],[nomrel2, val2],[nomrel3, val3],...,[nomreln, valn]]
from .Noeuds import *
import pickle

class Matrice:
    def __init__(self, listeVecteurs : list[list[list[tuple[str,float]]]] = None):
        n = len(listeVecteurs)
        self.size = n
        self.matrice : list[list[float]] = []
        for c in range(self.size):
            self.matrice.append([])
            for l in range(self.size):
                if c != l and c < n and l < n:
                    self.matrice[c].append(produitscalaire(listeVecteurs[c],listeVecteurs[l]))
                else :
                    self.matrice[c].append(0)  # Pour ne pas perturber le max (déjà égale à zéro si je dis pas de bêtise)
    def setMatrice(self, matrice : list[list[float]]):
        if matrice == None: return
        self.matrice = matrice
        self.size = len(self.matrice)

            
    def maxMatriceIndices(self) -> tuple[float, int, int]:
        '''
        Fonction renvoyant les indices et la valeur max de la matrice
        '''
        max_val = float('-inf')
        indice_i, indice_j = -1, -1
        nb_comp = 0
        for i in range(self.size):
            for j in range(self.size):
                nb_comp += 1
                if i != j and self.matrice[i][j] > max_val:
                    max_val = self.matrice[i][j]
                    indice_i, indice_j = i, j
        return max_val, indice_i, indice_j
    def enlever_indices(self, indices : list[int]):
        """
        Supprime les lignes et colonnes correspondant aux indices donnés.
        indices : liste d'indices à supprimer (ex : [i,j])
        """
        # On garde uniquement les lignes dont l'index n'est pas dans indices
        new_matrice = [
            [val for col_id, val in enumerate(ligne) if col_id not in indices]
            for ligne_id, ligne in enumerate(self.matrice) if ligne_id not in indices
        ]
        self.setMatrice(new_matrice)

    def ajouter_ligne_colonne_zero(self):
        '''
        ajouter_ligne_colonne_zero : Fonction ajoutant une ligne et une colonne de zéro à la matrice donné
        '''
        # Ajouter 0 à la fin de chaque ligne existante
        for ligne in self.matrice: # O(n) où n est la taille de la matrice
            ligne.append(0)
        # Ajouter une nouvelle ligne de zéros
        nouvelle_ligne = [0] * (self.size + 1) # Création d'une liste de taille n + 1 rempli de 0
        self.matrice.append(nouvelle_ligne)
        self.size += 1

    def calculDernierLigneColonneMatrice(self,listeVecteurs : list[list[list[tuple[str,float]]]]):
        #On ajoute la ligne et la colonne correspondant au vecteur rajouté. 
        self.ajouter_ligne_colonne_zero()
        n = len(listeVecteurs)  # taille après ajout du nouveau vecteur
        # Dernier vecteur ajouté
        dernier_vecteur = listeVecteurs[-1]
        for i in range(n - 1):  # on met à jour les valeurs avec tous les autres vecteurs
            valeur = produitscalaire(dernier_vecteur, listeVecteurs[i])
            self.matrice[i][n - 1] = valeur  # dernière colonne
            self.matrice[n - 1][i] = valeur  # dernière ligne

        self.matrice[n - 1][n - 1] = 0

def constructionArbre(listeVecteurs : list[list[list[tuple[str,float]]]], prec_noeuds : list[Noeud] = None) -> Noeud:
    '''
    constructionArbre : Fonction permettant la création d'un arbre de relation en se basant sur une liste de vecteurs
    de relation donné. 
    Renvoie le noeud racine de cet arbre.
    '''
    cptNomNoeud = len(listeVecteurs)
    NoeudEnCours = creationNoeudDepart(listeVecteurs)
    for i in range(cptNomNoeud) :
        listeVecteurs[i] = vecteurNorme(listeVecteurs[i])
    matrice = Matrice(listeVecteurs)
    while len(listeVecteurs)>1:
        _, v1, v2 = matrice.maxMatriceIndices() # on récupère les vecteurs les plus similaires
        v3 = fusionVecteur(listeVecteurs[v1], listeVecteurs[v2])
        n1 = NoeudEnCours[v1]
        n2 = NoeudEnCours[v2]
        n3 = fusionnerNoeuds(n1, n2, f"f{cptNomNoeud}", v3)
        
        print("fusion : ", n1.nom, n2.nom, n3.nom)
        
        print(n3.nom + " : encoder")
        NoeudEnCours.append(n3)
        cptNomNoeud +=1
        # Remplacement dans listeVecteurs : enlever v1 et v2 et ajouter v3
        # On enlève d'abord les indices les plus grands pour ne pas perturber l'index
        # de même avec la liste de noeuds
        
        for idx in sorted([v1, v2], reverse=True):
            del listeVecteurs[idx]
            del NoeudEnCours[idx]
            
        # On supprime mtn les lignes dans la matrice :
        matrice.enlever_indices([v1, v2])
        listeVecteurs.append(v3)
        matrice.calculDernierLigneColonneMatrice(listeVecteurs)
    return  NoeudEnCours[0] # Renvoie la racine