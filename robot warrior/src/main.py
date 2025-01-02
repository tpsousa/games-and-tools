import pygame
import random
import sys
from tela_inicial import inicializar_tela

# Inicialização do Pygame e do mixer
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("O Calouro -")

# Carregar a imagem de fundo
background = pygame.image.load('./recurses/imagens/dinossaur.jpeg')

# Criar uma superfície para escurecer o fundo
dark_overlay = pygame.Surface((WIDTH, HEIGHT))
dark_overlay.set_alpha(100)  # Ajuste a transparência (0-255), 128 é 50% transparente
dark_overlay.fill((0, 0, 0))  # Preencha com preto

# Carregar a música de fundo
pygame.mixer.music.load('./recurses/sounds/mortalKombatTheme.mp3')
pygame.mixer.music.set_volume(0.2)

# Carregar o som do efeito "wasted" e "round 2"
wasted_sound = pygame.mixer.Sound('./recurses/sounds/wastedEffect.mp3')
wasted_sound.set_volume(0.3)  # Ajuste o volume aqui (entre 0.0 e 1.0)

round_sound = pygame.mixer.Sound('./recurses/sounds/roundEffect.mp3')
round_sound.set_volume(0.3)  # Ajuste o volume aqui (entre 0.0 e 1.0)

# Cores
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Carregar a imagem do robô
robo_image = pygame.image.load('./recurses/imagens/robot.png')  # Certifique-se de ter a imagem do robô

# Classes para representar as letras (matérias)
class Letra:
    def __init__(self, letra, cor, velocidade, bonus):
        self.letra = letra
        self.cor = cor
        self.velocidade = velocidade
        self.bonus = bonus
        self.x = random.randint(50, WIDTH - 50)
        self.y = 0
        self.text_surface = font.render(self.letra, True, self.cor)  # Superfície de texto para colisão

    def mover(self):
        self.y += self.velocidade

    def desenhar(self):
        screen.blit(self.text_surface, (self.x, self.y))

    def colidido(self, x, y):
        # Verifica se o ponto (x, y) está dentro da letra
        letra_rect = self.text_surface.get_rect(topleft=(self.x, self.y))
        return letra_rect.collidepoint(x, y)

# Classe para representar os tiros
class Tiro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 12  # Aumentei a velocidade dos tiros
        self.cor = WHITE
    def mover(self):
        self.y -= self.velocidade

    def desenhar(self):
        pygame.draw.circle(screen, self.cor, (self.x, self.y), 5)

# Classe para representar o objeto que atira (jogador)
class ObjetoAtirador:
    def __init__(self):
        self.imagem = pygame.transform.scale(robo_image, (40, 40))  # Ajuste o tamanho conforme necessário
        self.rect = self.imagem.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2  # Posição inicial no centro da tela
        self.rect.y = HEIGHT - self.rect.height - 10  # Posição inicial próximo ao fundo da tela
        self.velocidade = 25  # Aumentei a velocidade do objeto atirador
        self.tiros = []

    def mover_esquerda(self):
        self.rect.x -= self.velocidade
        if self.rect.x < 0:
            self.rect.x = 0

    def mover_direita(self):
        self.rect.x += self.velocidade
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

    def atirar(self):
        tiro = Tiro(self.rect.centerx, self.rect.top)
        self.tiros.append(tiro)

    def desenhar(self):
        screen.blit(self.imagem, self.rect.topleft)

# Lista de matérias com suas características
materias_dificeis = [
    ("Cálculo III", RED, 8.0, 0),  # Aumentei a velocidade
    ("Álgebra Linear", RED, 8.0, 0),  # Aumentei a velocidade
    ("Equações Diferenciais", RED, 8.0, 0),  # Aumentei a velocidade
    ("Física I", RED, 8.0, 0),  # Aumentei a velocidade
    ("Banco de Dados", RED, 8.0, 0),  # Aumentei a velocidade
    ("Estrutura de Dados", RED, 8.0, 0),  # Aumentei a velocidade
    ("Algoritmos II", RED, 8.0, 0),  # Aumentei a velocidade
    ("Matemática Discreta", RED, 8.0, 0)  # Aumentei a velocidade
]

materias_simples = [
    ("Cálculo I", GREEN, 6.0, 0.25),  # Aumentei a velocidade
    ("Geometria Analítica", GREEN, 6.0, 0.25),  # Aumentei a velocidade
    ("Introdução à Computação", GREEN, 6.0, 0.25),  # Aumentei a velocidade
    ("Ética", GREEN, 6.0, 0.25),  # Aumentei a velocidade
    ("Algoritmos I", GREEN, 6.0, 0.25)  # Aumentei a velocidade
]

