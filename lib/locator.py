import test_objects as test
import calculator as cal

#A locator object corresponds to a board and and saves stones the locator is or was looking at in the past in 
#a dict .locations (init with key = 0, and value = the stone in the middle of the board and its coordinate)
#note that the values of locations shall represent the location the locator was on, which consists of the stone 
#and its coordinate the moment the locator landed on this stone. it may happen that the stones coordinate
#changes with time, but the coordinate which gets saved in locator is (should be) fixed and gives the information
#of the "location" of the locator. 
#note that empty fields formally have a stone of type "empty" on it.  
#the maximum number of stones the locator is saving in .locations is set by int .look_into_past 
#to create a locator board and players have to be given, then a test_board and test_players are 
#set to give the possibility to test out moves etc
class Locator:
    def __init__(self, board, look_into_past):
        #board, test_board and players
        self.board = board #this is a Board object
        
        self.test_board = test.Test_Board(self.board.size, self.board.surfaces)
        
        self.look_into_past = look_into_past
        
        self.initial_stone = self.board.board[(round(self.board.size / 2),round(self.board.size / 2))]
        self.locations = {0: (self.initial_stone, self.initial_stone.board_pos)} #potential error source
        self.new_key = 1
    
    #move locator to position coord, add the stone there to the locator. 
    #.new_key will always go up by one, to generally count the number of stones in total the locator
    #has been looking at since created, and to not have double keys accidently 
    #note, that you have to give the board on which the locator shall move its position (board or test_board), 
    #it then may land on a different stone
    def move_to_position(self, coord, which_board):
        if self.get_position()[1] != coord:
            stone = which_board.board[coord[0]][coord[1]]
            if len(self.locations) == self.look_into_past:
                self.remove_stone()
            new_coord = stone.board_pos
            self.locations[self.new_key] = (stone, new_coord) #add stone and position with key new_key 
            self.new_key += 1
    
    #get actual position, return stone
    def get_position(self):
        return self.locations[self.new_key - 1]
    
    #remove stone with lowest key
    def remove_stone(self):
        self.locations.__delitem__(min(self.locations.keys()))
        
    #clear locations and initialize as in __init__, set new_key to 1
    def clear_stones(self):
        self.locations = {0: (self.initial_stone, self.initial_stone.board_pos)}
        self.new_key = 1
        
    
    




