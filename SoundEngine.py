import pyaudio
import simpleaudio
from pydub import AudioSegment
from random import randint
from typing import Literal

PlayingSound = None
SoundRegistry = {}
SoundList = []
for soundName in SoundRegistry:
    if "gain" not in soundName:
        SoundList.append(soundName)
AllSounds = Literal[tuple(SoundList)]

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
def playSound(soundName: AllSounds):
    if soundName in SoundRegistry:
        soundPaths = SoundRegistry[soundName]
        usePath = soundPaths[randint(0, len(soundPaths) - 1)]
        gain = SoundRegistry[soundName + str("gain")]
        try:
            seg = AudioSegment.from_wav(usePath) + gain
            global PlayingSound
            PlayingSound = simpleaudio.play_buffer(
                seg.raw_data,
                num_channels=seg.channels,
                bytes_per_sample=seg.sample_width,
                sample_rate=seg.frame_rate
            )
            try:
                PlayingSound.wait_done()
            except KeyboardInterrupt:
                PlayingSound.stop()
        except:
            RuntimeError(f"Could not play {soundName}")
    else:
        RuntimeError(f"Missing Sound Registry for sound \"{soundName}\"")

"""May generate a warning when playing a sound, this can be ignored."""
playSound("Sound")