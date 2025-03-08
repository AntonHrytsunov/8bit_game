import pygame
import os
from menu import SoundManager


class Out:
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font or pygame.font.Font("../assets/menu_font.otf", 28)
        self.options = ["Так", "Ні"]
        self.current_selection = 1
        self.selected_color = (255, 255, 0)
        self.unselected_color = (255, 255, 255)
        self.background_path = "../assets/menu/delete_old_saves.png"
        self.background = self.load_background()

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

        # Виділення питання напівпрозорим прямокутником
        question_surface = self.font.render("Всі минулі збереження будуть видалені. Продовжити?", True,
                                            self.unselected_color)
        question_rect = question_surface.get_rect(center=(screen_rect.width // 2, screen_rect.height // 3))

        rect_surface = pygame.Surface((question_rect.width + 20, question_rect.height + 10), pygame.SRCALPHA)
        rect_surface.fill((0, 0, 0, 180))  # Чорний колір з 70% прозорістю
        rect_rect = rect_surface.get_rect(center=question_rect.center)

        self.screen.blit(rect_surface, rect_rect)
        self.screen.blit(question_surface, question_rect)

        for i, option in enumerate(self.options):
            is_selected = i == self.current_selection
            color = self.selected_color if is_selected else self.unselected_color

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
                return self.options[self.current_selection]
        return None
