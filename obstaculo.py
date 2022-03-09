import pygame
from config import *

imagens = {
  'x': './graficos/obstaculos/invisivel.png',
  'a': './graficos/obstaculos/a.png',
  'b': './graficos/obstaculos/b.png',
  'c': './graficos/obstaculos/c.png',
  'd': './graficos/obstaculos/d.png',
  'e': './graficos/obstaculos/e.png',
  'f': './graficos/obstaculos/f.png',
  'r': './graficos/obstaculos/r.png',
  '1': './graficos/obstaculos/1.png',
  '2': './graficos/obstaculos/2.png',
  '3': './graficos/obstaculos/3.png',
  '4': './graficos/obstaculos/4.png',
  '5': './graficos/obstaculos/5.png',
  't': './graficos/obstaculos/t.png',
  'm': './graficos/obstaculos/m.png'
}


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, tipo):
        super().__init__(grupos)

        self.image = pygame.image.load(imagens[tipo]).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-8, -16)
        self.tipo = tipo
