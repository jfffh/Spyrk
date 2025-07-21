import pygame
from .rendering import sprite

def flatten_surface_color(surface:pygame.Surface, color:tuple):
    flattened_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    mask = pygame.mask.from_surface(surface)
    mask.to_surface(flattened_surface, setcolor=color)
    return flattened_surface

def flatten_sprite_colors(sprite:sprite, color:tuple):
    surfaces = []
    for surface in sprite.surfaces:
        surfaces.append(flatten_surface_color(surface, color))
    sprite.surfaces = surfaces

def swap_colors_in_surface(surface:pygame.Surface, old_color:tuple, new_color:tuple):
    old_surface:pygame.Surface = surface.copy()
    old_surface.set_colorkey(old_color)
    new_surface = pygame.Surface(old_surface.get_size())
    new_surface.fill(new_color)
    new_surface.blit(old_surface, (0, 0))
    return new_surface

def swap_colors_in_sprite(sprite:sprite, old_color:tuple, new_color:tuple):
    surfaces = []
    for surface in sprite.surfaces:
        surfaces.append(swap_colors_in_surface(surface, old_color, new_color))
    sprite.surfaces = surfaces

def draw_gradient_circle(color:tuple, radius:int):
    diameter = radius * 2
    surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

    for i in range(radius):
        if len(color) == 4:
            temp_color = (color[0] * (1 - ((radius - i) / radius)), color[1] * (1 - ((radius - i) / radius)), color[2] * (1 - ((radius - i) / radius)), color[3] * (1 - ((radius - i) / radius)))
        else:
            temp_color = (color[0] * (1 - ((radius - i) / radius)), color[1] * (1 - ((radius - i) / radius)), color[2] * (1 - ((radius - i) / radius)))
        pygame.draw.circle(surface, temp_color, (radius, radius), (radius - i))

    return surface

def draw_outline_on_surface(surface:pygame.Surface, color:tuple, width:int):
    outlined_surface = surface.copy()
    surface_mask = pygame.mask.from_surface(surface)
    pygame.draw.lines(outlined_surface, color, False, surface_mask.outline(), width)
    return outlined_surface

def draw_outline_on_sprite(sprite:sprite, color:tuple, width:int):
    surfaces = []
    for surface in sprite.surfaces:
        surfaces.append(draw_outline_on_surface(surface, color, width))
    sprite.surfaces = surfaces