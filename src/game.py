# src/game.py
import pygame
import sys
from menu import PauseMenu  # переконайтеся, що цей модуль створено та містить клас PauseMenu

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.running = True
        # Тут можна ініціалізувати рівень, персонажа тощо
        self.level = None  # поки що None

    def run(self):
        # Основний цикл гри
        print("Гру запущено.")
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        # Обробка подій гри
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Викликаємо меню паузи при натисканні ESC
                    self.pause()
                # Обробка інших клавіш (наприклад, для руху героя) може додаватись тут

    def update(self):
        # Оновлення логіки гри (рух, колізії тощо)
        pass

    def render(self):
        # Рендеринг: очищення екрана та відображення ігрових об'єктів
        self.screen.fill((0, 0, 0))
        # Тут малюються об'єкти гри
        pygame.display.flip()

    def pause(self):
        pause_options = ["Продовжити гру", "Вийти у систему"]
        # Зберігаємо поточний вигляд екрану як фон паузи
        background = self.screen.copy()
        pause_menu = PauseMenu(self.screen, pause_options, background)
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False
                else:
                    selection = pause_menu.handle_events(event)
                    if selection is not None:
                        if selection == -1 or pause_options[selection] == "Продовжити гру":
                            paused = False
                        elif pause_options[selection] == "Вийти у систему":
                            pygame.quit()
                            sys.exit()
            pause_menu.display()