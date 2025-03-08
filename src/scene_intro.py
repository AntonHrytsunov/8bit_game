from scene import Scene
from settings import GameSettings
import pygame

class IntroScene(Scene):
    def __init__(self, screen, game_settings):
        """Сцена інтро, що успадковує Scene."""
        super().__init__(
            screen=screen,
            duration=45,
            background="../assets/scene/intro/image.png",
            texts=[
                ("Важкі часи у країні головного героя. Часи скорботи, часи втрати.", 10),
                ("Але це і часи героїв, часи сміливих, часи дії.", 10),
                ("Люди ховаються за стінами міст, сподіваючись, що буря мине їхні домівки, але надія слабшає з кожним днем.", 10),
                ("Головний герой стоїть на роздоріжжі: віддатися страху чи кинути виклик долі?", 8),
                ("Вибір зроблено. Його шлях починається зараз, і легенда про нового героя лише зароджується.", 10)

            ],
            game_settings=game_settings
        )