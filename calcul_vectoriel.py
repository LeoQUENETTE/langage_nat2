import api
import json

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

# Filename = le fichier de data, ou le fichier de la relation a évaluer
def generateVector(filename : str):
    with open(filename, "r") as f:
        sentences = json.load(f)

        resultat = []

        for i in range(len(sentences)):
            phrase = []

            for noeud in [sentences[i]["n1"], sentences[i]["n2"]]:
                vecteur_noeud = []

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
                if noeud == sentences[i]["n1"]:
                    LIST_RELATIONS_ID = LIST_RELATIONS_ID_N1
                else:
                    LIST_RELATIONS_ID = LIST_RELATIONS_ID_N2
                    vecteur_noeud.append(["det", sentences[i]["det"] / 2]) #pour normaliser

                #idem pour les 15 relations ; moyenne puis normalisation
                vecteur_temp = []
                w_max = 0
                for r_id in LIST_RELATIONS_ID:
                    somme = 0
                    rels_r_id = api.getRelationsFromNodeWithRelationID(noeud, r_id)["relations"]
                    if rels_r_id != "" and len(rels_r_id) > 0:
                        for r in rels_r_id:
                            poids = int(r["w"])
                            somme += poids
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

            # end for noeud n1 + n2
            resultat.append(phrase)

        # end for each sentence
        print(resultat)