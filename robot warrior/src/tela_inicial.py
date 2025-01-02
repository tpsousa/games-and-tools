import pygame
import sys
from PIL import Image
# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK = (0, 0, 0)

def draw_initial_screen(screen, font, button_text, button_rect, background_image, dark_overlay):
    screen.blit(background_image, (0, 0))  # Desenha a imagem de fundo
    screen.blit(dark_overlay, (0, 0))  # Desenha o overlay escuro
    pygame.draw.rect(screen, BLACK, button_rect.inflate(20, 20))
    screen.blit(button_text, button_rect)
    pygame.display.flip()

def inicializar_tela(screen):
    font = pygame.font.Font(None, 36)
    button_text = font.render('Entrar no curso Ciência da Computação', True, WHITE)
    button_rect = button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    # Carregar a imagem de fundo
    background_image = pygame.image.load('./recurses/imagens/tela_inicial.jpeg')
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    # Criar a superfície de overlay escuro
    dark_overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    dark_overlay.set_alpha(200)  # Opacidade ajustada para 50% (128 de 0 a 255)
    dark_overlay.fill((0, 0, 0))

    in_initial_screen = True
    while in_initial_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    in_initial_screen = False
        screen.fill(BLACK)  # Limpa a tela com preto
        draw_initial_screen(screen, font, button_text, button_rect, background_image, dark_overlay)

# Inicializar Pygame e definir a tela
pygame.init()
#screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Tela Inicial')


