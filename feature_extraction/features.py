import librosa
import numpy as np
import pretty_midi
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


def extract_absolute_pitch(filename):
    model_output, midi_data, note_events = predict(filename, ICASSP_2022_MODEL_PATH)
    with open("user_input/input.mid", 'wb') as output_file:
        midi_data.write(output_file)
    midi_data = pretty_midi.PrettyMIDI("user_input/input.mid")
    
    #get all pitches 
    pitches = []
    for note in midi_data.instruments[0].notes:
        pitches.append(note.pitch)
    
    return pitches

def extract_relative_pitch(absolute_pitch):
    relative_pitch = []
    for i in range(1, len(absolute_pitch)):
        relative_pitch.append(absolute_pitch[i] - absolute_pitch[i-1])
    return relative_pitch

def extract_tempo(filename):
    pm = pretty_midi.PrettyMIDI("user_input/input.mid")
    tempo = pm.get_tempo_changes()
    return tempo
    

import numpy as np
import librosa
import matplotlib.pyplot as plt

def compute_autocorrelation(signal):
    autocorr = np.correlate(signal, signal, mode='full')
    return autocorr[len(autocorr)//2:]

def compute_sacf(low_channel, high_channel_env):
    autocorr_low = compute_autocorrelation(low_channel)
    autocorr_high = compute_autocorrelation(high_channel_env)
    sacf = autocorr_low + autocorr_high
    return sacf

def enhance_sacf(sacf):
    # Clip the original SACF to positive values
    clipped_sacf = np.clip(sacf, 0, np.inf)

    # Time-scale the clipped SACF by a factor of two
    scaled_sacf = np.interp(2 * np.arange(len(clipped_sacf)), np.arange(len(clipped_sacf)), clipped_sacf)

    # Subtract the scaled SACF from the original clipped SACF
    enhanced_sacf = clipped_sacf - scaled_sacf

    return enhanced_sacf


def estimate_pitch(audio_file):
    signal, sr = librosa.load(audio_file, sr=None)

    # Check if the signal is too short
    if len(signal) < 2048:
        print("Error: Input signal is too short for processing.")
        return None

    # Spliting high and low channels
    low_channel = signal[signal < 1000]
    high_channel = signal[signal >= 1000]

    high_channel_env = np.abs(librosa.stft(high_channel)[0])

    
    sacf = compute_sacf(low_channel, high_channel_env)

    # Esacf
    enhanced_sacf = enhance_sacf(sacf)

    
    hop_size = int(0.05 * sr)  
    
    estimated_pitches, _, _ = librosa.pyin(enhanced_sacf, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), hop_length=hop_size)

    
    estimated_pitches = np.round(estimated_pitches)
    
    #remove the nan values
    estimated_pitches = estimated_pitches[~np.isnan(estimated_pitches)]

    timestamps = librosa.frames_to_time(np.arange(len(estimated_pitches)), sr=sr, hop_length=hop_size)

    return list(zip(timestamps, estimated_pitches))

# audio_file_path = "input.wav"
# extract_absolute_pitch(audio_file_path)

#
