import pygame
from sky_racers.classes.config import *

class LapTimesBox:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font("game_over.ttf", 50)
        self.grayBoxes = pygame.image.load("grayBoxes.png").convert_alpha()

    def _drawText(self, message, x, y):
        text = self.font.render(message, True, (255, 0, 0))
        textRect = text.get_rect()
        textRect = textRect.move(x, y)
        SCREEN.blit(text, textRect)



    def display(self, car1LapTimes, car2LapTimes):
        SCREEN.blit(self.grayBoxes, (0, 0))
        self._drawText("--HUMAN--", 23, 650)
        self._drawText("Lap 1: " + car1LapTimes[0], 23, 670)
        self._drawText("Lap 2: " + car1LapTimes[1], 23, 690)
        self._drawText("Lap 3: " + car1LapTimes[2], 23, 710)
        self._drawText("Total: " + car1LapTimes[3], 23, 730)

        self._drawText("--ROBOT--", 173, 650)
        self._drawText("Lap 1: " + car2LapTimes[0], 173, 670)
        self._drawText("Lap 2: " + car2LapTimes[1], 173, 690)
        self._drawText("Lap 3: " + car2LapTimes[2], 173, 710)
        self._drawText("Total: " + car2LapTimes[3], 173, 730)

