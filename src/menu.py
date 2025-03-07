# Скрипт для створення класу "Menu", в якому буде Menu,
# який відповідатиме за відображення меню та обробку подій.


# Імпортуємо необхідні бібліотеки
import pygame

# Основний клас Menu
class Menu:
    def __init__(self, screen, options, font=None):
        self.screen = screen
        self.options = options  # Список рядків з опціями меню
        self.current_selection = 0  # Індекс поточного вибору

        # Використовуємо стандартний шрифт, якщо не задано інший
        self.font = font or pygame.font.SysFont("Arial", 36)
        self.selected_color = (255, 255, 0)  # Жовтий для вибраного пункту
        self.unselected_color = (255, 255, 255)  # Білий для решти

    def display(self):
        self.screen.fill((0, 0, 0))  # Заливка фону чорним
        screen_rect = self.screen.get_rect()

        # Обчислюємо позицію для відображення меню вертикально
        total_options = len(self.options)
        option_height = self.font.get_height() + 10  # Висота одного рядка із відступами
        start_y = (screen_rect.height - total_options * option_height) // 2

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.current_selection else self.unselected_color
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_rect.width // 2, start_y + i * option_height))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.current_selection  # Повертаємо вибір при натисканні Enter
        return None

