import pygame
import math
import random
from . import utils
from . import default_constants as constants

def transform_surface(surface:pygame.Surface, x_flip:bool = False, y_flip:bool = False, rotation:int = 0, alpha:int = 255, scale:int|float|tuple = 1, copy:bool = True):
    if copy:
        surface = surface.copy()
    
    if x_flip or y_flip:
        surface = pygame.transform.flip(surface, x_flip, y_flip)
    if rotation != 0:
        surface = pygame.transform.rotate(surface, rotation)
    surface.set_alpha(alpha)
    if type(scale) == int or type(scale) == float:
        if scale != 1:
            surface_size = surface.get_size()
            surface_size = (surface_size[0] * scale, surface_size[1] * scale)
            surface = pygame.transform.scale(surface, surface_size)
    else:
        if scale != surface.get_size():
            surface = pygame.transform.scale(surface, scale)
    surface.set_colorkey((0, 0, 0))
    return surface

#sprite -> contains an image/animation
class sprite:
    __slots__ = ("surfaces", "duration", "type", "duration_per_frame", "frames", "offset")
    def __init__(self, surfaces:list, duration:int|None = None, offset:tuple = (0, 0)):
        self.surfaces = surfaces

        self.duration = duration
        if self.duration != None:
            self.type = "animation"
            self.duration_per_frame = math.floor(duration / len(surfaces))
            self.frames = len(surfaces)
        else:
            self.type = "image"
            self.duration_per_frame = None
            self.frames = 1
        
        self.offset = offset

    def get_frame(self, frame:int = 0) -> tuple[pygame.Surface, tuple[int|float, int|float]]:
        frame = math.floor(frame)
        if self.type == "image":
            return self.surfaces[0], self.offset
        else:
            frame = math.floor((frame % self.duration) / self.duration_per_frame)
            return self.surfaces[frame], self.offset
        
    def get_frame_hash(self, frame:int = 0):
        frame = math.floor(frame)
        if self.type == "image":
            return 0
        else:
            frame = math.floor((frame % self.duration) / self.duration_per_frame)
            return frame
        
    def copy(self):
        new_surfaces = []
        for surface in self.surfaces:
            new_surfaces.append(surface.copy())
        return sprite(new_surfaces, self.duration, self.offset)

#spritesheet -> handles loading/storage/retrieval of sprites
class spritesheet:
    def __init__(self, file:str|None = None, size:tuple|None = None):
        self.sprites = {}
        if file == None or size == None:
            pass
        else:
            self.load_spritesheet(file, size)

    def load_spritesheet(self, file:str, size:tuple):
        self.sprite_sheet = pygame.image.load(file).convert_alpha()
        self.sprite_size = size
        self.x = 0; self.y = 0

    def load_image(self, name:str|list[str], offset:tuple = (0, 0)):
        rect = pygame.FRect(self.x * self.sprite_size[0], self.y * self.sprite_size[1], self.sprite_size[0], self.sprite_size[1])
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sprite_sheet, (0, 0), rect)
        image.set_colorkey((0, 0, 0))
        if type(name) == list:
            for i in name:
                self.sprites[i] = sprite([image], offset=offset)
        else:
            self.sprites[name] = sprite([image], offset=offset)
        self.next_sprite()
    
    def load_images(self, group_name:str, images_in_group:int, offset:tuple = (0, 0)):
        for i in range(images_in_group):
            self.load_image(group_name + " " + str(i), offset)

    def load_animation(self, name:str|list[str], frames:int, duration:int, offset:tuple = (0, 0)):
        surfaces = []
        for i in range(frames):
            rect = pygame.FRect(self.x * self.sprite_size[0], self.y * self.sprite_size[1], self.sprite_size[0], self.sprite_size[1])
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sprite_sheet, (0, 0), rect)
            image.set_colorkey((0, 0, 0))
            surfaces.append(image)
            self.next_sprite()
        
        if type(name) == list:
            for i in name:
                self.sprites[i] = sprite(surfaces, duration, offset)
        else:
            self.sprites[name] = sprite(surfaces, duration, offset)

    def next_sprite(self):
        self.x += 1
        if self.x >= math.floor(self.sprite_sheet.get_width() / self.sprite_size[0]):
            self.x = 0
            self.y += 1

    def skip(self, steps:int):
        for i in range(steps):
            self.next_sprite()

    def reverse(self, steps:int):
        for i in range(steps):
            self.x -= 1
            if self.x < 0:
                self.x = math.floor(self.sprite_sheet.get_width() / self.sprite_size[0]) - 1
                self.y -= 1
    
    def add_sprite(self, name:str, sprite:sprite):
        self.sprites[name] = sprite

    def create_sprite_variants(self, name:str, variants:int, x_flip:bool = False, y_flip:bool = False, rotation:int = 0, alpha:int = 255, scale:int|float|tuple = 1):
        self.sprites[name + " 0"] = self.sprites[name].copy()

        sprite = self.sprites[name].copy()
        del self.sprites[name]

        for i in range(variants):
            for j, surface in enumerate(sprite.surfaces):
                sprite.surfaces[j] = transform_surface(surface, x_flip, y_flip, rotation, alpha, scale)
            
            offset = sprite.offset
            if x_flip:
                offset = (offset[0] * -1, offset[1])
            if y_flip:
                offset = (offset[0], offset[1] * -1)
            if rotation != 0:
                direction = math.atan2(offset[1], offset[0])
                distance = math.sqrt((offset[0] ** 2) + (offset[1] ** 2))
                direction -= math.radians(rotation)
                offset = (round(math.cos(direction) * distance, 3), round(math.sin(direction) * distance, 3))
            if scale != 1:
                if type(scale) == int or type(scale) == float:
                    offset = (offset[0] * scale, offset[1] * scale)
                elif type(scale) == tuple:
                    offset = (offset[0] * (scale[0] / sprite["size"][0]), offset[1] * (scale[1] / sprite["size"][1]))
            
            sprite.offset = offset
            self.sprites[name + " " + str(i + 1)] = sprite.copy()

    def get_sprite(self, name:str, frame:int = 0) -> tuple[pygame.Surface, tuple[int|float, int|float]]:
        return self.sprites[name].get_frame(frame)
    
    def check_for_sprite(self, name:str):
        return name in self.sprites

    def get_sprite_duration(self, name:str):
        return self.sprites[name].duration
        
    def get_sprite_frames(self, name:str):
        return self.sprites[name].frames
        
    def get_sprite_frame_duration(self, name:str):
        return self.sprites[name].duration_per_frame
    
    def get_sprite_frame_hash(self, name:str, frame:int = 0):
        return self.sprites[name].get_frame_hash(frame)

    def delete_sprite(self, name:str):
        del self.sprites[name]

    def get_full_sprite(self, name:str):
        return self.sprites[name]

