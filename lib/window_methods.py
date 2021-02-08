#methods for window
import texts as t
import colors as c

def unmark_hexagons(game, player, marked_hexagons):
    for hexagon in marked_hexagons:
        hexagon.is_marked = False
    game.painter.draw_unmarked_side_area(player, game.surfaces)
    game.painter.draw_board(game.board, game.surfaces, game.buttons)
    marked_hexagons.clear()  
    
def mark_hexagons(game, marked_hexagons, mark_width):
    game.painter.draw_set_of_hexagon_markings(marked_hexagons, c.marking_color, mark_mode = mark_width)
    
def check_winner(painter, surfaces, color, surr, game_over):
    if color == "white":    opp_color = "black"
    else:   opp_color = "white"
    color_surr = surr[0]
    opp_color_surr = surr[1]
    if color_surr and opp_color_surr:   
        painter.write_box_text(surfaces, t.win_text["tied"], "white")
        painter.write_box_text(surfaces, t.win_text["tied"], "black")
        game_over = True
    elif color_surr:    
        painter.write_box_text(surfaces, t.win_text[opp_color], "white")
        painter.write_box_text(surfaces, t.win_text[opp_color], "black")
        game_over = True
    elif opp_color_surr:  
        painter.write_box_text(surfaces, t.win_text[color], "white")
        painter.write_box_text(surfaces, t.win_text[color], "black")
        game_over = True
    return game_over

def point_in_surface(surface, point):
    surface_offset = surface.get_abs_offset()
    xcond = surface_offset[0] < point[0] and point[0] < surface_offset[0] + surface.get_width()
    ycond = surface_offset[1] < point[1] and point[1] < surface_offset[1] + surface.get_height()
    if xcond and ycond: return True
    return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    