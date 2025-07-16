import pygame
import math
from ..core import rendering

#decal_group -> a group of decals
class decal_group_primitive:
    def __init__(self):
        self.decals = {}

    def add_decal(self, position:tuple, name:tuple, size:tuple, offset:tuple, layer:int, data:dict = {}):
        self.decals[position] = {"name":name, "size":size, "offset":offset, "layer":layer, "data":data.copy()}.copy()

    def delete_decal_at_position(self, position:tuple):
        rect = pygame.FRect(0, 0, 1, 1)
        for decal_position in self.decals.copy().keys():
            decal = self.decals[decal_position]
            rect.width, rect.height = decal["size"]
            rect.center = (decal_position[0] + decal["offset"][0], decal_position[1] + decal["offset"][1])
            if rect.collidepoint(position[0], position[1]):
                del self.decals[decal_position]
    
    def delete_decal_on_layer(self, position:tuple, layer:int):
        rect = pygame.FRect(0, 0, 1, 1)
        for decal_position in self.decals.copy().keys():
            decal = self.decals[decal_position]
            rect.width, rect.height = decal["size"]
            rect.center = (decal_position[0] + decal["offset"][0], decal_position[1] + decal["offset"][1])
            if rect.collidepoint(position[0], position[1]) and layer == decal["layer"]:
                del self.decals[decal_position]

def draw_decals(decal_group:decal_group_primitive|object, display:rendering.display, spritesheet:rendering.spritesheet, frame:int):
    for i, position in enumerate(decal_group.decals):
        decal = decal_group.decals[position]
        surface, offset = spritesheet.get_sprite(decal["name"], frame)
        display.add_temp_display_surface(surface, (position[0] + offset[0], position[1] + offset[1]), decal["layer"], use_camera=True, use_shake=True)
