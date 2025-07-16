import pygame
import asyncio
from engine import *
from engine.level import *

#pygame init
pygame.init()

#setup constants
DISPLAY_SIZE = (640, 480)
DISPLAY_CENTER = (DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2)
DISPLAY_LAYERS = 5

#init
screen = pygame.display.set_mode(DISPLAY_SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()

async def initialize_game():
    global screen

    global globals
    globals = global_vars.globals(screen, DISPLAY_SIZE, DISPLAY_LAYERS)

    global scene_manager
    scene_manager = scenes.scene_manager({})
    scene_manager.set_scene()

async def run_game():
    global globals, scene_manager

    run = True

    while run:
        globals.delta_time = clock.tick() / 1000

        await asyncio.sleep(0)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        globals.display.reset_display()

        #update
        scene_manager.update_scene(globals, events)

        #draw
        scene_manager.draw_scene(globals)

        pygame.display.flip()
        pygame.display.set_caption("fps: " + str(round(clock.get_fps())))

    scene_manager.stop_scene(globals)

async def main():
    await initialize_game()
    await run_game()

asyncio.run(main())
