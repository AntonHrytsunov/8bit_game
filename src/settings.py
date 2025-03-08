import json
import os
import pygame

class GameSettings:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        # Значення за замовчуванням
        self.defaults = {
            "fullscreen": False,
            "resolution": [800, 600],
            "difficulty": "Легко"
        }
        self.settings = {}
        self.load()

    def load(self):
        # Якщо файл існує, завантажуємо налаштування, інакше використовуємо значення за замовчуванням
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = self.defaults.copy()
            self.save()

    def save(self):
        # Записуємо налаштування у файл
        with open(self.filename, "w") as f:
            json.dump(self.settings, f, indent=4)

    def update(self, key, value):
        # Оновлюємо конкретну настройку та зберігаємо файл
        self.settings[key] = value
        self.save()

    def get(self, key):
        # Повертаємо значення налаштування
        return self.settings.get(key, self.defaults.get(key))


def get_all_resolutions():
    modes = pygame.display.list_modes()
    if not modes:
        return ["800x600"]
    # Отримуємо унікальні режими та сортуємо за загальною кількістю пікселів (від більшого до меншого)
    unique_modes = sorted(set(modes), key=lambda m: m[0]*m[1], reverse=True)
    res_options = [f"{m[0]}x{m[1]}" for m in unique_modes]
    # Додаємо опцію "Максимальна", яка дозволяє встановити найбільший режим
    if "Максимальна" not in res_options:
        res_options.append("Максимальна")
    return res_options