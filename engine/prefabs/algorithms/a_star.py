from ...core import utils
import heapq

#tile_filter -> (tile_position:tuple, other_data:dict) -> bool (False if not a valid tiles)
#other_checks - > (tile_position, new_tile_position, other_data) -> bool (True if not a valid tile)
#cost_modifier -> (tile_position, new_tile_position, cost, other_data) -> int (revised cost)

ORTHOGONAL_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ALL_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def a_star(starting_tile:tuple, target_tile:tuple, max_pathfinding_distance:int, tile_filter = None, other_checks = None, cost_modifier = None, other_data:dict = {}, offsets:list = [(-1, 0), (1, 0), (0, -1), (0, 1)]):
    def trace_path(parent_tiles:dict, target_tile:tuple):
        tile_position = target_tile

        path = []

        while tile_position is not None:
            path.append(tile_position)
            tile_position = parent_tiles[tile_position]
        
        path.reverse()

        return path
    
    open_tiles = [(0, 0, starting_tile)]
    closed_tiles = set()
    parent_tiles = {starting_tile:None}

    while len(open_tiles) > 0:
        cost, distance_to_start, tile_position = heapq.heappop(open_tiles)

        if distance_to_start > max_pathfinding_distance:
            continue
        
        for offset in offsets:
            new_tile_position = (tile_position[0] + offset[0], tile_position[1] + offset[1])
            if new_tile_position == target_tile:
                if new_tile_position != starting_tile:
                    parent_tiles[new_tile_position] = tile_position
                return trace_path(parent_tiles, target_tile)
            else:
                if not tile_filter(new_tile_position, other_data):
                    continue
                if new_tile_position == starting_tile:
                    continue

                distance = distance_to_start + utils.get_distance(tile_position, new_tile_position)
                new_cost = (distance + utils.get_distance(target_tile, new_tile_position))

                if cost_modifier != None:
                    new_cost = cost_modifier(tile_position, new_tile_position, new_cost, other_data)

                if new_tile_position in closed_tiles:
                    continue

                if other_checks != None:
                    if other_checks(tile_position, new_tile_position, other_data):
                        continue
                
                heapq.heappush(open_tiles, (new_cost, distance, new_tile_position))
                parent_tiles[new_tile_position] = tile_position
                closed_tiles.add(new_tile_position)

    return None