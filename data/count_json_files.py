import os, json

data_dir = "./data/json/"

os.makedirs(data_dir, exist_ok=True)

onlyfiles = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
for file in onlyfiles:
    with open(data_dir+file, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(file + " : " + str(len(data)))