import pygame


class Menu:
    def __init__(self, mouse_pos):
        self.image = pygame.image.load('./graficos/menu/principal.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.display_superficie = pygame.display.get_surface()
        self.mouse_pos = mouse_pos
        self.comando = None
        self.janela = 'principal'
        self.dificuldade = '1'

        pygame.mixer.music.load('./musicas/adventure_begin.ogg')
        pygame.mixer.music.play(-1)

    # Botões do menu.
    def identificar_comando(self):
        if self.janela == 'principal':
            if 570 < self.mouse_pos[0] < 820 and 200 < self.mouse_pos[1] < 325:
                self.comando = 'jogar'
            elif 885 < self.mouse_pos[0] < 1130 and 200 < self.mouse_pos[1] < 325:
                self.comando = 'opcoes'
                self.janela = 'opcoes'
                self.image = pygame.image.load('./graficos/menu/opcoes.png').convert_alpha()
            elif 570 < self.mouse_pos[0] < 820 and 380 < self.mouse_pos[1] < 490:
                self.comando = 'controles'
                self.janela = 'controles'
                self.image = pygame.image.load('./graficos/menu/controles.png').convert_alpha()
            elif 885 < self.mouse_pos[0] < 1130 and 380 < self.mouse_pos[1] < 490:
                self.comando = 'sair'
            else:
                self.comando = None

        elif self.janela == 'opcoes':
            if 570 < self.mouse_pos[0] < 735 and 200 < self.mouse_pos[1] < 290:
                self.comando = 'dificuldade'
                self.dificuldade = '1'
            elif 790 < self.mouse_pos[0] < 950 and 200 < self.mouse_pos[1] < 290:
                self.comando = 'dificuldade'
                self.dificuldade = '2'
            elif 1010 < self.mouse_pos[0] < 1170 and 200 < self.mouse_pos[1] < 290:
                self.comando = 'dificuldade'
                self.dificuldade = '3'
            elif 670 < self.mouse_pos[0] < 835 and 315 < self.mouse_pos[1] < 400:
                self.comando = 'dificuldade'
                self.dificuldade = '4'
            elif 910 < self.mouse_pos[0] < 1070 and 315 < self.mouse_pos[1] < 400:
                self.comando = 'dificuldade'
                self.dificuldade = '5'
            elif 735 < self.mouse_pos[0] < 1010 and 440 < self.mouse_pos[1] < 560:
                self.comando = 'voltar'
                self.janela = 'principal'
                self.image = pygame.image.load('./graficos/menu/principal.png').convert_alpha()
            else:
                self.comando = None

        elif self.janela == 'controles':
            if 769 < self.mouse_pos[0] < 985 and 475 < self.mouse_pos[1] < 570:
                self.comando = 'voltar'
                self.janela = 'principal'
                self.image = pygame.image.load('./graficos/menu/principal.png').convert_alpha()
            else:
                self.comando = None

    def updade_menu(self, mouse_pos):
        self.display_superficie.blit(self.image, self.rect)
        self.mouse_pos = mouse_pos
        self.identificar_comando()
