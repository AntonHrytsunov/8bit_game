import pygame


class HeroCreator:
    def __init__(self, screen, game_settings):
        self.screen = screen
        self.game_settings = game_settings
        self.font = pygame.font.Font("../assets/menu_font.otf", 30)

        self.classes = ["Маг", "Важкий воїн", "Легкий воїн", "Лучник"]
        self.races = ["Людина", "Ельф", "Дворф"]
        self.colors = ["Червоний", "Синій", "Зелений"]

        self.selected_class = 0
        self.selected_race = 0
        self.selected_color = 0

        self.running = True
        self.finished = False  # Додаємо, щоб гра знала, коли персонажа створено

    def handle_events(self, event):
        """Обробляє натискання клавіш для вибору параметрів."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_class = (self.selected_class - 1) % len(self.classes)
            elif event.key == pygame.K_DOWN:
                self.selected_class = (self.selected_class + 1) % len(self.classes)
            elif event.key == pygame.K_LEFT:
                self.selected_race = (self.selected_race - 1) % len(self.races)
            elif event.key == pygame.K_RIGHT:
                self.selected_race = (self.selected_race + 1) % len(self.races)
            elif event.key == pygame.K_SPACE:
                self.selected_color = (self.selected_color + 1) % len(self.colors)
            elif event.key == pygame.K_RETURN:
                self.save_hero()
                self.finished = True  # Завершуємо створення персонажа

    def update(self, paused):
        """Оновлює екран, аналогічно до Scene."""
        if paused:
            return  # Якщо гра на паузі, не оновлюємо

        self.render()

    def render(self):
        """Малює інтерфейс вибору персонажа."""
        self.screen.fill((0, 0, 0))

        title = self.font.render("Створення персонажа", True, (255, 255, 255))
        class_text = self.font.render(f"Клас: {self.classes[self.selected_class]}", True, (200, 200, 200))
        race_text = self.font.render(f"Раса: {self.races[self.selected_race]}", True, (200, 200, 200))
        color_text = self.font.render(f"Колір одягу: {self.colors[self.selected_color]}", True, (200, 200, 200))
        instructions = self.font.render("Інструкції", True, (150, 150, 150))

        self.screen.blit(title, (50, 50))
        self.screen.blit(class_text, (50, 150))
        self.screen.blit(race_text, (50, 250))
        self.screen.blit(color_text, (50, 350))
        self.screen.blit(instructions, (50, 500))

        pygame.display.flip()

    def save_hero(self):
        """Зберігає вибір героя в налаштування."""
        hero_data = {
            "class": self.classes[self.selected_class],
            "race": self.races[self.selected_race],
            "color": self.colors[self.selected_color],
        }
        self.game_settings["hero"] = hero_data
        print("Персонаж створений:", hero_data)

    def is_finished(self):
        """Перевіряє, чи завершено створення персонажа."""
        return self.finished