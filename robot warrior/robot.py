import pygame

# Inicialização do Pygame
pygame.init()

# Definição das dimensões da imagem
WIDTH, HEIGHT = 60, 60

# Criação da superfície
robot_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Desenho do corpo do robô (tons de cinza)
pygame.draw.rect(robot_surface, (150, 150, 150), (20, 20, 20, 30))  # Corpo
pygame.draw.rect(robot_surface, (100, 100, 100), (25, 10, 10, 10))  # Cabeça

# Desenho dos olhos com fogo
pygame.draw.rect(robot_surface, (255, 0, 0), (27, 15, 3, 5))  # Olho esquerdo (vermelho)
pygame.draw.rect(robot_surface, (255, 0, 0), (30, 15, 3, 5))  # Olho direito (vermelho)
pygame.draw.rect(robot_surface, (255, 69, 0), (27, 15, 3, 3))  # Olho esquerdo (laranja)
pygame.draw.rect(robot_surface, (255, 69, 0), (30, 15, 3, 3))  # Olho direito (laranja)

# Desenho da espada
pygame.draw.line(robot_surface, (192, 192, 192), (40, 40), (55, 25), 3)  # Espada
pygame.draw.rect(robot_surface, (128, 128, 128), (38, 38, 6, 6))  # Cabo da espada

# Desenho dos braços
pygame.draw.line(robot_surface, (100, 100, 100), (20, 30), (15, 40), 3)  # Braço esquerdo
pygame.draw.line(robot_surface, (100, 100, 100), (40, 30), (45, 40), 3)  # Braço direito

# Salvando a imagem
pygame.image.save(robot_surface, 'robot.png')

# Fechando o Pygame
pygame.quit()
