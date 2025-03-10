import pygame
import time
import random


class Scene:
    def __init__(self, screen, backgrounds, texts, game_settings, music_file=None):
        self.screen = screen
        self.backgrounds = backgrounds  # [(шлях, тривалість, fade-in, fade-out, move, move_direction)]
        self.texts = texts
        self.music_file = music_file
        self.current_text_index = 0
        self.current_bg_index = 0
        self.elapsed_time = 0
        self.paused = False
        self.font = pygame.font.Font("../assets/menu_font.otf", 30)
        self.text_start_time = time.time()

        self.screen_resolution = tuple(game_settings.get("resolution"))
        self.fullscreen = game_settings.get("fullscreen")

        self.bg_image = None
        self.bg_scaled = None
        self.bg_pos = (0, 0)

        self.bg_alpha = 255
        self.fade_in_duration = 0
        self.fade_out_duration = 0
        self.fade_state = None
        self.bg_start_time = 0

        self.bg_start_pos = (0, 0)
        self.bg_end_pos = (0, 0)
        self.should_move = False
        self.move_direction = None

        self.paused_time = 0  # Час, коли була поставлена пауза
        self.last_update_time = 0  # Останній момент оновлення

        self.load_background(self.current_bg_index)
        if self.music_file:
            self.play_music()


    def load_background(self, index):
        """Завантажує фон за його індексом у списку `backgrounds`."""
        if index < len(self.backgrounds):
            bg_path, duration, fade_in_duration, fade_out_duration, self.should_move, *optional_move_direction = self.backgrounds[index]
            self.move_direction = optional_move_direction[0] if optional_move_direction else None
            try:
                self.bg_image = pygame.image.load(bg_path).convert_alpha()
                self.scale_background()

                if self.bg_scaled is None:
                    print(f"Помилка: фон {bg_path} не завантажився правильно!")

                # Встановлення параметрів fade-in та fade-out
                self.fade_in_duration = min(fade_in_duration, duration)  # fade-in не може бути довшим за фон
                self.fade_out_duration = min(fade_out_duration, duration)  # fade-out не може бути довшим за фон
                self.bg_start_time = self.elapsed_time  # Оновлюємо час початку фону

                # Якщо fade-in активний, починаємо з прозорого зображення
                if self.fade_in_duration > 0:
                    self.bg_alpha = 0
                    self.fade_state = "fade_in"
                else:
                    self.bg_alpha = 255
                    self.fade_state = None  # Якщо fade-in нема, просто показуємо зображення

                self.set_background_animation()
            except pygame.error:
                print(f"Помилка завантаження фону: {bg_path}")


    def set_background_animation(self):
        """Встановлює напрямок руху для фону, якщо він заданий, або обирає випадковий напрямок."""
        if self.bg_scaled:
            bg_width, bg_height = self.bg_scaled.get_size()
            screen_width, screen_height = self.screen_resolution

            overflow_x = bg_width - screen_width
            overflow_y = bg_height - screen_height

            if not self.should_move:
                return

            # Визначаємо можливі напрямки руху
            possible_directions = []
            if overflow_x > 0:
                possible_directions.extend(["left", "right"])
            if overflow_y > 0:
                possible_directions.extend(["up", "down"])

            # 🔹 Використовуємо move_direction, якщо він вказаний і можливий
            if self.move_direction in possible_directions:
                move_direction = self.move_direction
            else:
                move_direction = random.choice(possible_directions) if possible_directions else None

            # 🔹 Примусово встановлюємо рух у вказаному напрямку
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
            self.animation_progress = 0  # Початковий стан анімації


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

            if self.should_move:  # Перевіряємо, чи потрібно рухати фон
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
            else:
                self.should_move = False


    def play_music(self):
        """Запускає музику для сцени."""
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"Помилка завантаження музичного файлу: {self.music_file}")


    def stop_music_fadeout(self, fade_duration=3000):
        """Плавно зупиняє музику із затуханням."""
        if pygame.mixer.music.get_busy():  # Якщо музика ще грає
            pygame.mixer.music.fadeout(fade_duration)


    def handle_events(self, event):
        """Обробка подій: `Space` пропускає текст, `T` завершує сцену."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.skip_text()
            elif event.key == pygame.K_t:
                self.end_scene()

    def end_scene(self):
        """Миттєво завершує сцену."""
        self.scene_finished = True
        self.stop_music_fadeout()  # Плавне вимкнення музики
        self.elapsed_time = sum(bg[1] for bg in self.backgrounds)  # Перемотуємо час до кінця
        self.current_bg_index = len(self.backgrounds)  # Пропускаємо всі фони
        self.current_text_index = len(self.texts)  # Пропускаємо всі тексти


    def skip_text(self):
        """Пропускає поточний текст і відображає наступний, якщо дозволено."""
        _, text_duration, min_skip_time = self.texts[self.current_text_index]
        elapsed_text_time = time.time() - self.text_start_time

        if elapsed_text_time >= min_skip_time:
            if self.current_text_index < len(self.texts) - 1:
                self.current_text_index += 1
                self.text_start_time = time.time()


    def update(self, paused):
        """Оновлення сцени: рух фону, fade-in, fade-out та зміна фону."""
        if self.scene_finished:
            return  # Якщо сцена завершена, не малюємо нічого

        if paused:
            self.paused = True
            return  # Не оновлюємо нічого під час паузи

        if self.paused:
            self.paused = False  # Виходимо з паузи

        if self.current_text_index >= len(self.texts):  # Перевіряємо, чи є ще текст
            return

        _, text_duration, _ = self.texts[self.current_text_index]
        elapsed_text_time = time.time() - self.text_start_time

        if elapsed_text_time >= text_duration:
            self.skip_text()

        self.elapsed_time += 1 / 60  # Оновлюємо таймер

        total_scene_duration = sum(bg[1] for bg in self.backgrounds)  # Загальний час сцени
        fade_music_start_time = total_scene_duration - 3  # Початок затухання за 3 сек до кінця сцени

        if self.elapsed_time >= fade_music_start_time and self.music_file:
            self.stop_music_fadeout()  # 🔹 Запускаємо затухання музики перед кінцем сцени

        if self.current_bg_index < len(self.backgrounds):  # Переконуємось, що індекс в межах списку
            current_bg_duration = self.backgrounds[self.current_bg_index][1]
            time_since_bg_start = self.elapsed_time - self.bg_start_time

            # ✅ Обробка fade-in
            if not paused and self.fade_state == "fade_in" and time_since_bg_start < self.fade_in_duration:
                fade_step = int(255 / (self.fade_in_duration * 60))
                self.bg_alpha = min(255, self.bg_alpha + fade_step)

                if self.bg_alpha >= 255:
                    self.fade_state = None

            # ✅ Обробка fade-out перед зміною фону
            fade_out_start_time = current_bg_duration - self.fade_out_duration
            if not paused and self.fade_out_duration > 0 and time_since_bg_start >= fade_out_start_time:
                self.fade_state = "fade_out"

            if not paused and self.fade_state == "fade_out":
                fade_step = int(255 / (self.fade_out_duration * 60))
                self.bg_alpha = max(0, self.bg_alpha - fade_step)

                if self.bg_alpha <= 0:
                    self.current_bg_index += 1
                    if self.current_bg_index < len(self.backgrounds):
                        self.load_background(self.current_bg_index)

            if self.should_move:
                progress = min(1, time_since_bg_start / current_bg_duration)
                self.bg_pos = (
                    self.bg_start_pos[0] + (self.bg_end_pos[0] - self.bg_start_pos[0]) * progress,
                    self.bg_start_pos[1] + (self.bg_end_pos[1] - self.bg_start_pos[1]) * progress
                )

        self.render()


    def render(self):
        """Малює сцену на екрані з fade-in та fade-out ефектами."""
        if self.scene_finished:
            return  # Якщо сцена завершена, нічого не малюємо

        if self.bg_scaled:
            temp_bg = self.bg_scaled.copy()
            temp_bg.set_alpha(self.bg_alpha)  # ✅ Встановлюємо прозорість
            self.screen.blit(temp_bg, self.bg_pos)
        else:
            self.screen.fill((0, 0, 0))

        # Перевіряємо, чи є ще текст для відображення
        if self.current_text_index < len(self.texts):
            self.font = self.get_scaled_font()
            text, _, _ = self.texts[self.current_text_index]
            text_surface = self.font.render(text, True, (255, 255, 255))

            text_rect = text_surface.get_rect(center=(self.screen_resolution[0] // 2, self.screen_resolution[1] - 100))
            if text.strip():
                padding = 10  # Відступи довкола тексту
                bg_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding,
                                      text_rect.width + padding * 2, text_rect.height + padding * 2)

                # Створюємо поверхню для фону
                text_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                text_bg.fill((0, 0, 0, 150))
                self.screen.blit(text_bg, bg_rect.topleft)

            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()


    def is_finished(self):
        """Перевіряє, чи завершилася сцена (всі фони показані повністю)."""

        # Якщо ще є фони для показу – сцена не завершена
        if self.current_bg_index < len(self.backgrounds) - 1:
            return False

        # Якщо загальний час сцени ще не закінчився – продовжуємо
        if self.elapsed_time < sum(bg[1] for bg in self.backgrounds):
            return False

        self.stop_music_fadeout()  # ✅ Зупиняємо музику після завершення сцени
        return True


    def get_scaled_font(self):
        """Обчислює розмір шрифту залежно від висоти екрану."""
        screen_height = self.screen_resolution[1]
        font_size = max(14, int(screen_height * 0.03))
        return pygame.font.Font("../assets/menu_font.otf", font_size)


    def update_screen_settings(self, new_resolution, fullscreen):
        """Оновлює розмір екрану та адаптує текст і фон."""
        if new_resolution == "Максимальна":
            new_resolution = pygame.display.get_desktop_sizes()[0]  # Отримуємо максимальну роздільну здатність екрану
            fullscreen = True  # Автоматично включаємо повноекранний режим

        self.screen_resolution = new_resolution
        self.fullscreen = fullscreen