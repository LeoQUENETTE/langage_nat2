import requests
import json
import re
import os


JDM_URL = "https://jdm-api.demo.lirmm.fr/v0/"


def get_search_result(url):
    filenameURL = re.sub(r'[^\w\-_]', '_', url)
    data = ""
    if not os.path.exists(f"cache/{filenameURL}.json"):
        RequestData = requests.get(url)
        if RequestData.status_code == 200:
            data = RequestData.json()
            with open(f'cache/{filenameURL}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        else:
            print(f"Erreur")
    else:
        with open(f"cache/{filenameURL}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    return data



def getRelationsByTypeId(relation_type : str) -> str:
    url = JDM_URL + "relations/by_type_id/" + relation_type
    return get_search_result(url)
    
def getRelationsFromById(node_id : str) -> str:
    url = JDM_URL + "relations/from_by_id/" + node_id
    return get_search_result(url)
    
def getRelationsFromTo(node1_name : str, node2_name : str) -> str:
    url = JDM_URL + "relations/from/" + node1_name + "/to/" + node2_name + "?min_weight="+str(1)
    return get_search_result(url)
    
def getRelationsFromToId(node1_id :str, node2_id : str) -> str:
    url = JDM_URL + "relations/from_by_id/" + node1_id+"/to_by_id/"+node2_id
    return get_search_result(url)

def getRelationsFromNodeWithRelationID(node_name : str, r_id : str) -> str:
    url = JDM_URL + "relations/from/" + node_name + "?types_ids=" + r_id + "&min_weight="+str(1)
    return get_search_result(url)
    
def getRelationsTo(node_name : str) -> str:
    url = JDM_URL + "relations/to/" + node_name
    return get_search_result(url)
    
def getRelationsToById(node_id : str) -> str:
    url = JDM_URL + "relations/to_by_id/" + node_id
    return get_search_result(url)
    
def getRelationsTypes() -> str:
    url = JDM_URL + "relations_types"
    return get_search_result(url)
    
def getRelationsFrom(node_name : str) -> str:
    url = JDM_URL + "relations/from/" + node_name
    return get_search_result(url)
    

def getNodeById(node_id) -> str:
    url = JDM_URL + "node_by_id/" + node_id
    return get_search_result(url)
    
def getNodeByName(node_name) -> str:
    url = JDM_URL + "node_by_name/" + node_name
    return get_search_result(url)
    
def getNodeRefinements(node_name) -> str:
    url = JDM_URL + "refinements/" + node_name
    return get_search_result(url)

def getNodeTypes() -> str:
    url = JDM_URL + "nodes_types"
    return get_search_result(url)