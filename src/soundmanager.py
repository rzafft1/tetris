import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "row_clear": pygame.mixer.Sound("src/sounds/rowcleared.mp3"),
            "make_move": pygame.mixer.Sound("src/sounds/makemove.mp3"),
            "click": pygame.mixer.Sound("src/sounds/click.mp3"),
            "level_up": pygame.mixer.Sound("src/sounds/levelup.mp3")
        }

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def set_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)  # 0.0 to 1.0

    def stop_all(self):
        pygame.mixer.stop()