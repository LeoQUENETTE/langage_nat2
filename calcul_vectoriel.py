import api
import json
def generateVector(filename : str, relation_name : str):
    with open(filename, "r") as f:
        sentances = json.dump(filename)
        api.getNodeByName(sentances[0]["n1"])