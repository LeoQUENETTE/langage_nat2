import api.api as api
import json, os
import math

R_ISA = "6"
R_INFO_POT = "36"
LIST_RELATIONS_ID_N1 = ["70", "54", "173", "42", "172", "10", "113", "15", "50", "171", "174", "142", "139", "76", "122"]
LIST_RELATIONS_ID_N2 = ["137", "53", "153", "41", "9", "113", "28", "51", "58", "80", "138", "121"]

'''
{
"phrases" : "La photo de famille",
"n1":"photo",
"n2":"famille",
"det":[0,1,2],
"types":[]
}

listeVecteurs = 
[
  [
    [["isa_chat", 0.8], ["isa_baleine", 0.1], ["has_part", 0.5]], 
    [["isa_bois", 0.4], ["isa_vert", 0.31], ["commande", 0.1]]
  ],
  [ 
    [["isa_chien", 0.7], ["isa_dauphin", 0.2], ["has_part", 0.6]], 
    [["isa_metal", 0.5], ["isa_gris", 0.2], ["commande", 0.05]]
  ],
  [
    [["isa_oiseau", 0.6], ["isa_chat", 0.3], ["has_wing", 0.9]],
    [["isa_plastique", 0.3], ["isa_bleu", 0.4], ["commande", 0.2]]
  ]
]
'''

def generateVector(parsed_sentence :dict[str,str]) -> list[list[tuple[str,float]]]:
    phrase = []
    for noeud in [parsed_sentence["n1"], parsed_sentence["n2"]]:
        vecteur_noeud = []
        noeud = noeud.strip().lower()
        all_r_isa = api.getRelationsFromNodeWithRelationID(noeud, R_ISA)
        all_r_info_pot =  api.getRelationsFromNodeWithRelationID(noeud, R_INFO_POT)
        
        if all_r_isa == "" or all_r_info_pot == "" or noeud == "":
            phrase.append(vecteur_noeud)
            break
        
        r_isa_rels = all_r_isa["relations"]
        r_info_pot_rels = all_r_info_pot["relations"]
        
        if r_isa_rels != []:
            w_list = []
            # liste des poids des r-isa ; but : récup le max
            for r in r_isa_rels:
                w_list.append(int(r["w"]))
            w_max = max(w_list)
            # pour chaque poids, récup son node et ajouter ce poids normalisé
            for j in range(len(w_list)):
                vecteur_noeud.append(["(6)" + str(r_isa_rels[j]["node2"]) , w_list[j] / w_max])

        if r_info_pot_rels != []:
            # idem pour r-info-sem
            w_list = []
            for r in r_info_pot_rels:
                w_list.append(int(r["w"]))
            w_max = max(w_list)
            for j in range(len(w_list)):
                vecteur_noeud.append([str(r_info_pot_rels[j]["node2"]) , w_list[j] / w_max])
        
        
        LIST_RELATIONS_ID = None
        if noeud == parsed_sentence["n1"]:
            LIST_RELATIONS_ID = LIST_RELATIONS_ID_N1
        else:
            LIST_RELATIONS_ID = LIST_RELATIONS_ID_N2
            vecteur_noeud.append(["det", parsed_sentence["det"] / 2]) #pour normaliser

        #idem pour les 15 relations ; moyenne puis normalisation
        vecteur_temp = []
        w_max = 0
        for r_id in LIST_RELATIONS_ID:
            somme = 0
            rels_r_id = api.getRelationsFromNodeWithRelationID(noeud, r_id)["relations"]
            if rels_r_id != "" and len(rels_r_id) > 0:
                for r in rels_r_id:
                    poids = int(r["w"]) # calculer en fonction du log du nb de relation : 1 + log10(100) = 3
                    somme += poids
                    # Voir ensuite comment normaliser, puisqu'il faut calibrer
                    # Boite à idée : max, pondération, 
                moyenne = somme // len(rels_r_id)
                vecteur_temp.append([r_id,moyenne])
                if moyenne > w_max:
                    w_max = moyenne
        for r in vecteur_temp:
            r[1] /= w_max

        for vect in vecteur_temp:
            vecteur_noeud.append(vect)

        #color
        couleur = api.getRelationsFromTo(noeud, "sans%20couleur")
        if couleur != "" and couleur["relations"] != []:
            vecteur_noeud.append(["106", 1])
        
        phrase.append(vecteur_noeud)
    return phrase

