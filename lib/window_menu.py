import pygame
import variables as v
import button
import colors as c
import window_hvsh, window_hvsc, window_cvsc, window_settings
import game as g
pygame.init()
clock = pygame.time.Clock()

 
# Welcome to hive !

# for insights of processing times use the follwing pattern to check code for its needed processing time:
#import time
#t = time.clock()
# ##code##
#print(time.clock() - t)


class Menu:
    def __init__(self, settings = {"music": False, "sound": True, "version": "basic", "mode": "hvsh", "resolution": (1152,664)}):
        self.running = False
        self.buttons = None
        self.display = None
        self.settings = settings
        self.wg = None #window game
 
    def on_init(self):
        
        #create display and set display attr
        pygame.display.init()
        self.display = pygame.display.set_mode(v.menu_size, 0, 32)
        pygame.display.set_caption("Spiel-Menue")
        self.display.fill(c.background_main_menu)
            
        #create buttons and draw them
        self.buttons = self.create_buttons()
        for button0 in self.buttons.values():
            button0.draw_button()
        
        pygame.display.update()

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            
            if self.buttons["settings"].pressed(event.pos):
                
                ws = window_settings.Window_Settings()
                ws.on_execute()
                self.running = False
                
            elif self.buttons["start_game"].pressed(event.pos):
                
                game = g.Game(self.settings)
                if self.settings["mode"] == "hvsh":
                    self.wg = window_hvsh.Window_HvsH(game)
                elif self.settings["mode"] == "hvsc":
                    self.wg = window_hvsc.Window_HvsC(game)
                elif self.settings["mode"] == "cvsc":
                    self.wg = window_cvsc.Window_CvsC(game)
                    
                self.wg.on_execute()
                self.running = False
        
            
    def on_loop(self):
        clock.tick(v.FPS)
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if not self.running:
            self.on_init()
            self.running = True
 
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            
        self.on_cleanup()
        
    def create_buttons(self):
        settings_button = button.Button(self.display, "Settings", 25, 
                                          (v.menu_x_size * 5 // 12, v.menu_y_size * 1 // 3), 
                                          (v.menu_x_size * 2 // 12, v.menu_y_size * 1 // 12),
                                          c.button_color, (0,0,0))
        
        start_game_button = button.Button(self.display, "Start Game", 25, 
                                          (v.menu_x_size * 5 // 12, v.menu_y_size * 2 // 3), 
                                          (v.menu_x_size * 2 // 12, v.menu_y_size * 1 // 12),
                                          c.button_color, (0,0,0))
        return {"settings": settings_button, "start_game": start_game_button}



