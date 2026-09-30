import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from random import randint

SoundRegistry = {}

"""Stores Sound names and paths in a dictionary"""
def register(soundName: str, soundPath: list, gain: int):
    SoundRegistry[soundName] = soundPath
    SoundRegistry[soundName + str("gain")] = gain

"""
Register Sound as a SoundName that links to one or multiple paths. 
Always store paths in list. 
The gain is measured in db and increases or decreases the volume of the sound.
Please store all sounds in the 'sounds' folder for organisation purposes.
"""
register("Sound",["sounds/TestSound.wav"],30)

"""
Finds the path(s) associated with the SoundName.
If a SoundName is associated with multiple paths, a path will be chosen at random to play.
"""
def playSound(soundName: str):
    if soundName in SoundRegistry:
        soundPaths = SoundRegistry[soundName]
        usePath = soundPaths[randint(0, len(soundPaths) - 1)]
        gain = SoundRegistry[soundName + str("gain")]
        try:
            play(AudioSegment.from_wav(usePath) + gain)
        except:
            RuntimeError(f"Could not play {soundName}")
    else:
        RuntimeError(f"Missing Sound Registry for sound \"{soundName}\"")

"""May generate a warning when playing a sound, this can be ignored."""
playSound("Sound")