import unittest
import math
from modele.Vecteur import *

class TestVecteur(unittest.TestCase):
    def testMoyenneArithmétique(self):
        value1 = moyenneArithmétique(3,5)
        value2 = moyenneArithmétique(2,11)
        self.assertEqual(value1, float(4))
        self.assertEqual(value2, float(6.5))

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

        self.assertEqual(resultat , [
            [["a", 0]],
            [["b", 0]]
        ])