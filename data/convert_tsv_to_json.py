DATA_DIR = "./data/"
OUTPUT_TXT = DATA_DIR+"data_tsv_txt/"
types = {
    "r_has_causatif": "Conséquence",
    "r_has_property-1":"Caracterisation ",
    "r_objet>matière":"Matière",
    "r_lieu>origine":"Origine ",
    "r_topic":"Topic",
    "r_depict":"Despiction",
    "r_holo":"Holonymie",
    "r_lieu":"Lieu",
    "r_processus_agent":"Agent",
    "r_processus_patient":"Patient",
    "r_processus>instr-1":"Instrument",
    "r_own-1":"Possession",
    "r_quantificateur":"Quantification",
    "r_social_tie":"LienSocial",
    "r_product_of":"AuteurCréateur"
}

if __name__ == "__main__":
    phrases_par_types : dict[str , list[str]] = {}
    with open(DATA_DIR+"corpus_updated.tsv", "r",encoding="utf8") as f:
        lines = f.readlines()[1:]
        for l in lines:
            l.replace("\n","")
            data = l.split("\t")
            type = data[0]
            phrase = data[1]
            if not phrases_par_types.get(types.get(type)) : phrases_par_types[types.get(type)] = []
            phrases_par_types[types.get(type)].append(phrase)
    for k, v in phrases_par_types.items():
        with open(OUTPUT_TXT+str(k)+".txt", "w", encoding="utf8") as f:
            for p in v:
                f.write(str(p)+"\n")
            