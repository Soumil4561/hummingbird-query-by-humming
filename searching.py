import os
from elasticsearch import Elasticsearch
from elastic import elastic_connect as elastic_connect
from dtw import ldtw as ldtw
from dtw import dtw as dtw
from fastdtw import fastdtw
import heapq

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

def text_search(relative_pitches):
    results = []
    print("Searching...")
    for filename in os.listdir("index_dataset"):
        smallest = 10000000
        #best_segment = None
        f = open('index_dataset/' + filename, 'r')
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
            distance = ldtw(relative_pitches, note, 0.2)
            #distance,path = fastdtw(relative_pitches, note)
            #distance = dtw(relative_pitches, note)
            if distance < smallest:
                smallest = distance
                #best_segment = note
        
        results.append({filename: smallest})          
        f.close()
    
    #sort the results based on smallest distance
    results = sorted(results, key=lambda k: list(k.values())[0])
    
    #store the results in a file
    f = open("results.txt", "w")
    for result in results:
        f.write(str(result) + "\n")
    f.close()
    
    print("Done! Results stored in results.txt")