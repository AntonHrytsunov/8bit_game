import pygame
import re
import random
import os
import json


class HeroCreator:
    def __init__(self, screen, game_settings):
        self.screen = screen
        self.game_settings = game_settings
        self.screen_width, self.screen_height = screen.get_size()
        self.scale_factor = self.screen_height / 700  # Базовий розмір взято 700px

        self.font_size = int(30 * self.scale_factor)
        self.font = pygame.font.Font("../assets/menu_font.otf", self.font_size)

        self.classes = ["Маг", "Воїн", "Лучник"]
        self.races = ["Людина", "Ельф", "Гном", "Зверолюд"]
        self.genders = ["Парубок", "Дівчина"]

        self.selected_class = 0
        self.selected_race = 0
        self.selected_gender = 0
        self.input_name = ""
        self.active_input = True

        self.menu_options = ["Ім'я", "Клас", "Раса", "Стать", "Почати"]
        self.selected_option = 0

        self.running = True
        self.finished = False

        self.bg_image = pygame.image.load("../assets/scene/intro/black.png").convert_alpha()
        self.bg_scaled = self.scale_background(self.bg_image, screen.get_size())

        try:
            self.frame_image = pygame.image.load("../assets/characters/rama.png").convert_alpha()
        except pygame.error:
            print("Не вдалося завантажити рамку: ../assets/characters/rama.png")
            self.frame_image = None

        self.character_image = None
        self.character_scaled = None
        self.character_pos = None
        self.frame_scaled = None
        self.text_box_rect = None
        self.text_font_size = int(24 * self.scale_factor)
        self.text_font = pygame.font.Font("../assets/menu_font.otf", self.text_font_size)

        self.update_character_image()

        self.music_file = "../assets/scene/hero_creator/dark_wood.mp3"
        self.play_music()
        self.random_name = random.choice([
            "Раеліон", "Еріан", "Аурін", "Люміар", "Фейріс",
            "Селіан", "Варен", "Зелайр", "Каеліос", "Мірісан"
        ])


    def play_music(self):
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"Помилка завантаження музичного файлу: {self.music_file}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def scale_background(self, image, screen_size):
        img_width, img_height = image.get_size()
        screen_width, screen_height = screen_size
        scale_factor = max(screen_width / img_width, screen_height / img_height)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
        x_offset = (screen_width - new_width) // 2
        y_offset = screen_height - new_height
        return scaled_image, (x_offset, y_offset)

    def draw_gradient_circle(self, surface, center, radius, rd, g, b, max_alpha=255):
        gradient_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        for r in range(radius, 0, -1):
            alpha = int(max_alpha * (1 - (r / radius)))  # Прозорість поступово зменшується до 0 біля країв
            color = (rd, g, b, alpha)
            pygame.draw.circle(gradient_surface, color, (radius, radius), r)

        surface.blit(gradient_surface, (center[0] - radius, center[1] - radius))

    def update_character_image(self):
        class_eng = {"Маг": "mag", "Воїн": "war", "Лучник": "archer"}[self.classes[self.selected_class]]
        race_eng = {"Людина": "hum", "Ельф": "elf", "Гном": "dwarf", "Зверолюд": "beast"}[self.races[self.selected_race]]
        gender_eng = {"Парубок": "male", "Дівчина": "female"}[self.genders[self.selected_gender]]

        image_path = f"../assets/characters/{race_eng}_{class_eng}_{gender_eng}.png"

        try:
            self.character_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            print(f"Не вдалося завантажити зображення: {image_path}")
            self.character_image = pygame.Surface((100, 150), pygame.SRCALPHA)

        screen_width, screen_height = self.screen.get_size()
        frame_height = int(screen_height * 0.6)

        if self.frame_image:
            aspect_ratio = self.frame_image.get_width() / self.frame_image.get_height()
            frame_width = int(frame_height * aspect_ratio)
            frame_x = screen_width - frame_width
            frame_y = screen_height - frame_height

            self.frame_scaled = pygame.transform.smoothscale(self.frame_image, (frame_width, frame_height))
            self.frame_pos = (frame_x, frame_y)

            char_width = int(frame_width * 0.7)
            char_aspect_ratio = self.character_image.get_width() / self.character_image.get_height()
            char_height = int(char_width / char_aspect_ratio)

            self.character_scaled = pygame.transform.smoothscale(self.character_image, (char_width, char_height))

            char_x = frame_x + (frame_width - char_width) // 2
            char_y = frame_y + (frame_height - char_height) // 2
            self.character_pos = (char_x, char_y)

            self.circle_center = (char_x + char_width // 2, char_y + char_height // 2)
            self.circle_radius = int(frame_width * 0.45)
            self.circle_radius_black = int(frame_width * 0.9)

        self.text_box_rect = pygame.Rect(20, frame_y + frame_height/2, frame_x - 40, frame_height/2)

    def scale_character(self, image, screen_size):
        screen_width, screen_height = screen_size
        img_width, img_height = image.get_size()

        # Визначаємо масштаб, щоб висота була 1/3 висоти екрану
        scale_factor = (screen_height / 2) / img_height
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))

        # Визначаємо позицію (10% від правого краю)
        x_pos = screen_width - new_width - int(screen_width * 0.1)
        y_pos = screen_height - new_height  # Нижній край зображення співпадає з краєм екрану

        return scaled_image, (x_pos, y_pos)

    def draw_text_box(self):
        if self.text_box_rect:
            # **Не малюємо фон, а просто рендеримо текст поверх сцени**
            text = self.get_character_description()
            lines = self.wrap_text(text, self.text_box_rect.width - 20)

            y_offset = self.text_box_rect.y + 10
            for line in lines:
                rendered_text = self.text_font.render(line, True, (255, 255, 255))  # Білий текст без фону
                self.screen.blit(rendered_text, (self.text_box_rect.x + 10, y_offset))
                y_offset += self.text_font.get_height()

    def get_character_description(self):
        file_path = "../assets/characters/characters.txt"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.rstrip() for line in file.readlines()]  # Видаляємо зайві пробіли праворуч
        except FileNotFoundError:
            print(f"Помилка: Файл {file_path} не знайдено.")
            return "Опис відсутній."

        # Визначаємо секцію, яку потрібно знайти ("Чоловіки" або "Жінки")
        gender_header = "Чоловіки:" if self.genders[self.selected_gender] == "Парубок" else "Жінки:"

        found_gender_section = False  # Чи знайшли секцію Чоловіки/Жінки
        found_character = False  # Чи знайшли відповідного персонажа
        description = []  # Опис персонажа

        # Формуємо ключ персонажа: "Клас - Раса"
        character_key = f"{self.classes[self.selected_class]} - {self.races[self.selected_race]}"

        print(f"Шукаємо: {character_key} у секції {gender_header}")  # Діагностика

        for line in lines:
            print(f"Читаємо рядок: {line}")  # Дебаг вивід кожного рядка

            # Пошук секції (Чоловіки або Жінки)
            if not found_gender_section:
                if line == gender_header:
                    found_gender_section = True
                    print(f"✅ Знайдено секцію: {gender_header}")
                continue

            # Якщо натрапили на інший заголовок (Чоловіки/Жінки), виходимо з пошуку
            if found_gender_section and (line == "Чоловіки:" or line == "Жінки:"):
                print(f"⛔ Виявлено новий заголовок ({line}), виходимо з блоку пошуку.")
                break

            # Якщо вже знайшли потрібного персонажа, записуємо його опис
            if found_character:
                if line == "":  # Порожній рядок = кінець опису
                    print("🔚 Кінець опису персонажа.")
                    break
                description.append(line)
                print(f"➕ Додаємо опис: {line}")

            # Якщо знайшли потрібного персонажа, починаємо записувати опис
            elif line == character_key:
                found_character = True
                print(f"🎯 Знайдено персонажа: {character_key}")

        # Якщо знайдено опис - повертаємо його
        if description:
            return " ".join(description)
        else:
            print("⚠️ Персонаж не знайдений, повертаємо 'Опис відсутній'")
            return "Опис відсутній."

    def wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.text_font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.selected_option == 0:
                if event.key == pygame.K_BACKSPACE:
                    self.input_name = self.input_name[:-1]
                else:
                    char = event.unicode
                    if re.match("^[А-Яа-яІіЇїЄєҐґ]$", char) and len(self.input_name) < 15:
                        if len(self.input_name) == 0:
                            self.input_name += char.upper()
                        else:
                            self.input_name += char.lower()
            if self.selected_option == 4:
                if event.key == pygame.K_RETURN:
                    self.save_hero()

            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_LEFT:
                if self.selected_option == 1:
                    self.selected_class = (self.selected_class - 1) % len(self.classes)
                elif self.selected_option == 2:
                    self.selected_race = (self.selected_race - 1) % len(self.races)
                elif self.selected_option == 3:
                    self.selected_gender = (self.selected_gender - 1) % len(self.genders)
                self.update_character_image()  # Оновлення зображення після зміни параметрів
            elif event.key == pygame.K_RIGHT:
                if self.selected_option == 1:
                    self.selected_class = (self.selected_class + 1) % len(self.classes)
                elif self.selected_option == 2:
                    self.selected_race = (self.selected_race + 1) % len(self.races)
                elif self.selected_option == 3:
                    self.selected_gender = (self.selected_gender + 1) % len(self.genders)
                self.update_character_image()  # Оновлення зображення після зміни параметрів
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 4 and self.input_name:
                    self.save_hero()
                    self.finished = True
                    self.stop_music()

    def update(self, paused):
        if paused:
            return
        self.render()

    def render(self):
        self.screen.blit(*self.bg_scaled)
        y_offset = int(self.screen_height*0.05)

        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (200, 200, 200)

            if option == "Ім'я":
                text = f"Ім'я: {self.input_name if self.input_name else self.random_name}"
            elif option == "Клас":
                text = f"Клас: {self.classes[self.selected_class]}"
            elif option == "Раса":
                text = f"Раса: {self.races[self.selected_race]}"
            elif option == "Стать":
                text = f"Стать: {self.genders[self.selected_gender]}"
            else:
                text = option

            rendered_text = self.font.render(text, True, color)
            self.screen.blit(rendered_text, (50, y_offset))
            y_offset += int(self.screen_height*0.1)

        self.draw_text_box()

        if self.character_scaled:
            self.draw_gradient_circle(self.screen, self.circle_center, self.circle_radius_black, 20, 20, 40, 255)
            self.draw_gradient_circle(self.screen, self.circle_center, self.circle_radius, 255, 255, 255, 255)
            self.screen.blit(self.character_scaled, self.character_pos)

        if self.frame_scaled:
            self.screen.blit(self.frame_scaled, self.frame_pos)

        pygame.display.flip()

    def save_hero(self):
        hero_data = {
            "name": self.input_name if self.input_name else self.random_name,
            "class": self.classes[self.selected_class],
            "race": self.races[self.selected_race],
            "gender": self.genders[self.selected_gender],
            "hero_create": "done"
        }

        save_dir = "../game_save/"

        # Отримуємо список усіх файлів з розширенням .sav
        save_files = [f for f in os.listdir(save_dir) if f.endswith(".sav")]

        if save_files:
            save_path = os.path.join(save_dir, save_files[0])  # Беремо перший .sav файл
            with open(save_path, "w", encoding="utf-8") as save_file:
                json.dump(hero_data, save_file, ensure_ascii=False, indent=4)
            print("Персонаж збережений у файл:", save_path)
        else:
            print("Помилка: Файл .sav не знайдено у каталозі game_save.")

    def is_finished(self):
        return self.finished