letras_em_jogo = []
objeto_atirador = ObjetoAtirador()
pontos = 0
palavras_deixadas_passar = 0
LIMITE_PALAVRAS_PERDIDAS = 5
chances_restantes = 1
estado_jogo = "jogando"  # pode ser "jogando", "reposicao", "reprovado"

# Função para desenhar a tela
def desenhar_tela():
    screen.blit(background, (0, 0))  # Desenhar a imagem de fundo
    screen.blit(dark_overlay, (0, 0))  # Desenhar a superfície escura sobre o fundo
    for letra in letras_em_jogo:
        letra.desenhar()
    for tiro in objeto_atirador.tiros:
        tiro.desenhar()
    objeto_atirador.desenhar()

    # Desenhar pontuação
    pontuacao_texto = font.render(f"Pontos: {pontos}", True, WHITE)
    screen.blit(pontuacao_texto, (10, 10))

    if estado_jogo == "reposicao":
        reposicao_texto = font.render("Reposição - Pressione 'r' para reiniciar", True, WHITE)
        reposicao_rect = reposicao_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(reposicao_texto, reposicao_rect)

    if estado_jogo == "reprovado":
        wasted_texto = font.render("WASTED", True, RED)
        wasted_rect = wasted_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(wasted_texto, wasted_rect)
        if not pygame.mixer.get_busy():  # Verifica se o canal de música está ocupado
            pygame.mixer.music.play(loops=-1)  # Reinicia a música de fundo do Mortal Kombat
        pygame.mixer.music.pause()  # Pausa a música de fundo do Mortal Kombat

        reprovado_texto = font.render("REPROVADO", True, RED)
        reprovado_rect = reprovado_texto.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(reprovado_texto, reprovado_rect)

    pygame.display.flip()

# Função para reiniciar o jogo
def reiniciar_jogo():
    global pontos, palavras_deixadas_passar, letras_em_jogo, estado_jogo, chances_restantes
    pontos = 0
    palavras_deixadas_passar = 0
    letras_em_jogo = []
    objeto_atirador.tiros = []
    estado_jogo = "jogando"

    # Tocar o som "round 2"
    round_sound.play()
    # Aguardar 4 segundos
    pygame.time.wait(2000)
    chances_restantes -= 1

# Função principal do jogo
def main():
    global estado_jogo, chances_restantes, palavras_deixadas_passar, pontos

    # Inicializa a tela inicial
    inicializar_tela(screen)

    pygame.mixer.music.play(loops=-1)  # Toca a música de fundo do Mortal Kombat

    clock = pygame.time.Clock()
    running = True
    while running:
        keys = pygame.key.get_pressed()  # Verifica as teclas pressionadas

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and estado_jogo == "jogando":
                    objeto_atirador.atirar()
                elif event.key == pygame.K_r and estado_jogo == "reposicao":
                    reiniciar_jogo()
                elif event.key == pygame.K_q and estado_jogo == "reprovado":
                    running = False

        if estado_jogo == "jogando":
            # Mover o jogador com as setas do teclado
            if keys[pygame.K_LEFT]:
                objeto_atirador.mover_esquerda()
            if keys[pygame.K_RIGHT]:
                objeto_atirador.mover_direita()

            # Adiciona novas letras ao jogo
            if random.random() < 0.02:  # Ajuste a probabilidade de aparecer uma nova letra
                materia = random.choice(materias_dificeis + materias_simples)
                letras_em_jogo.append(Letra(*materia))

            # Mover e desenhar letras
            for letra in letras_em_jogo[:]:
                letra.mover()
                if letra.y > HEIGHT:
                    letras_em_jogo.remove(letra)
                    palavras_deixadas_passar += 1

            # Mover e desenhar tiros
            for tiro in objeto_atirador.tiros[:]:
                tiro.mover()
                if tiro.y < 0:
                    objeto_atirador.tiros.remove(tiro)
                else:
                    for letra in letras_em_jogo[:]:
                        if letra.colidido(tiro.x, tiro.y):
                            objeto_atirador.tiros.remove(tiro)
                            letras_em_jogo.remove(letra)
                            pontos += 1 if letra.bonus == 0 else 5  # Ajuste para contagem correta dos pontos
                            break

            if palavras_deixadas_passar >= LIMITE_PALAVRAS_PERDIDAS:
                if chances_restantes > 0:
                    estado_jogo = "reposicao"
                else:
                    estado_jogo = "reprovado"
                    wasted_sound.play()  # Tocar o som "wasted"

        desenhar_tela()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
