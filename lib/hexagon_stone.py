from math import sqrt

class hexagon_stone:
    
    def __init__(self, size, stone_type = "empty", number = 1):
        
        self.type = stone_type
        self.number = number
        
        self.size = size
        self.color = ""
        
        self.is_empty = True
        self.is_on_board = False
        self.is_drawn = False
        self.is_marked = False
        
        self.has_bug_on = False
        self.is_mosquito = False
    
###setting methods    
    def set_board_pos(self, board_pos):
        self.board_pos = board_pos
        
    def set_color(self, color):
        self.color = color
    
    #hexagon gets drawn on a surface, save it here in this attribute
    def set_drawn_surface(self, surface):
        self.drawn_surface = surface
    
    #set pixel position of the hexagon. if it gets drawn, it will get drawn with these pixel positions onto
    #self.drawn_surface
    def set_pixel_pos(self, pixel_pos):
        self.pixel_pos = pixel_pos
        self.points = self.getting_hexa(self.size, self.pixel_pos)
    
    #just for bug and mosquito, shall contain all stones under the bug        
    def init_underlaying_stones(self):
        self.underlaying_stones = []
###
    
    #aim is to copy a hexagon to have the same attr, but different id    
    def copy_hexagon(self, hexagon):
        for attr in list(hexagon.__dict__.keys()):
            self.__dict__[attr] = hexagon.__dict__[attr]
    
    #calculate the six hexagon points with starting point start_vector (point top left) and side size scaling    
    def getting_hexa(self, scaling_ratio, start_vector):    
        hex_coords = [(0,0), (1,0), (1.5, 3**(1/2)/2), (1, 3**(1/2)), (0,3**(1/2)), (-0.5, 3**(1/2)/2)]
        scaled_coords = []
        for x,y in hex_coords:
            scaled_coords.append([x*scaling_ratio + start_vector[0], y*scaling_ratio + start_vector[1]])
        return scaled_coords
    
    def hexagon_center(self, hexagon_points):
        return hexagon_points[0]+((hexagon_points[1]-hexagon_points[0])*0.5, (hexagon_points[1]-hexagon_points[0])* 3**(0.5)*0.5)

    #hex_stone was drawn on subsurface, and click was on global pixel_coords. is it inside the hex_stone ? 
    def point_in_hexagon(self, event_pos):
        
        global_pixel_pos = (self.pixel_pos[0] + self.drawn_surface.get_abs_offset()[0],
                            self.pixel_pos[1] + self.drawn_surface.get_abs_offset()[1])
        points = self.getting_hexa(self.size, global_pixel_pos)
        
        def euclidean_metric(vector):
            squared = [x*x for x in vector]
            return sqrt(sum(squared))
        
        boundary_vectors = []
        connection_vectors = []
        for i in range(len(points)):
            boundary_vectors.append((points[(i+1)%len(points)][0]-points[i][0],points[(i+1)%len(points)][1]-points[i][1]))
            connection_vectors.append((event_pos[0]-points[i][0], event_pos[1]-points[i][1]))
        test = True
        angles = []
        for i in range(len(points)):
            angles.append((boundary_vectors[i][0]*connection_vectors[i][0]+boundary_vectors[i][1]*connection_vectors[i][1])
                          /(euclidean_metric(boundary_vectors[i])*euclidean_metric(connection_vectors[i])))
            if angles[i] <= -0.5:
                test = False
                
        return test
    
