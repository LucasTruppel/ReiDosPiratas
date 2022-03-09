import pygame
from config import *
from obstaculo import Obstaculo
from jogador import Jogador


class Mapa:
    def __init__(self, dif, mouse_pos, tempo):

        # Sprites
        self.sprites_visiveis = Camera()
        self.sprites_obstaculos = pygame.sprite.Group()
        self.sprites_moedas = pygame.sprite.Group()

        self.dificuldade = dif
        self.som_moeda = pygame.mixer.Sound('./sons/coin.wav')
        self.mouse_pos = mouse_pos
        self.tempo_inicial = tempo

        # Mapa criação
        self.criar_mapa()

    def criar_mapa(self):
        for linha_pos, linha in enumerate(mapa_matriz):
            for coluna_pos, coluna in enumerate(linha):
                if coluna != ' ':
                    x = coluna_pos * 64
                    y = linha_pos * 64

                    if coluna == 'p':
                        self.jogador = Jogador((x, y), [self.sprites_visiveis], self.sprites_obstaculos)
                    elif coluna == 'x' or coluna == 'r' or coluna == 'e' or coluna == 'f' or coluna == 't':
                        Obstaculo((x, y), [self.sprites_visiveis, self.sprites_obstaculos], coluna)
                    elif coluna == 'm':
                        Obstaculo((x, y), [self.sprites_visiveis, self.sprites_obstaculos, self.sprites_moedas], coluna)
                    else:
                        Obstaculo((x, y-64), [self.sprites_visiveis, self.sprites_obstaculos], coluna)

        pygame.mixer.music.load('./musicas/story.ogg')
        pygame.mixer.music.play(-1)

    def trocar_musica(self):
        if self.jogador.local_anterior != self.jogador.local:
            if self.jogador.local == 'inicio':
                pygame.mixer.music.load('./musicas/story.ogg')
            elif self.jogador.local == 'labirinto':
                pygame.mixer.music.load('./musicas/ascension.ogg')
            elif self.jogador.local == 'final':
                pygame.mixer.music.load('./musicas/final_area.ogg')
            pygame.mixer.music.play(-1)

    def avaliar_moedas(self):
        for sprite in self.sprites_moedas:
            if sprite.rect.colliderect(self.jogador.hitbox) and self.jogador.interagir:
                self.jogador.velocidade += 0.5
                self.jogador.velocidade_animacao += 0.01
                sprite.kill()
                pygame.mixer.Sound.play(self.som_moeda)

    def rodar(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.trocar_musica()
        self.avaliar_moedas()
        self.sprites_visiveis.desenhar(self.jogador, self.mouse_pos)
        self.sprites_visiveis.exibir_tempo(self.tempo_inicial, self.jogador)
        self.sprites_visiveis.update()
        self.sprites_visiveis.aplicar_difculdade(self.jogador, self.dificuldade)


# Responsável por desenhar as imagens na tela.
class Camera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_superficie = pygame.display.get_surface()
        self.deslocamento = pygame.math.Vector2()

        self.largura = 1200
        self.altura = 600
        self.meia_largura = 600
        self.meia_altura = 300

        self.image = pygame.image.load('./graficos/obstaculos/chao.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(-576, -576))

        self.inicio_image = pygame.image.load('./graficos/menu/inicio.png').convert_alpha()
        self.inicio_rect = self.image.get_rect(topleft=(0, 0))

        self.final_image = pygame.image.load('./graficos/menu/final.png').convert_alpha()
        self.final_rect = self.image.get_rect(topleft=(0, 0))
        self.estado_menu = 'final'

        self.tempo = 0
        self.fonte_texto = pygame.font.Font('fonte/pixeltype.ttf', 50)

    def aplicar_difculdade(self, jogador, dif):
        # Reduz o tamanho da tela baseado na dificuldade.
        if jogador.local == 'labirinto':
            self.largura = dificuldade[dif]
            self.altura = self.largura // 2
            self.meia_largura = self.largura // 2
            self.meia_altura = self.altura // 2
        else:
            self.largura = 1200
            self.altura = 600
            self.meia_largura = 600
            self.meia_altura = 300

        # Reduz o tamanho da fonte do texto do tempo na dificuldade 5.
        if dif == '5':
            self.fonte_texto = pygame.font.Font('fonte/pixeltype.ttf', 30)

    def desenhar(self, jogador, mouse_pos):
        # Desenhos dos sprites. Toma a posição do jogador como referência.
        self.deslocamento.x = jogador.rect.centerx - self.meia_largura
        self.deslocamento.y = jogador.rect.centery - self.meia_altura

        self.posicao = self.rect.topleft - self.deslocamento
        self.display_superficie.blit(self.image, self.posicao)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite.posicao = sprite.rect.topleft - self.deslocamento
            self.display_superficie.blit(sprite.image, sprite.posicao)

        # Mensagem do início do jogo.
        if jogador.local == 'inicio':
            self.display_superficie.blit(self.inicio_image, self.inicio_rect)

        # Tela do final do jogo.
        elif jogador.estado == 'final':
            self.display_superficie.blit(self.final_image, self.final_rect)
            if self.estado_menu == 'final':
                if 505 < mouse_pos[0] < 705 and 465 < mouse_pos[1] < 555:
                    self.final_image = pygame.image.load('./graficos/menu/creditos.png').convert_alpha()
                    self.estado_menu = 'creditos'
            elif self.estado_menu == 'creditos':
                if 1030 < mouse_pos[0] < 1175 and 420 < mouse_pos[1] < 525:
                    self.estado_menu = 'menu'

    def exibir_tempo(self, tempo_inicial, jogador):
        if jogador.estado != 'final':
            self.tempo = (pygame.time.get_ticks() - tempo_inicial) // 1000

            minutos = self.tempo // 60
            segundos = self.tempo % 60
            if minutos < 10:
                minutos = '0' + str(minutos)
            if segundos < 10:
                segundos = '0' + str(segundos)
            self.tempo = f'{minutos}:{segundos}'

        tempo_surf = self.fonte_texto.render(f'{self.tempo}', False, '#000000')
        tempo_rect = tempo_surf.get_rect(bottomleft = (5, self.altura))
        self.display_superficie.blit(tempo_surf, tempo_rect)
