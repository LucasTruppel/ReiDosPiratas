import pygame
import sys
from mapa import *
from menu import *


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Rei dos Piratas')

        self.tela = pygame.display.set_mode((1200, 600))
        self.clock = pygame.time.Clock()

        self.mouse_pos = (0, 0)
        self.mouse_pos_anterior = (0, 0)

        self.dificuldade = '1'
        self.estado = 'menu'
        self.menu = Menu(self.mouse_pos)

    def rodar(self):
        while True:
            self.mouse_pos = (0, 0)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pos_anterior = self.mouse_pos
                    self.mouse_pos = pygame.mouse.get_pos()

            if self.estado == 'menu':
                self.menu.updade_menu(self.mouse_pos)
                if self.menu.comando == 'jogar':
                    tempo = pygame.time.get_ticks()
                    self.mapa = Mapa(self.dificuldade, self.mouse_pos, tempo)
                    self.estado = 'jogo'
                elif self.menu.comando == 'sair' and self.mouse_pos != self.mouse_pos_anterior:
                    pygame.quit()
                    sys.exit()
                elif self.menu.comando == 'dificuldade':
                    self.dificuldade = self.menu.dificuldade

            if self.estado == 'jogo':
                if self.mapa.jogador.local != self.mapa.jogador.local_anterior:
                    self.tela = pygame.display.set_mode((self.mapa.sprites_visiveis.largura, self.mapa.sprites_visiveis.altura))
                self.mapa.rodar(self.mouse_pos)
                if self.mapa.sprites_visiveis.estado_menu == 'menu':
                    self.estado = 'menu'
                    pygame.mixer.music.load('./musicas/adventure_begin.ogg')
                    pygame.mixer.music.play(-1)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
