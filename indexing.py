import os
import pretty_midi
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elastic import elastic_connect as elastic_connect

def create_index(es):
    load_dotenv()
    mapping = {
                "mappings": {
                    "properties": {
                        'song': { 'type': 'text' },
                        'tempo': { 'type': 'float'},
                        'paa_lower': { 'type': 'float'},
                        'paa_upper': { 'type': 'float'},
                        'paa_relative': { 'type': 'float'}
                    }
                }
            }
            
    ES_INDEX = os.getenv("ES_INDEX")
    if(es.indices.exists(index=ES_INDEX)):
        es.indices.delete(index=ES_INDEX)

    es.indices.create(index=ES_INDEX, body=mapping, ignore=400)
    
def index():
    #1. Main module asks for query input
    #2. Gives query to feature extraction module
    #3. Sends the query to pitch extraction module to gain pitch vectors and note duration.
    #4. Find the tempo and estimate the relative pitch of the query
    #5. Create a new folder for the query
    #6. Create a new file for the query
    #7. Write the absolute pitch, relative pitch and tempo to the file
    #8. Create a new folder for the query
    #9. Create a new file for the query
    #10. Write the absolute pitch, relative pitch and tempo to the file
    #11. Repeat 5-10 for all files in the database
    #12. Return the database
    # database = {}
    # for root, dirs, files in os.walk("database"):
    #     for file in files:
    #         if file.endswith(".wav"):
    #             filename = os.path.join(root, file)
    #             absolute_pitch, tempo, relative_pitch = extract.extract(filename, apitch=True, tempo=True, rpitch=True)
    #             database[filename] = (absolute_pitch, tempo, relative_pitch)
    # return database
    
    #now index the song
    es = elastic_connect()
            
    #create index
    create_index(es)
    
    for song in os.listdir("test_dataset"):
        #given song is in midi format
        print(song)
        if song.endswith(".mid"):
            mid_data = pretty_midi.PrettyMIDI("test_dataset/" + song)
            
            
            
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # pitch_vector = []
            # for notes in mid_data.instruments[0].notes:
            #     pitch_vector.append(notes.pitch)
            
            # #now we have the pitch vector, lets find the tempo
            # tempo = mid_data.estimate_tempo()
            
            # #calculate the relative pitch
            # relative_pitch = []
            # for i in range(1, len(pitch_vector)):
            #     relative_pitch.append(pitch_vector[i] - pitch_vector[i-1])
                
            # #find the lower and upper envelope of the relative pitch
            # env_lower, env_upper = envelopes(relative_pitch, 5)
            
            # #find the paa of the lower, upper envelope and relative pitch
            # paa_lower = paa(env_lower, 30)
            # paa_upper = paa(env_upper, 30)
            # paa_relative = paa(relative_pitch, 30)
            
            # ES_INDEX = os.getenv("ES_INDEX")
            
            # #index the song
            # es.index(index=ES_INDEX, body={
            #     'song': song,
            #     'tempo': tempo,
            #     'paa_lower': paa_lower,
            #     'paa_upper': paa_upper,
            #     'paa_relative': paa_relative
            # })

def index_text():
    for filename in os.listdir("test_dataset/dataset_beetles"):
        try:
            midi_data = pretty_midi.PrettyMIDI("test_dataset/dataset_beetles/" + filename)
        except:
            continue
        
        #first find the song duration
        song_duration = midi_data.get_end_time()
        
        segment_duration = 15
        
        f = open('index_dataset/' + filename + '.txt', 'w')
        
        for i in range(0, int(song_duration) - segment_duration):
            prev = 1
            for j in range(prev, len(midi_data.instruments[0].notes)):
                note = midi_data.instruments[0].notes[j]
                if note.start > i and note.end < i + segment_duration:
                    # relative pitches should be written
                    f.write(str(note.pitch - midi_data.instruments[0].notes[j - 1].pitch) + " ")
                    # f.write(str(abs(note.pitch)) + " ")
            f.write("\n")
            prev = j + 1

        f.close()
        
#Lower-bounding technique and indexing scheme
def envelopes(X, k):
    #first we recieve a time series X, and we compute the upper and lower envelope of X
    env_lower = []
    env_upper = []
    
    #calcalating lower envelope
    for i in range(0, len(X)):
        lowest = 1000
        for j in range(-k,k+1):
            if(i+j >= 0 and i+j < len(X)):
                if(X[i+j] < lowest):
                    lowest = X[i+j]
        env_lower.append(lowest)
    
    #calcalating upper envelope
    for i in range(0, len(X)):
        highest = 0
        for j in range(-k,k+1):
            if(i+j >= 0 and i+j < len(X)):
                if(X[i+j] > highest):
                    highest = X[i+j]
        env_upper.append(highest)
    
    return env_lower, env_upper

def paa(X,m):
    #find the piecewise aggregate approximation of X with m segments
    #first we find the length of each segment
    length = len(X)//m
    
    #then we find the mean of each segment
    paa = []
    for i in range(1, m):
        sum = 0
        for j in range((i-1)*length+1, i*length):
            sum += X[j]
        paa.append(sum/length)
        
    return paa

#index_text()