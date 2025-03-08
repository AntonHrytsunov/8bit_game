import pygame
import sys
from menu import PauseMenu  # Використовуємо вже реалізоване меню паузи
from scene_intro import IntroScene  # Імпортуємо сцену


class Game:
    def __init__(self, screen, game_settings):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.running = True
        self.paused = False
        self.scene = IntroScene(screen, game_settings)  # Додаємо сцену на початку гри
        self.scene_playing = True  # Чи відбувається зараз сцена
        self.level = None  # Рівень буде завантажено після сцени

    def run(self):
        print("Гру запущено.")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()

                if self.scene_playing:
                    self.scene.handle_events(event)  # Викликаємо обробку подій для сцени!

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused  # Перемикаємо паузу

    def update(self):
        if not self.paused:
            pass  # Логіка гри

    def render(self):
        if not self.paused:
            self.screen.fill((0, 0, 0))
            pygame.display.flip()

    def start_level(self):
        print("Сцена завершена, запускаємо рівень!")
        self.scene = None
        self.scene_playing = False

    def show_pause_menu(self):
        """Відображаємо меню паузи, використовуючи існуючий клас `PauseMenu`."""
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