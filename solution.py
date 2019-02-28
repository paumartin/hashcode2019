import numpy as np
from tqdm import tqdm

POSITION_ROW=0
N_TAGS_ROW=1

fileNames = [ "a_example.txt", "b_lovely_landscapes.txt", "c_memorable_moments.txt", "d_pet_pictures.txt", "e_shiny_selfies.txt" ] 
# fileNames = [ "a_example.txt" ] 

def importer(file_path):
    with open(file_path, 'r') as file:
        firstLine = file.readline()
        numberOfImages = int(firstLine)
        dataSet = {}
        i = 0
        for line in file:
            tokenizedLine = line.split()

            image = {
                "id": i,
                "position": tokenizedLine[POSITION_ROW],
                "tags": set(),
                "nTags": int(tokenizedLine[N_TAGS_ROW])
            }

            pendingImages.add(i)
            positionMap[image["position"]].add(image["id"]) 

            for j in range(2, image["nTags"]+2): 
                tag = tokenizedLine[j]
                if not tag in tagsMap:
                    tagsMap[tag] = set()
                tagsMap[tag].add(image["id"])
                if image["position"] != "H":
                    if not tag in vTagsMap:
                        vTagsMap[tag] = set()
                    vTagsMap[tag].add(image["id"])
                image["tags"].add(tag)
    
            i = i+1
            dataSet[image["id"]] = image
        return (numberOfImages, dataSet)
         
def calculateImagesDistance(slide1, slide2):
    trans1Tags = set([ tag for imageId in slide1 for tag in dataset[imageId]["tags"]])
    trans2Tags = set([ tag for imageId in slide2 for tag in dataset[imageId]["tags"]]) 

    commonTags = trans1Tags & trans2Tags
    notPresentIn2 = trans1Tags - trans2Tags
    notPresentIn1 = trans2Tags - trans1Tags

    distanceArray = [ len(commonTags), len(notPresentIn1), len(notPresentIn2) ]
    
    return min(distanceArray)

def writeOutputFile(fileName):
    f = open("./ouputs/" + fileName, "w")
    f.write(str(len(slides))+"\n")
    for slide in slides:
        f.write(' '.join([str(image) for image in slide])+"\n")

def findBestCandidate(prevSlide): 

    previousTags = set([ tag for imageId in prevSlide for tag in dataset[imageId]["tags"]])
    candidates = []
    for tag in previousTags:
        candidate = []
        if len(tagsMap[tag]) > 0:
            currentImage = tagsMap[tag].pop()
            candidate.append(currentImage)
            if dataset[currentImage]["position"] != "H": 
                positionMap["V"].discard(currentImage)
                currentImage2=None
                for tag2 in previousTags:
                    if tag2 in vTagsMap and len(vTagsMap[tag2]) > 0:
                        currentImage2 = vTagsMap[tag2].pop()
                        tagsMap[tag2].discard(currentImage2)
                        positionMap["V"].discard(currentImage2)
                if not currentImage2: 
                    currentImage2 = positionMap["V"].pop()
                    [ tagsMap[tagToRemove].discard(currentImage2) for tagToRemove in dataset[currentImage2]["tags"] ]
                    [ vTagsMap[tagToRemove].discard(currentImage2) for tagToRemove in dataset[currentImage2]["tags"] ]
                candidate.append(currentImage2)
            else: 
                positionMap["H"].discard(currentImage)
        else:
            if len(positionMap["H"]) > 0:
                candidate = [ positionMap["H"].pop() ]
            elif len(positionMap["V"]) >= 2:
                candidate = [ positionMap["V"].pop(), positionMap["V"].pop() ]
            elif  len(positionMap["V"]) >= 1:
                candidate = [ positionMap["V"].pop() ]
             
            if len(candidate) > 0:
                for currentImage in candidate:
                    [ tagsMap[tagToRemove].discard(currentImage) for tagToRemove in dataset[currentImage]["tags"] ]
                    [ vTagsMap[tagToRemove].discard(currentImage)  if tagToRemove in vTagsMap else None for tagToRemove in dataset[currentImage]["tags"] ]

        if len(candidate) > 0:
            candidates.append(candidate)

    punctuations = [ calculateImagesDistance(prevSlide, candidate) for candidate in candidates ]  
    bestIndex = punctuations.index(max(punctuations))
    bestCandidate = candidates[bestIndex]
    candidates.remove(bestCandidate)

    for candidate in candidates: 
        if dataset[candidate[0]]["position"] != "H": 
            [ vTagsMap[tagToAdd].add(candidate[0]) for tagToAdd in dataset[candidate[0]]["tags"] ]
            [ tagsMap[tagToAdd].add(candidate[0]) for tagToAdd in dataset[candidate[0]]["tags"] ]
            positionMap["V"].add(candidate[0])

            [ vTagsMap[tagToAdd].add(candidate[1]) for tagToAdd in dataset[candidate[1]]["tags"] ]
            [ tagsMap[tagToAdd].add(candidate[1]) for tagToAdd in dataset[candidate[1]]["tags"] ]
            positionMap["V"].add(candidate[1])
        else: 
            [ tagsMap[tagToAdd].add(candidate[0]) for tagToAdd in dataset[candidate[0]]["tags"] ]
            positionMap["H"].add(candidate[0])

    [ usedImages.add(currentImage) for currentImage in bestCandidate ]
    [ pendingImages.discard(currentImage) for currentImage in bestCandidate ]

    return bestCandidate

for fileName in fileNames: 

    tagsMap = {}
    positionMap = {
        "H": set(),
        "V": set()
    }

    vTagsMap = {}

    slides = [] 
    usedImages = set()
    pendingImages = set()

    numberOfImages, dataset = importer('./inputs/'+fileName)

    # choose first image
    initialSlide = [ positionMap["H"].pop() ] if len(positionMap["H"]) > 0 else [ positionMap["V"].pop(), positionMap["V"].pop()]
    [ usedImages.add(imageId) for imageId in initialSlide ]
    [ pendingImages.remove(imageId) for imageId in initialSlide ]
    [ tagsMap[tagToRemove].discard(currentImage) for currentImage in initialSlide for tagToRemove in dataset[currentImage]["tags"]  ]
    [ vTagsMap[tagToRemove].discard(currentImage) if tagToRemove in vTagsMap else None for currentImage in initialSlide for tagToRemove in dataset[currentImage]["tags"] ]

    slides.append(initialSlide)

    previousSlide = initialSlide

    while len(pendingImages) > 0:
        bestCandidate = findBestCandidate(previousSlide)
        slides.append(bestCandidate)
        previousSlide = bestCandidate

    writeOutputFile(fileName)

