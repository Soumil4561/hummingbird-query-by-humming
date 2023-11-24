import input_query.record as record
import feature_extraction.extract as extract

def query():
    record_input = record.RecordQuery(15)
    features = extract(record_input, apitch=True, tempo=True, rpitch=True)
    
    
    

if __name__ == "__main__":
    # # Create a new instance of the application class
    # app = QApplication(sys.argv)
    # # Show the application's GUI
    # view = MainWindow()
    # view.show()
    # # Run the application's main loop
    # sys.exit(app.exec_())
    query()