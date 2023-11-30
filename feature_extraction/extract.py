import feature_extraction.features as features

def extract(filename, apitch = True, tempo = False, rpitch = False):
    absolute_pitch = features.extract_absolute_pitch(filename)
    relative_pitch = None
    if rpitch:
        relative_pitch = features.extract_relative_pitch(absolute_pitch)
    audio_tempo = None
    if tempo:
        audio_tempo = features.extract_tempo(filename)
    return absolute_pitch, relative_pitch, audio_tempo