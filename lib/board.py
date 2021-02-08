import hexagon_stone as hs

class Board:
    def __init__(self, board_size, surfaces):
        self.size = board_size
        self.surfaces = surfaces
        self.initial_hexagon_size = int(0.03 * self.surfaces["surface_full"].get_width())
        self.hexagon_size = self.initial_hexagon_size
        self.initial_draw_position = (0, -self.hexagon_size)
        self.draw_position = self.initial_draw_position #where on the surface shall the hexagon matrix be drawn ? 
        #(reference point is upper left corner of upper left hexagon)
        
        self.board = self.set_empty_hexagon_board() #quadratic matrix of hexagons
        self.set_hexagons_positions(self.board)
        
        self.nonempty_fields = [] #will contain matrix coordinates
        
        # this variable shall save past board constellations to look them up when hitting the "back" button.
        # it saves past boards in a dictionary. the keys are natural numbers representing the amount of puts or moves
        # so far done in the game, starting with 0, the values are again dicts with keys board_pos, and values the 
        #hexagon stones which layed there at this time. 
        # eg: {0: {(0,0): hstone, (0,1): hstone, ...}, 1: {(0,0): hstone, (0,1): hstone, ...}, ...}
        self.past_boards = {0: {"turn": ("white", 1)}} #init
        
    #get neighbour coordinates of (i,j) starting from top going clockwise, number them from 0 to 5
    def get_neighbours(self, coord):
        i = coord[0]
        j = coord[1]
        s = self.size
        if i % 2 == 1: return {0: ((i-2) % s,j % s), 1: ((i-1) % s,(j+1) % s), 2: ((i+1) % s,(j+1) % s), 3: ((i+2) % s,j % s), 4: ((i+1) % s,j % s), 5: ((i-1) % s,j % s)} 
        else: return {0: ((i-2) % s,j % s), 1: ((i-1) % s,j % s), 2: ((i+1) % s,j % s), 3: ((i+2) % s,j % s), 4: ((i+1) % s,(j-1) % s), 5: ((i-1) % s,(j-1) % s)} 
    
    def get_nonempty_neighbours(self, coord):
        nonempty_neigh = []
        for neigh in self.get_neighbours(coord).values():
            if not self.board[neigh].is_empty: nonempty_neigh.append(neigh)
        return nonempty_neigh
    
    def get_empty_neighbours(self, coord):
        return [neigh for neigh in self.get_neighbours(coord).values() if neigh not in self.get_nonempty_neighbours(coord)]
    
    #create a quadratic board of hexagons as a matrix of hexagon objects with respective correct positions    
    def set_empty_hexagon_board(self):
        hexagon_board = {}
        for i in range(self.size):
            for j in range(self.size):
                hexagon_board[(i,j)] = hs.hexagon_stone(self.hexagon_size)
                hexagon_board[(i,j)].set_board_pos((i,j))
        return hexagon_board
        
    #calculate the pixel_pos of all hexagons in board and empty_board with given self.draw_position (pixel_pos of top left hexagon)
    def set_hexagons_positions(self, board):
        even_numbers = [i for i in range(self.size) if i % 2 == 0]
        odd_numbers = [i for i in range(self.size) if i % 2 == 1]
        for i in even_numbers:
            position = (self.draw_position[0], self.draw_position[1] + i/2 * 3**(1/2) * self.hexagon_size)
            for k in range(self.size):
                hstone = board[(i,k)]
                hstone.set_pixel_pos((position[0] + k * 3 * self.hexagon_size, position[1]))
                if hstone.type == "bug":
                    for stone in hstone.underlaying_stones: stone.set_pixel_pos((position[0] + k * 3 * self.hexagon_size, position[1]))
        for i in odd_numbers:
            start_position = (self.draw_position[0] + 3/2 * self.hexagon_size, self.draw_position[1] + 3**(1/2)/2 * self.hexagon_size)
            position = (start_position[0], start_position[1] + (i-1)/2 * 3**(1/2) * self.hexagon_size)
            for k in range(self.size):
                hstone = board[(i,k)]
                hstone.set_pixel_pos((position[0] + k * 3 * self.hexagon_size, position[1]))
                if hstone.type == "bug":
                    for stone in hstone.underlaying_stones: stone.set_pixel_pos((position[0] + k * 3 * self.hexagon_size, position[1]))
    
    
    #check whether a scroll on event_pos is inside the whole hexagon board or not    
    def scroll_is_inside_board(self, event_pos):
        for hstone in self.board.values():
            if hstone.point_in_hexagon(event_pos):   return True
        return False
    




















