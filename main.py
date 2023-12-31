import input_query.record as record
import feature_extraction.extract as extract

from indexing import envelopes as envelopes
from indexing import paa as paa
from searching import text_search as search
from searching import elastic_search as search_elastic
from searching import ts_search_text as search_ts_text

from tightness import tightness

def query():
    #1. Main module asks for query input
    #record_input = record.RecordQuery(15)
    
    #2. Gives query to feature extraction module
    #3. Sends the query to pitch extraction module to gain pitch vectors and note duration.
    #4. Find the tempo and estimate the relative pitch of the query
    absolute_pitch, relative_pitch, tempo = extract.extract("user_input/query.wav", apitch=True, tempo=True, rpitch=True)
    search(relative_pitch,absolute_pitch,tempo)    
    # # #create the envelope of the relative pitch
    # env_lower, env_upper = envelopes(relative_pitch, 5)
    
    # #find the paa of the lower, upper envelope and relative pitch
    # f = open("query_samples/Adiac_TRAIN", "r")
    # content = f.read()
    # content = content.split("\n")
    # content = content[0].split(",")
    
    # for i in range(len(content)):
    #     content[i] = float(content[i])
        
    # env_lower, env_upper = envelopes(content, 5)
    # paa_lower = paa(env_lower, 4)
    # paa_upper = paa(env_upper, 4)
    # paa_relative = paa(content, 4)
    
    # # #send these to search module
    # results = search_ts_text(paa_lower, paa_upper, paa_relative)
    # for i in range(len(results)):
    #     key,value = results[i].popitem()
    #     key = key.split(".")
    #     key = int(key[0])
        
    #     t = tightness(key,value,content)
    #     print(t)
        
    

if __name__ == "__main__":
    # # Create a new instance of the application class
    # app = QApplication(sys.argv)
    # # Show the application's GUI
    # view = MainWindow()
    # view.show()
    # # Run the application's main loop
    # sys.exit(app.exec_())
    query()