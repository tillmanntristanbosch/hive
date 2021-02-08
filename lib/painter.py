import pygame, os
from math import sqrt, log
import colors as c

hive_paths = {"ant": os.path.join("pictures", "ant.png"), "hopper": os.path.join("pictures", "hopper.png"),
              "spider": os.path.join("pictures", "spider.png"), "bee": os.path.join("pictures", "bee.png"),
              "bug": os.path.join("pictures", "beetle.png"), "mosquito": os.path.join("pictures", "mosquito.png"),
              "ladybug": os.path.join("pictures", "ladybug.png")}

class Painter:
    
    def __init__(self, backgrounds = None):
        self.backgrounds = backgrounds
    
    #fill background with color
    def draw_background(self, surface):
        surface.fill(c.background_board)
#        surface.blit(self.backgrounds[surface], (0,0))
        
    #draw full hexagon (shall a frame with mark_mode = 0 also be drawn ?)
    def draw_hexagon(self, hexagon, surface):
        if not hexagon.is_drawn:
            hexagon.is_drawn = True
            hexagon.set_drawn_surface(surface)
        if hexagon.type == "empty": 
            pass
           # pygame.draw.polygon(surface, c.empty_stone_color, hexagon.points)
        else:
            if hexagon.color == "white":    pygame.draw.polygon(surface, c.creme_white, hexagon.points) #creme white
            elif hexagon.color == "black":  pygame.draw.polygon(surface, c.creme_black, hexagon.points) #creme black
            #blit insect on the polygon
            if hexagon.is_mosquito:  insect = "mosquito"
            else:   insect = hexagon.type
            insect_image = pygame.image.load(hive_paths[insect])
            insect_image = pygame.transform.scale(insect_image, (hexagon.size, int(hexagon.size * 3**(0.5))))
            surface.blit(insect_image, hexagon.pixel_pos)
            
    def draw_all_existing_markings(self, board, color = c.marking_color, mark_mode = 0):
        for hstone in board.board.values():
            if hstone.is_marked:    self.draw_hexagon_marking(hstone, color, mark_mode)
    
    #draw a list of full hexagons 
    def draw_set_of_hexagons(self, hstone_list, surface):
        for hstone in hstone_list:  self.draw_hexagon(hstone, surface)
    
    #draw the whole board of hexagons on surface
    def draw_board(self, board, surfaces, buttons, mark_mode = 0):
        self.draw_background(surfaces["surface_board"])
        for hstone in board.board.values():
            self.draw_hexagon(hstone, surfaces["surface_board"])
        self.draw_all_existing_markings(board, mark_mode = mark_mode)
        self.draw_ingame_frame(surfaces["surface_full"])
        for button in buttons.values():
            if button.shall_be_seen:
                button.draw_button()
                
    def draw_hexagon_frame(self, hexagon, color = (0,0,0), width = 1):
        width = (hexagon.size + 2 * width / sqrt(3) - (width // 2)) // 15
        pygame.draw.lines(hexagon.drawn_surface, color, True, hexagon.points, int(width))
        
    def draw_half_hexagon_frame(self, hexagon, color = (0,0,0), width = 1):
        width = (hexagon.size + 2 * width / sqrt(3) - (width // 2)) // 15
        points1 = [hexagon.points[2], hexagon.points[3]]
        points2 = [hexagon.points[3], hexagon.points[4]]
        pygame.draw.lines(hexagon.drawn_surface, color, True, points1, int(width))
        pygame.draw.lines(hexagon.drawn_surface, color, True, points2, int(width))

    #try different marking code    
    def draw_hexagon_marking(self, hexagon, color = (0,0,0), mark_mode = 0):
        pygame.draw.lines(hexagon.drawn_surface, color, True, hexagon.points, int(mark_mode))
        hexagon.is_marked = True
        
    #draw set of hexagons with respective color and mark_mode, for example when drawing all possible 
    #hexagons a stone can move to 
    def draw_set_of_hexagon_markings(self, hexagon_list, color, mark_mode = 0):
        for hexagon in hexagon_list:    self.draw_hexagon_marking(hexagon, color, mark_mode)
    
    #draw standard game frame (left and right side areas with text fields at the bottom and middle board area)
    def draw_ingame_frame(self, surface):
        width = surface.get_width()
        height = surface.get_height()
        line_width = width // 350
        pygame.draw.line(surface, c.ingame_frame_color, (0.1 * width, 0), (0.1 * width, 0.95 * height), line_width)
        pygame.draw.line(surface, c.ingame_frame_color, (0.9 * width, 0),(0.9 * width, 0.95 * height), line_width)
        pygame.draw.line(surface, c.ingame_frame_color, (0, 0.95 * height), (0.5 * width, 0.95 * height), line_width)
        pygame.draw.line(surface, c.ingame_frame_color, (0.5 * width, 0.95 * height), (width, 0.95 * height), line_width)
        pygame.draw.line(surface, c.ingame_frame_color, (0.5 * width, 0.95 * height), (0.5 * width, height), line_width)
        
    def write_text(self, surface, text, font_size, color, position):
        myText = pygame.font.SysFont("Arial", font_size).render(text, 1, color)
        surface.blit(myText, position)
        
    def write_box_text(self, surfaces, text, player_color):
        surface = surfaces["surface_text"][player_color]
        self.draw_background(surface)
        font_size = int(25 - log(len(text))) 
        color = c.box_text_color
        position = (0.05 * surface.get_width(), 0.1 * surface.get_height())
        self.write_text(surface, text, font_size, color, position)
        self.draw_ingame_frame(surfaces["surface_full"])
    
    def draw_stone_number(self, player, hexagon, surfaces, text_color = (0,0,0)):
        stone_size = player.stone_size
        text_size = int(1.2 * stone_size)
        test_font = pygame.font.SysFont("Arial", text_size)
        (width, height) = test_font.size("0")
        position =  (hexagon.pixel_pos[0] - 13 * stone_size / 18 - width,
                     hexagon.pixel_pos[1] + sqrt(3) * 0.5 * stone_size - 0.5 * height)
        rect_subsurface = surfaces["surface_stones"][player.color].subsurface(pygame.Rect(position, (width, height)))
        rect_subsurface.fill(surfaces["surface_stones"][player.color].get_at_mapped((7,7)))
        self.write_text(rect_subsurface, str(player.side_stones_numbers[hexagon.type]), 
                                text_size, c.stone_number_color, (0,0))
        
    def draw_all_stone_numbers(self, player, surfaces, text_color = (0,0,0)):
        for hexagon in player.side_stones.values(): self.draw_stone_number(player, hexagon, surfaces, text_color)
        
    def draw_unmarked_side_area(self, player, surfaces):
        surfaces["surface_stones"][player.color].fill(surfaces["surface_stones"][player.color].get_at_mapped((7,7)))
        self.draw_set_of_hexagons(player.side_stones.values(), surfaces["surface_stones"][player.color])
        self.draw_all_stone_numbers(player, surfaces)
        
    def draw_menu(self, surfaces, buttons):
#        full_rect = surfaces["surface_full"].copy()
#        full_rect.fill((255,255,255))
#        full_rect.fill((100,100,100,100))
        
        #draw menu buttons
        surfaces["surface_menu"].fill(c.background_menu)
        buttons["continue_game_button"].draw_button()
        buttons["back_to_menu_button"].draw_button()
        
        #blit rects
#        surfaces["surface_full"].blit(full_rect, (0,0))
#        offset = surfaces["surface_menu"].get_offset()
#        surfaces["surface_full"].blit(surfaces["surface_menu"], offset)
        
        
        
        
        
        
        

#nothing    
