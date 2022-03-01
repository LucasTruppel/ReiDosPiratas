import pygame
from config import *


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, pos, grupos):
        super().__init__(grupos)
        self.image = pygame.image.load('./graficos/obstaculos/arvore.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
