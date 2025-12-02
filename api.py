import requests, json, os, ast

JDM_URL = "https://jdm-api.demo.lirmm.fr/v0/"


def search_result(url):
    try:
        with open("storage.json", "r") as f:
            f_data = json.load(f)
        if not isinstance(f_data.get("requests"), list):
            f_data["requests"] = []
    except (FileNotFoundError, json.JSONDecodeError):
        f_data = {"requests": []}
    
    if len(f_data["requests"]) == 0:
        return None
    
    for request in f_data["requests"]:
        if url in request:
            return request[url]
    return None

def create_storage():
    if not os.path.exists("storage.json"):
        with open("storage.json", "w") as f:
            json.dump({"requests" : []}, f, indent=4)
def make_get_request(url):
    create_storage()
    result = search_result(url)
    if result != None:
        print("")
        print("Requête dans la base")
        print("")
        result = json.dumps(result)
        parsed = json.loads(result)
        return parsed
    print("")
    print("Requête pas dans la base")
    print("")
    
    r = requests.get(url)
    if r.status_code != 200:
        print("ERREUR LORS DE LA REQUÊTE")
        print(r.text)
        return ""
    
    parsed = json.loads(r.text)
    add_new_request(url, r)
    return parsed
    
def add_new_request(url : str, request : dict):
    new_data = json.loads(request.text)
    try:
        with open("storage.json", "r") as f:
            f_data = json.load(f)
            
        if not isinstance(f_data.get("requests"), list):
            f_data["requests"] = []
            
    except (FileNotFoundError, json.JSONDecodeError):
        f_data = {"requests": []}

    new_entry = {url: new_data}
    f_data["requests"].append(new_entry)
    
    with open("storage.json", "w") as f:
        json.dump(f_data, f, indent=4)



def getRelationsByTypeId(relation_type : str) -> str:
    url = JDM_URL + "relations/by_type_id/" + relation_type
    return make_get_request(url)
    
def getRelationsFromById(node_id : str) -> str:
    url = JDM_URL + "relations/from_by_id/" + node_id
    return make_get_request(url)
    
def getRelationsFromTo(node1_name : str, node2_name : str) -> str:
    url = JDM_URL + "relations/from/" + node1_name + "/to/" + node2_name
    return make_get_request(url)
    
def getRelationsFromToId(node1_id :str, node2_id : str) -> str:
    url = JDM_URL + "relations/from_by_id/" + node1_id+"/to_by_id/"+node2_id
    return make_get_request(url)

def getRelationsFromNodeWithRelationID(node_name : str, r_id : str) -> str:
    url = JDM_URL + "relations/from/" + node_name + "?types_ids=" + r_id
    return make_get_request(url)
    
def getRelationsTo(node_name : str) -> str:
    url = JDM_URL + "relations/to/" + node_name
    return make_get_request(url)
    
def getRelationsToById(node_id : str) -> str:
    url = JDM_URL + "relations/to_by_id/" + node_id
    return make_get_request(url)
    
def getRelationsTypes() -> str:
    url = JDM_URL + "relations_types"
    return make_get_request(url)
    
def getRelationsFrom(node_name : str) -> str:
    url = JDM_URL + "relations/from/" + node_name
    return make_get_request(url)
    

def getNodeById(node_id) -> str:
    url = JDM_URL + "node_by_id/" + node_id
    return make_get_request(url)
    
def getNodeByName(node_name) -> str:
    url = JDM_URL + "node_by_name/" + node_name
    return make_get_request(url)
    
def getNodeRefinements(node_name) -> str:
    url = JDM_URL + "refinements/" + node_name
    return make_get_request(url)

def getNodeTypes() -> str:
    url = JDM_URL + "nodes_types"
    return make_get_request(url)