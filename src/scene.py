import pygame
import time
import random


class Scene:
    def __init__(self, screen, duration, backgrounds, texts, game_settings, music_file=None):
        self.screen = screen
        self.duration = duration
        self.backgrounds = backgrounds
        self.texts = texts
        self.music_file = music_file
        self.current_text_index = 0
        self.current_bg_index = 0
        self.elapsed_time = 0  # Наш власний таймер
        self.paused = False  # Статус паузи
        self.font = pygame.font.Font(None, 36)

        self.screen_resolution = tuple(game_settings.get("resolution"))
        self.fullscreen = game_settings.get("fullscreen")

        self.bg_image = None
        self.bg_scaled = None
        self.bg_pos = (0, 0)
        self.load_background(self.current_bg_index)
        if self.music_file:
            self.play_music()

    def load_background(self, index):
        """Завантажує фон за його індексом у списку `backgrounds`."""
        if index < len(self.backgrounds):
            bg_path, _ = self.backgrounds[index]
            try:
                self.bg_image = pygame.image.load(bg_path)
                self.scale_background()  # ✅ Масштабуємо фон

                if self.bg_scaled is None:
                    print(f"Помилка: фон {bg_path} не завантажився правильно!")

                self.bg_start_time = self.elapsed_time  # ✅ Використовуємо наш таймер
                self.bg_elapsed_time = 0  # ✅ Таймер для контролю зміни фону
                self.set_background_animation()  # ✅ Запускаємо рух

            except pygame.error:
                print(f"Помилка завантаження фону: {bg_path}")


    def set_background_animation(self):
        """Встановлює випадковий напрямок руху для нового фону."""
        if self.bg_scaled:
            bg_width, bg_height = self.bg_scaled.get_size()
            screen_width, screen_height = self.screen_resolution

            overflow_x = bg_width - screen_width
            overflow_y = bg_height - screen_height

            possible_directions = []
            if overflow_x > 0:
                possible_directions.extend(["left", "right"])
            if overflow_y > 0:
                possible_directions.extend(["up", "down"])

            move_direction = random.choice(possible_directions)

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

            self.bg_pos = self.bg_start_pos

    def scale_background(self):
        """Масштабує фон, зберігаючи пропорції, та налаштовує анімацію руху."""
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


    def play_music(self):
        """Запускає музику для сцени."""
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"Помилка завантаження музичного файлу: {self.music_file}")

    def stop_music(self):
        """Зупиняє музику після завершення сцени."""
        pygame.mixer.music.stop()

    def handle_events(self, event):
        """Обробка подій: при натисканні `Space` перемикає текст."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.skip_text()

    def skip_text(self):
        """Пропускає поточний текст і відображає наступний."""
        if self.current_text_index < len(self.texts) - 1:
            self.current_text_index += 1
            self.start_time = time.time()

    def update(self, paused):
        """Оновлення сцени та правильна зміна фону."""

        if paused:
            self.paused = True  # Зупиняємо оновлення під час паузи
            return

        if self.paused:
            self.paused = False  # Скидаємо статус паузи

        # 1️⃣ Оновлення загального часу сцени
        self.elapsed_time += 1 / 60  # Симулюємо FPS=60 (1 сек = 60 кадрів)
        self.bg_elapsed_time += 1 / 60  # Таймер для контролю зміни фону

        # 2️⃣ Зміна тексту за таймінгами
        if self.elapsed_time >= sum(text[1] for text in self.texts[:self.current_text_index + 1]):
            self.skip_text()

        # 3️⃣ Зміна фону за таймінгами
        if self.current_bg_index < len(self.backgrounds) - 1:
            next_bg_time = sum(
                bg[1] for bg in self.backgrounds[:self.current_bg_index + 1])  # Загальний час для поточного фону

            if self.elapsed_time >= next_bg_time:
                self.current_bg_index += 1  # ✅ Переходимо до наступного фону
                self.load_background(self.current_bg_index)  # ✅ Завантажуємо його
                self.set_background_animation()  # ✅ Запускаємо рух
                self.bg_elapsed_time = 0  # ✅ Скидаємо таймер фону
                self.render()  # ✅ Оновлюємо екран після зміни фону

        # 4️⃣ Оновлення позиції фону (анімація руху)
        progress = min(1, self.bg_elapsed_time / self.backgrounds[self.current_bg_index][1])

        self.bg_pos = (
            self.bg_start_pos[0] + (self.bg_end_pos[0] - self.bg_start_pos[0]) * progress,
            self.bg_start_pos[1] + (self.bg_end_pos[1] - self.bg_start_pos[1]) * progress
        )


    def render(self):
        """Малює сцену на екрані."""
        if self.bg_scaled:
            self.screen.blit(self.bg_scaled, self.bg_pos)
        else:
            self.screen.fill(self.background)

        text, _ = self.texts[self.current_text_index]
        text_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = text_surface.get_rect(center=(self.screen_resolution[0] // 2, self.screen_resolution[1] - 100))

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def is_finished(self):
        """Перевіряє, чи завершилася сцена (всі фони показані повністю)."""

        # Якщо ще є фони для показу – сцена не завершена
        if self.current_bg_index < len(self.backgrounds) - 1:
            return False

        # Отримуємо загальний час останнього фону
        last_bg_duration = self.backgrounds[-1][1]

        # Якщо загальний час сцени ще не закінчився – продовжуємо
        if self.elapsed_time < sum(bg[1] for bg in self.backgrounds):
            return False

        self.stop_music()  # ✅ Зупиняємо музику після завершення сцени
        return True