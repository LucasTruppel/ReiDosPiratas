import pygame
from config import *


class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, sprites_obstaculos):
        super().__init__(grupos)
        self.image = pygame.image.load('./graficos/jogador/jogador_direita.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direcao = pygame.math.Vector2()
        self.velocidade = 5

        self.sprites_obstaculos = sprites_obstaculos

    def comando(self):
        botoes = pygame.key.get_pressed()

        if botoes[pygame.K_w]:
            self.direcao.y = -1
        elif botoes[pygame.K_s]:
            self.direcao.y = 1
        else:
            self.direcao.y = 0

        if botoes[pygame.K_d]:
            self.direcao.x = 1
        elif botoes[pygame.K_a]:
            self.direcao.x = -1
        else:
            self.direcao.x = 0

    def mover(self, velocidade):
        if self.direcao.magnitude() != 0:
            self.direcao = self.direcao.normalize()

        self.rect.x += self.direcao.x * velocidade
        self.colisao('horizontal')

        self.rect.y += self.direcao.y * velocidade
        self.colisao('vertical')

        # Direção que o personagem está olhando.
        if self.direcao.x > 0:
            self.image = pygame.image.load('./graficos/jogador/jogador_direita.png').convert_alpha()
        elif self.direcao.x < 0:
            self.image = pygame.image.load('./graficos/jogador/jogador_esquerda.png').convert_alpha()

    def colisao(self, direcao):
        if direcao == 'horizontal':
            for sprite in self.sprites_obstaculos:
                if sprite.rect.colliderect(self.rect):
                    if self.direcao.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direcao.x < 0:
                        self.rect.left = sprite.rect.right

        if direcao == 'vertical':
            for sprite in self.sprites_obstaculos:
                if sprite.rect.colliderect(self.rect):
                    if self.direcao.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direcao.y < 0:
                        self.rect.top = sprite.rect.bottom



    def update(self):
        self.comando()
        self.mover(self.velocidade)



