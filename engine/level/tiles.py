import pygame
import math
from ..core import rendering

class tilemap_primitive:
    def __init__(self, tile_size:tuple):
        self.tiles = {}
        self.tile_size = tile_size
        self.tile_center = (tile_size[0] / 2, tile_size[1] / 2)

    def set_tile(self, tile_position:tuple, tile:str, layer:int = 0):
        self.tiles[(tile_position[0], tile_position[1], layer)] = tile
    
    def delete_tile_on_layer(self, tile_position:tuple, layer:int = 0):
        if (tile_position[0], tile_position[1], layer) in self.tiles:
            del self.tiles[(tile_position[0], tile_position[1], layer)]

    def delete_tiles(self, tile_position:tuple, layers:set):
        for layer in layers:
            if (tile_position[0], tile_position[1], layer) in self.tiles:
                del self.tiles[(tile_position[0], tile_position[1], layer)]
    
    def check_for_tile(self, tile_position:tuple, layer:int = 0):
        return (tile_position[0], tile_position[1], layer) in self.tiles
    
    def get_tile(self, tile_position:tuple, layer:int = 0):
        return self.tiles[(tile_position[0], tile_position[1], layer)]
    
    def compile_tiles_to_set(self, tile_names:str|set|None = None):
        compiled_tiles = set()
        for tile_position in self.tiles:
            if tile_names == None:
                compiled_tiles.add(tile_position)
            elif type(tile_names) == str:
                if tile_names == self.tiles[tile_position]:
                    compiled_tiles.add(tile_position)
            elif type(tile_names) == set:
                if self.tiles[tile_position] in tile_names:
                    compiled_tiles.add(tile_position)
        return compiled_tiles

class tile_stacker:
    def __init__(self):
        self.tile_stacks = {}

    def add_tile_stack(self, tile_position:tuple):
        self.tile_stacks[tile_position] = set()

    def delete_tile_stack(self, tile_position:tuple):
        del self.tile_stacks[tile_position]

    def add_to_tile_stack(self, tile_position:tuple, object):
        self.tile_stacks[tile_position].add(object)

    def delete_from_tile_stack(self, tile_position:tuple, object):
        self.tile_stacks[tile_position].remove(object)

    def check_for_tile_stack(self, tile_position:tuple):
        return tile_position in self.tile_stacks
    
    def get_tile_stack(self, tile_position:tuple):
        return self.tile_stacks[tile_position]

def draw_tiles_in_tile_map(tilemap:tilemap_primitive|object, display:rendering.display, display_grid_size:tuple, spritesheet:rendering.spritesheet, frame:int = 0, display_grid_offset:tuple = (0, 0), layers:tile_stacker|set = {0}, layer_offset:int = 0):
    def draw_tile_stack(tilemap:tilemap_primitive|object, tile_position:tuple, display:rendering.display, spritesheet:rendering.spritesheet, tile_stack:set, layer_offset:int):  
        def draw_tile(tilemap:tilemap_primitive|object, tile_position:tuple, position:tuple, layer:int, display:rendering.display, spritesheet:rendering.spritesheet, layer_offset:int):
            if tilemap.check_for_tile(tile_position, layer):
                tile = tilemap.get_tile(tile_position, layer)
                surface, offset = spritesheet.get_sprite(tile, frame)

                display.add_temp_display_surface(surface, (position[0] + offset[0], position[1] + offset[1]), layer + layer_offset, use_camera=True, use_shake=True)

        position = (round(tile_position[0] * tilemap.tile_size[0] + tilemap.tile_center[0]), round(tile_position[1] * tilemap.tile_size[1] + tilemap.tile_center[1]))
        if tile_stack == None:
            for layer in range(0):
                draw_tile(tilemap, tile_position, position, layer, display, spritesheet, layer_offset)
        else:
            for layer in tile_stack:
                draw_tile(tilemap, tile_position, position, layer, display, spritesheet, layer_offset)

    if type(layers) == tile_stacker:
        use_tile_stacker = True
    else:
        use_tile_stacker = False
    
    top_left = (math.floor(display.camera_x / tilemap.tile_size[0]) + display_grid_offset[0], math.floor(display.camera_y / tilemap.tile_size[1]) + display_grid_offset[1])
    for xi in range(display_grid_size[0]):
        for yi in range(display_grid_size[1]):
            tile_position = (top_left[0] + xi, top_left[1] + yi)
            if use_tile_stacker:
                if layers.check_for_tile_stack(tile_position):
                    draw_tile_stack(tilemap, tile_position, display, spritesheet, layers, layer_offset)
            else:
                draw_tile_stack(tilemap, tile_position, display, spritesheet, layers, layer_offset)

def create_tile_mask(size:tuple):
    tile_mask = []
    x = (size[0] - 1) / -2
    for xi in range(size[0]):
        y = (size[1] - 1) / -2
        for yi in range(size[1]):
            tile_mask.append((x + xi, y + yi))
    return tile_mask

def get_tiles_in_tile_mask(tile_mask:list, tilemap:tilemap_primitive|object, layer:int = 0):
    tiles = []
    for tile_position in tile_mask:
        if tilemap.check_for_tile(tile_position, layer):
            tiles.append(tilemap.get_tile(tile_position, layer))