import pygame
import sys
from mapa import Mapa


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Rei dos Piratas')

        self.tela = pygame.display.set_mode((1200, 600))
        self.clock = pygame.time.Clock()
        self.mapa = Mapa()

    def rodar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.tela.fill('Green')
            self.mapa.rodar()
            
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodar()
