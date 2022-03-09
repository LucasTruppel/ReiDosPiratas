import pygame
from config import *


class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, grupos, sprites_obstaculos):
        super().__init__(grupos)

        self.image = pygame.image.load('./graficos/jogador/baixo_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(-10, -20)
        self.direcao = pygame.math.Vector2()
        self.velocidade = 4

        self.contador_animacao_x = 0
        self.contador_animacao_y = 0
        self.velocidade_animacao = 0.05

        self.sprites_obstaculos = sprites_obstaculos
        self.interagir = False
        self.local = 'inicio'
        self.local_anterior = None
        self.bau = False
        self.estado = 'jogando'

        self.jogador_animacao_baixo = [pygame.image.load('./graficos/jogador/baixo_0.png').convert_alpha(),
                                       pygame.image.load('./graficos/jogador/baixo_1.png').convert_alpha(),
                                       pygame.image.load('./graficos/jogador/baixo_2.png').convert_alpha(),
                                       pygame.image.load('./graficos/jogador/baixo_3.png').convert_alpha()]

        self.jogador_animacao_cima = [pygame.image.load('./graficos/jogador/cima_0.png').convert_alpha(),
                                      pygame.image.load('./graficos/jogador/cima_1.png').convert_alpha(),
                                      pygame.image.load('./graficos/jogador/cima_2.png').convert_alpha(),
                                      pygame.image.load('./graficos/jogador/cima_3.png').convert_alpha()]

        self.jogador_animacao_direita = [pygame.image.load('./graficos/jogador/direita_0.png').convert_alpha(),
                                         pygame.image.load('./graficos/jogador/direita_1.png').convert_alpha(),
                                         pygame.image.load('./graficos/jogador/direita_2.png').convert_alpha(),
                                         pygame.image.load('./graficos/jogador/direita_3.png').convert_alpha()]

        self.jogador_animacao_esquerda = [pygame.image.load('./graficos/jogador/esquerda_0.png').convert_alpha(),
                                          pygame.image.load('./graficos/jogador/esquerda_1.png').convert_alpha(),
                                          pygame.image.load('./graficos/jogador/esquerda_2.png').convert_alpha(),
                                          pygame.image.load('./graficos/jogador/esquerda_3.png').convert_alpha()]

    def comando(self):
        if self.estado == 'jogando':
            botoes = pygame.key.get_pressed()

            if botoes[pygame.K_s]:
                self.direcao.y = 1
            elif botoes[pygame.K_w]:
                self.direcao.y = -1
            else:
                self.direcao.y = 0

            if botoes[pygame.K_d]:
                self.direcao.x = 1
            elif botoes[pygame.K_a]:
                self.direcao.x = -1
            else:
                self.direcao.x = 0

            if botoes[pygame.K_SPACE]:
                self.interagir = True
            else:
                self.interagir = False

    def colisao_horizontal(self):
        for sprite in self.sprites_obstaculos:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direcao.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                elif self.direcao.x < 0:
                    self.hitbox.left = sprite.hitbox.right

    def colisao_vertical(self):
        for sprite in self.sprites_obstaculos:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direcao.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                elif self.direcao.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom

    def mover(self):
        # Movimentação
        if self.direcao.magnitude() != 0:
            self.direcao = self.direcao.normalize()
        self.hitbox.x += self.direcao.x * self.velocidade
        self.colisao_horizontal()
        self.hitbox.y += self.direcao.y * self.velocidade
        self.colisao_vertical()
        self.rect.center = self.hitbox.center

        # Animação do personagem
        if self.direcao.y != 0:
            self.contador_animacao_y += self.velocidade_animacao
            if self.contador_animacao_y >= 4:
                self.contador_animacao_y = 0
            if self.direcao.y > 0:
                self.image = self.jogador_animacao_baixo[int(self.contador_animacao_y)]
            else:
                self.image = self.jogador_animacao_cima[int(self.contador_animacao_y)]
        elif self.direcao.x != 0:
            self.contador_animacao_x += self.velocidade_animacao
            if self.contador_animacao_x >= 4:
                self.contador_animacao_x = 0
            if self.direcao.x > 0:
                self.image = self.jogador_animacao_direita[int(self.contador_animacao_x)]
            else:
                self.image = self.jogador_animacao_esquerda[int(self.contador_animacao_x)]

        # Coloca a imagem certa quando o personagem está parado.
        if self.direcao == (0, 0):
            self.contador_animacao_x = 0
            self.contador_animacao_y = 0
            if self.image in self.jogador_animacao_direita:
                self.image = self.jogador_animacao_direita[0]
            elif self.image in self.jogador_animacao_esquerda:
                self.image = self.jogador_animacao_esquerda[0]
            elif self.image in self.jogador_animacao_cima:
                self.image = self.jogador_animacao_cima[0]
            elif self.image in self.jogador_animacao_baixo:
                self.image = self.jogador_animacao_baixo[0]

    def encontrar_local(self):
        self.local_anterior = self.local
        if 1700 < self.rect.x < 2600 and 950 < self.rect.y < 1500:
            self.local = 'inicio'
        elif 1200 < self.rect.x < 1750 and 1250 < self.rect.y < 2070:
            self.local = 'final'
            if 1200 < self.rect.x < 1459 and 1250 < self.rect.y < 1370:
                self.bau = True
        else:
            self.local = 'labirinto'

    def interagir_bau(self):
        if self.bau and self.interagir and self.estado == 'jogando':
            self.estado = 'final'
            self.interagir = False
            self.direcao.x, self.direcao.y = 0, 0
            pygame.mixer.music.load('./musicas/good_time.ogg')
            pygame.mixer.music.play(-1)

    def update(self):
        self.comando()
        self.mover()
        self.encontrar_local()
        self.interagir_bau()
