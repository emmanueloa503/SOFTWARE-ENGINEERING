
from ..classes.sounds import Sounds
import pygame
import os
from os import path
import time

test_passed = True
sound_path = path.abspath(path.join(path.dirname(__file__), os.pardir))
sound_path = path.join(sound_path, 'assets')
sound_path = path.join(sound_path, 'sounds')

sounds = Sounds(sound_path)

pygame.mixer.init()
sounds.play_bg_music()
time.sleep(1)
ui = int(input("Is the background music playing? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False
sounds.bg_pause()
ui = int(input("Did the background music pause? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False
sounds.bg_unpause()
ui = int(input("Did the background music resume? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False
sounds.bg_pause()
sounds.play_crash_sound()
ui = int(input("Did the crash sound play? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False
sounds.play_drift_sound()
ui = int(input("Did the drift sound play? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False
sounds.stop_drift_sound()
ui = int(input("Did the drift sound stop? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False
sounds.play_race_start()
ui = int(input("Did the race start play? (1/0): "))
if ui == 1:
    print("Passed")
else:
    print("Test Failed")
    test_passed = False

if test_passed:
    print("Sounds Passed")
else:
    print("Sounds Failed")