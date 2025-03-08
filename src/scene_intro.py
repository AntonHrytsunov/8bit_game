from scene import Scene
from settings import GameSettings
import pygame

class IntroScene(Scene):
    def __init__(self, screen, game_settings):
        """Сцена інтро, що успадковує Scene."""
        super().__init__(
            screen=screen,
            duration=25,
            background="../assets/scene/intro/image.png",
            texts=[
                ("Важкі часи у країні головного героя. Часи скорботи, часи втрати.", 10),
                ("Але це і часи героїв, часи сміливих, часи дії.", 10)
            ],
            game_settings=game_settings
        )