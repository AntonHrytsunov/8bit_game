import pygame
import time
import random


class Scene:
    def __init__(self, screen, duration, background, texts, game_settings):
        self.screen = screen
        self.duration = duration
        self.background = background
        self.texts = texts
        self.current_text_index = 0
        self.start_time = time.time()
        self.scene_start_time = self.start_time  # Час початку всієї сцени
        self.pause_time = None
        self.font = pygame.font.Font(None, 36)

        self.screen_resolution = tuple(game_settings.get("resolution"))
        self.fullscreen = game_settings.get("fullscreen")

        # Завантаження фону
        self.bg_image = None
        self.bg_scaled = None  # Масштабоване зображення
        self.bg_pos = (0, 0)  # Початкова позиція

        # Змінні для анімації руху фону
        self.bg_start_pos = (0, 0)  # Початкова позиція (X, Y)
        self.bg_end_pos = (0, 0)  # Кінцева позиція (X, Y)

        if isinstance(self.background, str):
            try:
                self.bg_image = pygame.image.load(self.background)
                self.scale_background()  # Масштабуємо зображення
            except pygame.error:
                print(f"Помилка завантаження фону: {self.background}")

    def scale_background(self):
        """Масштабує фон так, щоб один його край примикав до краю екрана, а рух відбувався у випадковому напрямку."""
        if self.bg_image:
            bg_width, bg_height = self.bg_image.get_size()
            screen_width, screen_height = self.screen_resolution

            # Обчислюємо коефіцієнт масштабування для покриття екрану без спотворень
            scale_factor = max(screen_width / bg_width, screen_height / bg_height)

            # Нові розміри зображення
            new_width = int(bg_width * scale_factor)
            new_height = int(bg_height * scale_factor)

            # Масштабуємо зображення
            self.bg_scaled = pygame.transform.smoothscale(self.bg_image, (new_width, new_height))

            # Визначаємо, чи фон ширший або вищий за екран
            overflow_x = new_width - screen_width
            overflow_y = new_height - screen_height

            # Визначаємо можливі напрямки руху
            possible_directions = []
            if overflow_x > 0:
                possible_directions.extend(["left", "right"])
            if overflow_y > 0:
                possible_directions.extend(["up", "down"])

            # Випадково обираємо один з можливих напрямків руху
            move_direction = random.choice(possible_directions)

            # Встановлюємо початкову позицію залежно від напрямку
            if move_direction == "left":
                self.bg_start_pos = (0, -overflow_y // 2)
                self.bg_end_pos = (-overflow_x, -overflow_y // 2)
            elif move_direction == "right":
                self.bg_start_pos = (-overflow_x, -overflow_y // 2)
                self.bg_end_pos = (0, -overflow_y // 2)
            elif move_direction == "up":
                self.bg_start_pos = (-overflow_x // 2, 0)
                self.bg_end_pos = (-overflow_x // 2, -overflow_y)
            elif move_direction == "down":
                self.bg_start_pos = (-overflow_x // 2, -overflow_y)
                self.bg_end_pos = (-overflow_x // 2, 0)

            # Початкова позиція
            self.bg_pos = self.bg_start_pos

    def handle_events(self, event):
        """Обробка подій: при натисканні `Space` перемикає текст."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.skip_text()

    def skip_text(self):
        """Пропускає поточний текст і відображає наступний."""
        if self.current_text_index < len(self.texts) - 1:
            remaining_time = self.texts[self.current_text_index][1] - (time.time() - self.start_time)
            self.duration -= max(0, remaining_time)
            self.current_text_index += 1
            self.start_time = time.time()

    def update(self, paused):
        """Оновлення логіки сцени та плавного руху фону."""
        if paused:
            if self.pause_time is None:
                self.pause_time = time.time()
            return

        if self.pause_time is not None:
            time_paused = time.time() - self.pause_time
            self.start_time += time_paused
            self.scene_start_time += time_paused
            self.pause_time = None

        elapsed_time = time.time() - self.scene_start_time  # Час, що пройшов з початку сцени
        progress = min(1, elapsed_time / self.duration)  # Прогрес сцени (0.0 - 1.0)

        # Лінійне зміщення від початкової до кінцевої позиції
        self.bg_pos = (
            self.bg_start_pos[0] + (self.bg_end_pos[0] - self.bg_start_pos[0]) * progress,
            self.bg_start_pos[1] + (self.bg_end_pos[1] - self.bg_start_pos[1]) * progress
        )

        if elapsed_time >= self.texts[self.current_text_index][1]:
            self.skip_text()

    def render(self):
        """Малює сцену на екрані."""
        if self.bg_scaled:
            self.screen.blit(self.bg_scaled, self.bg_pos)  # Відображаємо фон, що рухається
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
        return time.time() - self.scene_start_time >= self.duration