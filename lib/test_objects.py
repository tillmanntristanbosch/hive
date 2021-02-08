import board
import player
import hexagon_stone as hs
import copy

class Test_Board(board.Board):
    
    def set_calculator(self, calculator):
        self.calculator = calculator
        
    def set_test_players(self, test_players):
        self.test_players = test_players
    
    #aim is to copy the board matrix of an board object, and also make copies of all hexagons inside the matrix
    #use copy_hexagon. input is an board object
    def copy_board(self, board): 
        
        #input is a matrix (list of lists)
        def copy_board_matrix(board_matrix):
            copied_board = {}
            for hstone in board_matrix.values():
                hexagon_copy = hs.hexagon_stone(hstone.size)
                hexagon_copy.copy_hexagon(hstone)
                copied_board[hstone.board_pos] = hexagon_copy
            return copied_board
        
        self.board = copy_board_matrix(board.board)
        self.nonempty_fields = board.nonempty_fields.copy()
        
        
        
    def copy_board2(self, board):
        return copy.deepcopy(board)
    
    #this function evaluates and executes a potential stone put. input is the player and both clicked hexagons, 
    #first the hexagon at the side, second a hexagon on the board   
    def execute_stone_put(self, player, fhex, shex):
        
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
        self.board[draw_hexagon.board_pos] = draw_hexagon
        self.nonempty_fields.append(draw_hexagon.board_pos)
        #set is_on_board
        draw_hexagon.is_on_board = True
        
    #this function evaluates and executes a potential stone move on ground. input is the player and both clicked hexagons, 
    #first the hexagon where a stone wants to be moved, second the hexagon the stone wants to be moved to
    def execute_stone_move(self, player, fhex, shex):
        
        old_board_pos = fhex.board_pos
        old_pixel_pos = fhex.pixel_pos
        fhex.set_board_pos(shex.board_pos)
        fhex.set_pixel_pos(shex.pixel_pos)
        #refill "old" place with empty stone
        new_empty_stone = hs.hexagon_stone(fhex.size)
        new_empty_stone.set_pixel_pos(old_pixel_pos)
        new_empty_stone.set_board_pos(old_board_pos)
        self.board[old_board_pos] = new_empty_stone
        #fill "new" place with fhex
        self.board[fhex.board_pos] = fhex
        #actualize board.nonempty_fields
        self.nonempty_fields.append(fhex.board_pos)
        self.nonempty_fields.remove(old_board_pos)
            
        
    #player wants to move the bug fhex onto a nonempty stone shex, or bug is already on a nonempty stone
    #and wants to fall down onto an empty field
    def move_bug_on_nonempty_stone(self, player, fhex, shex):
        
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
                self.nonempty_fields.append(fhex.board_pos)
            last_stone.has_bug_on = False
            #check whether fhex is mosquito. if it is and shex.is_empty then reput "mosquito" type
            if fhex.is_mosquito and shex.is_empty: fhex.type = "mosquito"
            #refill old place with last_stone and new place with fhex
            self.board[old_board_pos] = last_stone
            self.board[fhex.board_pos] = fhex
            #no adaptation for nonempty_fields needed
            
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
            self.board[old_board_pos] = new_empty_stone
            #fill "new" place with fhex
            self.board[fhex.board_pos] = fhex
            #actualize board.nonempty_fields
            self.nonempty_fields.remove(old_board_pos)
            
                
    #action like put or move, bug moves etc get executed here        
    def execute_action(self, player, fhex, shex, action_type):
        if action_type == "put":    self.execute_stone_put(player, fhex, shex)
        elif action_type == "move":
            if fhex.type in {"bug", "mosquito"}:
                if not shex.is_empty or len(fhex.underlaying_stones) > 0:   
                    self.move_bug_on_nonempty_stone(player, fhex, shex)
                else: self.execute_stone_move(player, fhex, shex)
            else: self.execute_stone_move(player, fhex, shex)
        
        for player0 in self.test_players.values():
            self.calculator.set_action_hexagons(player0)
        
class Test_Player(player.Player):
    pass

