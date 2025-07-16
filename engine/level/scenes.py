import pygame
from .global_vars import globals

class scene_primitive:
    def __init__(self, globals:globals):
        pass

    def start(self, globals:globals):
        pass

    def update(self, globals:globals, events:list[pygame.Event]):
        pass

    def draw(self, globals:globals):
        pass

    def stop(self, globals:globals):
        pass

class scene_manager:
    def __init__(self, scenes:dict[str, scene_primitive|object]):
        self.scenes = scenes
        self.current_scene:scene_primitive|object|None = None
        self.scene_name = None

    def set_scene(self, scene_name:str, globals:globals):
        if self.current_scene != None:
            self.current_scene.stop()
        
        self.current_scene = self.scenes[scene_name]
        self.scene_name = scene_name
    
        self.current_scene.start(globals)

    def update_scene(self, globals:globals, events:list[pygame.Event]):
        self.current_scene.update(globals, events)

    def draw_scene(self, globals:globals):
        self.current_scene.draw(globals)

    def stop_scene(self, globals:globals):
        self.current_scene.stop(globals)