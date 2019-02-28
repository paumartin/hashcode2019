import numpy as np
from tqdm import tqdm

POSITION_ROW=0
N_TAGS_ROW=1

fileName = "a_example.txt"
#fileName = "b_lovely_landscapes.txt"
#fileName = "c_memorable_moments.txt"
#fileName = "d_pet_pictures.txt"
#fileName = "e_shiny_selfies.txt"

numberOfImages = 0
tagsMap = {}
positionMap = {
    "H": set(),
    "V": set()
}

slides = [] 
usedImages = set()

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
         
dataset = importer('./inputs/'+fileName)

def calculateImagesDistance(slide1, slide2):
    trans1Tags = set([ tag for imageId in slide1 for tag in dataset[imageId]["tags"]])
    trans2Tags = set([ tag for imageId in slide2 for tag in dataset[imageId]["tags"]]) 

    commonTags = trans1Tags & trans2Tags
    notPresentIn2 = trans1Tags - trans2Tags
    notPresentIn1 = trans2Tags - trans1Tags

    distanceArray = [ len(commonTags), len(notPresentIn1), len(notPresentIn2) ]
    
    return min(distanceArray)

def writeOutputFile():
    f = open("./ouputs/" + fileName, "w")
    f.write(str(len(slides))+"\n")
    for slide in slides:
        f.write(' '.join([str(image) for image in slide])+"\n")

for imageId, image in tqdm(dataset.items()):
    if not imageId in usedImages:
        currentSlide = []
        if image["position"] == "H": 
            currentSlide.append(imageId)
        else:
            positionMap["V"].remove(imageId)
            currentSlide.append(imageId)
            complementaryImage = positionMap["V"].pop()
            currentSlide.append(complementaryImage)
            usedImages.add(complementaryImage)
        usedImages.add(imageId)
        slides.append(currentSlide)

writeOutputFile()
