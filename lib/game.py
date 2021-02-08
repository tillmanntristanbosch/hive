import board
import player as plh
import player_extended as ple
import player_computer as plc
import locator
import calculator_extended as cal_ex
import interactor
import painter
import pygame
import button
import colors as c
import backgrounds as bg
import computer_action as ca
import sound_maker as sm
import copy



class Game:
    def __init__(self, settings = {"music": False, "sound": True, "version": "basic", "mode": "hvsh", "resolution": (1152,864)}):
        self.board_size = 30
        self.turn = ("white", 1)
        self.settings = settings
        self.surface = None

    def set_surface(self, surface):
        self.surface = surface

    def set_attributes(self):
        
        if self.surface is not None:
            
            #create following attributes, when surface is set
            self.surfaces = {"surface_full": self.surface, 
                             "surface_board": self.surface.subsurface(pygame.Rect(0.1 * self.surface.get_width(), 0, 0.8 * self.surface.get_width(), 0.95 * self.surface.get_height())),
                             "surface_stones": {"white": self.surface.subsurface(pygame.Rect(0, 0, 0.1 * self.surface.get_width(), 0.95 * self.surface.get_height())),
                                                "black": self.surface.subsurface(pygame.Rect(0.9 * self.surface.get_width(), 0, 0.1 * self.surface.get_width(), 0.95 * self.surface.get_height()))},
                             "surface_text": {"white": self.surface.subsurface(pygame.Rect(0, 0.95 * self.surface.get_height(), 0.5 * self.surface.get_width(), 0.05 * self.surface.get_height())),
                                              "black": self.surface.subsurface(pygame.Rect(0.5 * self.surface.get_width(), 0.95 * self.surface.get_height(), 0.5 * self.surface.get_width(), 0.05 * self.surface.get_height()))},
                             "surface_menu": self.surface.subsurface(pygame.Rect(1/3 * self.surface.get_width(), 1/3 * self.surface.get_height(), 1/3 * self.surface.get_width(), 1/3 * self.surface.get_height()))}
            
            #the following building of backgrounds takes very long, as tickled color backgrounds are live calculated (random ect, see in backgrounds)
