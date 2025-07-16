import pygame
from ..core.rendering import display
from ..core.inputs import keymap, cursor

class globals:
    def __init__(self, screen:pygame.Surface, display_size:tuple, display_layers:tuple):
        self.keymap = keymap()
        self.cursor = cursor()
        self.display = display(display_size, display_layers)
        
        self.screen = screen

        self.delta_time = 0.01