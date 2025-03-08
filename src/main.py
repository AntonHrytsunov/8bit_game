import pygame
import sys
from menu import Menu, Settings
from game import Game
from settings import GameSettings

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8bit_game")
    clock = pygame.time.Clock()
    FPS = 60

    # Ініціалізуємо GameSettings
    game_settings = GameSettings()

    # Створюємо стартове меню
    menu_options = ["Почати гру", "Продовжити гру", "Налаштування", "Вийти"]
    menu = Menu(screen, menu_options)

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            selection_menu = menu.handle_events(event)
            if selection_menu is not None:
                if menu_options[selection_menu] == "Почати гру":
                    print("Запуск нової гри...")
                    in_menu = False
                elif menu_options[selection_menu] == "Продовжити гру":
                    print("Завантаження збереженої гри...")
                    in_menu = False
                elif menu_options[selection_menu] == "Налаштування":
                    print("Відкривається вікно з налаштуваннями")
                    in_menu = False
                    settings_options = ["Повноекранний режим", "Роздільна здатність екрану", "Складність гри", "Назад"]
                    settings = Settings(screen, settings_options, game_settings)
                    in_settings = True
                    while in_settings:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            selection_settings = settings.handle_events(event)
                            if selection_settings is not None:
                                if settings_options[selection_settings] == "Назад":
                                    print("Повертаємось у меню")
                                    in_settings = False
                                    in_menu = True
                        settings.display()
                elif menu_options[selection_menu] == "Вийти":
                    pygame.quit()
                    sys.exit()
        menu.display()
        clock.tick(FPS)

    # Перед запуском гри оновлюємо роздільну здатність і режим вікна згідно з GameSettings
    new_resolution = tuple(game_settings.get("resolution"))
    if game_settings.get("fullscreen"):
        screen = pygame.display.set_mode(new_resolution, pygame.FULLSCREEN)
        print(f"Запущено у повноекранному режимі, роздільна здатність: {new_resolution}")
    else:
        screen = pygame.display.set_mode(new_resolution)
        print(f"Роздільна здатність: {new_resolution}")

    # Запуск гри
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()