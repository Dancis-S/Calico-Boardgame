import pygame

class GameScreen:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        self.screen.fill((50, 50, 50))
