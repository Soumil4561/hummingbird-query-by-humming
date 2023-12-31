from fastdtw import fastdtw
def tightness(key,value,content):
    dataline = open("test_dataset/UCR/Adiac_TRAIN", "r")
    dataline = dataline.read()
    dataline = dataline.split("\n")
    dataline = dataline[key].split(",")
    for i in range(len(dataline)):
        dataline[i] = float(dataline[i])
    dataline = dataline[1:]
    
    distance,path = fastdtw(content, dataline)
    
    t = value/distance
    return t
    
    