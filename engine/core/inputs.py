import pygame
from .scale import scaled_window

class keymap:
    def __init__(self):
        self.keys = {}

    def update_keys(self, event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        if event.type == pygame.KEYUP:
            self.keys[event.key] = False

    def set_keys(self, keys:int|list, state:bool):
        if type(keys) == int:
            self.keys[keys] = state
        else:
            for key in keys:
                self.keys[key] = state

    def check_if_key_pressed(self, key_code:int):
        if key_code in self.keys:
            return self.keys[key_code]
        else:
            return False

class cursor:
    def __init__(self, scaled_window:scaled_window|None):
        self.real_x = 0; self.real_y = 0
        self.held_down = 0
        self.left_click = False
        self.right_click = False

        self.scaled_window = scaled_window

    def update_cursor(self, delta_time:float):
        self.real_x, self.real_y = pygame.mouse.get_pos()
        if self.scaled_window != None:
            self.x, self.y = self.scaled_window.scale_mouse_position((self.real_x, self.real_y))
        else:
            self.x, self.y = self.real_x, self.real_y
        buttons = pygame.mouse.get_pressed()
        self.left_click = buttons[0]
        self.right_click = buttons[2]

        if self.left_click or self.right_click:
            self.held_down += 1000 * delta_time
        else:
            self.held_down = 0

    @property
    def clicked(self):
        return self.held_down > 0
    
    @property
    def position(self):
        return (self.x, self.y)

class key_buffer:
    def __init__(self, keymap:keymap):
        self.keys_to_buffer = {}
        self.keymap = keymap
        self.buffered_keys = {}

    def set_keys_to_buffer(self, keys:dict):
        self.keys_to_buffer = keys

    def update_buffer(self, delta_time:float):
        for key in self.keys_to_buffer:
            if self.keymap.check_if_key_pressed(key):
                self.buffered_keys[key] = self.keys_to_buffer[key]
        
        for key in self.buffered_keys.copy():
            if self.buffered_keys[key] > 0:
                self.buffered_keys[key] -= 1000 * delta_time
                if self.buffered_keys[key] == 0:
                    del self.buffered_keys[key]

    def check_for_buffered_key_press(self, key:int):
        return key in self.buffered_keys
        