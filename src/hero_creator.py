

class HeroCraetor:
    def _init__(self, screen, game_settings):
        self.screen = screen
        self.screen_resolution = tuple(game_settings.get("resolution"))
        self.fullscreen = game_settings.get("fullscreen")