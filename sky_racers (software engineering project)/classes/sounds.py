#Class that plays background music and sound effects for certain events

import pygame
import sys
from os import path

class Sounds:
    def __init__(self, sound_path):
        self.sound_path = sound_path
        pygame.mixer.init()
        pygame.mixer.music.load(path.join(sound_path, 'music.wav'))
        self.bg_playing = False
        self.start_played = False
        
    def bg_pause(self):
        pygame.mixer.music.pause()
        self.bg_playing = False
        
    def bg_unpause(self):
        pygame.mixer.music.unpause()
        self.bg_playing = True

    def play_bg_music(self):
        pygame.mixer.music.load(path.join(self.sound_path, 'music.wav'))
        pygame.mixer.music.play(-1)
        self.bg_playing = True

    def play_crash_sound(self):
        pygame.mixer.music.load(path.join(self.sound_path, 'crash.wav'))
        pygame.mixer.music.play()

    def play_drift_sound(self):
        pygame.mixer.music.load(path.join(self.sound_path, 'drift.wav'))
        pygame.mixer.music.play()

    def stop_drift_sound(self):
        pygame.mixer.music.pause()

    def play_race_start(self):
        pygame.mixer.music.load(path.join(self.sound_path, 'RaceStart.wav'))
        pygame.mixer.music.play()
        self.start_played = True
    
