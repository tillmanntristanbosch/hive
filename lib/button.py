# -*- coding: cp1252 -*-
#/usr/bin/env python
#Simon H. Larsen
#Buttons
#Project startet: d. 26. august 2012
import pygame

pygame.init()

class Button:
    def __init__(self, surface, button_text = "", text_width = 0, pixel_pos = (0,0), button_size = (0,0), 
                 back_color = (100,100,100), text_color = (0,0,0), shall_be_seen = True):
        self.surface = surface
        self.text = button_text
        self.text_width = text_width
        self.pixel_pos = pixel_pos
        self.size = button_size
        self.back_color = back_color
        self.text_color = text_color
        
        self.shall_be_seen = shall_be_seen
        self.is_drawn = False
        
        self.rect = pygame.Rect(pixel_pos, button_size)
    
    def draw_button(self):
        self.draw_button_background(self.back_color)
        self.write_text(self.text, self.text_color)
        self.is_drawn = True
    
    def write_text(self, text, text_color):
        x, y = self.pixel_pos
        length, height = self.size
        myFont = pygame.font.SysFont("Comic Sans MS", self.text_width)
        myText = myFont.render(text, 1, text_color)
        self.surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))

    def draw_button_background(self, back_color):
        x, y = self.pixel_pos
        length, height = self.size         
        for i in range(1,10):
            s = pygame.Surface((length + (i*2), height + (i*2)))
            s.fill(back_color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, back_color, (x-i, y-i, length + i, height + i), self.text_width)
            self.surface.blit(s, (x-i, y-i))
        pygame.draw.rect(self.surface, back_color, (x, y, length, height), 0)
        pygame.draw.rect(self.surface, (190,190,190), (x, y, length, height), 1)  

    def pressed(self, position):
        offset = self.surface.get_abs_offset()
        position = (position[0] - offset[0], position[1] - offset[1])
        if position[0] > self.rect.topleft[0]:
            if position[1] > self.rect.topleft[1]:
                if position[0] < self.rect.bottomright[0]:
                    if position[1] < self.rect.bottomright[1]:
                        #print ("Some button was pressed!")
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
