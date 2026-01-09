import unittest
from modele.Vecteur import * 
from modele.Noeuds import *

class TestNoeuds(unittest.TestCase):
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
        noeuds = creationNoeudDepart(self.listeVecteurs)
        for n in range(len(noeuds)) :
            self.assertEqual(noeuds[n].valeur, self.listeVecteurs[n])
            self.assertIsNone(noeuds[n].gauche)
            self.assertIsNone(noeuds[n].droite)

    def testFusionner(self):
        n = fusionnerNoeuds(self.n1, self.n2, "n3", "valeur")
        self.assertEqual(n.droite,self.n2)
        self.assertEqual(n.gauche ,self.n1)
        self.assertEqual(n.nom ,"n3")
        self.assertEqual(n.valeur, "valeur")
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

    def testParcoursChoix(self):
        # Création de vecteurs simples pour le test
        v1 = [[["rel1", 0.5], ["rel2", 0.5]], [["rel3", 0.2]]]
        v2 = [[["rel1", 0.9], ["rel2", 0.1]], [["rel3", 0.7]]]
        v_racine = fusionVecteur(v1, v2)

        # Création des noeuds
        n1 = Noeud(v1, nom="n1")
        n2 = Noeud(v2, nom="n2")
        racine = fusionnerNoeuds(n1, n2, "racine", v_racine)

        # Vecteur cible pour le test
        cible = [[["rel1", 0.9], ["rel2", 0.1]], [["rel3", 0.7]]]

        # Test 1 : choix du noeud avec produit scalaire le plus élevé
        resultat = parcours_choix(racine, cible)
        assert resultat > 0, "Le résultat doit être supérieur à 0"

        # Test 2 : racine avec valeurs toutes nulles → doit renvoyer None
        racine_faible = Noeud(
            [[["rel1", 0], ["rel4", 0]], [["rel3", 0]]],
            nom="faible"
        )
        resultat_none = parcours_choix(racine_faible, cible)
        assert resultat_none is None, "Doit retourner None si racine faible"