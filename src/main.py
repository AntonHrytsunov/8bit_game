import pygame
import sys

# Ініціалізація Pygame
pygame.init()

# Налаштування параметрів вікна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8bit_game")

# Основний цикл гри
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заливка фону (наприклад, чорний колір)
    screen.fill((0, 0, 0))

    # Оновлення екрану
    pygame.display.flip()

    # Обмеження FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()