#display surface -> pygame.Surface wrapper
class display_surface:
    __slots__ = ("surface", "position", "layer", "z", "use_camera", "use_shake", "special_flags")
    def __init__(self, surface:pygame.Surface|None, position:tuple, layer:int, z:int = 0, use_camera:bool = True, use_shake:bool = False, special_flags:int = 0):
        self.surface = surface
        self.position = position
        self.layer = layer
        self.z = z
        self.use_camera = use_camera
        self.use_shake = use_shake
        self.special_flags = special_flags

    @property
    def x(self):
        return self.position[0]
    
    @x.setter
    def x(self, value:int):
        self.position = (value, self.position[1])

    @property
    def y(self):
        return self.position[1]
    
    @y.setter
    def y(self, value:int):
        self.position = (self.position[0], value)
#surface group -> a group of display surfaces
class surface_group:
    def __init__(self):
        self.display_surfaces:list[display_surface] = []

    def add_surface(self, display_surface:display_surface):
        self.display_surfaces.append(display_surface)

    def clear(self):
        self.display_surfaces.clear()

    def merge_in_surface_group(self, surface_group):
        for display_surface in surface_group.display_surfaces:
            self.display_surfaces.append(display_surface)

#camera -> handles camera
class camera:
    def initialize_camera(self):
        self.camera_x, self.camera_y = 0, 0
        self.camera_x_shake = 0; self.camera_y_shake = 0
        self.camera_x_shake_speed = 0; self.camera_y_shake_speed = 0

    def set_camera_position(self, camera_x:int, camera_y:int):
        self.camera_x = camera_x; self.camera_y = camera_y
    
    def move_camera_position(self, target_x:int|None, target_y:int|None, x_buffer:int = 1, y_buffer:int = 1):
        self.camera_x = self.camera_x + utils.interpolate(self.camera_x, target_x, x_buffer)
        self.camera_y = self.camera_y + utils.interpolate(self.camera_y, target_y, y_buffer)

    def move_camera_x(self, target_x, x_buffer:int = 1):
        self.camera_x = self.camera_x + utils.interpolate(self.camera_x, target_x, x_buffer)

    def move_camera_y(self, target_y, y_buffer:int = 1):
        self.camera_y = self.camera_y + utils.interpolate(self.camera_y, target_y, y_buffer)

    def limit_camera(self, min_x:int, min_y:int, max_x:int, max_y:int):
        if self.camera_x < min_x:
            self.camera_x = min_x
        if self.camera_y < min_y:
            self.camera_y = min_y
        if self.camera_x > max_x:
            self.camera_x = max_x
        if self.camera_y > max_y:
            self.camera_y = max_y

    def update_shake(self, shake_spring_force:float, shake_dampening:float, delta_time:float):
        self.camera_x_shake_speed += (-shake_spring_force * (self.camera_x_shake - 0)) - (shake_dampening * self.camera_x_shake_speed)
        self.camera_x_shake += self.camera_x_shake_speed * delta_time
        self.camera_y_shake_speed += (-shake_spring_force * (self.camera_y_shake - 0)) - (shake_dampening * self.camera_y_shake_speed)
        self.camera_y_shake += self.camera_y_shake_speed * delta_time

    def set_shake(self, x_shake:int|float, y_shake:int|float):
        if random.randint(0, 1) == 0:
            self.camera_x_shake = x_shake
        else:
            self.camera_x_shake = -x_shake
        if random.randint(0, 1) == 0:
            self.camera_y_shake = y_shake
        else:
            self.camera_y_shake = -y_shake

    def add_shake(self, x_shake:int|float, y_shake:int|float):
        if random.randint(0, 1) == 0:
            self.camera_x_shake += x_shake
        else:
            self.camera_x_shake -= x_shake
        if random.randint(0, 1) == 0:
            self.camera_y_shake += y_shake
        else:
            self.camera_y_shake -= y_shake

    @property
    def camera_position(self):
        return (self.camera_x, self.camera_y)
    
    def get_position_relative_to_camera(self, x:int, y:int, use_shake:bool):
        if use_shake:
            return (x - self.camera_x + round(self.camera_x_shake), y - self.camera_y + round(self.camera_y_shake))
        else:
            return (x - self.camera_x, y - self.camera_y)
    
