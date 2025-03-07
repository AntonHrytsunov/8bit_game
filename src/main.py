# src/main.py
import pygame
import sys
from menu import Menu
from game import Game

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8bit_game")
    clock = pygame.time.Clock()
    FPS = 60

    # Створюємо стартове меню
    menu_options = ["Почати гру", "Продовжити гру", "Вийти"]
    menu = Menu(screen, menu_options)

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            selection = menu.handle_events(event)
            if selection is not None:
                if menu_options[selection] == "Почати гру":
                    print("Запуск нової гри...")
                    in_menu = False
                elif menu_options[selection] == "Продовжити гру":
                    print("Завантаження збереженої гри...")
                    in_menu = False
                elif menu_options[selection] == "Вийти":
                    pygame.quit()
                    sys.exit()
        menu.display()
        clock.tick(FPS)

    # Після виходу з меню запускаємо гру
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()