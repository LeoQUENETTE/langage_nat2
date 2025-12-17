
from matrice import *
import unittest, copy

class TestMatrice(unittest.TestCase):
    def setUp(self):
        self.n1 = Noeud("toto", nom="f1")
        self.n2 = Noeud("toto2", nom="f2")
        self.n3 = Noeud("toto3", nom="f3")
        self.n3.droite = self.n1
        self.n3.gauche = self.n2
        
        self.listeVecteurs = [[[["isa_chat", 0.8], ["isa_baleine", 0.1], ["has_part", 0.5]], [["isa_bois", 0.4], ["isa_vert", 0.31], ["commande", 0.1]]],
                [[["isa_chien", 0.7], ["isa_dauphin", 0.2], ["has_part", 0.6]], [["isa_metal", 0.5], ["isa_gris", 0.2], ["commande", 0.05]]],
                [[["isa_oiseau", 0.6], ["isa_chat", 0.3], ["has_wing", 0.9]],[["isa_plastique", 0.3], ["isa_bleu", 0.4], ["commande", 0.2]]],
                [[["isa_poisson", 0.9], ["isa_baleine", 0.05], ["has_fin", 0.8]],[["isa_bois", 0.2], ["isa_vert", 0.5], ["commande", 0.1]]],
                [[["isa_lapin", 0.75], ["isa_chat", 0.15], ["has_ear", 0.6]], [["isa_verre", 0.6], ["isa_transparent", 0.7], ["commande", 0.3]]],
                [[["isa_tigre", 0.85], ["isa_lion", 0.1], ["has_stripe", 0.9]],[["isa_beton", 0.4], ["isa_gris", 0.6], ["commande", 0.05]]],
                [[["isa_cheval", 0.8], ["isa_zebra", 0.1], ["has_tail", 0.7]],[["isa_bois", 0.3], ["isa_marron", 0.5], ["commande", 0.2]]]]

    def testCreationNoeudDepart(self):
        noeud = creationNoeudDepart(self.listeVecteurs)
        for n in range(len(noeud)) :
            assert noeud[n].valeur == self.listeVecteurs[n]
            assert noeud[n].droite == None
            assert noeud[n].gauche == None
            print(noeud[n].nom)

    def testFusionner(self):
        n = fusionner(self.n1, self.n2, "n3", "valeur")
        self.assertEqual(n.droite,self.n2)
        self.assertEqual(n.gauche ,self.n1)
        self.assertEqual(n.nom ,"n3")
        self.assertEqual(n.valeur, "valeur")

    def testMoyenneArithmétique(self):
        self.assertEqual(moyenneArithmétique(3,5), 4)
        self.assertEqual(moyenneArithmétique(2,11), 6.5)

    def testNorme(self):
        self.assertEqual(norme([["isa_chat", 1], ["isa_baleine", 2], ["has_part", 3]]) , math.sqrt(14))
        self.assertEqual(norme([["isa_chat", 1], ["isa_baleine", 0], ["has_part", 0]]) , 1)
        self.assertEqual(norme([["isa_chat", 0], ["isa_baleine", 0], ["has_part", 0]]) , 0)

    def testVecteurNorme(self):
        self.assertEqual(vecteurNorme([[["isa_chat", 1], ["isa_baleine", 2], ["has_part", 3]],[["isa_chat", 1], ["isa_baleine", 0], ["has_part", 0]]]) , [[["isa_chat", 1/math.sqrt(14)], ["isa_baleine", 2/math.sqrt(14)], ["has_part", 3/math.sqrt(14)]],[["isa_chat", 1], ["isa_baleine", 0], ["has_part", 0]]])
        self.assertEqual(vecteurNorme([[["isa_chat", 1], ["isa_baleine", 0], ["has_part", 0]],[["isa_chat", 0], ["isa_baleine", 0], ["has_part", 0]]]) , [[["isa_chat", 1], ["isa_baleine", 0], ["has_part", 0]],[["isa_chat", 0], ["isa_baleine", 0], ["has_part", 0]]])

    def testProduitscalaire(self):

        # Cas 1 : vecteurs identiques → cosinus = 1 par partie
        v1 = [
            [["isa_chat", 1], ["isa_baleine", 0]],
            [["has_part", 1]]
        ]
        v2 = [
            [["isa_chat", 1], ["isa_baleine", 0]],
            [["has_part", 1]]
        ]

        # 1 + 1 = 2
        self.assertEqual(produitscalaire(v1, v2) , 2)


        # Cas 2 : aucun lien commun → cosinus = 0
        v3 = [
            [["isa_chat", 1]],
            [["has_part", 1]]
        ]
        v4 = [
            [["isa_chien", 1]],
            [["has_tail", 1]]
        ]

        self.assertEqual(produitscalaire(v3, v4) , 0)


        # Cas 3 : correspondance partielle
        v5 = [
            [["isa_chat", 2], ["isa_baleine", 0]],
            [["has_part", 1]]
        ]
        v6 = [
            [["isa_chat", 1], ["isa_baleine", 0]],
            [["has_part", 0]]
        ]

        # Partie 1 :
        # produit = 2*1 = 2
        # norme(v5) = 2
        # norme(v6) = 1
        # cos = 2 / (2*1) = 1
        #
        # Partie 2 :
        # produit = 1*0 = 0
        #
        # total = 1
        self.assertEqual(produitscalaire(v5, v6), 1)


        # Cas 4 : vecteur nul → cosinus défini comme 0
        v7 = [
            [["isa_chat", 0]],
            [["has_part", 0]]
        ]

        self.assertEqual(produitscalaire(v7, v7), 0)

    def testMatriceSimple(self):
        v1 = [
            [["a", 1]],
            [["b", 1]]
        ]
        v2 = [
            [["a", 1]],
            [["c", 1]]
        ]
        # Calcul manuel :
        # Sous-vecteur 1 : a vs a → 1 / (1*1) = 1
        # Sous-vecteur 2 : b vs c → 0
        # Total = 1
        m = matrice([v1, v2])
        self.assertEqual(m, [[0, 1],[1, 0]])

    def testMatriceTroisVecteurs(self):
        v1 = [
            [["a", 1]],
            [["b", 1]]
        ]
        v2 = [
            [["a", 1]],
            [["b", 0]]
        ]
        v3 = [
            [["c", 1]],
            [["b", 1]]
        ]

        m = matrice([v1, v2, v3])

        # Diagonale nulle
        for i in range(3):
            self.assertEqual(m[i][i], 0)

        # Symétrie
        self.assertEqual(m[0][1] ,m[1][0])
        self.assertEqual(m[0][2] ,m[2][0])
        self.assertEqual(m[1][2] ,m[2][1])

        # Valeurs attendues
        # v1 vs v2 :
        # a/a = 1, b/0 = 0 → total = 1
        self.assertEqual(m[0][1] ,1)

        # v1 vs v3 :
        # a/c = 0, b/b = 1 → total = 1
        self.assertEqual(m[0][2] ,1)

        # v2 vs v3 :
        # a/c = 0, b/b = 0 → total = 0
        self.assertEqual(m[1][2] ,0)

    def testMaxMatriceIndices(self):

        # Cas 1 : matrice simple
        m1 = [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0]
        ]

        max_val, i, j = maxMatriceIndices(m1)

        self.assertEqual(max_val, 3)
        self.assertTrue((i, j) == (1, 2) or (i, j) == (2, 1))


        # Cas 2 : plusieurs valeurs égales (doit prendre la première rencontrée)
        m2 = [
            [0, 5, 5],
            [5, 0, 5],
            [5, 5, 0]
        ]

        max_val, i, j = maxMatriceIndices(m2)

        self.assertEqual(max_val,5)
        self.assertEqual((i, j) ,(0, 1))  # premier max trouvé (ordre i puis j)


        # Cas 3 : valeurs négatives
        m3 = [
            [0, -1, -2],
            [-1, 0, -0.5],
            [-2, -0.5, 0]
        ]

        max_val, i, j = maxMatriceIndices(m3)

        self.assertEqual(max_val , -0.5)
        self.assertTrue((i, j) == (1, 2) or (i, j) == (2, 1))


        # Cas 4 : matrice 1x1 (aucune comparaison possible)
        m4 = [[0]]

        max_val, i, j = maxMatriceIndices(m4)

        self.assertEqual(max_val, float('-inf'))
        self.assertTrue(i == -1 and j == -1)

    def testFusionVecteur(self):

        # --------------------------------------------------
        # Cas 1 : relations communes
        # --------------------------------------------------
        v1 = [
            [["a", 2], ["b", 2]],
            [["c", 2]]
        ]

        v2 = [
            [["a", 4], ["b", 0]],
            [["c", 0]]
        ]

        resultat = fusionVecteur(v1, v2)

        self.assertEqual(resultat, vecteurNorme([[["a", 3], ["b", 1]], [["c", 1]]]))


        # --------------------------------------------------
        # Cas 2 : aucune relation commune
        # --------------------------------------------------
        v3 = [
            [["x", 2]],
            [["y", 4]]
        ]

        v4 = [
            [["a", 6]],
            [["b", 8]]
        ]

        resultat = fusionVecteur(v3, v4)

        self.assertEqual(resultat, vecteurNorme([[["x", 1],["a", 3]],[["y", 2],["b", 4]]]))


        # --------------------------------------------------
        # Cas 3 : MIXTE (relation commune + non commune)
        # --------------------------------------------------
        v5 = [
            [["a", 4], ["b", 2]],
            [["c", 6]]
        ]

        v6 = [
            [["a", 2]],
            [["d", 10]]
        ]

        resultat = fusionVecteur(v5, v6)

        self.assertEqual(resultat, vecteurNorme([[["a", 3], ["b", 1]], [["c", 3],["d", 5]]]))


        # --------------------------------------------------
        # Cas 4 : vecteurs nuls
        # --------------------------------------------------
        v7 = [
            [["a", 0]],
            [["b", 0]]
        ]

        v8 = [
            [["a", 0]],
            [["b", 0]]
        ]

        resultat = fusionVecteur(v7, v8)

        self.assertEqual(resultat == [
            [["a", 0]],
            [["b", 0]]
        ])


    def testEnleverIndices(self):

        # --------------------------------------------------
        # Cas 1 : suppression d’un seul index
        # --------------------------------------------------
        m1 = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        resultat = enlever_indices(m1, [1])

        self.assertEqual(resultat == [
            [0, 2],
            [6, 8]
        ])


        # --------------------------------------------------
        # Cas 2 : suppression de deux indices
        # --------------------------------------------------
        m2 = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ]

        resultat = enlever_indices(m2, [1, 3])

        self.assertEqual( resultat == [
            [0, 2],
            [8, 10]
        ])


        # --------------------------------------------------
        # Cas 3 : indices non triés
        # --------------------------------------------------
        resultat = enlever_indices(m2, [3, 1])

        self.assertEqual(resultat , [
            [0, 2],
            [8, 10]
        ])


        # --------------------------------------------------
        # Cas 4 : aucun index supprimé
        # --------------------------------------------------
        m3 = [
            [1, 2],
            [3, 4]
        ]

        resultat = enlever_indices(m3, [])

        self.assertEqual( resultat , m3)


        # --------------------------------------------------
        # Cas 5 : suppression de tous les indices
        # --------------------------------------------------
        m4 = [
            [1, 2],
            [3, 4]
        ]

        resultat = enlever_indices(m4, [0, 1])

        self.assertEqual(resultat, [])

    def testCalculDernierLigneColonneMatrice(self):

        # --------------------------------------------------
        # Cas 1 : ajouter_ligne_colonne_zero
        # --------------------------------------------------
        m1 = [
            [1, 2],
            [3, 4]
        ]

        resultat = ajouter_ligne_colonne_zero([row[:] for row in m1])  # copy pour ne pas modifier m1

        self.assertEqual(resultat, [
            [1, 2, 0],
            [3, 4, 0],
            [0, 0, 0]
        ])


        # --------------------------------------------------
        # Cas 2 : CalculDernierLigneColonneMatrice avec produitscalaire simple
        # --------------------------------------------------
        # On utilise des vecteurs simples pour contrôle manuel
        v1 = [[["a", 1]], [["b", 1]]]
        v2 = [[["a", 0]], [["b", 1]]]
        v3 = [[["a", 1]], [["b", 0]]]

        listeVecteurs = [v1, v2, v3]

        # Matrice initiale vide (2x2) correspondant à v1 et v2
        matrice_initiale = [
            [0, produitscalaire(v1, v2)],
            [produitscalaire(v2, v1), 0]
        ]

        matrice_finale = CalculDernierLigneColonneMatrice([row[:] for row in matrice_initiale], listeVecteurs)

        # Vérifications :
        n = len(matrice_finale)
        assert n == 3
        # diagonale = 0
        for i in range(n):
            assert matrice_finale[i][i] == 0
        # dernière ligne/colonne = produit scalaire avec v1 et v2
        self.assertEqual(matrice_finale[2][0] , produitscalaire(v3, v1))
        self.assertEqual(matrice_finale[2][1] , produitscalaire(v3, v2))
        self.assertEqual(matrice_finale[0][2] , produitscalaire(v1, v3))
        self.assertEqual(matrice_finale[1][2] , produitscalaire(v2, v3))
        # dernière case
        self.assertEqual(matrice_finale[2][2], 0)

    def testConstructionArbre(self):

        # Chaque vecteur = liste de sous-vecteurs
        # Chaque sous-vecteur = liste [nom,valeur]
        listeVecteurs = [
            [  # vecteur 0
                [["a", 1], ["b", 2]],
                [["c", 3]]
            ],
            [  # vecteur 1
                [["a", 0.5], ["b", 1]],
                [["d", 4]]
            ]
        ]

        # Construction de l'arbre
        racine = constructionArbre(copy.deepcopy(listeVecteurs))

        # --------------------------------------------------
        # Vérifications structurelles
        # --------------------------------------------------
        self.assertEqual(isinstance(racine, Noeud), "La racine doit être un Noeud")
        self.assertTrue(racine.gauche is not None and racine.droite is not None, "La racine doit avoir deux enfants") 

        # Les feuilles doivent contenir les vecteurs originaux
        feuilles = [racine.gauche, racine.droite]
        for f in feuilles:
            self.assertTrue(isinstance(f, Noeud))
            self.assertIsNone(f.gauche, "Les feuilles de gauche ne doivent pas avoir d'enfant")
            self.assertIsNone(f.droite,"Les feuilles de droite ne doivent pas avoir d'enfant")

        # Vérification noms des noeuds
        self.assertTrue(racine.nom.startswith("f"), "Nom du noeud fusionné doit commencer par 'f'")
        for f in feuilles:
            self.assertTrue(f.nom.startswith("f") or f.nom.startswith("f0") or f.nom.startswith("f1"))

    def testParcoursChoix_Complet(self):
        # ------------------------------
        # Création de vecteurs pour l'arbre
        # ------------------------------
        # Feuilles très distinctes
        f1 = [[["a", 1]], [["x", 0.5]]]
        f2 = [[["b", 1]], [["y", 0.5]]]
        f3 = [[["c", 1]], [["z", 0.5]]]
        f4 = [[["d", 1]], [["w", 0.5]]]

        # Noeuds intermédiaires
        n1_val = fusionVecteur(f1, f2)
        n2_val = fusionVecteur(f3, f4)

        # Création des noeuds
        n1 = Noeud(n1_val, nom="n1")
        n1.gauche = Noeud(f1, nom="f1")
        n1.droite = Noeud(f2, nom="f2")

        n2 = Noeud(n2_val, nom="n2")
        n2.gauche = Noeud(f3, nom="f3")
        n2.droite = Noeud(f4, nom="f4")

        # Racine
        racine_val = fusionVecteur(n1_val, n2_val)
        racine = Noeud(racine_val, nom="racine")
        racine.gauche = n1
        racine.droite = n2

        # ------------------------------
        # Cas de test
        # ------------------------------
        cible_f1 = [[["a", 1]], [["x", 0.5]]]
        res1 = parcours_choix(racine, cible_f1)
        assert abs(res1 - produitscalaire(f1, cible_f1)) < 1e-6, "Erreur : devrait choisir f1"

        cible_f2 = [[["b", 1]], [["y", 0.5]]]
        res2 = parcours_choix(racine, cible_f2)
        assert abs(res2 - produitscalaire(f2, cible_f2)) < 1e-6, "Erreur : devrait choisir f2"

        cible_f3 = [[["c", 1]], [["z", 0.5]]]
        res3 = parcours_choix(racine, cible_f3)
        assert abs(res3 - produitscalaire(f3, cible_f3)) < 1e-6, "Erreur : devrait choisir f3"

        cible_f4 = [[["d", 1]], [["w", 0.5]]]
        res4 = parcours_choix(racine, cible_f4)
        assert abs(res4 - produitscalaire(f4, cible_f4)) < 1e-6, "Erreur : devrait choisir f4"

        # Cible trop faible
        cible_faible = [[["a", 0]], [["x", 0]]]
        res5 = parcours_choix(racine, cible_faible)
        assert res5 is None, "Erreur : valeur trop faible à la racine, doit retourner None"

        print("testParcoursChoix_Complet : OK")

    def testParcoursChoix(self):
        # Création de vecteurs simples pour le test
        v1 = [[["rel1", 0.5], ["rel2", 0.5]], [["rel3", 0.2]]]
        v2 = [[["rel1", 0.9], ["rel2", 0.1]], [["rel3", 0.7]]]
        v_racine = fusionVecteur(v1, v2)

        # Création des noeuds
        n1 = Noeud(v1, nom="n1")
        n2 = Noeud(v2, nom="n2")
        racine = fusionner(n1, n2, "racine", v_racine)

        # Vecteur cible pour le test
        cible = [[["rel1", 0.9], ["rel2", 0.1]], [["rel3", 0.7]]]

        # Test 1 : choix du noeud avec produit scalaire le plus élevé
        resultat = parcours_choix(racine, cible)
        print("Résultat produit scalaire choisi :", resultat)
        assert resultat > 0, "Le résultat doit être supérieur à 0"

        # Test 2 : racine avec valeurs toutes nulles → doit renvoyer None
        racine_faible = Noeud(
            [[["rel1", 0], ["rel4", 0]], [["rel3", 0]]],
            nom="faible"
        )
        resultat_none = parcours_choix(racine_faible, cible)
        print("Résultat pour racine faible :", resultat_none)
        assert resultat_none is None, "Doit retourner None si racine faible"

        print("Tous les tests pour parcours_choix passent.")
        


if __name__ == "__main__":
    unittest.main()