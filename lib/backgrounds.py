import random
import pygame
pygame.init()
pygame.display.init()


#create a tickled surface of the same size as the given surface and blit it onto it
def tickled_color(surface, color1, color2):
    s = pygame.Surface((surface.get_width(), surface.get_height()))
    for i in range(s.get_width()):
        for j in range(s.get_height()):
            color = random.choice([color1, color1, color2])
            s.set_at((i,j), color)
    return s


def standard_color(surface, color):
    s = pygame.Surface((surface.get_width(), surface.get_height()))
    s.fill(color)
    return s


