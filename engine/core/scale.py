import pygame

#scaled_window -> handles window scaling
class scaled_window:
    def __init__(self, original_window_size:tuple, target_window_size:tuple):
        self.original_window_size = original_window_size
        self.target_window_size = target_window_size

        x_scale = round(self.target_window_size[0] / self.original_window_size[0], 1)
        y_scale = round(self.target_window_size[1] / self.original_window_size[1], 1)

        if y_scale < x_scale:
            self.scale = y_scale
        else:
            self.scale = x_scale

        self.scaled_window_size = (self.original_window_size[0] * self.scale, self.original_window_size[1] * self.scale)
        self.target_window_center = (self.target_window_size[0] / 2, self.target_window_size[1] / 2)
        self.window_offset = ((self.target_window_size[0] - self.scaled_window_size[0]) / 2, (self.target_window_size[1] - self.scaled_window_size[1]) / 2)

    def scale_surface(self, surface:pygame.Surface):
        surface = pygame.transform.scale(surface, self.scaled_window_size)
        new_surface = pygame.Surface(self.target_window_size, pygame.SRCALPHA)
        new_surface.blit(surface, surface.get_rect(center = self.target_window_center))
        return new_surface
    
    def scale_mouse_position(self, mouse_position:tuple):
        mouse_position = (mouse_position[0] * self.scale, mouse_position[1] * self.scale)
        mouse_position = (mouse_position[0] - self.window_offset[0], mouse_position[1] - self.window_offset[1])
        return mouse_position