#            self.backgrounds = {self.surfaces["surface_board"]: bg.tickled_color(self.surfaces["surface_board"], c.background_color2, c.background_color3),
#                                self.surfaces["surface_stones"]["white"]: bg.standard_color(self.surfaces["surface_stones"]["white"], c.background_side_stones),
#                                self.surfaces["surface_stones"]["black"]: bg.standard_color(self.surfaces["surface_stones"]["black"], c.background_side_stones),
#                                self.surfaces["surface_text"]["white"]: bg.standard_color(self.surfaces["surface_text"]["white"], c.background_text_box),
#                                self.surfaces["surface_text"]["black"]: bg.standard_color(self.surfaces["surface_text"]["black"], c.background_text_box)}
            self.backgrounds = None
            
            self.painter = painter.Painter(self.backgrounds)
            self.board = board.Board(self.board_size, self.surfaces)
            self.locator = locator.Locator(self.board, 100)
            self.buttons = self.create_buttons()
            
            #create sound_maker, players and interactor according to settings
            self.sound_maker = sm.sound_maker(sound = self.settings["sound"], music = self.settings["music"])
            if self.settings["mode"] == "hvsh":
                if self.settings["version"] == "basic":
                    self.players = {"white": plh.Human_Player("white", self.surfaces), "black": plh.Human_Player("black", self.surfaces)}
                    self.interactor = interactor.Interactor(self.painter, cal_ex.Calculator_Extended(self.locator, self.players), self.turn, self.buttons, self.sound_maker)
                elif self.settings["version"] == "extended":
                    self.players = {"white": ple.Human_Player_Extended("white", self.surfaces), "black": ple.Human_Player_Extended("black", self.surfaces)}
                    self.interactor = interactor.Interactor(self.painter, cal_ex.Calculator_Extended(self.locator, self.players), self.turn, self.buttons, self.sound_maker)
            elif self.settings["mode"] == "hvsc":
                if self.settings["version"] == "basic":
                    self.players = {"white": plh.Human_Player("white", self.surfaces), "black": plc.Computer_Player("black", self.surfaces)}
                    self.com_action = ca.Computer_Action(self.locator, self.players)
                    self.calculator = cal_ex.Calculator_Extended(self.locator, self.players)
                    self.interactor = interactor.Interactor(self.painter, self.calculator, self.turn, self.buttons, self.sound_maker)
                elif self.settings["version"] == "extended":
                    self.players = {"white": ple.Human_Player_Extended("white", self.surfaces), "black": plc.Computer_Player_Extended("black", self.surfaces)}
                    self.com_action = ca.Computer_Action(self.locator, self.players)
                    self.calculator = cal_ex.Calculator_Extended(self.locator, self.players)
                    self.interactor = interactor.Interactor(self.painter, self.calculator, self.turn, self.buttons, self.sound_maker)
            elif self.settings["mode"] == "cvsc":
                if self.settings["version"] == "basic":
                    self.players = {"white": plc.Computer_Player("white", self.surfaces), "black": plc.Computer_Player("black", self.surfaces)}
                    self.calculator = cal_ex.Calculator_Extended(self.locator, self.players)
                    self.interactor = interactor.Interactor(self.painter, self.calculator, self.turn, self.buttons, self.sound_maker)
                    self.com_action = {"white": ca.Computer_Action(self.locator, self.players, "white"),
                                       "black": ca.Computer_Action(self.locator, self.players, "black")}
                elif self.settings["version"] == "extended":
                    self.players = {"white": plc.Computer_Player_Extended("white", self.surfaces), "black": plc.Computer_Player_Extended("black", self.surfaces)}
                    self.calculator = cal_ex.Calculator_Extended(self.locator, self.players)
                    self.interactor = interactor.Interactor(self.painter, self.calculator, self.turn, self.buttons, self.sound_maker) 
                    self.com_action = {"white": ca.Computer_Action(self.locator, self.players, "white"),
                                       "black": ca.Computer_Action(self.locator, self.players, "black")}
        
    def turn_up(self):
        if self.turn[0] == "white": self.turn = ("black", self.turn[1])
        else:   self.turn = ("white", self.turn[1] + 1)
        self.board.past_boards[len(self.board.past_boards) - 1]["turn"] = self.turn #save the new turn in the actual board constellation
        
    def create_buttons(self):
        center_button = button.Button(self.surfaces["surface_board"], "center",
                                      int(1/30 * self.surfaces["surface_board"].get_height()),
                                      (int(4/9 * self.surfaces["surface_board"].get_width()), int(12/13 * self.surfaces["surface_board"].get_height())),
                                      (int(1/9 * self.surfaces["surface_board"].get_width()), int(1/20 * self.surfaces["surface_board"].get_height())),
                                      c.center_button_color, (0,0,0))
        back_button = button.Button(self.surfaces["surface_board"], "back",
                                      int(1/30 * self.surfaces["surface_board"].get_height()),
                                      (int(1/9 * self.surfaces["surface_board"].get_width()), int(12/13 * self.surfaces["surface_board"].get_height())),
                                      (int(1/9 * self.surfaces["surface_board"].get_width()), int(1/20 * self.surfaces["surface_board"].get_height())),
                                      c.center_button_color, (0,0,0))
        restart_button = button.Button(self.surfaces["surface_board"], "restart",
                                      int(1/30 * self.surfaces["surface_board"].get_height()),
                                      (int(7/9 * self.surfaces["surface_board"].get_width()), int(12/13 * self.surfaces["surface_board"].get_height())),
                                      (int(1/9 * self.surfaces["surface_board"].get_width()), int(1/20 * self.surfaces["surface_board"].get_height())),
                                      c.center_button_color, (0,0,0))
        menu_button = button.Button(self.surfaces["surface_board"], "menu",
                                      int(1/30 * self.surfaces["surface_board"].get_height()),
                                      (int(1/18 * self.surfaces["surface_board"].get_width()), int(1/18 * self.surfaces["surface_board"].get_height())),
                                      (int(1/14 * self.surfaces["surface_board"].get_width()), int(1/20 * self.surfaces["surface_board"].get_height())),
                                      c.center_button_color, (0,0,0))
        back_to_menu_button = button.Button(self.surfaces["surface_menu"], "back to menu",
                                      int(1/20 * self.surfaces["surface_menu"].get_height()),
                                      (int(1/4 * self.surfaces["surface_menu"].get_width()), int(3/5 * self.surfaces["surface_menu"].get_height())),
                                      (int(2/4 * self.surfaces["surface_menu"].get_width()), int(1/5 * self.surfaces["surface_menu"].get_height())),
                                      c.center_button_color, (0,0,0), shall_be_seen = False)
        continue_game_button = button.Button(self.surfaces["surface_menu"], "continue game",
                                      int(1/20 * self.surfaces["surface_menu"].get_height()),
                                      (int(1/4 * self.surfaces["surface_menu"].get_width()), int(1/5 * self.surfaces["surface_menu"].get_height())),
                                      (int(2/4 * self.surfaces["surface_menu"].get_width()), int(1/5 * self.surfaces["surface_menu"].get_height())),
                                      c.center_button_color, (0,0,0), shall_be_seen = False)
        return {"center_button": center_button, "back_button": back_button, "restart_button": restart_button, "menu_button": menu_button,
                "back_to_menu_button": back_to_menu_button, "continue_game_button": continue_game_button}
        
        







