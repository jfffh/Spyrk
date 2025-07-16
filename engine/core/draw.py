import pygame
from .rendering import sprite

def flatten_sprite_colors(sprite:sprite, color:tuple):
    surfaces = []
    for surface in sprite.surfaces:
        mask = pygame.mask.from_surface(surface)
        new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        mask.to_surface(new_surface, setcolor=color)

        surfaces.append(new_surface)
    sprite.surfaces = surfaces

def swap_colors_in_sprite(sprite:sprite, old_color:tuple, new_color:tuple):
    surfaces = []
    for surface in sprite.surfaces:
        old_surface:pygame.Surface = surface.copy()
        old_surface.set_colorkey(old_color)
        new_surface = pygame.Surface(old_surface.get_size())
        new_surface.fill(new_color)
        new_surface.blit(old_surface, (0, 0))

        surfaces.append(new_surface)
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