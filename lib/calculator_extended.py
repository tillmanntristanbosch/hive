import calculator


#NOTE: calculator_extended has players as attr and can calculate player depending things
class Calculator_Extended(calculator.Calculator):
    
    def __init__(self, locator, players):
        super().__init__(locator)
        self.players = players
        
    #define winning condition: player wins if opposite bee is surrounded
    def winning_condition(self, color):
        if color == "white":    opp_color = "black"
        else:   opp_color = "white"
        color_bee = list(self.players[color].stones["bee"].values())[0]
        opp_color_bee = list(self.players[opp_color].stones["bee"].values())[0]
        color_bee_surr = False
        opp_color_bee_surr = False
        if color_bee.is_on_board:   
            color_bee_surr = True
            for neigh in self.board.get_neighbours(color_bee.board_pos).values():
                if self.board.board[neigh].is_empty:   color_bee_surr = False
        if opp_color_bee.is_on_board:
            opp_color_bee_surr = True
            for neigh in self.board.get_neighbours(opp_color_bee.board_pos).values():
                if self.board.board[neigh].is_empty:   opp_color_bee_surr = False
        return [color_bee_surr, opp_color_bee_surr]
    
    #event click at event_pos. in which hexagon is it ? return is a list containing exactly one hexagon 
    #iff the clicked was in this hexagon. look for empty or nonempty hexagons on the board, and for side_stones                
    def get_clicked_hexagon(self, event_pos):
        #look for both players
        for player in self.players.values():
            #look in player.side_stones for a clicked hexagon
            for hstone in player.side_stones.values():
                if hstone.point_in_hexagon(event_pos):
                    return hstone
            #look in player.stones for a clicked hexagon
            for hstone1 in player.stones.values():
                for hstone2 in hstone1.values():
                    if hstone2.is_drawn and not hstone2.has_bug_on:
                        if hstone2.point_in_hexagon(event_pos):
                            return hstone2
        #look on the board
        for hstone in self.board.board.values():
            if hstone.point_in_hexagon(event_pos):
                return hstone
        return self.empty_help_stone