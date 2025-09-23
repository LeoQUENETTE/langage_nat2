import json
if __name__ == "__main__":
    root = "data/"
    with open(f"{root}phrases_250.json", "r") as f:
        f_data = json.load(f)
        doublons = []
        for p in f_data["phrases"]:
            for p2 in f_data:
                if p2 == p:
                    doublons.append(p)
    for i in doublons:
        print(doublons)