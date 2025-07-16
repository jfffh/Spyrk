import uuid
import math
import inspect
from ..core import rendering
from ..core.utils import index
from .scenes import scene_primitive
from .global_vars import globals

class entity_primitive:
    def __init__(self, position:tuple, layer:int, type:str, spritesheet:rendering.spritesheet, flags:list = []):
        self.x, self.y = position
        self.speed_x, self.speed_y = 0, 0
        self.type = type
        self.id = uuid.uuid4().int
        self.delete = False
        self.flags = flags.copy()

        self.layer = layer
        self.spritesheet = spritesheet
        self.animation = None; self.animation_frame = 0

        self.x_flip = False; self.y_flip = False
        self.rotation = 0
        self.alpha = 255
        self.scale = 1
        self.z_sort_pos = 0

        self.display_surface = rendering.display_surface(None, self.position, self.layer, use_camera=True, use_shake=True)
        self.surface_group = rendering.surface_group()

    @property
    def position(self):
        return (self.x, self.y)
    
    @staticmethod
    def instance(position:tuple, data:dict):
        pass

    def update(self, globals:globals, current_scene:scene_primitive|object):
        pass

    def draw(self, globals:globals):
        self.surface_group.clear()
        self.draw_main_sprite()
        self.other_drawing(globals)
        self.draw_surface_group(globals.display)

    def draw_main_sprite(self):
        surface, offset = self.spritesheet.get_sprite(self.animation, self.animation_frame)
        surface = rendering.transform_surface(surface, self.x_flip, self.y_flip, self.rotation, self.alpha, self.scale)
        self.display_surface.surface = surface
        self.display_surface.z = self.z_sort_pos
        self.display_surface.position = (self.x + offset[0], self.y + offset[1])
        self.surface_group.add_surface(self.display_surface)
    
    def draw_surface_group(self, display:rendering.display):
        display.add_surface_group(self.surface_group)

    def update_animation_frame(self, globals:globals):
        self.animation_frame += 1000 * globals.delta_time

    def set_animation(self, animation:str, reset_animation_frame:bool = False):
        self.animation = animation
        if reset_animation_frame:
            self.animation_frame = 0

    def other_drawing(self, globals:globals):
        pass

    def kill(self, globals:globals, current_scene:scene_primitive|object):
        self.delete = True

    def accelerate(self, dx:int, dy:int):
        pass

    def apply_laws_of_physics(self):
        pass

    def move(self):
        pass

#entity_group -> a group of entities
class entity_group:
    def __init__(self):
        self.entities:dict[int:entity_primitive|object] = {}

    def add_entity(self, entity:entity_primitive|object):
        self.entities[entity.id] = entity

    def delete_entity(self, entity:entity_primitive|object):
        del self.entities[entity.id]

    def update_entities(self, globals:globals, current_scene:scene_primitive|object):
        for entity in self.entities.copy().values():
            entity.update(globals, current_scene)
            if entity.delete:
                self.delete_entity(entity)

    def draw_entities(self, globals:globals, *args):
        for entity in self.entities.values():
            entity.draw(globals, *args)

