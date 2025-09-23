import requests, json, os

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
        return ''
    
    for request in f_data["requests"]:
        if url in request:
            return request[url]
    return ''

def create_storage():
    if not os.path.exists("storage.json"):
        with open("storage.json", "w") as f:
            json.dump({"requests" : []}, f, indent=4)
def make_get_request(url):
    create_storage()
    result = search_result(url)
    if result != '':
        print(result)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Erreur lors de la requête")
    
    new_data = json.loads(r.text)
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
        

def getRelationsByTypeId(relation_type : str):
    url = JDM_URL + "relations/by_type_id/" + relation_type
    make_get_request(url)
    
def getRelationsFromById(node_id : str):
    url = JDM_URL + "relations/from_by_id/" + node_id
    make_get_request(url)
    
def getRelationsFromTo(node1_name : str, node2_name : str):
    url = JDM_URL + "relations/from/" + node1_name + "/to/" + node2_name
    make_get_request(url)
    
def getRelationsFromToId(node1_id :str, node2_id : str):
    url = JDM_URL + "relations/from_by_id/" + node1_id+"/to_by_id/"+node2_id
    make_get_request(url)
    
def getRelationsTo(node_name : str):
    url = JDM_URL + "relations/to/" + node_name
    make_get_request(url)
    
def getRelationsToById(node_id : str):
    url = JDM_URL + "relations/to_by_id/" + node_id
    make_get_request(url)
    
def getRelationsTypes():
    url = JDM_URL + "relations_types"
    make_get_request(url)
    
def getRelationsFrom(node_name : str):
    url = JDM_URL + "relations/from/" + node_name
    make_get_request(url)
    

def getNodeById(node_id):
    url = JDM_URL + "node_by_id/" + node_id
    make_get_request(url)
    
def getNodeByName(node_name):
    url = JDM_URL + "node_by_name/" + node_name
    make_get_request(url)
    
def getNodeRefinements(node_name):
    url = JDM_URL + "refinements/" + node_name
    make_get_request(url)

def getNodeTypes():
    url = JDM_URL + "nodes_types"
    make_get_request(url)