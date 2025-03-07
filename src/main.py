# Скрипт основного циклу гри

# Імпортуємо необхідні бібліотеки
import pygame
import sys
from menu import Menu

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8bit_game")

    clock = pygame.time.Clock()
    FPS = 60

    # Пункти меню
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
                # Обробка вибору меню
                if menu_options[selection] == "Почати гру":
                    print("Запуск нової гри...")
                    in_menu = False  # Перехід до гри
                elif menu_options[selection] == "Продовжити гру":
                    print("Завантаження збереженої гри...")
                    in_menu = False  # Перехід до гри
                elif menu_options[selection] == "Вийти":
                    pygame.quit()
                    sys.exit()

        menu.display()
        clock.tick(FPS)

    # Тут починається основний цикл гри після виходу з меню
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()