def min(value1, value2, value3):
    if value1 < value2 && value1 < value3:
        return value1
    if value2 < value1 && value2 < value3:
        return value2
    return value3

def writeOutputFile(filename, slides):
    f = open(filename, "w")
    f.write(len(slides))
    for slide in slides:
        for picture in slide:
            f.write(picture)