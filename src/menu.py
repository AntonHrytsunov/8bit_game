import pygame
from settings import get_all_resolutions
import random, os
import save_game


class Menu:
    def __init__(self, screen, options, font=None):
        self.screen = screen
        self.options = options
        self.current_selection = 0
        self.font = font or pygame.font.Font("../assets/menu_font.otf", 28)
        self.selected_color = (255, 255, 0)
        self.unselected_color = (255, 255, 255)
        self.disabled_color = (128, 128, 128)
        self.background_path = "../assets/menu/image_menu.png"
        self.background = self.load_background()
        self.update_continue_option()

    def update_continue_option(self):
        """Перевіряє, чи є файли збереження, і робить опцію 'Продовжити гру' активною або ні."""
        self.has_save = save_game.get_latest_save() is not None

    def load_background(self):
        if os.path.exists(self.background_path):
            return pygame.image.load(self.background_path).convert()
        return pygame.Surface(self.screen.get_size())  # Порожній фон, якщо файл не знайдено

    def display(self):
        scaled_bg = pygame.transform.scale(self.background, self.screen.get_size())
        self.screen.blit(scaled_bg, (0, 0))

        screen_rect = self.screen.get_rect()
        total_options = len(self.options)
        option_height = self.font.get_height() + 10
        start_y = (screen_rect.height - total_options * option_height) // 2

        for i, option in enumerate(self.options):
            is_selected = i == self.current_selection
            is_disabled = option == "Продовжити гру" and not self.has_save
            color = self.selected_color if is_selected else self.unselected_color
            if is_disabled:
                color = self.disabled_color

            rect_alpha = 180 if is_selected else 128  # 70% і 50% прозорості
            rect_surface = pygame.Surface((screen_rect.width // 2, option_height), pygame.SRCALPHA)
            rect_surface.fill((0, 0, 0, rect_alpha))
            rect_rect = rect_surface.get_rect(center=(screen_rect.width // 2, start_y + i * option_height))
            self.screen.blit(rect_surface, rect_rect)

            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_rect.width // 2, start_y + i * option_height))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.options)
                sound_manager = SoundManager(volume=0.5)  # Гучність 50%
                sound_manager.play_random_sound()
            elif event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.options)
                sound_manager = SoundManager(volume=0.5)  # Гучність 50%
                sound_manager.play_random_sound()
            elif event.key == pygame.K_RETURN:
                sound_manager = SoundManager(sound_folder="../assets/menu/sound_return", volume=0.5)  # Гучність 50%
                sound_manager.play_random_sound()
                return self.current_selection
        return None


class Settings:
    def __init__(self, screen, options, game_settings, font=None):
        self.screen = screen
        self.options = options
        self.current_selection = 0
        self.font = font or pygame.font.Font("../assets/menu_font.otf", 28)
        self.selected_color = (255, 255, 0)
        self.unselected_color = (255, 255, 255)
        self.game_settings = game_settings
        self.background_path = "../assets/menu/setting_menu.png"
        self.background = self.load_background()

        # Використовуємо динамічно згенерований список для роздільної здатності
        self.settings_values = {
            "Повноекранний режим": ["Вимкнено", "Повноекранний"],
            "Роздільна здатність екрану": get_all_resolutions(),
            "Складність гри": ["Легко", "Середня", "Складно", "Ти будеш плакати"]
        }
        self.current_values = {
            "Повноекранний режим": 0,
            "Роздільна здатність екрану": 0,
            "Складність гри": 0
        }
        self.sync_with_game_settings()

    def load_background(self):
        if os.path.exists(self.background_path):
            return pygame.image.load(self.background_path).convert()
        return pygame.Surface(self.screen.get_size())

    def sync_with_game_settings(self):
        # Повноекранний режим
        fs = self.game_settings.get("fullscreen")
        self.current_values["Повноекранний режим"] = 1 if fs else 0

        # Роздільна здатність
        res_tuple = tuple(self.game_settings.get("resolution"))
        res_str = f"{res_tuple[0]}x{res_tuple[1]}"
        res_options = self.settings_values["Роздільна здатність екрану"]
        if res_str in res_options:
            self.current_values["Роздільна здатність екрану"] = res_options.index(res_str)
        else:
            self.current_values["Роздільна здатність екрану"] = 0

        # Складність гри
        diff = self.game_settings.get("difficulty")
        if diff in self.settings_values["Складність гри"]:
            self.current_values["Складність гри"] = self.settings_values["Складність гри"].index(diff)
        else:
            self.current_values["Складність гри"] = 0

    def display(self):
        scaled_bg = pygame.transform.scale(self.background, self.screen.get_size())
        self.screen.blit(scaled_bg, (0, 0))
        screen_rect = self.screen.get_rect()
        total_options = len(self.options)
        option_height = self.font.get_height() + 10
        start_y = (screen_rect.height - total_options * option_height) // 2
        margin = 50

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.current_selection else self.unselected_color
            rect_alpha = 180 if i == self.current_selection else 128
            rect_surface = pygame.Surface((screen_rect.width - margin * 2, option_height), pygame.SRCALPHA)
            rect_surface.fill((0, 0, 0, rect_alpha))
            rect_rect = rect_surface.get_rect(left=margin, top=start_y + i * option_height)
            self.screen.blit(rect_surface, rect_rect)

            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(left=margin + 10, top=start_y + i * option_height)
            self.screen.blit(text_surface, text_rect)

            if option != "Назад" and option in self.settings_values:
                current_index = self.current_values[option]
                current_value = self.settings_values[option][current_index]
                value_surface = self.font.render(current_value, True, color)
                value_rect = value_surface.get_rect(right=screen_rect.width - margin, top=start_y + i * option_height)
                self.screen.blit(value_surface, value_rect)
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.options)
                sound_manager = SoundManager(volume=0.5)  # Гучність 50%
                sound_manager.play_random_sound()
            elif event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.options)
                sound_manager = SoundManager(volume=0.5)  # Гучність 50%
                sound_manager.play_random_sound()
            elif event.key == pygame.K_RETURN:
                option = self.options[self.current_selection]
                if option == "Назад":
                    sound_manager = SoundManager(sound_folder="../assets/menu/sound_return", volume=0.5)  # Гучність 50%
                    sound_manager.play_random_sound()
                pass
                return self.current_selection
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                option = self.options[self.current_selection]
                if option != "Назад":
                    sound_manager = SoundManager(sound_folder="../assets/menu/sound_return", volume=0.5)  # Гучність 50%
                    sound_manager.play_random_sound()
                pass
                if option != "Назад" and option in self.settings_values:
                    current_index = self.current_values[option]
                    if event.key == pygame.K_LEFT:
                        current_index = (current_index + 1) % len(self.settings_values[option])
                    elif event.key == pygame.K_RIGHT:
                        current_index = (current_index - 1) % len(self.settings_values[option])
                    self.current_values[option] = current_index

                    # Оновлюємо GameSettings відповідно до вибраного значення
                    if option == "Повноекранний режим":
                        new_fs = True if self.settings_values[option][current_index] == "Повноекранний" else False
                        self.game_settings.update("fullscreen", new_fs)
                    elif option == "Роздільна здатність екрану":
                        res_str = self.settings_values[option][current_index]
                        if res_str == "Максимальна":
                            modes = pygame.display.list_modes()
                            if modes:
                                width, height = modes[0]
                            else:
                                width, height = 800, 600
                        else:
                            width, height = map(int, res_str.split("x"))
                        self.game_settings.update("resolution", [width, height])
                    elif option == "Складність гри":
                        new_diff = self.settings_values[option][current_index]
                        self.game_settings.update("difficulty", new_diff)
        return None


class PauseMenu:
    def __init__(self, screen, options, background, font=None):
        self.screen = screen
        self.background = background  # Збережене зображення гри
        self.options = options  # Наприклад: ["Продовжити гру", "Вийти у систему"]
        self.current_selection = 0
        self.font = font or pygame.font.Font("../assets/menu_font.otf", 36)
        self.selected_color = (255, 255, 0)
        self.unselected_color = (255, 255, 255)

    def display(self):
        # Спершу малюємо збережене зображення гри
        self.screen.blit(self.background, (0, 0))
        # Тепер створюємо поверхню з підтримкою альфа-каналу
        overlay = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Чорний з прозорістю 150
        self.screen.blit(overlay, (0, 0))

        screen_rect = self.screen.get_rect()
        total_options = len(self.options)
        option_height = self.font.get_height() + 10
        start_y = (screen_rect.height - total_options * option_height) // 2

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.current_selection else self.unselected_color
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_rect.width // 2, start_y + i * option_height))
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Повертаємо -1, щоб сигналізувати про завершення меню паузи (продовження гри)
                return -1
            elif event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.current_selection
        return None


class SoundManager:
    def __init__(self, sound_folder="../assets/menu/sound_menu", volume=1.0):
        pygame.mixer.init()
        self.sound_folder = sound_folder
        self.volume = volume
        self.sounds = self._load_sounds()

    def _load_sounds(self):
        """Завантажує всі звукові файли з папки."""
        if not os.path.exists(self.sound_folder):
            print(f"Папка {self.sound_folder} не існує!")
            return []

        return [os.path.join(self.sound_folder, f) for f in os.listdir(self.sound_folder) if
                f.endswith((".wav", ".mp3", ".ogg"))]

    def play_random_sound(self):
        """Відтворює випадковий звук із папки."""
        if not self.sounds:
            print("Немає доступних звуків для відтворення.")
            return

        sound_file = random.choice(self.sounds)
        sound = pygame.mixer.Sound(sound_file)
        sound.set_volume(self.volume)
        sound.play()


    def set_volume(self, volume):
        """Змінює гучність звуків (0.0 - 1.0)."""
        self.volume = max(0.0, min(1.0, volume))  # Обмежуємо значення між 0.0 і 1.0


    def stop_music(self):
        pygame.time.delay(1000)
        pygame.mixer.stop()
        pygame.mixer.music.unload()