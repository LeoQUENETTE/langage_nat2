from modele.Matrice import Matrice, constructionArbre
from modele.Vecteur import *
from modele.Noeuds import Noeud
import unittest, copy

class TestMatrice(unittest.TestCase):

    def testMatriceSimple(self):
        v1 = [
            [["a", 1]],
            [["b", 1]]
        ]
        v2 = [
            [["a", 1]],
            [["c", 1]]
        ]

        m_obj = Matrice()
        m_obj.setMatrice(Matrice([v1, v2]).matrice)
        m = m_obj.matrice

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

        m_obj = Matrice()
        m_obj.setMatrice(Matrice([v1, v2, v3]).matrice)
        m = m_obj.matrice

        for i in range(3):
            self.assertEqual(m[i][i], 0)

        self.assertEqual(m[0][1], m[1][0])
        self.assertEqual(m[0][2], m[2][0])
        self.assertEqual(m[1][2], m[2][1])

        self.assertEqual(m[0][1], 1)
        self.assertEqual(m[0][2], 1)
        self.assertEqual(m[1][2], 0)

    def testMaxMatriceIndices(self):

        m1 = Matrice()
        m1.setMatrice([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0]
        ])

        max_val, i, j = m1.maxMatriceIndices()
        self.assertEqual(max_val, 3)
        self.assertTrue((i, j) == (1, 2) or (i, j) == (2, 1))

        m2 = Matrice()
        m2.setMatrice([
            [0, 5, 5],
            [5, 0, 5],
            [5, 5, 0]
        ])

        max_val, i, j = m2.maxMatriceIndices()
        self.assertEqual(max_val,5)
        self.assertEqual((i, j),(0, 1))

        m3 = Matrice()
        m3.setMatrice([
            [0, -1, -2],
            [-1, 0, -0.5],
            [-2, -0.5, 0]
        ])

        max_val, i, j = m3.maxMatriceIndices()
        self.assertEqual(max_val, -0.5)
        self.assertTrue((i, j) == (1, 2) or (i, j) == (2, 1))

        m4 = Matrice()
        m4.setMatrice([[0]])

        max_val, i, j = m4.maxMatriceIndices()
        self.assertEqual(max_val, float('-inf'))
        self.assertTrue(i == -1 and j == -1)

    def testEnleverIndices(self):

        m1 = Matrice()
        m1.setMatrice([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ])

        resultat = m1.enlever_indices([1])
        self.assertEqual(resultat, [[0, 2],[6, 8]], "Le a ligne n'a pas été retiré")

        m2 = Matrice()
        m2.setMatrice([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ])

        resultat = m2.enlever_indices([1, 3])
        self.assertEqual(resultat, [[0, 2],[8, 10]])

        resultat = m2.enlever_indices([3, 1])
        self.assertEqual(resultat, [[0, 2],[8, 10]])

        m3 = Matrice()
        m3.setMatrice([
            [1, 2],
            [3, 4]
        ])

        resultat = m3.enlever_indices([])
        self.assertEqual(resultat, m3.matrice)

        m4 = Matrice()
        m4.setMatrice([
            [1, 2],
            [3, 4]
        ])

        resultat = m4.enlever_indices([0, 1])
        self.assertEqual(resultat, [])

    def testCalculDernierLigneColonneMatrice(self):

        m1 = Matrice()
        m1.setMatrice([
            [1, 2],
            [3, 4]
        ])

        m1.ajouter_ligne_colonne_zero()
        self.assertEqual(m1.matrice, [
            [1, 2, 0],
            [3, 4, 0],
            [0, 0, 0]
        ])

        v1 = [[["a", 1]], [["b", 1]]]
        v2 = [[["a", 0]], [["b", 1]]]
        v3 = [[["a", 1]], [["b", 0]]]

        listeVecteurs = [v1, v2, v3]

        matrice_initiale = Matrice()
        matrice_initiale.setMatrice([
            [0, produitscalaire(v1, v2)],
            [produitscalaire(v2, v1), 0]
        ])

        matrice_initiale.calculDernierLigneColonneMatrice(listeVecteurs)
        matrice_finale = matrice_initiale.matrice

        n = len(matrice_finale)
        assert n == 3

        for i in range(n):
            assert matrice_finale[i][i] == 0

        self.assertEqual(matrice_finale[2][0], produitscalaire(v3, v1))
        self.assertEqual(matrice_finale[2][1], produitscalaire(v3, v2))
        self.assertEqual(matrice_finale[0][2], produitscalaire(v1, v3))
        self.assertEqual(matrice_finale[1][2], produitscalaire(v2, v3))
        self.assertEqual(matrice_finale[2][2], 0)

    def testConstructionArbre(self):

        listeVecteurs = [
            [[["a", 1], ["b", 2]], [["c", 3]]],
            [[["a", 0.5], ["b", 1]], [["d", 4]]]
        ]

        racine = constructionArbre(copy.deepcopy(listeVecteurs))

        self.assertTrue(isinstance(racine, Noeud), "La racine doit être un Noeud")
        self.assertTrue(racine.gauche is not None and racine.droite is not None)

        feuilles = [racine.gauche, racine.droite]
        for f in feuilles:
            self.assertTrue(isinstance(f, Noeud))
            self.assertIsNone(f.gauche)
            self.assertIsNone(f.droite)

        self.assertTrue(racine.nom.startswith("f"))
        for f in feuilles:
            self.assertTrue(f.nom.startswith("f") or f.nom.startswith("f0") or f.nom.startswith("f1"))

if __name__ == "__main__":
    unittest.main()
