import pygame
import math
from engine import *
from engine.level import *

#pygame init
pygame.init()

#setup constants (default to editor)
DISPLAY_SIZE = (640, 480)
DISPLAY_CENTER = (DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2)
DISPLAY_LAYERS = 5

TILE_SIZE = (32, 32)
DISPLAY_GRID_SIZE = (math.floor(DISPLAY_SIZE[0] / TILE_SIZE[0]) + 2, math.floor(DISPLAY_SIZE[1] / TILE_SIZE[1]) + 2) 
DISPLAY_GRID_OFFSET = (-1, -1)

EDITOR_BAR_WIDTH = 200
EDITOR_BAR_COLOUR = (255, 255, 255)
EDITOR_BAR_SECONDARY_COLOUR = (EDITOR_BAR_COLOUR[0] * 0.75, EDITOR_BAR_COLOUR[1] * 0.75, EDITOR_BAR_COLOUR[2] * 0.75)
EDITOR_BAR_TERTIARY_COLOUR = (EDITOR_BAR_SECONDARY_COLOUR[0] * 0.75, EDITOR_BAR_SECONDARY_COLOUR[1] * 0.75, EDITOR_BAR_SECONDARY_COLOUR[2] * 0.75)

UI_FONT = fonts.font(None, [15])
UI_FONT_COLOUR = (1, 1, 1)

UI_SCROLL_SPEED = 500
CAMERA_SCROLL_SPEED = 500

BACKGROUND = (0, 0, 0)

#any other necessary constants

#init
screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()

#interactive pallet
class interactive_pallet:
    def __init__(self, pallet:editor_funcs.pallet):
        self.pallet = pallet

        self.brush_rects = []

        surface:pygame.Surface = pallet.spritesheet.get_sprite(self.pallet.brushes[0])[0]
        rect = surface.get_rect()
        rect.width += 8; rect.height += 8
        x = 0

        for brush in pallet.brushes:
            surface:pygame.Surface = pallet.spritesheet.get_sprite(brush)[0]
            rect = surface.get_rect()
            rect.width += 8; rect.height += 8

            x += (rect.width / 2)
            rect.centerx = x
            
            if rect.right > EDITOR_BAR_WIDTH - 16:
                x = (rect.width / 2)
                rect.centerx = x
            
            for temp_rect in self.brush_rects:
                if temp_rect.colliderect(rect):
                    rect.top = temp_rect.bottom
            
            x += (rect.width / 2)
            self.brush_rects.append(rect.copy())
        
        def rect_key(rect:pygame.FRect):
            return rect.bottom

        self.pallet_display_height = max(self.brush_rects, key=rect_key).bottom

        self.draw_pallet_display()

        self.y_scroll = 0

    def get_cursor_interaction(self, globals:global_vars.globals, pallet_display_offset:tuple):
        for i in range(len(self.brush_rects)):
            rect = self.brush_rects[i].copy()
            rect.left += pallet_display_offset[0]
            rect.top += pallet_display_offset[1] - self.y_scroll
            if rect.collidepoint(globals.cursor.x, globals.cursor.y) and globals.cursor.left_click:
                return i
        return None

    def draw_pallet_display(self):
        self.pallet_display = pygame.Surface((EDITOR_BAR_WIDTH - 16, self.pallet_display_height))
        self.pallet_display.set_colorkey((0, 0, 0))

        for i, brush in enumerate(self.pallet.brushes):
            brush_surface:pygame.Surface = self.pallet.spritesheet.get_sprite(brush)[0]
            surface = pygame.Surface((brush_surface.get_width() + 8, brush_surface.get_height() + 8), pygame.SRCALPHA)
            if i == self.pallet.brush_hash:
                surface.fill(EDITOR_BAR_SECONDARY_COLOUR)
            surface.blit(brush_surface, brush_surface.get_rect(center = (surface.get_width() / 2, surface.get_height() / 2)))

            self.pallet_display.blit(surface, self.brush_rects[i])

#systems
class tilemap_primitive_system:
    def __init__(self, type:str, tile_size:tuple, pallets:list[editor_funcs.pallet], spritesheet:rendering.spritesheet, toggle_key:int|None = None, layers:set = {0}, tile_stacker:tiles.tile_stacker|None = None, layer_offset:int = 0):
        self.type = type

        self.tilemap = tiles.tilemap_primitive(tile_size)

        self.selected_pallet = 0
        self.pallets = pallets
        self.interactive_pallets = [interactive_pallet(pallet) for pallet in pallets]

        self.spritesheet = spritesheet

        self.toggle_key = toggle_key
        self.show = self.toggle_key == None

        self.layers = layers
        
        self.max_layer = max(layers)
        self.min_layer = min(layers)

        self.current_layer = self.min_layer

        self.tile_stacker = tile_stacker
        self.layer_offset = layer_offset

