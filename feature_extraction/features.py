import librosa
import numpy as np

def extract_absolute_pitch(filename):
    #load the audio file
    y, sr = librosa.load(filename)
    
    #extract the pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    #get the index of the maximum pitch
    index = np.argmax(pitches)
    
    #get the frequency of the maximum pitch
    absolute_pitch = pitches[index]
    
    return absolute_pitch

def extract_relative_pitch(filename, absolute_pitch):
    #load the audio file
    y, sr = librosa.load(filename)
    
    #extract the pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    #get the index of the maximum pitch
    index = np.argmax(pitches)
    
    #get the frequency of the maximum pitch
    relative_pitch = pitches[index] - absolute_pitch
    
    return relative_pitch

def extract_tempo(filename):
    #load the audio file
    y, sr = librosa.load(filename)
    
    #extract the tempo
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    return tempo