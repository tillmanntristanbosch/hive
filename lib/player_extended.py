import hexagon_stone as hs
from math import sqrt

#this player has all stones, tm basic stones and mosquito, ladybug
class Player_Extended:

    def __init__(self, color, surfaces):
        self.color = color
        self.surfaces = surfaces
        self.initial_stone_size = int(0.03 * self.surfaces["surface_full"].get_width())
        self.stone_size = self.initial_stone_size
        
        self.stones = self.create_stones(self.stone_size)
        self.stones_list = self.get_stones_list() #all stones in one list
        self.side_stones = self.create_side_stones(self.stone_size)
        self.set_side_stones_positions(7) #side positions for the side stones
        #side_stone_numbers shall display how many of each insect type are not yet on the board
        self.initial_side_stones_numbers = {"bee": 1, "ant": 3, "hopper": 3, "spider": 2, "bug": 2, "mosquito": 1, "ladybug": 1}
        self.side_stones_numbers = self.initial_side_stones_numbers.copy()
        #init action hexagons (move and put)
        self.moveable_hexagons = []
        self.putable_hexagons = list(self.side_stones.values()).copy()
        self.can_act = True
        
        

    def create_stones(self, stone_size):
        hstones = {"bee": {1: hs.hexagon_stone(stone_size, "bee", 1)},
                   "ant": {1: hs.hexagon_stone(stone_size, "ant", 1),
                           2: hs.hexagon_stone(stone_size, "ant", 2),
                           3: hs.hexagon_stone(stone_size, "ant", 3)},
                   "hopper": {1: hs.hexagon_stone(stone_size, "hopper", 1),
                              2: hs.hexagon_stone(stone_size, "hopper", 2),
                              3: hs.hexagon_stone(stone_size, "hopper", 3)},
                   "spider": {1: hs.hexagon_stone(stone_size, "spider", 1),
                              2: hs.hexagon_stone(stone_size, "spider", 2)},
                   "bug": {1: hs.hexagon_stone(stone_size, "bug", 1),
                           2: hs.hexagon_stone(stone_size, "bug", 2)},
                   "mosquito": {1: hs.hexagon_stone(stone_size, "mosquito", 1)},
                   "ladybug": {1: hs.hexagon_stone(stone_size, "ladybug", 1)}}
        for hstones1 in hstones.values():
            for hstone in hstones1.values():
                hstone.set_color(self.color)
                hstone.is_empty = False
        for hstone in hstones["bug"].values():
            hstone.init_underlaying_stones() #initialize underlying stones with empty list
        #care about mosquito attributes
        hstones["mosquito"][1].init_underlaying_stones() 
        hstones["mosquito"][1].is_mosquito = True
        return hstones
    
    def create_side_stones(self, stone_size):
        hstones = {"bee": hs.hexagon_stone(stone_size, "bee"),
                "ant": hs.hexagon_stone(stone_size, "ant"),
                "hopper": hs.hexagon_stone(stone_size, "hopper"),
                "spider": hs.hexagon_stone(stone_size, "spider"),
                "bug": hs.hexagon_stone(stone_size, "bug"),
                "mosquito": hs.hexagon_stone(stone_size, "mosquito"),
                "ladybug": hs.hexagon_stone(stone_size, "ladybug")} #bug stone here does not need init underlaying stones
        for hstone in hstones.values():
            hstone.set_color(self.color)
            hstone.is_empty = False
        hstones["mosquito"].is_mosquito = True
        return hstones
    
    #calculate positions of hexagons laying at the side depending on player white or black and set them 
    #for self.stones
    def set_side_stones_positions(self, number):
        #set constants
        sqrt_3 = sqrt(3)
        surface_width = self.surfaces["surface_stones"]["white"].get_width()
        surface_height = self.surfaces["surface_stones"]["white"].get_height()
        x_distance = (surface_width * 21) // 40
        y_distance = (surface_height - number * sqrt_3 * self.stone_size) // (number + 1)
        #calculate side stones positions
        insect_positions = []
        for k in range(number):
            insect_positions.append((x_distance, (k+1) * y_distance + k * sqrt_3 * self.stone_size))
        #assign positions to side_stones
        for k in range(number):
            list(self.side_stones.values())[k].set_pixel_pos(insect_positions[k])
    
    #set the number attribute of side_stones to display how many of each insect type are not on the board
    #for example after each stone put this function has to be called
    def set_side_stones_numbers(self):
        for insect in self.stones:
            counter = 0
            for hstone in self.stones[insect].values():
                if not hstone.is_on_board:
                    counter += 1
            self.side_stones_numbers[insect] = counter
            
    def get_stones_list(self):
        stones_list = []
        for stones in self.stones.values():
            for stone in stones.values():
                stones_list.append(stone)
        return stones_list
    
    
    #at some points we need to know the set of movable and putable hexagons of a player. here we actualize them
    def set_action_hexagons(self, calculator):
        self.moveable_hexagons = calculator.get_moveable_hexagons(self.color)
        self.putable_hexagons = calculator.get_putable_hexagons(self.color, self.side_stones, self.side_stones_numbers)
        if not self.moveable_hexagons and not self.putable_hexagons: self.can_act = False
        else: self.can_act = True
    
class Human_Player_Extended(Player_Extended):
    pass


        
