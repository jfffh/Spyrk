import math
from ...level.tiles import tilemap_primitive

#intersection checker -> (start_position:tuple, end_position:tuple, tile_position:tuple, tilemap:tilemap_primitive) -> bool, (line intersection, line intersection distance)

def raycast_line(start_position:tuple, end_position:tuple, tilemap:tilemap_primitive, intersection_checker:object):
    start_tile = (math.floor(start_position[0] / tilemap.tile_size[0]), math.floor(start_position[1] / tilemap.tile_size[1]))
    end_tile = (math.floor(end_position[0] / tilemap.tile_size[0]), math.floor(end_position[1] / tilemap.tile_size[1]))

    dx = end_tile[0] - start_tile[0]
    dy = end_tile[1] - start_tile[1]

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    
    steps = max(steps, 1)

    x_increment = dx / steps
    y_increment = dy / steps

    tile_x, tile_y = start_tile

    intersection = None
    intersection_distance_to_start = float("inf")

    for i in range(int(steps) + 1):
        tile = (round(tile_x), round(tile_y))
        for offset in [(0, 0), (-1, 0), (1, 0), (0, 1), (0, -1)]:
            tile_to_check = (tile[0] + offset[0], tile[1] + offset[1])

            collision, line_intersection_data = intersection_checker(start_position, end_position, tile_to_check, tilemap)

            if collision:
                if line_intersection_data[1] < intersection_distance_to_start:
                    intersection, intersection_distance_to_start = line_intersection_data
                    
        if intersection != None:
            return intersection

        tile_x += x_increment
        tile_y += y_increment
    
    return intersection