import pygame
from . import rendering, inputs

#creates a group of assets
def group_of_assets(group_name:str, assets:int):
    pallet = []
    for asset in range(assets):
        pallet.append(group_name + " " + str(asset))
    return pallet

#pallet -> takes a spritesheet and turns it into a pallet
class pallet:
    def __init__(self, pallet_type:str):
        self.spritesheet = rendering.spritesheet()
        self.brushes = []
        self.brush_hash = 0

        self.brush = None
        self.pallet_type = pallet_type

    def add_sprite_to_pallet(self, sprite_name:str, sprite:rendering.sprite):
        self.brushes.append(sprite_name)
        self.spritesheet.add_sprite(sprite_name, sprite)

    def add_spritesheet_to_pallet(self, spritesheet:rendering.spritesheet, sprites:list|None = None):
        for sprite_name in spritesheet.sprites:
            if sprites == None:
                self.brushes.append(sprite_name)
                self.spritesheet.add_sprite(sprite_name, spritesheet.sprites[sprite_name].copy())
            else:
                words = sprite_name.split(" ")
                for word in words:
                    if word.isdigit():
                        words.remove(word)
                name = ""
                for word in words:
                    name = name + word + " "
                name = name.removesuffix(" ")

                for sprite in sprites:
                    if sprite == name:
                        self.brushes.append(sprite_name)
                        self.spritesheet.add_sprite(sprite_name, spritesheet.sprites[sprite_name].copy())
                        break
                        
    def reset_brush(self):
        self.brush_hash = 0
        self.get_brush()

    def get_brush(self):
        self.brush = self.brushes[self.brush_hash]

    def set_brush(self, brush_hash:int):
        self.brush_hash = brush_hash
        self.get_brush()

    def next_brush(self):
        self.brush_hash += 1
        if self.brush_hash >= len(self.brushes):
            self.brush_hash = 0
        self.get_brush()

    def previous_brush(self):
        self.brush_hash -= 1
        if self.brush_hash < 0:
            self.brush_hash = len(self.brushes) - 1
        self.get_brush()