def generateAllVectorsFromFile(filename : str) -> list[list[list[tuple[str,float]]]]:
    '''
    generateVector
    
    :param filename: le fichier de data, ou le fichier de la relation a évaluer
    :type filename: str
    '''
    with open(filename, "r", encoding="utf8") as f:
        sentences : list[dict[str,str]] = json.load(f)
        n = len(sentences)
        resultat = []

        for i in range(n):
            phrase = generateVector(sentences[i])
            # end for noeud n1 + n2
            resultat.append(phrase)
            avancement = (i / n) * 100

        # end for each sentence
        return resultat
def moyenneArithmétique (a,b) -> float:
    '''
    moyenneArithmétique : Fonction calculant la moyenne arithmétique de deux valeurs
    '''
    return (a+b)/2

def norme(vecteur : list[tuple[str, float]]) -> float:
    '''
    norme : Fonction calculant la norme d'un vecteur (|u| = sqrt( x_1 ** 2 + x_2 ** 2 + ... + x_n * 2))
    '''
    # Calcule la norme du vecteur
    norme = 0
    for relation in vecteur :
        norme += relation[1]**2 # On ajoute tous les carré 
    return math.sqrt(norme)

def vecteurNorme(vecteurdepart : list[list[tuple[str, float]]]):
    # Norme le vecteur (les deux parties du vecteur)
    for v in range(len(vecteurdepart)):
        vecteur = vecteurdepart[v]
        normevecteur = norme(vecteur)
        if normevecteur == 0:
            normevecteur = 1  # Pour éviter le problème avec la division que l'on fait après
        for i in range(len(vecteur)) :
            vecteur[i][1] = vecteur[i][1]/normevecteur
        vecteurdepart[v] = vecteur
    return vecteurdepart

def produitscalaire(vecteur1depart : list[tuple[str,float]],vecteur2depart : list[tuple[str,float]]) -> float:  # Cosinus ici
    '''
    produitscalaire : Fonction calculant la distance entre deux vecteur en renvoyant le cosinus de ces deux vecteurs
    Renvoie un float correspondant à la distance des vecteurs, donc au cosinus
    '''
    # Trier les vecteurs pour que l'on puisse sortir au plus tôt de la boucle
    # Temps exec globaux (benchmarks)
    resultatfinal = 0
    for v in range(2): # On traite chaque vecteur séparement
        v1 = vecteur1depart[v]
        v2 = vecteur2depart[v]
        multiplicationTerme = 0
        # On mutiplie les valeurs des relations si ce sont les même relations
        for relation1 in v1:
            for relation2 in v2:
                if relation1[0]==relation2[0]: 
                    multiplicationTerme += relation1[1] * relation2[1]
        normeTest = norme(v1)*norme(v2)
        if normeTest == 0:
            normeTest = 1
        resultat = multiplicationTerme / normeTest # division sert à rien car en soit la norme est 1 (si c'est le cas, norme test sert à rien)
        resultatfinal += resultat
    return resultatfinal



def fusionVecteur(v1depart : list[list[tuple[str,float]]],v2depart : list[list[tuple[str,float]]]):
    # Renvoie la fusion norme des deux vecteurs
    Vcree = []
    for v in range(len(v1depart)):
        v1 = v1depart[v]
        v2 = v2depart[v]
        VcreePart = []
        listeTestV2 = []
        for relation1 in v1:
            no_match : bool = True # Pour tester si on trouve ou pas un vecteur correspondant
            for relation2 in v2:
                if relation1[0]==relation2[0]: # regarde si le nom des relations est le même 
                    no_match = False
                    VcreePart.append([relation1[0],moyenneArithmétique(relation1[1],relation2[1])]) # tester somme, arithm, geo
                    listeTestV2.append(relation2)
            if no_match:
                VcreePart.append([relation1[0],relation1[1]/2])
        for relation2 in v2: # Voir si on peut pas le mettre dans la boucle précédente
            # Si on fait la somme de deux vecteurs cela signie faire la somme de toutes 
            # leurs composantes, et donc diviser par deux n'est pas nécessaire, normer est 
            # suffisant
            if relation2 not in listeTestV2:
                VcreePart.append([relation2[0],relation2[1]/2])
        Vcree.append(VcreePart)
    Vcree = vecteurNorme(Vcree)
    return Vcree