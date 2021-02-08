import pygame
import texts as t
import window_methods as wm
import variables as v
import time as ti
import window_menu
pygame.init()
clock = pygame.time.Clock()

 
class Window_CvsC:
    def __init__(self, game):
        self.running = False
        self.display = None
        self.game = game
        
        self.start_game_mode = True
        
        self.game_over = False
        self.drag = False
        self.moved = False
        self.menu_open = False
        
        self.counter = None
        self.pos = None
 
    def on_init(self):
        self.display = pygame.display.set_mode(self.game.settings["resolution"])
        pygame.display.set_caption("Spielbrett")
        self.game.set_surface(self.display) 
        self.game.set_attributes()
        self.com_player1 = self.game.players["white"]
        self.com_player2 = self.game.players["black"]
        self.running = True
    
    def on_loop(self):
        
        if not self.game_over:
        
            if self.game.turn == ("white", 1):
                
                ti.sleep(2)
                
                dir_hexagon = self.game.board.board[v.first_stone_board_pos]
                first_stone = self.game.com_action["white"].choose_first_stone()
                self.game.interactor.execute_action(self.com_player1, first_stone, dir_hexagon, "put")
                self.game.turn_up()
                
            elif self.game.turn == ("black", 1):
                vec = self.game.com_action["black"].choose_first_stone()
                first_stone = vec[0]
                dir_hexagon = vec[1]
                self.game.interactor.execute_action(self.com_player2, first_stone, dir_hexagon, "put")
                self.game.turn_up()
            
            elif self.game.turn[1] > 1:
                current_player = self.game.players[self.game.turn[0]]
                
                if not current_player.can_act:
                    self.game.turn_up()
                else:
                    com_decision = self.game.com_action[current_player.color].get_action_decision()
                    self.game.interactor.execute_action(current_player, com_decision[0], com_decision[1], com_decision[2])    
                    self.game.turn_up() #set new turn    
                    self.game_over = wm.check_winner(self.game.painter, self.game.surfaces, current_player.color, self.game.interactor.calculator.winning_condition(current_player.color), self.game_over)
                    
            pygame.display.update()
            ti.sleep(v.computer_decision_time)
            
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if not self.running:
            self.on_init()
            
        while self.running:
            
            for event in pygame.event.get():
                self.on_event(event)
                pygame.display.update()
                clock.tick(v.FPS)
            
            if not self.drag and not self.menu_open:
                self.on_loop()
            
        self.on_cleanup()
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        
        if self.start_game_mode:
                        
            self.game.painter.draw_background(self.game.surfaces["surface_board"])
            self.game.painter.draw_background(self.game.surfaces["surface_stones"]["white"])
            self.game.painter.draw_background(self.game.surfaces["surface_stones"]["black"])
            self.game.painter.draw_background(self.game.surfaces["surface_text"]["white"])
            self.game.painter.draw_background(self.game.surfaces["surface_text"]["black"])

            self.game.painter.draw_set_of_hexagons(self.game.players["white"].side_stones.values(), self.game.surfaces["surface_stones"]["white"])
            self.game.painter.draw_set_of_hexagons(self.game.players["black"].side_stones.values(), self.game.surfaces["surface_stones"]["black"])
            self.game.painter.draw_all_stone_numbers(self.game.players["white"], self.game.surfaces)
            self.game.painter.draw_all_stone_numbers(self.game.players["black"], self.game.surfaces)
            
            self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons)
            
            self.game.painter.draw_ingame_frame(self.game.surfaces["surface_full"])
            
            self.start_game_mode = False 
            
            #print a text claiming that white begins
            self.game.painter.write_box_text(self.game.surfaces, t.welcome_text, "white")
            self.game.painter.write_box_text(self.game.surfaces, t.welcome_text, "black")
            
        elif not self.start_game_mode:
            
            if self.menu_open:
