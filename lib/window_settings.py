import pygame
import variables as v
import button
import colors as c
import painter as pt
import window_menu as menu
import sound_maker as sm
pygame.init()
clock = pygame.time.Clock()

 
class Window_Settings:
    def __init__(self):
        self.running = False
        self.buttons = None
        self.display = None             #surface
        self.values = {"music":False, "sound":True, "version":"basic", "mode":"hvsh", "resolution":(1152, 664)}
 
    def on_init(self):
        
        #create display and set display attr
        pygame.display.init()
        self.display = pygame.display.set_mode(v.menu_size, 0, 32)
        pygame.display.set_caption("Einstellungen")
        self.display.fill((50,50,200))
        
        #create buttons and draw them
        self.buttons = self.create_buttons()
        for button0 in self.buttons.values():
            button0.draw_button()
        pt.Painter().write_text(self.display, "Settings", 50, (255,255,255), (v.menu_x_size * 0.42, v.menu_y_size * 0.05))
        
        pt.Painter().write_text(self.display, "music:", 25, (255,255,255), (v.menu_x_size * 0.1, v.menu_y_size * 0.25))
        pt.Painter().write_text(self.display, "sound:", 25, (255,255,255), (v.menu_x_size * 0.5, v.menu_y_size * 0.25))
        pt.Painter().write_text(self.display, "version:", 25, (255,255,255), (v.menu_x_size * 0.1, v.menu_y_size * 0.5))
        pt.Painter().write_text(self.display, "mode:", 25, (255,255,255), (v.menu_x_size * 0.5, v.menu_y_size * 0.5))
        pt.Painter().write_text(self.display, "resolution:", 25, (255,255,255), (v.menu_x_size * 0.35, v.menu_y_size * 0.75))
        pygame.display.update()

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.buttons["back_button"].pressed(event.pos):
                men = menu.Menu(self.values)
                men.on_execute()
                self.running = False
            if self.buttons["musicOn_button"].pressed(event.pos):
                self.values["music"] = True
                sm.sound_maker(music = self.values["music"], sound = self.values["sound"]).play_music()
            elif self.buttons["musicOff_button"].pressed(event.pos):
                self.values["music"] = False
                pygame.mixer.music.stop()
            elif self.buttons["soundOn_button"].pressed(event.pos):
                self.values["sound"] = True
            elif self.buttons["soundOff_button"].pressed(event.pos):
                self.values["sound"] = False
            elif self.buttons["basic_button"].pressed(event.pos):
                self.values["version"] = "basic"
            elif self.buttons["extended_button"].pressed(event.pos):
                self.values["version"] = "extended"
            elif self.buttons["hvsh_button"].pressed(event.pos):
                self.values["mode"] = "hvsh"
            elif self.buttons["hvsc_button"].pressed(event.pos):
                self.values["mode"] = "hvsc"
            elif self.buttons["cvsc_button"].pressed(event.pos):
                self.values["mode"] = "cvsc"
            elif self.buttons["resolution1_button"].pressed(event.pos):
                self.values["resolution"] = (800,600)
            elif self.buttons["resolution2_button"].pressed(event.pos):
                self.values["resolution"] = (1152,664)
            elif self.buttons["resolution3_button"].pressed(event.pos):
                self.values["resolution"] = (1920,1280)
        clock.tick(v.FPS)
            
    def on_loop(self):
        pass
    def on_render(self):
        pass
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
            self.on_render()
        self.on_cleanup()
        
    def create_buttons(self):
        musicOn_button = button.Button(self.display, "on", 20, 
                                          (v.menu_x_size * 0.175, v.menu_y_size * 0.25), 
                                          (v.button_x_size*0.25, v.button_y_size*0.25),
                                          (255,255,255), (0,0,0))
        
        musicOff_button = button.Button(self.display, "off", 20, 
                                             (v.menu_x_size * 0.25, v.menu_y_size * 0.25), 
                                             (v.button_x_size*0.25, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        soundOn_button = button.Button(self.display, "on", 20, 
                                          (v.menu_x_size * 0.575, v.menu_y_size * 0.25), 
                                          (v.button_x_size*0.25, v.button_y_size*0.25),
                                          (255,255,255), (0,0,0))
        
        soundOff_button = button.Button(self.display, "off", 20, 
                                             (v.menu_x_size * 0.65, v.menu_y_size * 0.25), 
                                             (v.button_x_size*0.25, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        basic_button = button.Button(self.display, "basic", 20, 
                                          (v.menu_x_size * 0.19, v.menu_y_size * 0.5), 
                                          (v.button_x_size*0.4, v.button_y_size*0.25),
                                          (255,255,255), (0,0,0))
        extended_button = button.Button(self.display, "extended", 19, 
                                             (v.menu_x_size * 0.29, v.menu_y_size * 0.5), 
                                             (v.button_x_size*0.5, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        hvsh_button = button.Button(self.display, "h vs. h", 20, 
                                             (v.menu_x_size * 0.575, v.menu_y_size * 0.5), 
                                             (v.button_x_size*0.5, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        hvsc_button = button.Button(self.display, "h vs. c", 20, 
                                             (v.menu_x_size * 0.68, v.menu_y_size * 0.5), 
                                             (v.button_x_size*0.5, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        cvsc_button = button.Button(self.display, "c vs. c", 20, 
                                             (v.menu_x_size * 0.785, v.menu_y_size * 0.5), 
                                             (v.button_x_size*0.5, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        resolution1_button = button.Button(self.display, "800x600", 20, 
                                             (v.menu_x_size * 0.47, v.menu_y_size * 0.67), 
                                             (v.button_x_size*0.6, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        resolution2_button = button.Button(self.display, "1152x664", 20, 
                                             (v.menu_x_size * 0.47, v.menu_y_size * 0.75), 
                                             (v.button_x_size*0.6, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        resolution3_button = button.Button(self.display, "1920x1280", 19, 
                                             (v.menu_x_size * 0.47, v.menu_y_size * 0.83), 
                                             (v.button_x_size*0.6, v.button_y_size*0.25),
                                             (255,255,255), (0,0,0))
        back_button = button.Button(self.display, "<--Back--", 15, 
                                             (v.menu_x_size * 0.025, v.menu_y_size * 0.025), 
                                             (v.button_x_size*0.5, v.button_y_size*0.25),
                                             c.button_color, (0,0,0))
        return {"back_button": back_button, "musicOn_button": musicOn_button, "musicOff_button": musicOff_button,
                "soundOn_button": soundOn_button, "soundOff_button": soundOff_button,
                "basic_button": basic_button, "extended_button": extended_button, "hvsh_button": hvsh_button, "hvsc_button": hvsc_button, "cvsc_button": cvsc_button, "resolution1_button": resolution1_button, "resolution2_button": resolution2_button, "resolution3_button": resolution3_button}



 
if __name__ == "__main__" :
    window_pregame = Window_Settings()
    window_pregame.on_execute()