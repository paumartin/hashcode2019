import numpy as np

POSITION_ROW=0
N_TAGS_ROW=1

numberOfImages = 0
tagsMap = {}
positionMap = {
    "H": set(),
    "V": set()
}

def importer(file_path):
    with open(file_path, 'r') as file:
        firstLine = file.readline()
        numberOfImages = int(firstLine)
        dataSet = {}
        i = 1
        for line in file:
            tokenizedLine = line.split()

            image = {
                "id": i,
                "position": tokenizedLine[POSITION_ROW],
                "tags": set(),
                "nTags": int(tokenizedLine[N_TAGS_ROW])
            }

            positionMap[image["position"]].add(image["id"]) 

            for j in range(2, image["nTags"]+2): 
                tag = tokenizedLine[j]
                if not tag in tagsMap:
                    tagsMap[tag] = set()
                tagsMap[tag].add(image["id"])
                image["tags"].add(tag)
    
            i = i+1
            dataSet[image["id"]] = image
        return dataSet
         
dataset = importer('./inputs/a_example.txt')

print(dataset)
print(tagsMap)
print(positionMap)