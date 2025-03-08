import pygame
import time


class Scene:
    def __init__(self, screen, duration, background, texts, game_settings):
        """
        Базовий клас для всіх сцен.

        :param screen: Екран Pygame, на якому буде відображатися сцена
        :param duration: Тривалість сцени у секундах
        :param background: Зображення або колір фону сцени
        :param texts: Список кортежів (текст, час відображення)
        :param game_settings: Об'єкт GameSettings для отримання розширення екрану та режиму
        """
        self.screen = screen
        self.duration = duration
        self.background = background
        self.texts = texts
        self.current_text_index = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.pause_time = None  # Фіксує час, коли сцена ставиться на паузу
        self.font = pygame.font.Font(None, 36)  # Шрифт для тексту

        self.screen_resolution = tuple(game_settings.get("resolution"))
        self.fullscreen = game_settings.get("fullscreen")

        # Завантаження фону
        self.bg_image = None
        if isinstance(self.background, str):
            try:
                self.bg_image = pygame.image.load(self.background)
                self.bg_image = pygame.transform.scale(self.bg_image, self.screen_resolution)
            except pygame.error:
                print(f"Помилка завантаження фону: {self.background}")

    def update(self, paused):
        """Оновлення логіки сцени (перемикання тексту тощо)."""
        if paused:
            if self.pause_time is None:  # Фіксуємо час паузи тільки один раз
                self.pause_time = time.time()
            return

        if self.pause_time is not None:
            # Компенсуємо час паузи
            self.start_time += time.time() - self.pause_time
            self.pause_time = None  # Скидаємо значення після виходу з паузи

        self.elapsed_time = time.time() - self.start_time

        if self.current_text_index < len(self.texts) - 1:
            text_duration = self.texts[self.current_text_index][1]
            if self.elapsed_time >= text_duration:
                self.current_text_index += 1
                self.start_time = time.time()

    def render(self):
        """Малює сцену на екрані."""
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill(self.background)

        if self.texts:
            text, _ = self.texts[self.current_text_index]
            text_surface = self.font.render(text, True, (255, 255, 255))

            text_rect = text_surface.get_rect(center=(self.screen_resolution[0] // 2, self.screen_resolution[1] - 100))

            text_background = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
            text_background.fill((0, 0, 0, 150))

            self.screen.blit(text_background, (text_rect.x - 10, text_rect.y - 5))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def is_finished(self):
        """Перевіряє, чи завершилася сцена."""
        return self.elapsed_time >= self.duration