#display -> handles layered rendering, camera
class display(camera):
    def __init__(self, size:tuple, layers:int):
        self.size = size
        self.center = (size[0] / 2, size[1] / 2)

        self.layers:list[list[display_surface]] = [[].copy() for i in range(layers)]

        self.temp_display_surfaces:list[display_surface] = []
        self.used_temp_display_surfaces:list[display_surface] = []

        self.initialize_camera()

    @property
    def width(self):
        return self.size[0]
    
    @property
    def height(self):
        return self.size[1]

    def reset_display(self):
        for i in range(len(self.layers)):
            self.layers[i].clear()
        self.temp_display_surfaces.extend(self.used_temp_display_surfaces)
        self.used_temp_display_surfaces.clear()
    
    def add_display_surface(self, display_surface:display_surface):
        self.layers[display_surface.layer].append(display_surface)

    def add_temp_display_surface(self, surface:pygame.Surface|None, position:tuple, layer:int, z:int = 0, use_camera:bool = True, use_shake:bool = False, special_flags:int = 0):
        if len(self.temp_display_surfaces) > 0:
            temp_display_surface = self.temp_display_surfaces[0]
            self.used_temp_display_surfaces.append(temp_display_surface)
            self.temp_display_surfaces.pop(0)

            temp_display_surface.surface = surface
            temp_display_surface.position = position
            temp_display_surface.layer = layer
            temp_display_surface.z = z
            temp_display_surface.use_camera = use_camera
            temp_display_surface.use_shake = use_shake
            temp_display_surface.special_flags = special_flags
        else:
            temp_display_surface = display_surface(surface, position, layer, z, use_camera, use_shake, special_flags)
            self.used_temp_display_surfaces.append(temp_display_surface)
        self.add_display_surface(temp_display_surface)

    def add_surface_group(self, surface_group:surface_group):
        for display_surface in surface_group.display_surfaces:
            self.layers[display_surface.layer].append(display_surface)

    def draw_to_surface(self, target_surface:pygame.Surface, layers:str|list = "all", optimize_using_fblits:bool = False):
        if layers == "all":
            layers = [i for i in range(len(self.layers))]

        def get_fblit_data(display_surface):
            position = display_surface.surface.get_rect(center = display_surface.position).topleft
            if display_surface.use_camera:
                position = self.get_position_relative_to_camera(position[0], position[1], display_surface.use_shake)
            return (display_surface.surface, position)
        
        for layer in layers:
            if optimize_using_fblits:
                target_surface.fblits(list(map(get_fblit_data, self.layers[layer])))
            else:
                for display_surface in self.layers[layer]:
                    if display_surface.surface != None:
                        position = display_surface.position
                        if display_surface.use_camera:
                            position = self.get_position_relative_to_camera(position[0], position[1], display_surface.use_shake)
                        target_surface.blit(display_surface.surface, display_surface.surface.get_rect(center = position), special_flags=display_surface.special_flags)