class decal_group_primitive_system:
    def __init__(self, type:str, pallets:list[editor_funcs.pallet], spritesheet:rendering.spritesheet, toggle_key:int|None = None, layer:int = 0):
        self.type = type

        self.selected_pallet = 0
        self.pallets = pallets
        self.interactive_pallets = [interactive_pallet(pallet) for pallet in pallets]

        self.spritesheet = spritesheet

        self.toggle_key = toggle_key
        self.show = self.toggle_key == None

        self.current_layer = layer
        self.min_layer, self.max_layer = layer, layer
        
        self.decal_group = decal.decal_group_primitive()

        self.new_click = False

def load_level(force_old:bool = False):
    global systems

    path = json.get_JSON_file_from_main_directoy()
    if path == None:
        if force_old:
            raise FileExistsError("Unable to find json level in main directory!")
        else:
            path = "level.json"
    else:
        save = json.load_JSON(path)
        for system_name in save:
            system_data = save[system_name]

            target_system = None
            for system in systems:
                if system.type == system_name:
                    target_system:tilemap_primitive_system|decal_group_primitive_system = system

            if target_system == None:
                raise ValueError("Unable to find a system with a matching type!")
            
            if type(target_system) == tilemap_primitive_system:
                target_system.tilemap.tiles = json.deserialize_tuples_dictionary_keys(system_data["tilemap"])
                if "tile_stacker" in system_data:
                    tile_stacks = {}
                    for tile_position in system_data["tile_stacks"]:
                        tile_stacks[json.serialize_tuples(tile_position)] = tuple(system_data["tile_stacks"][tile_position])
                    target_system.tile_stacker.tile_stacks = tile_stacks
            elif type(target_system) == decal_group_primitive_system:
                decals = {}
                for decal_position in system_data:
                    decal = system_data[decal_position]
                    decals[json.deserialize_tuples(decal_position)] = {
                        "name":decal["name"], 
                        "size":json.serialize_tuples(decal["size"]), 
                        "offset":json.serialize_tuples(decal["offset"]),
                        "layer":decal["layer"], 
                        "data":decal["data"]}
                target_system.decal_group.decals = decals
            else:
                raise SystemError("No system explicit load method found!")

    return path

def save_level(path:str):
    global systems

    save = {}

    for system in systems:
        if type(system) == tilemap_primitive_system:
            save[system.type] = {"tilemap":json.serialize_tuples_dictionary_keys(system.tilemap.tiles)}
            if system.tile_stacker != None:
                tile_stacker_data = {}
                for tile_position in system.tile_stacker.tile_stacks:
                    tile_stacker_data[json.serialize_tuples(tile_position)] = list(system.tile_stacker.tile_stacks[tile_position])
                save[system.type]["tile_stacks"] = tile_stacker_data
        elif type(system) == decal_group_primitive_system:
            decals_data = {}
            for decal_position in system.decal_group.decals:
                decal = system.decal_group.decals[decal_position]
                decals_data[json.serialize_tuples(decal_position)] = {
                    "name":decal["name"], 
                    "size":json.serialize_tuples(decal["size"]), 
                    "offset":json.serialize_tuples(decal["offset"]),
                    "layer":decal["layer"], 
                    "data":decal["data"]}
            save[system.type] = decals_data
        else:
            raise SystemError("No system explicit save method found!")

    json.save_JSON(path, save)
              
def initialize_editor():
    global screen

    global globals
    globals = global_vars.globals(screen, DISPLAY_SIZE, DISPLAY_LAYERS)

    #an array of systems
    global systems
    systems = [
    ]

    global default_system

    default_system = None
    for i, system in enumerate(systems):
        if system.toggle_key == None:
            if default_system == None:
                default_system = i
            else:
                raise ValueError("More than 1 default system was detected!")

    global frame
    frame = 0

    global show_editor_bar
    show_editor_bar = True

    global pallet_display_top_left
    pallet_display_top_left = (0, 0)

