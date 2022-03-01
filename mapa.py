import pygame
from config import *
from obstaculo import Obstaculo
from jogador import Jogador


class Mapa:
    def __init__(self):

        # Sprites criação
        self.sprites_visiveis = Camera()
        self.sprites_obstaculos = pygame.sprite.Group()

        # Mapa criação
        self.criar_mapa()

    def criar_mapa(self):
        for linha_pos, linha in enumerate(mapa_matriz):
            for coluna_pos, coluna in enumerate(linha):
                x = coluna_pos * 64
                y = linha_pos * 64

                if coluna == 'x':
                    Obstaculo((x, y), [self.sprites_visiveis, self.sprites_obstaculos])
                if coluna == 'p':
                    self.jogador = Jogador((x, y), [self.sprites_visiveis], self.sprites_obstaculos)

    def rodar(self):
        self.sprites_visiveis.desenhar(self.jogador)
        self.sprites_visiveis.update()


class Camera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_superficie = pygame.display.get_surface()
        self.deslocamento = pygame.math.Vector2()

    def desenhar(self, jogador):
        self.deslocamento.x = jogador.rect.centerx - 600
        self.deslocamento.y = jogador.rect.centery - 300

        for sprite in self.sprites():
            sprite.posicao = sprite.rect.topleft - self.deslocamento
            self.display_superficie.blit(sprite.image, sprite.posicao)
