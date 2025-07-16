import pygame
import math
from ...core import rendering
from ...core import draw

class light_renderer:
    class light_template:
        def __init__(self, diameter:int, strength:int, color:tuple|None = None, darkness_colour:tuple = (0, 0, 0)):
            self.diameter = math.floor(diameter / 2) * 2
            self.radius = int(diameter / 2)
            self.strength = strength
            self.color = color

            self.light_surface = draw.draw_gradient_circle((darkness_colour[0], darkness_colour[1], darkness_colour[2], strength), self.radius)

            if color == None:
                self.has_color = False
                self.color_surface = None
            else:
                self.has_color = True
                self.color_surface = draw.draw_gradient_circle(color, self.radius)

        def get_draw_package(self, position:tuple):
            if self.has_color:
                return (position, self.light_surface, self.color_surface)
            else:
                return (position, self.light_surface)

    def __init__(self, default_brightness:int, darkness_colour:tuple = (0, 0, 0)):
        self.light_templates:dict[str:self.light_template] = {}

        self.drawn_lights = []

        self.default_brightness = default_brightness
        self.darkness_colour = darkness_colour

    @staticmethod
    def get_light_code(diameter:int, strength:int, color:tuple|None = None):
        return (diameter, strength, color)
    
    def clear_lights(self):
        self.drawn_lights.clear()

    def add_light(self, position:tuple, diameter:int, strength:int, color:tuple|None = None):
        light_code = self.get_light_code(diameter, strength, color)
        if not light_code in self.light_templates:
            self.light_templates[light_code] = self.light_template(diameter, strength, color, self.darkness_colour)

        light_template:light_renderer.light_template = self.light_templates[light_code]
        
        self.drawn_lights.append(light_template.get_draw_package(position))

    def draw(self, light_surface:pygame.Surface, color_surface:pygame.Surface, camera:rendering.camera|None = None, use_shake:bool = True):
        light_surface.fill((self.darkness_colour[0], self.darkness_colour[1], self.darkness_colour[2], self.default_brightness))
        for light in self.drawn_lights:
            position = light[0]
            if camera != None:
                position = camera.get_position_relative_to_camera(position[0], position[1], use_shake)
            light_surface.blit(light[1], light[1].get_rect(center = position), special_flags=pygame.BLEND_RGBA_SUB)
            if len(light) > 2:
                color_surface.blit(light[2], light[2].get_rect(center = position), special_flags=pygame.BLEND_RGB_ADD)