import input_query.record as record
import feature_extraction.extract as extract

from indexing import envelopes as envelopes
from indexing import paa as paa
from searching import text_search as search

def query():
    #1. Main module asks for query input
    #record_input = record.RecordQuery(15)
    
    #2. Gives query to feature extraction module
    #3. Sends the query to pitch extraction module to gain pitch vectors and note duration.
    #4. Find the tempo and estimate the relative pitch of the query
    absolute_pitch, relative_pitch, tempo = extract.extract("user_input/query.wav", apitch=True, tempo=True, rpitch=True)
    #print(relative_pitch)
    search(relative_pitch)    
    # #create the envelope of the relative pitch
    # env_lower, env_upper = envelopes(relative_pitch, 5)
    
    # #find the paa of the lower, upper envelope and relative pitch
    # paa_lower = paa(env_lower, 30)
    # paa_upper = paa(env_upper, 30)
    # paa_relative = paa(relative_pitch, 30)
    
    # #send these to search module
    # results = search(paa_lower, paa_upper, paa_relative)
    
    # print(results)

if __name__ == "__main__":
    # # Create a new instance of the application class
    # app = QApplication(sys.argv)
    # # Show the application's GUI
    # view = MainWindow()
    # view.show()
    # # Run the application's main loop
    # sys.exit(app.exec_())
    query()