import pygame
import math
from ..core import rendering

#field group -> a group of fields
class tile_field_group_primitive:
    def __init__(self, tile_size:tuple):
        self.tile_fields = []
        self.tile_size = tile_size

    def add_tile_field(self, top_left:tuple, bottom_right:tuple, flag:str, data:dict = {}):
        self.tile_fields.append({"top_left":top_left, "bottom_right":bottom_right, "size":(bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]) ,"flag":flag, "data":data.copy()}.copy())

    def delete_tile_field_at_position(self, position:tuple):
        rect = pygame.FRect(0, 0, 1, 1)
        for tile_field in self.tile_fields.copy():
            rect.left = tile_field["top_left"][0] * self.tile_size[0]
            rect.top = tile_field["top_left"][1] * self.tile_size[1]
            rect.width = tile_field["size"][0] * self.tile_size[0]
            rect.height = tile_field["size"][1] * self.tile_size[1]
            if rect.collidepoint(position[0], position[1]):
                self.tile_fields.remove(tile_field)

def draw_tile_fields(tile_field_group:tile_field_group_primitive|object, display:rendering.display, colors:dict[str:tuple], layer:int = 0):
    rect = pygame.FRect(0, 0, 1, 1)
    screen_rect = pygame.FRect(display.camera_x, display.camera_y, display.width, display.height)
    for tile_field in tile_field_group.tile_fields:
        rect.left = tile_field["top_left"][0] * tile_field_group.tile_size[0]
        rect.top = tile_field["top_left"][1] * tile_field_group.tile_size[1]
        rect.width = tile_field["size"][0] * tile_field_group.tile_size[0]
        rect.height = tile_field["size"][1] * tile_field_group.tile_size[1]
        if rect.colliderect(screen_rect):
            surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.rect(surface, colors[tile_field["flag"]], (0, 0, rect.width, rect.height), 2)
            display.add_temp_display_surface(surface, rect.center, layer, use_camera=True, use_shake=True)
