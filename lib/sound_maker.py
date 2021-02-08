import pygame, os
from time import sleep
pygame.init() 


hive_paths = {"ant": os.path.join("sounds", "ant.wav"), "hopper": os.path.join("sounds", "hopper.wav"),
              "spider": os.path.join("sounds", "spider.wav"), "bee": os.path.join("sounds", "bee.wav"),
              "bug": os.path.join("sounds", "ladybug.wav"), "mosquito": os.path.join("sounds", "mosquito.wav"),
              "ladybug": os.path.join("sounds", "ladybug.wav"), "music": os.path.join("sounds", "music.mp3")}
pygame.mixer.music.load(hive_paths["music"])

class sound_maker():
    def __init__(self, music = False, sound = True):
        self.sound = sound
        self.music = music
    
    def make_sound(self, insect_type):
        if self.sound:
#            if self.music:
#                pygame.mixer.music.stop()
#                sleep(0.2)
            pygame.mixer.Sound(hive_paths[insect_type]).play()
#            if self.music:
#                sleep(1)
#                self.play_music()
                    
    
    def play_music(self):
        if self.music:
            return pygame.mixer.music.play(-1)