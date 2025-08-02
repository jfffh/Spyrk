import pygame
import math
from dataclasses import dataclass
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
        return self.tiles.get((tile_position[0], tile_position[1], layer))
    
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

class tilemap_renderer:
    @dataclass
    class tile_group:
        surface:pygame.Surface
        refresh:bool
    
    def __init__(self, layer_groupings:dict, tile_size:tuple, tile_groupings:tuple, display_grid_size:tuple, display_grid_offset:tuple = (0, 0)):
        self.cached_surfaces:dict[tuple:self.tile_group] = {}

        self.layer_groupings = layer_groupings
        self.tile_size = tile_size
        self.tile_center = (self.tile_size[0] / 2, self.tile_size[1] / 2)
        self.tile_groupings = tile_groupings
        self.tile_grouping_size = (tile_groupings[0] * tile_size[0], tile_groupings[1] * tile_size[1])
        self.tile_grouping_center = (self.tile_grouping_size[0] / 2, self.tile_grouping_size[1] / 2)
        self.display_grid_size = display_grid_size
        self.display_grid_offset = display_grid_offset

    def refresh_tile_group(self, tile_group:tuple, tilemap:tilemap_primitive|object, layer:int):
        layer_grouping = None
        for layer_group in self.layer_groupings:
            if layer in layer_group:
                layer_grouping = layer_group
        self.cached_surfaces[((tile_group[0], tile_group[1], id(tilemap)), layer_grouping)].refresh = True

    def refresh_tile_group_at_tile_position(self, tile_position:tuple, tilemap:tilemap_primitive|object, layer:int):
        tile_group = (math.floor(tile_position[0] / 2), math.floor(tile_position[1] / 2))
        layer_grouping = None
        for layer_group in self.layer_groupings:
            if layer in layer_group:
                layer_grouping = layer_group
        self.cached_surfaces[((tile_group[0], tile_group[1], id(tilemap)), layer_grouping)].refresh = True

    def get_tile_group_surface(self, tile_group:tuple, tilemap:tilemap_primitive|object, layer:int):
        return self.cached_surfaces.get(((tile_group[0], tile_group[1], id(tilemap)), layer).surface, pygame.Surface(self.tile_grouping_size, pygame.SRCALPHA))
    
    def get_tile_group_surface_at_tile_position(self, tile_position:tuple, tilemap:tilemap_primitive|object, layer:int):
        tile_group = (math.floor(tile_position[0] / 2), math.floor(tile_position[1] / 2))
        return self.cached_surfaces.get(((tile_group[0], tile_group[1], id(tilemap)), layer).surface, pygame.Surface(self.tile_grouping_size, pygame.SRCALPHA))

    def draw_tiles_in_tilemap(self, tilemap:tilemap_primitive|object, display:rendering.display, spritesheet:rendering.spritesheet, frame:int = 0):
        top_left_tile_grouping = (math.floor(display.camera_x / self.tile_grouping_size[0]) + self.display_grid_offset[0], math.floor(display.camera_y / self.tile_grouping_size[1]) + self.display_grid_offset[1])
        for xi in range(self.display_grid_size[0]):
            for yi in range(self.display_grid_size[1]):
                tile_grouping = (top_left_tile_grouping[0] + xi, top_left_tile_grouping[1] + yi, id(tilemap))
                tile_grouping_position = (tile_grouping[0] * self.tile_grouping_size[0] + self.tile_grouping_center[0], tile_grouping[1] * self.tile_grouping_size[1] + self.tile_grouping_center[1])
                for layer in self.layer_groupings.keys():
                    can_use_cache = False
                    if (tile_grouping, layer) in self.cached_surfaces:
                        if self.cached_surfaces[(tile_grouping, layer)]:
                            can_use_cache = True

                    if can_use_cache:
                        display.add_temp_display_surface(self.cached_surfaces[(tile_grouping, layer)].surface, tile_grouping_position, layer, use_camera=True, use_shake=True)
                    else:
                        tile_group_surface = pygame.Surface(self.tile_grouping_size, pygame.SRCALPHA)
                        top_left_tile = (tile_grouping[0] * self.tile_groupings[0], tile_grouping[1] * self.tile_groupings[1])
                        contains_animation = False
                        for tile_layer in self.layer_groupings[layer]:
                            for xj in range(self.tile_groupings[0]):
                                for yj in range(self.tile_groupings[1]):
                                    tile = tilemap.get_tile((top_left_tile[0] + xj, top_left_tile[1] + yj), tile_layer)
                                    if tile != None:
                                        surface, offset = spritesheet.get_sprite(tile, frame)
                                        position = (xj * self.tile_size[0] + self.tile_center[0] + offset[0], yj * self.tile_size[1] + self.tile_center[1] + offset[1])
                                        tile_group_surface.blit(surface, surface.get_rect(center = position))
                                        if spritesheet.get_sprite_frames(tile) > 1:
                                            contains_animation = True
                        if (tile_grouping, layer) in self.cached_surfaces:
                            tile_group = self.cached_surfaces[(tile_grouping, layer)]
                            tile_group.surface = tile_group_surface
                            tile_group.refresh = contains_animation

                        else:
                            self.cached_surfaces[(tile_grouping, layer)] = self.tile_group(tile_group_surface, contains_animation)
                        display.add_temp_display_surface(tile_group_surface, tile_grouping_position, layer, use_camera=True, use_shake=True)

def draw_tiles_in_tile_map(tilemap:tilemap_primitive|object, display:rendering.display, display_grid_size:tuple, spritesheet:rendering.spritesheet, frame:int = 0, display_grid_offset:tuple = (0, 0), layers:set = {0}, layer_offset:int = 0):
    def draw_tile_stack(tilemap:tilemap_primitive|object, tile_position:tuple, display:rendering.display, spritesheet:rendering.spritesheet, tile_stack:set, layer_offset:int):  
        def draw_tile(tilemap:tilemap_primitive|object, tile_position:tuple, position:tuple, layer:int, display:rendering.display, spritesheet:rendering.spritesheet, layer_offset:int):
            if tilemap.check_for_tile(tile_position, layer):
                tile = tilemap.get_tile(tile_position, layer)
                surface, offset = spritesheet.get_sprite(tile, frame)
                display.add_temp_display_surface(surface, (position[0] + offset[0], position[1] + offset[1]), layer + layer_offset, use_camera=True, use_shake=True)

        position = (round(tile_position[0] * tilemap.tile_size[0] + tilemap.tile_center[0]), round(tile_position[1] * tilemap.tile_size[1] + tilemap.tile_center[1]))
        for layer in tile_stack:
            draw_tile(tilemap, tile_position, position, layer, display, spritesheet, layer_offset)

    top_left = (math.floor(display.camera_x / tilemap.tile_size[0]) + display_grid_offset[0], math.floor(display.camera_y / tilemap.tile_size[1]) + display_grid_offset[1])
    for xi in range(display_grid_size[0]):
        for yi in range(display_grid_size[1]):
            tile_position = (top_left[0] + xi, top_left[1] + yi)
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