# menu buttons                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
                
                    if self.game.buttons["continue_game_button"].pressed(event.pos):
                        self.menu_open = False
                        self.display.blit(self.actual_full_surface, (0,0))
                        
                    elif self.game.buttons["back_to_menu_button"].pressed(event.pos):
                        window_menu.Menu().on_execute()
                        self.running = False
            
            elif not self.menu_open:
            
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if wm.point_in_surface(self.game.surfaces["surface_board"], event.pos):
                        if event.button == 1: #button 1: left mouse click
                            if not self.drag:
                                self.drag = True
                                self.pos = (event.pos, event.pos)
                                self.counter = 0
                        elif event.button == 5: #button 4: scroll in 
                            #the following if check ensures that you do not zoom to much out, as for some reason you cannot zoom in again 
                            #(why does this happen ? is there a better factor than 100 ?)
                            if self.game.board.hexagon_size > self.game.surfaces["surface_full"].get_width() // 80: 
                                ratio = 0.85 #zoom out
                                ep, dp = event.pos, self.game.board.draw_position
                                #make the event.pos the center of zooming
                                if self.game.board.scroll_is_inside_board(ep):   offset = ((1 - ratio) * (ep[0] - dp[0]), (1 - ratio) * (ep[1] - dp[1]))
                                else:   offset = (0,0)
                                self.game.interactor.scale_board(ratio)
                                self.game.interactor.translate_board(offset)
                                self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                        elif event.button == 4: #button 5: scroll out
                            ratio = 1.18 #zoom in
                            ep, dp = event.pos, self.game.board.draw_position
                            #make the event.pos the center of zooming
                            if self.game.board.scroll_is_inside_board(ep):   offset = ((1 - ratio) * (ep[0] - dp[0]), (1 - ratio) * (ep[1] - dp[1]))
                            else:   offset = (0,0)
                            self.game.interactor.scale_board(ratio)
                            self.game.interactor.translate_board(offset)
                            self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                        
                elif event.type == pygame.MOUSEMOTION and self.drag:
                    if self.counter == 2: #makes the clicking nicer (there should not be dragging, just because a click was not completely precise)
                        self.moved = True
                        self.pos = self.pos[1], event.pos #save actual and one mousepos before to always add a new draw offset from pixel to pixel
                        if wm.point_in_surface(self.game.surfaces["surface_board"], self.pos[1]):
                            self.game.interactor.translate_board((self.pos[1][0] - self.pos[0][0], self.pos[1][1] - self.pos[0][1]))
                            self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                    else: self.counter += 1
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.drag = False
                    if self.moved:   self.moved = False
                    else:
                        if self.game.buttons["center_button"].pressed(event.pos):
                            self.game.board.draw_position = self.game.board.initial_draw_position
                            self.game.interactor.scale_board(self.game.board.initial_hexagon_size / self.game.board.hexagon_size)
                            self.game.painter.draw_board(self.game.board, self.game.surfaces, self.game.buttons, v.mark_size)
                            
                        elif self.game.buttons["back_button"].pressed(event.pos):
                            if not self.game.turn == ("white", 1): 
                                del self.game.board.past_boards[len(self.game.board.past_boards) - 1]
                                last_constellation = self.game.board.past_boards[len(self.game.board.past_boards) - 1]
                                self.game.interactor.put_into_constellation(last_constellation)
                                self.game.turn = last_constellation["turn"]
                                self.game_over = False
                                
                        elif self.game.buttons["restart_button"].pressed(event.pos):
                            #at this point we could just overwrite the actual board and players with a new init board and new 
                            #players, and then init a new interactor etc (see the chronology in class self.game). But by this we do not
                            #have the same board, player and stone objects as before, which we may want in the future to analize 
                            #gaming behavour better. Therefore the self.game gets restarted by resetting all board, player and stones attr
                            #manually.
                            self.game.interactor.restart_game()
                            self.game.turn = ("white", 1)
                            self.game_over = False
                            
                        elif self.game.buttons["menu_button"].pressed(event.pos):
                            self.menu_open = True
                            self.actual_full_surface = self.display.copy()
                            self.game.painter.draw_menu(self.game.surfaces, self.game.buttons)
                        

#if __name__ == "__main__" :
#    theApp = App()
#    theApp.on_execute()
