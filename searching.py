import os
from elasticsearch import Elasticsearch
from elastic import elastic_connect as elastic_connect
from dtw import ldtw as ldtw
from dtw import dtw as dtw
from fastdtw import fastdtw

def elastic_search(paa_lower, paa_upper, paa_relative):
    es = elastic_connect()
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "paa_lower": {
                                "gte": paa_lower - 0.1,
                                "lte": paa_lower + 0.1
                            }
                        }
                    },
                    {
                        "range": {
                            "paa_upper": {
                                "gte": paa_upper - 0.1,
                                "lte": paa_upper + 0.1
                            }
                        }
                    },
                    {
                        "range": {
                            "paa_relative": {
                                "gte": paa_relative - 0.1,
                                "lte": paa_relative + 0.1
                            }
                        }
                    }
                ]
            }
        }
    }
    res = es.search(index="midi", body=query)
    print(res['hits']['hits'])
    return res['hits']['hits']


def elastic_search(paa_lower, paa_upper, paa_ts):
    es = elastic_connect()
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "paa_lower": {
                                "gte": paa_lower - 0.1,
                                "lte": paa_lower + 0.1
                            }
                        }
                    },
                    {
                        "range": {
                            "paa_upper": {
                                "gte": paa_upper - 0.1,
                                "lte": paa_upper + 0.1
                            }
                        }
                    },
                    {
                        "range": {
                            "paa_ts": {
                                "gte": paa_ts - 0.1,
                                "lte": paa_ts + 0.1
                            }
                        }
                    }
                ]
            }
        }
    }
    res = es.search(index="midi", body=query)
    print(res['hits']['hits'])
    return res['hits']['hits']

def text_search(relative_pitches,absolute_pitches,tempo):
    results1 = []
    print("Searching...")
    for filename in os.listdir("index_dataset/index_beetles/rel"):
        smallest = 10000000
        #best_segment = None
        f = open('index_dataset/index_beetles/' + filename, 'r')
        content = f.read()
        notes = content.split("\n")
        
        for note in notes:
            if note == '':
                continue
            #convert string to array of integers
            
            note = note.split(" ")
            #remove last element
            note.pop()
            note = list(map(int, note))
            #distance = ldtw(relative_pitches, note, 0.2,20)
            distance,path = fastdtw(relative_pitches, note)
            #distance = dtw(relative_pitches, note)
            if distance < smallest:
                smallest = distance
                #best_segment = note
        
        results1.append({filename: smallest})          
        f.close()
    
    # results2 = []
    # for filename in os.listdir("index_dataset/index_beetles/abs"):
    #     smallest = 10000000
    #     #best_segment = None
    #     f = open('index_dataset/index_beetles/abs/' + filename, 'r')
    #     content = f.read()
    #     notes = content.split("\n")
        
    #     for note in notes:
    #         if note == '':
    #             continue
    #         #convert string to array of integers
            
    #         note = note.split(" ")
    #         #remove last element
    #         note.pop()
    #         note = list(map(int, note))
    #         #distance = ldtw(relative_pitches, note, 0.2,20)
    #         distance,path = fastdtw(absolute_pitches, note)
    #         #distance = dtw(relative_pitches, note)
    #         if distance < smallest:
    #             smallest = distance
    #             #best_segment = note
        
    #     results2.append({filename: smallest})          
    #     f.close()
        
    # results3 = []
    # for filename in os.listdir("index_dataset/index_beetles/tempo"):
    #     f = open('index_dataset/index_beetles/tempo/' + filename, 'r')
    #     content = f.read()
    #     notes = content.split("\n")
    #     notes = notes[0]
    #     notes = float(notes)
        
    #     distance = abs(tempo - notes)
        
    #     results3.append({filename: distance})          
    #     f.close()
    #sort the results based on smallest distance
    
    #add all the results together based on weights and sort them
    results = []
    # for i in range(len(results1)):
    #     key1,value1 = results1[i].popitem()
    #     #key2,value2 = results2[i].popitem()
    #     key3,value3 = results3[i].popitem()
        
    #     #value = 0.5*value1 + 0.5*value2 + 0.5*value3
    #     value = 2*value1 + 1*value3
    #     results.append({key1: value})
    
    results = sorted(results1, key=lambda k: list(k.values())[0])
    
    #store the results in a file
    f = open("results.txt", "w")
    for result in results:
        f.write(str(result) + "\n")
    f.close()
    
    print("Done! Results stored in results.txt")
    
def ts_search_text(paa_lower, paa_upper, paa_ts):
    results = []
    for filename in os.listdir("index_dataset/UCR"):
        f = open("index_dataset/UCR/"+filename, "r")
        content = f.read()
        notes = content.split("\n")
        notes.pop()
        
        for i in range(len(notes)):
            #remove the first and last element
            notes[i] = notes[i][1:]
            notes[i] = notes[i][:-1]
            
            #convert to float
            notes[i] = notes[i].split(",")
            
            for j in range(len(notes[i])):
                notes[i][j] = float(notes[i][j])
                
        distance = ldtw(paa_ts,notes[2], 0.1,20)
        #distance,path = fastdtw(paa_ts, notes[2])
        #distance = dtw(paa_ts, notes[2])
        
        results.append({filename: distance})
        f.close()
    
    #sort the results based on smallest distance
    results = sorted(results, key=lambda k: list(k.values())[0])
    
    #store the results in a file
    f = open("results.txt", "w")
    for result in results:
        f.write(str(result) + "\n")
    f.close()
    
    return results
    
            
        