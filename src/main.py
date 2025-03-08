import pygame
import sys
from menu import *
from game import Game
from settings import GameSettings
import save_game, delete_old_saves

def main():
    pygame.init()
    WIDTH, HEIGHT = 700, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8bit_game")
    clock = pygame.time.Clock()
    FPS = 60

    # Ініціалізуємо GameSettings
    game_settings = GameSettings()

    # Створюємо стартове меню
    menu_options = ["Нова гра", "Продовжити гру", "Налаштування", "Вийти"]
    menu = Menu(screen, menu_options)

    sound_manager = SoundManager(sound_folder="../assets/menu/menu_ost", volume=0.5)
    sound_manager.play_random_sound()  # Запуск музики в меню

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            selection_menu = menu.handle_events(event)
            if selection_menu is not None:
                if menu.has_save is False:
                    if menu_options[selection_menu] == "Нова гра":
                        print("Запуск нової гри...")
                        in_menu = False
                        sound_manager.stop_music()
                        save_game.delete_all_saves()
                        save_game.create_new_save()
                        menu.update_continue_option()
                else:
                    if menu_options[selection_menu] == "Нова гра":
                        print("Запуск вікна видалення збережень")
                        in_menu = False
                        delete_confirm = delete_old_saves.DeleteOldSaves(screen)
                        confirming = True
                        while confirming:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                confirm_selection = delete_confirm.handle_events(event)
                                if confirm_selection == "Так":
                                    print("Розпочато нову гру.")
                                    save_game.delete_all_saves()
                                    save_game.create_new_save()
                                    menu.update_continue_option()
                                    confirming = False
                                    in_menu = False
                                    sound_manager.stop_music()
                                elif confirm_selection == "Ні":
                                    print("Повернення у меню.")
                                    confirming = False
                                    in_menu = True  # Повернення у меню без запуску гри
                                    menu.update_continue_option()
                                    menu.display()
                                    continue  # Пропускаємо залишок виконання цього блоку
                            delete_confirm.display()

                    elif menu_options[selection_menu] == "Продовжити гру" and menu.has_save:
                        print("Завантаження збереженої гри...")
                        in_menu = False
                        sound_manager.stop_music()


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
                                        print("Повернення у меню.")
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


    # Запуск гри
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()