def run_editor():
    global globals, systems, frame

    run = True

    while run:
        globals.delta_time = clock.tick() / 1000

        #getting inputs
        keys_to_toggle = []
        for system in systems:
            if system.toggle_key != None:
                keys_to_toggle.append(system.toggle_key)

        events = pygame.event.get()
        globals.keymap.set_keys(keys_to_toggle, False)
        globals.keymap.set_keys(pygame.K_e, False)
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            globals.keymap.update_keys(event)
        globals.cursor.update_cursor(globals.delta_time)

        globals.display.reset_display()

        #update
        update_systems()

        draw_systems()
        draw_editor_bar()

        globals.display.draw_to_surface(screen)

        frame += 1000 * globals.delta_time

        pygame.display.flip()
        pygame.display.set_caption("fps: " + str(round(clock.get_fps())))

def update_systems():
    global globals, systems, show_editor_bar, default_system

    cursor_position = (globals.cursor.x + globals.display.camera_x, globals.cursor.y + globals.display.camera_y)
    cursor_tile_position = (math.floor(cursor_position[0] / TILE_SIZE[0]), math.floor(cursor_position[1] / TILE_SIZE[1]))

    if globals.keymap.check_if_key_pressed(pygame.K_e):
        show_editor_bar = not show_editor_bar

    valid_cursor_position = True
    if show_editor_bar:
        if globals.cursor.x < EDITOR_BAR_WIDTH:
            valid_cursor_position = False

    #toggling show
    for system in systems:
        if system.toggle_key != None:
            if globals.keymap.check_if_key_pressed(system.toggle_key):
                if system.show == False:
                    system.show = True
                    for interactive_pallet in system.interactive_pallets:
                        interactive_pallet.draw_pallet_display()
                    for i in range(len(systems)):
                        other_system = systems[i]
                        if not other_system is system:
                            if other_system.toggle_key != None:
                                other_system.show = False
                else:
                    system.show = False
    
    current_system:tilemap_primitive_system|decal_group_primitive_system = systems[default_system]
    for i, system in enumerate(systems):
        if i != default_system:
            if system.show:
                current_system = system

    pallet = current_system.pallets[current_system.selected_pallet]
    interactive_pallet = current_system.interactive_pallets[current_system.selected_pallet]

    if pallet.brush == None:
        pallet.set_brush(0)
    
    #system interactions
    if type(current_system) == tilemap_primitive_system:
        if globals.cursor.clicked and valid_cursor_position:
            if globals.cursor.left_click:
                current_system.tilemap.set_tile(cursor_tile_position, pallet.brush, current_system.current_layer)
            if globals.cursor.right_click:
                current_system.tilemap.delete_tile_on_layer(cursor_tile_position, current_system.current_layer)
    
    elif type(current_system) == decal_group_primitive_system:
        if globals.cursor.clicked:
            if valid_cursor_position:
                surface, offset = current_system.spritesheet.get_sprite(pallet.brush)
                if globals.cursor.left_click and current_system.new_click:
                    current_system.decal_group.add_decal(cursor_position, pallet.brush, surface.size, offset, current_system.current_layer)
                if globals.cursor.right_click:
                    current_system.decal_group.delete_decal_on_layer(cursor_position, current_system.current_layer)
            current_system.new_click = False
        else:
            current_system.new_click = True
    
    else:
        raise SystemError("No system explicit interaction method found!")

    if globals.keymap.check_if_key_pressed(pygame.K_x) and valid_cursor_position:
        for system in systems:
            if type(system) == tilemap_primitive_system:
                system.tilemap.delete_tiles(cursor_tile_position, system.layers)
            if type(system) == decal_group_primitive_system:
                system.decal_group.delete_decal_at_position(cursor_position)

    #updating pallet
    if valid_cursor_position == False:
        new_brush = interactive_pallet.get_cursor_interaction(globals, pallet_display_top_left)
        if new_brush != None:
            pallet.set_brush(new_brush)
            interactive_pallet.draw_pallet_display()
    
    if globals.keymap.check_if_key_pressed(pygame.K_UP):
        interactive_pallet.y_scroll -= UI_SCROLL_SPEED * globals.delta_time
        if interactive_pallet.y_scroll < 0:
            interactive_pallet.y_scroll = 0
    
    if globals.keymap.check_if_key_pressed(pygame.K_DOWN):
        interactive_pallet.y_scroll += UI_SCROLL_SPEED * globals.delta_time

    if globals.keymap.check_if_key_pressed(pygame.K_LEFT):
        current_system.selected_pallet -= 1
        if current_system.selected_pallet < 0:
            current_system.selected_pallet = len(current_system.pallets) - 1

    if globals.keymap.check_if_key_pressed(pygame.K_RIGHT):
        current_system.selected_pallet += 1
        if current_system.selected_pallet >= len(current_system.pallets):
            current_system.selected_pallet = 0

    #camera controls
    if globals.keymap.check_if_key_pressed(pygame.K_w):
        globals.display.camera_y -= CAMERA_SCROLL_SPEED * globals.delta_time

    if globals.keymap.check_if_key_pressed(pygame.K_s):
        globals.display.camera_y += CAMERA_SCROLL_SPEED * globals.delta_time
        
    if globals.keymap.check_if_key_pressed(pygame.K_a):
        globals.display.camera_x -= CAMERA_SCROLL_SPEED * globals.delta_time
        
    if globals.keymap.check_if_key_pressed(pygame.K_d):
        globals.display.camera_x += CAMERA_SCROLL_SPEED * globals.delta_time

    #layer controls
    if globals.keymap.check_if_key_pressed(pygame.K_l):
        current_system.current_layer += 1
        if current_system.current_layer > current_system.max_layer:
            current_system.current_layer = current_system.min_layer
           
