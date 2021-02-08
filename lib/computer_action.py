import calculator_extended
import random
import variables as v


#this class makes calculations for a computer player. therefore expressions like opp_color or opp_player refer
#to the opponent player (human or computer)
class Computer_Action(calculator_extended.Calculator_Extended):
    def __init__(self, locator, players, color = "black"):
        super().__init__(locator, players)
        self.cplayer = self.players[color] #this com player is the player this Computer_Action object makes calculations for
        self.opp_player = self.players[[color0 for color0 in ["white", "black"] if color0 != color].pop()]
        
    random.seed()
    
    #input are the board constellations (you can find them aswell in self.calculator.board.past_boards) 
    #and the decision type (eg random, score_fct, etc)
    #return is tuple containing the hstone which wants to be moved, the direction stone it wants to be moved to
    #and the type of action (put or move)
    def get_action_decision(self, decision_type = "random"):
        
        #random computer player: decides to randomly put or move a random hstone
        if decision_type == "random":
            self.set_action_hexagons(self.cplayer)
            if self.cplayer.putable_hexagons:
                if self.cplayer.moveable_hexagons:
                    action_type = random.choice(["move", "put"])
                    if action_type == "move":
                        src_hexagon = self.random_move_hexagon(self.cplayer)
                        dir_coord = random.choice(self.get_possible_move_fields(src_hexagon))
                        dir_hexagon = self.board.board[dir_coord]
                    else:
                        src_hexagon = self.random_put_hexagon(self.cplayer)
                        dir_coord = random.choice(self.get_possible_put_fields(src_hexagon.color))
                        dir_hexagon = self.board.board[dir_coord]
                else:
                    action_type = "put"
                    src_hexagon = self.random_put_hexagon(self.cplayer)
                    dir_coord = random.choice(self.get_possible_put_fields(src_hexagon.color))
                    dir_hexagon = self.board.board[dir_coord]
            else:
                action_type = "move"
                src_hexagon = self.random_move_hexagon(self.cplayer)
                dir_coord = random.choice(self.get_possible_move_fields(src_hexagon))
                dir_hexagon = self.board.board[dir_coord]
        

        #computer player which evaluates according to a score function
        elif decision_type == "score_fct":
            pass
        
        return (src_hexagon, dir_hexagon, action_type)
    
    
    
    def random_move_hexagon(self, player):
        return random.choice(player.moveable_hexagons)
    
    def random_put_hexagon(self, player):
        put_hstone = random.choice(player.putable_hexagons)
        return player.side_stones[put_hstone.type]
    
    def random_element(self, elements):
        return random.choice(elements)
    
    def choose_first_stone(self):
        if self.cplayer.color == "white":
            return self.random_put_hexagon(self.cplayer)
        else:
            first_put_stone = self.random_element(list(self.opp_player.side_stones.values()))
            neigh_coords = self.board.get_neighbours(v.first_stone_board_pos).values()
            dir_hexagons = [self.board.board[coord] for coord in neigh_coords] #all empty neighbours of the middle hexagon
            dir_hexagon = self.random_element(dir_hexagons)
            return (first_put_stone, dir_hexagon)
    

    #move_hexagon wants to be moved to dir_coord. what is the evaluation of this turn ?
    def score_fct(self, fhex, shex, action_type):
        
        #make test_board and copy actual board_constellation
        test_board = self.locator.test_board
        test_board.copy(self.board)
        player = self.locator.test_players[fhex.color]
        test_board.execute_action(player, fhex, shex, action_type)
        
        
        ###low evaluation points
        cond0 = True
        if fhex.type == "spider" and shex.type == "bee":
            cond0 = self.get_ground_moving_distance(fhex, shex) == 3 
        
        #spider is 3 steps away from opp bee and bee would be blocked by spider move to bee +1
        #hopper is put next to own bee in the first 6 moves +1
        #opponent has few places to put stone +1
        #bug or hopper next to own bee +1/-1 (depends)
        #mosquito is moved next to only a spider -1
        
        
        ###middle evaluation points 
        #spider is blocked at own bee -1
        #opponent ant is blocked by own non-ant stone +2
        #mosquito is moved next to ant, bug or marienbug +2
        
        
        ###high evualuation points
        #bee can move out of a not anymore blocked situation +4
        #ant is blocked at own bee -3
        #spider next to opposite bee +3
        #bug is on opp bee with one possible place to put own stone +3
        #bug is on opp bee with at least two possible places to put own stone +4
        #own bee has one place left to fill, opp dangerous walking stone gets blocked by:
            #spider +700
            #hopper +600
            #bug  +500
            #marienbug  +400
            #ant +300
        #win move +1000
        pass
    
    #consider all (most) possible turns, which are the top number of turns ?
    def get_best_turns(self, number):
        pass
        
    def get_ground_moving_distance(self, fhex, shex):
        pass
    
    def is_blocked(self, fhex):
        pass
    
    