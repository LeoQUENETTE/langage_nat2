import api
import json

R_ISA = "6"
R_INFO_POT = "36"

LIST_RELATIONS_ID = ["70","54","23","41","172","10","113","28","50","171","58","142","25","14","121","106"]

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
# TODO en cours
def generateVector(filename : str):
    with open(filename, "r") as f:
        sentances = json.load(f)
        node_name = sentances[0]["n1"]
        # res = api.getNodeByName(node_name)
        # node_info = res
        # # print(json.dumps(res, indent=4))
        print(node_name)
        
        node_r_isa = api.getRelationsFromNodeWithRelationID(node_name, R_ISA)
        node_r_info_pot =  api.getRelationsFromNodeWithRelationID(node_name, R_INFO_POT)
        
        node_r_isa = node_r_isa["relations"]
        node_r_info_pot_n = node_r_info_pot["nodes"]
        node_r_info_pot_r = node_r_info_pot["relations"]
        
        node_vector = {}
        w_list = []
        for r in node_r_isa:
            n2 = r["node2"]
            w_list.append(int(r["w"]))
        w_max = max(w_list)
        for i in range(len(w_list)):
            w = w_list[i]
            node_vector[str(node_r_isa[i]["node2"]) + "(r_isa)"] = w / w_max
        w_list = []
        for r in node_r_info_pot_r:
            w_list.append(int(r["w"]))
        w_max = max(w_list)
        for i in range(len(w_list)):
            n_name = node_r_info_pot_n[i]["name"]
            w = w_list[i]
            if n_name != None and n_name != node_name:
                node_vector[n_name] = w / w_max
            
        for r_id in LIST_RELATIONS_ID:
            somme= 0
            node_r_id = api.getRelationsFromNodeWithRelationID(node_name, r_id)["relations"]
            for r in node_r_id:
                somme += int(r["w"])
            if len(node_r_id) > 0:
                node_vector[r_id] = somme // len(node_r_id)
        
        print(json.dumps(node_vector,indent=4))    