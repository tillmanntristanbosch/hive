import test_objects as to

#note that this graph objects gets the board matrix as input, and depending on the situation get set
#his points and edges
class Hexagon_Graph:
    def __init__(self, board):
        self.board = board #board object
        self.test_board = to.Test_Board(self.board.size, self.board.surfaces)
    
    def set_points(self, points):
        self.points = points
        #help structure for depth first search algorithm
        self.markings = [0] * len(self.points) 
        
    def set_edges(self, edges):
        self.edges = edges
    
    ##### points calculations
    
    #for a point in the graph calculate all connected neighbours                
    def get_graph_neighbours(self, point):
        graph_neighbours = []
        for point2 in self.points:
            if (point, point2) in self.edges:
                graph_neighbours.append(point2)
        return list(set(graph_neighbours))
    
    #intention is to move a stone from coord. return of this function is the set
    #of all empty neighbours of nonempty fields, where coord was removed from the nonempty fields, 
    #and then added to this set here
    def calculate_all_empty_neighbours(self, coord):
        points = []
        adapt_nonempty_fields = self.board.nonempty_fields.copy()
        adapt_nonempty_fields.remove(coord) #remove coord 
        for coords in adapt_nonempty_fields: #just iterate over this adapted nonempty_fields list
            for neigh in self.board.get_neighbours(coords).values():
                if self.board.board[neigh].is_empty:
                    points.append(neigh)
        points.append(coord) #as board is not empty on coord, append coord to the list here
        return list(set(points))
    
    #return all points of the connected component of point
    def calculate_connected_component(self, point):
        points = []
        self.markings = [0] * len(self.points) #reset markings
        self.depth_first_search(point) #run algo
        for k in range(len(self.points)):
            if self.markings[k] == 1:
                points.append(self.points[k])
        return list(set(points))
    #####
    
    
    ##### edges calculations
    
    #here points should be nonempty_fields of board, and edges will contain to nonempty fields, if they are neighbours 
    def calculate_standard_edges(self):
        edges = []
        for point in self.points:
            for point2 in self.points:
                if point in self.board.get_neighbours(point2).values():
                    edges.append((point, point2))
        return list(set(edges))
    
    #for spider
    #here points should be all empty neighbours of nonempty_fields, where coord was removed. 
    #edges: edge from point to point2 iff a stone can move on the ground from point to point2
    def calculate_ground_moving_edges(self, coord):
        edges = []
        #copy board into test_board
        self.test_board.copy_board(self.board)
        #remove stone at coord on test_board to calculate all moving fields correctly
        self.test_board.nonempty_fields.remove(coord)
        self.test_board.board[coord].type = "empty"
        self.test_board.board[coord].is_empty = True
        for point in self.points:
            for point2 in self.points:
                if self.can_move_to_neighbour_on_ground(point, point2, self.test_board):
                    edges.append((point, point2))
        return list(set(edges))
    
    #points and edges shall now already be calculated with calc_all_empty_neigh and calc_ground_moving_edges.
    #now we make new edges here iff there exist a three edge combination of one point to another
    def calculate_spider_move_edges(self):
        edges = []
        for src_point in self.points:
            for neigh1 in self.get_graph_neighbours(src_point):
                neighbours2 = self.get_graph_neighbours(neigh1)
                neighbours2.remove(src_point) #spider shall not go back to a coord she came from just before
                for neigh2 in neighbours2:
                    neighbours3 = self.get_graph_neighbours(neigh2)
                    neighbours3.remove(neigh1)
                    for neigh3 in neighbours3:  
                        if neigh3 != src_point: edges.append((src_point, neigh3))
        return list(set(edges))
    #####
    
    #algorithm depth-first search to check connectedness of the graph (source: internet)
    def depth_first_search(self, point):
        self.markings[self.points.index(point)] = 1
        relevant_points = [point2 for point2 in self.get_graph_neighbours(point) if self.markings[self.points.index(point2)] == 0]
        for point2 in relevant_points:  self.depth_first_search(point2)
    
    #check whether the graph is connected        
    def is_connected(self):
        if self.points:
            if len(self.calculate_connected_component(self.points[0])) == len(self.points): return True
            else: return False
        return True #if there are no points, return True
        
    #is it possible to move from coord1 to coord2 on the ground?
    #coord1 and coord2 have to be neighbour coordinates
    #helpful for all stones moving on the ground. 
    #yet this function doesnt check connectness of the board stones
    #again note that you have to give the board (board or test_board)
    #note, that coord2 does not to be empty in this function, this has to be checked elsewhere then if needed
    def can_move_to_neighbour_on_ground(self, coord1, coord2, which_board):
        nonempty_fields = which_board.nonempty_fields
        neighbours1 = list(which_board.get_neighbours(coord1).values())
        neighbours2 = list(which_board.get_neighbours(coord2).values())
        nonempty_neigh1 = [neigh for neigh in neighbours1 if neigh in nonempty_fields]
        nonempty_neigh2 = [neigh for neigh in neighbours2 if neigh in nonempty_fields]
        #conditions to make the move on the ground from coord1 to coord2 possible:
        #coord1 and coord2 are neighbours
        cond1 = coord1 in neighbours2
        #stone can physically "pass" from coord1 to coord2 (consider neighbour stones)
        #and there exists min one neighbour in the intersection -> exactly one neighbour
        #Note that the intersection of neigh1 and neigh2 contains 0,1 or 2 nonempty stones
        cond3 = len(set(nonempty_neigh1).intersection(nonempty_neigh2)) == 1
        #coord2 is not lying "outside" nonempty fields (that means at least "two" steps away of them)
        cond4 = len(nonempty_neigh2) >= 1 if which_board.board[coord1].is_empty else len(nonempty_neigh2) >= 2
        return cond1 and cond3 and cond4
        
    
    
                    
                



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        