def draw_systems():
    global globals, systems, frame

    globals.screen.fill(BACKGROUND)

    for system in systems:
        if system.show:
            #rendering logic, insert new logic as needed
            if type(system) == tilemap_primitive_system:
                if system.tile_stacker == None:
                    layers = system.layers
                else:
                    layers = system.tile_stacker
                tiles.draw_tiles_in_tile_map(system.tilemap, globals.display, DISPLAY_GRID_SIZE, system.spritesheet, frame, DISPLAY_GRID_OFFSET, layers, system.layer_offset)
            elif type(system) == decal_group_primitive_system:
                decal.draw_decals(system.decal_group, globals.display, system.spritesheet, frame)
            else:
                raise SystemError("No system explicit rendering method found!")

def draw_editor_bar():
    global globals, systems, frame, show_editor_bar, pallet_display_top_left

    if not show_editor_bar:
        return
    
    UI_surface = pygame.Surface((EDITOR_BAR_WIDTH, DISPLAY_SIZE[1]))
    UI_surface.fill(EDITOR_BAR_COLOUR)

    line_size = UI_FONT.get_line_size(15)

    text = "shown systems: " + str([system.type for system in systems if system.show])

    rect = UI_FONT.draw_text(UI_surface, (8, 8 + line_size / 2), fonts.ALIGN_LEFT, fonts.ALIGN_CENTER, 15, text, UI_FONT_COLOUR, text_wrap=200-16)

    cursor_position = (globals.cursor.x + globals.display.camera_x, globals.cursor.y + globals.display.camera_y)
    cursor_tile_position = (math.floor(cursor_position[0] / TILE_SIZE[0]), math.floor(cursor_position[1] / TILE_SIZE[1]))

    current_system:tilemap_primitive_system|decal_group_primitive_system = systems[default_system]
    for i, system in enumerate(systems):
        if i != default_system:
            if system.show:
                current_system = system
    
    pallet:editor_funcs.pallet = current_system.pallets[current_system.selected_pallet]
    interactive_pallet = current_system.interactive_pallets[current_system.selected_pallet]
    
    text = [
        "current system: " + str(current_system.type),
        "cursor position: " + str(cursor_position),
        "cursor tile position: " + str(cursor_tile_position),
        "brush: " + str(pallet.brush),
        "layer: " + str(current_system.current_layer),
        "min, max layer: " + str((current_system.min_layer, current_system.max_layer))
    ]

    rect = UI_FONT.draw_lines_of_text(UI_surface, (8, rect.bottom + line_size / 2), fonts.ALIGN_LEFT, fonts.ALIGN_CENTER, 15, text, UI_FONT_COLOUR)

    rect = UI_FONT.draw_text(UI_surface, (EDITOR_BAR_WIDTH / 2, rect.bottom + line_size / 2), fonts.ALIGN_CENTER, fonts.ALIGN_CENTER, 15, "pallet no. " + str(current_system.selected_pallet + 1), UI_FONT_COLOUR)

    pallet_surface = pygame.Surface((EDITOR_BAR_WIDTH - 16, DISPLAY_SIZE[1] - rect.bottom - 16))
    pallet_surface.fill(EDITOR_BAR_SECONDARY_COLOUR)

    pallet_surface.blit(interactive_pallet.pallet_display, (0, 0-interactive_pallet.y_scroll))

    UI_surface.blit(pallet_surface, (8, rect.bottom + 8))
    pallet_display_top_left = (8, rect.bottom + 8)

    globals.display.add_temp_display_surface(UI_surface, (EDITOR_BAR_WIDTH / 2, DISPLAY_SIZE[1] / 2), len(globals.display.layers) - 1, use_camera=False)

if __name__ == "__main__":
    initialize_editor()
    path = load_level()
    run_editor()
    # save_level(path)

pygame.quit()