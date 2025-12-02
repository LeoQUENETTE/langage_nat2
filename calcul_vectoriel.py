import api
import json

R_ISA = "6"
R_INFO_POT = "36"
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
        node_r_info_pot = node_r_info_pot["relations"]
        
        node_vector = []
        for r in node_r_isa:
            n2 = r["node2"]
            w = r["w"]
            node_w = {str(n2) + "(r_isa)":w}
            node_vector.append(node_w)
        for r in node_r_info_pot:
            n2 = r["node2"]
            w = r["w"]
            node_w = {str(n2) + "(r_info_pot)":w}
            node_vector.append(node_w)
        print(json.dumps(node_vector,indent=4))