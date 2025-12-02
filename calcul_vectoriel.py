import api
import json

R_ISA = 6
R_INFO_PLOT = 36
def generateVector(filename : str, relation_id : str):
    with open(filename, "r") as f:
        sentances = json.load(f)
        res = api.getNodeByName(sentances[0]["n1"])
        # print(json.dumps(res, indent=4))
        print(res["id"])
        
        