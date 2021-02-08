import pygame
import texts as t
import hexagon_stone as hs
pygame.init()


class Interactor:
    def __init__(self, painter, calculator, turn, buttons, sound_maker):
        self.painter = painter
        self.calculator = calculator
        self.players = self.calculator.players
        self.board = self.calculator.board
        self.surfaces = self.board.surfaces
        self.turn = turn
        self.buttons = buttons
        self.sound_maker = sound_maker
    
    #board pixel size wants to be adapted with this function. multiply ratio with stone_size
    def scale_board(self, ratio):
        #scale board attributes
        for hstone in self.board.board.values():
            hstone.size = int(ratio * hstone.size)
        #scale player attributes
        for player in self.players.values():
            for hstone in player.stones_list:
                if not hstone.is_on_board or hstone.has_bug_on:  hstone.size = int(ratio * hstone.size)
        self.board.hexagon_size = int(ratio * self.board.hexagon_size)
        self.board.set_hexagons_positions(self.board.board)
    
    def translate_board(self, offset):
        self.board.draw_position = (self.board.draw_position[0] + offset[0], self.board.draw_position[1] + offset[1])
        self.board.set_hexagons_positions(self.board.board)
    
    #this function evaluates and executes a potential stone put. input is the player and both clicked hexagons, 
    #first the hexagon at the side, second a hexagon on the board   
    def execute_stone_put(self, player, fhex, shex):
        cond1, cond2 = True, True
        if self.turn[1] >= 2:
            possible_put_fields = self.calculator.get_possible_put_fields(fhex.color)
            cond1 = self.put_stone_condition(player, fhex, shex)
            cond2 = shex.board_pos in possible_put_fields
            
        if cond1 and cond2:
            ##first execute logical aspects
            stone_type = fhex.type
            #find stone in player.stones which is not yet on the board
            for hstone in player.stones[stone_type].values():
                if not hstone.is_on_board:
                    draw_hexagon = hstone
                    break
            #set the corresponding side_stone_number one down
            player.side_stones_numbers[stone_type] -= 1
            #set new pixel_pos and board_pos
            draw_hexagon.set_pixel_pos(shex.pixel_pos)
            draw_hexagon.set_board_pos(shex.board_pos)
            #put the hexagon abstractly on the board at the corresponding position and adapt board attributes
            self.board.board[draw_hexagon.board_pos] = draw_hexagon
            self.board.nonempty_fields.append(draw_hexagon.board_pos)
            
            #set is_on_board
            draw_hexagon.is_on_board = True
            
            #make sound
            self.sound_maker.make_sound(stone_type)         
            
            ##then execute drawing aspects
            self.painter.draw_stone_number(player, fhex, self.surfaces)
            self.painter.draw_board(self.board, self.surfaces, self.buttons)
            self.painter.write_box_text(self.surfaces, t.insect_put_texts[fhex.type], fhex.color)
            

    #player want to put src_hstone on dir_stone. is that a legal ?
    def put_stone_condition(self, player, src_hstone, dir_hstone):
        coord = dir_hstone.board_pos
        
        #there are still stones of the src_hstone type left at the side
        cond0 = player.side_stones_numbers[src_hstone.type] != 0
        if not cond0:
            print("cond0 nicht erfüllt")
        #stone belongs to player
        cond1 = src_hstone.color == player.color 
        if not cond1:
            print("cond1 nicht erfüllt")
        #field at coord is empty
        cond3 = self.board.board[coord].is_empty 
        if not cond3:
            print("cond3 nicht erfüllt")
        #at least one same color neighbour, no other color neighbour.
        #watch the cases, that no or just one stone is on the board
        cond4 = False
        neighbours = self.board.get_neighbours(coord).values()
        if len(self.board.nonempty_fields) == 0:
            cond4 = True
        elif len(self.board.nonempty_fields) == 1:
            cond4 = coord in neighbours
        else:
            for neigh in neighbours:
                field = self.board.board[neigh]
                if not field.is_empty:
                    if field.color != src_hstone.color:
                        cond4 = False
                        break
                    else:
                        cond4 = True
        if not cond4:
            print("cond4 nicht erfüllt")
        #bee has been put until 4. stoneput
        cond5 = True
        if self.turn[1] == 4 and not player.stones["bee"].values()[0].is_on_board:
            cond5 = src_hstone.type == "bee"
        if not cond5:
            print("cond5 nicht erfüllt")
        return cond0 and cond1 and cond3  and cond4 and cond5
    
    
    
    #this function evaluates and executes a potential stone move on ground. input is the player and both clicked hexagons, 
    #first the hexagon where a stone wants to be moved, second the hexagon the stone wants to be moved to
    def execute_stone_move(self, player, fhex, shex):
        
        cond1 = self.move_stone_condition(player, fhex, shex)
        cond2 = shex.board_pos in self.calculator.get_possible_move_fields(fhex)
        if cond1 and cond2: 
            
            old_board_pos = fhex.board_pos
            old_pixel_pos = fhex.pixel_pos
            fhex.set_board_pos(shex.board_pos)
            fhex.set_pixel_pos(shex.pixel_pos)
            
            #refill "old" place with empty stone
            new_empty_stone = hs.hexagon_stone(fhex.size)
            new_empty_stone.set_pixel_pos(old_pixel_pos)
            new_empty_stone.set_board_pos(old_board_pos)
            self.board.board[old_board_pos] = new_empty_stone
            
            #fill "new" place with fhex
            self.board.board[fhex.board_pos] = fhex
            
            #actualize board.nonempty_fields
            self.board.nonempty_fields.append(fhex.board_pos)
            self.board.nonempty_fields.remove(old_board_pos)
            
            #make sound
            self.sound_maker.make_sound(fhex.type)
            
            self.painter.draw_board(self.board, self.surfaces, self.buttons)
            #write texts
            self.painter.write_box_text(self.surfaces, t.insect_move_texts[fhex.type], fhex.color)
            
            
    #player wants to move fhex to shex. is that generally possible ? that means independently of 
    #the stone type ? note that this game is yet without the "assel" stone    
    def move_stone_condition(self, player, fhex, shex):
        #different board_pos
        cond00 = fhex.board_pos != shex.board_pos
        #bee is on board
        cond0 = list(player.stones["bee"].values())[0].is_on_board
        #stone belongs to player
        cond1 = fhex.color == player.color
        #stone is on board
        cond2 = fhex.is_on_board
        #coord is empty (just for stone.type != "bug")
        cond3 = True
        if not fhex.type in {"bug", "mosquito"}:
            cond3 = shex.is_empty 
        return cond00 and cond0 and cond1 and cond2 and cond3
    
    

    #player wants to move the bug fhex onto a nonempty stone shex, or bug is already on a nonempty stone
    #and wants to fall down onto an empty field
    def move_bug_on_nonempty_stone(self, player, fhex, shex):
        
        cond1 = self.move_stone_condition(player, fhex, shex)
        cond2 = shex.board_pos in self.calculator.get_possible_move_fields(fhex)
        if cond1 and cond2: 
            
            old_board_pos = fhex.board_pos
            old_pixel_pos = fhex.pixel_pos
            fhex.set_board_pos(shex.board_pos)
            fhex.set_pixel_pos(shex.pixel_pos)
            
            if fhex.underlaying_stones: #case: fhex sits on at least one stone
                #get stone which lies directly under the bug
                last_stone = fhex.underlaying_stones[-1]
                fhex.underlaying_stones.clear()
                #define new stones under the bug
                if shex.type == "bug":
                    fhex.underlaying_stones = shex.underlaying_stones.copy()
                if not shex.is_empty:
                    fhex.underlaying_stones.append(shex)
                    shex.has_bug_on = True
                if shex.is_empty:
                    self.board.nonempty_fields.append(fhex.board_pos)
                last_stone.has_bug_on = False
                #check whether fhex is mosquito. if it is and shex.is_empty then reput "mosquito" type
                if fhex.is_mosquito and shex.is_empty: fhex.type = "mosquito"
                #refill old place with last_stone and new place with fhex
                self.board.board[old_board_pos] = last_stone
                self.board.board[fhex.board_pos] = fhex
                #no adaptation for nonempty_fields needed
                
                #make sound
                self.sound_maker.make_sound(fhex.type)
                
                #draw last_stone and fhex 
                self.painter.draw_board(self.board, self.surfaces, self.buttons)
                
               
            else: #case: bug will certainly move from an empty field onto a nonempty field
                if shex.type == "bug":
                    fhex.underlaying_stones = shex.underlaying_stones.copy()
                fhex.underlaying_stones.append(shex)
                shex.has_bug_on = True
                #check mosquito.
                if fhex.is_mosquito: fhex.type = "bug"
                #refill "old" place with empty stone
                new_empty_stone = hs.hexagon_stone(fhex.size)
                new_empty_stone.set_pixel_pos(old_pixel_pos)
                new_empty_stone.set_board_pos(old_board_pos)
                self.board.board[old_board_pos] = new_empty_stone
                
                #fill "new" place with fhex
                self.board.board[fhex.board_pos] = fhex
                
                #actualize board.nonempty_fields
                self.board.nonempty_fields.remove(old_board_pos)
                
                #make sound
                self.sound_maker.make_sound(fhex.type)
                
                self.painter.draw_board(self.board, self.surfaces, self.buttons)
                
    #add actual board constellation to the past_boards dict
    #save the ids of hexagon stones
    def add_board_constellation(self):
        new_board = {}
        for i in range(self.board.size):
            for j in range(self.board.size):
                hstone  = self.board.board[(i,j)]
                if not hstone.is_empty:
                    entry = [hstone]
                    if hstone.type in {"bug", "mosquito"}:
                        try_list = hstone.underlaying_stones.copy()
                        try_list.reverse()
                        for stone in try_list:
                            entry.append(stone)
                    new_board[(i,j)] = entry
        self.board.past_boards[len(self.board.past_boards)] = new_board
    
    #this function puts the board into some constellation of past_boards, tm put the stones to the positions
    #as refered in the given constellation and reorganize underlaying_stones and stone attributes  
    def put_into_constellation(self, constellation):
        
        constellation = constellation.copy()
        del constellation["turn"]
        
        #make board empty 
        self.board.board = self.board.set_empty_hexagon_board()
        self.board.set_hexagons_positions(self.board.board)
        self.board.nonempty_fields.clear()
        
        #reset all player stones
        #for all stones of the players which do not appear in the constellation, reset their attributes
        #back to not being on the board
        for player in self.players.values():
            for hstone in player.stones_list:
                if hstone.is_on_board:
                    self.reset_stone_attr(hstone)
            for hstone in player.side_stones.values():
                hstone.is_marked = False
        
        #set new hexagons laying on the board, and underlaying_stones 
        for coord in constellation:
            stone_list = constellation[coord]
            k = len(stone_list)
            ref_stone = self.board.board[coord]
            highest_stone = stone_list[0]
            self.board.board[coord] = highest_stone
            self.board.nonempty_fields.append(coord)
            self.set_stone_attr(highest_stone, ref_stone.board_pos, ref_stone.pixel_pos)
            
            for i in range(k-1): #only interesting for the case k > 1 (bug or mosquito)
                hstone = stone_list[i]
                for j in range(i+1, k):
                    stone = stone_list[j]
                    hstone.underlaying_stones.append(stone)
                    self.set_stone_attr(stone, ref_stone.board_pos, ref_stone.pixel_pos)
                    stone.has_bug_on = True
        
        #drawing aspect
        for player in self.players.values():
            player.set_side_stones_numbers()
            self.painter.draw_unmarked_side_area(player, self.surfaces)  
        self.painter.draw_board(self.board, self.surfaces, self.buttons)  
        
    
    #reset a player stone into a stone not being on the board
    def reset_stone_attr(self, hstone):
        del hstone.board_pos
        del hstone.pixel_pos
        del hstone.points
        del hstone.drawn_surface
        hstone.is_on_board = False
        hstone.has_bug_on = False
        hstone.is_drawn = False
        hstone.is_marked = False
        if hstone.type in {"bug", "mosquito"}:
            hstone.underlaying_stones.clear()
        if hstone.is_mosquito:
            hstone.type = "mosquito"
            
    #set stone attr of hstone as following 
    def set_stone_attr(self, hstone, board_pos, pixel_pos):
        hstone.set_board_pos(board_pos)
        hstone.set_pixel_pos(pixel_pos)
        hstone.set_drawn_surface(self.surfaces["surface_board"])
        hstone.is_on_board = True
        hstone.has_bug_on = False
        hstone.is_marked = False
        if hstone.type in {"bug", "mosquito"}:
            hstone.underlaying_stones = []
    
    #restart game, tm reset all attr to as they where at the beginning        
    def restart_game(self):
        #reset board:
        self.board.hexagon_size = self.board.initial_hexagon_size
        self.board.draw_position = self.board.initial_draw_position
        self.board.board = self.board.set_empty_hexagon_board()
        self.board.set_hexagons_positions(self.board.board)
        self.board.nonempty_fields.clear()
        self.board.past_boards = {0: {"turn": ("white", 1)}}
        
        #reset players:
        for player in self.players.values():
            player.stone_size = player.initial_stone_size
            #reset stones
            for stones in player.stones.values():
                for stone in stones.values():
                    stone.size = player.stone_size
                    if stone.is_mosquito: stone.type = "mosquito"
                    if stone.type in {"bug", "mosquito"}:
                        stone.underlaying_stones.clear()
                    if stone.is_on_board:
                        del stone.board_pos
                        del stone.points
                        del stone.pixel_pos
                    if stone.is_drawn:
                        del stone.drawn_surface
                    stone.is_on_board = False
                    stone.is_drawn = False
                    stone.is_marked = False
                    stone.has_bug_on = False
            player.side_stones_numbers = player.initial_side_stones_numbers.copy()
            player.moveable_hexagons.clear()
            player.putable_hexagons = list(player.side_stones.values()).copy()
            player.can_act = True
            
        #drawing aspect
        for player in self.players.values():
            self.painter.draw_unmarked_side_area(player, self.surfaces)  
        self.painter.draw_board(self.board, self.surfaces, self.buttons) 
            
    #its turn of player_color, print bee reminder for the opposite color if its bee is not put yet 
    def bee_reminder(self, player_color, game):
        opp_color = [color for color in ["white", "black"] if color != player_color].pop()
        if not game.players[opp_color].stones["bee"][1].is_on_board:
            game.painter.write_box_text(game.surfaces, t.bee_reminder, opp_color)
    

    #action like put or move, bug moves etc get executed here        
    def execute_action(self, player, fhex, shex, action_type):
        if action_type == "put":    self.execute_stone_put(player, fhex, shex)
        elif action_type == "move":
            if fhex.type in {"bug", "mosquito"}:
                if not shex.is_empty or len(fhex.underlaying_stones) > 0:   
                    self.move_bug_on_nonempty_stone(player, fhex, shex)
                else: self.execute_stone_move(player, fhex, shex)
            else: self.execute_stone_move(player, fhex, shex)
        
        #save board constellation
        self.add_board_constellation()
        
        #set action hexagons of players (moveable and putable hexagons)
        for player0 in self.players.values():
            self.calculator.set_action_hexagons(player0)
    







# ending