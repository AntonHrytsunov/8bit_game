import pygame
import sys
from menu import PauseMenu  # Меню паузи
from scene_intro import IntroScene  # Вступна сцена
import hero_creator

class Game:
    def __init__(self, screen, game_settings):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.running = True
        self.paused = False
        self.scene = IntroScene(screen, game_settings)  # Додаємо вступну сцену
        self.scene_playing = True  # Чи зараз відбувається сцена
        self.level = None  # Рівень завантажується після сцени
        self.game_settings = game_settings

    def run(self):
        """Основний ігровий цикл"""
        print("Гру запущено.")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    elif event.type == pygame.VIDEORESIZE:
                        new_resolution = (event.w, event.h)

                        # Перевіряємо, чи потрібно активувати повноекранний режим
                        if new_resolution == "Максимальна":
                            new_resolution = pygame.display.get_desktop_sizes()[0]  # Отримуємо максимальне розширення
                            fullscreen = True
                        else:
                            fullscreen = self.game_settings.get("fullscreen")

                        # Оновлюємо налаштування
                        self.game_settings.update("resolution", new_resolution)
                        self.game_settings.update("fullscreen", fullscreen)

                        # Оновлюємо сцену та екран
                        self.scene.update_screen_settings(new_resolution, fullscreen)

                        if fullscreen:
                            self.screen = pygame.display.set_mode(new_resolution, pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode(new_resolution, pygame.RESIZABLE)

                if self.scene_playing:
                    self.scene.handle_events(event)  # Обробка подій сцени

            if self.paused:
                self.show_pause_menu()
                continue

            if self.scene_playing:
                self.scene.update(self.paused)
                self.scene.render()

                if self.scene.is_finished():
                    self.scene_playing = False
                    self.start_level()
            else:
                self.update()
                self.render()

            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def toggle_pause(self):
        """Перемикає паузу"""
        self.paused = not self.paused

    def update(self):
        """Оновлення логіки гри"""
        if not self.paused:
            pass  # Додати логіку гри

    def render(self):
        """Малювання кадрів"""
        if not self.paused:
            self.screen.fill((0, 0, 0))
            pygame.display.flip()

    def start_level(self):
        """Запускає рівень після завершення сцени"""
        print("Інтро завершено, запускаємо перший рівень!")
        self.scene = IntroScene(self.screen, self.game_settings)
        self.scene_playing = True  # Активуємо рівень як сцену

    def show_pause_menu(self):
        """Меню паузи"""
        pause_options = ["Продовжити гру", "Вийти у систему"]
        background = self.screen.copy()
        pause_menu = PauseMenu(self.screen, pause_options, background)

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.paused = False
                selection = pause_menu.handle_events(event)
                if selection is not None:
                    if selection == -1 or pause_options[selection] == "Продовжити гру":
                        self.paused = False
                    elif pause_options[selection] == "Вийти у систему":
                        pygame.quit()
                        sys.exit()

            pause_menu.display()