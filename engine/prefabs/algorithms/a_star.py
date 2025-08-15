from ...core import utils

#tile_filter -> (open_tiles, other_data) -> dict
#other_checks - > (tile_position, new_tile_position, all_tiles, other_data) -> bool
#cost_modifier -> (tile_position, new_tile_position, all_tiles, cost, other_data) -> int

ORTHOGONAL_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ALL_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def a_star(starting_tile:tuple, target_tile:tuple, max_pathfinding_distance:int, tile_filter = None, other_checks = None, cost_modifier = None, other_data:dict = {}, offsets:list = [(-1, 0), (1, 0), (0, -1), (0, 1)]):
    def find_tile_with_lowest_cost(open_tiles:dict) -> tuple[int, int, float, float]:
        lowest_cost = None
        tile_position_with_lowest_cost = None

        for tile_position in open_tiles:
            tile = open_tiles[tile_position]
            if lowest_cost == None:
                tile_position_with_lowest_cost = tile_position
                lowest_cost = tile[2]
            else:
                if tile[2] < lowest_cost:
                    tile_position_with_lowest_cost = tile_position
                    lowest_cost = tile[2]
        
        return tile_position_with_lowest_cost
    
    def trace_path(tiles:dict, starting_tile:tuple, target_tile:tuple):
        tile_position = target_tile

        path = []

        while tile_position != starting_tile:
            path.append(tile_position)
            tile_position = (tiles[tile_position][0], tiles[tile_position][1])

        path.append(tile_position)
        
        path.reverse()

        return path

    all_tiles = {starting_tile:(starting_tile[0], starting_tile[1], 0, 0)}
    open_tiles = {starting_tile:(starting_tile[0], starting_tile[1], 0, 0)}
    closed_tiles = {}

    target_reached = False

    while len(open_tiles) > 0 and target_reached == False:
        if tile_filter != None:
            tile_position = find_tile_with_lowest_cost(tile_filter(open_tiles, other_data))
        else:
            tile_position = find_tile_with_lowest_cost(open_tiles)
        if tile_position == None:
            return None

        tile = open_tiles[tile_position]
        del open_tiles[tile_position]

        for offset in offsets:
            new_tile_position = (tile_position[0] + offset[0], tile_position[1] + offset[1])
            if new_tile_position == target_tile:
                all_tiles[new_tile_position] = (tile_position[0], tile_position[1], 0, 0)
                target_reached = True
            else:
                distance_between_tile_and_starting_tile = tile[3] + utils.get_distance(tile_position, new_tile_position)
                cost = (distance_between_tile_and_starting_tile + utils.get_distance(target_tile, new_tile_position))
                is_valid_tile = True


                if new_tile_position in open_tiles:
                    if open_tiles[new_tile_position][2] <= cost:
                        is_valid_tile = False
                if new_tile_position in closed_tiles:
                    if closed_tiles[new_tile_position][2] < cost:
                        is_valid_tile = False
                
                if distance_between_tile_and_starting_tile > max_pathfinding_distance:
                    is_valid_tile = False

                if other_checks != None:
                    if other_checks(tile_position, new_tile_position, all_tiles, other_data):
                        is_valid_tile = False
                
                if cost_modifier != None:
                    cost = cost_modifier(tile_position, new_tile_position, all_tiles, cost, other_data)

                if is_valid_tile:
                    open_tiles[new_tile_position] = (tile_position[0], tile_position[1], cost, distance_between_tile_and_starting_tile)
                    all_tiles[new_tile_position] = (tile_position[0], tile_position[1], cost, distance_between_tile_and_starting_tile)
        
        closed_tiles[tile_position] = tile
    if target_reached:
        return trace_path(all_tiles, starting_tile, target_tile)
    else:
        return None