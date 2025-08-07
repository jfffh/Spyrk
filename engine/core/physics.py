import pygame

class rect_collider:
    __slots__ = ("top_left", "bottom_right", "center", "rect", "offset", "offset_x_flip", "offset_y_flip", "flags", "_x", "_y")
    def __init__(self, top_left:tuple, bottom_right:tuple, center:tuple, position:tuple, flags:list = []):
        self.top_left = top_left; self.bottom_right = bottom_right; self.center = center

        self.rect = pygame.FRect(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])

        self.offset = (self.rect.centerx - center[0], self.rect.centery - center[1])
        self.offset_x_flip = False; self.offset_y_flip = False

        self.flags = flags.copy()

        self._x, self._y = position

        self.update_rect_based_on_position()
    
    @property
    def position(self):
        return (self._x, self._y)

    def update_rect_based_on_position(self):
        if self.offset_x_flip:
            self.rect.centerx = self._x - self.offset[0]
        else:
            self.rect.centerx = self._x + self.offset[0]
        if self.offset_y_flip:
            self.rect.centery = self._y - self.offset[1]
        else:
            self.rect.centery = self._y + self.offset[1]

    @position.setter
    def position(self, position:tuple):
        self._x, self._y = position
        self.update_rect_based_on_position()

    def set_offset_flips(self, offset_x_flip:bool|None = None, offset_y_flip:bool|None = None):
        if offset_x_flip != None:
            self.offset_x_flip = offset_x_flip
        if offset_y_flip != None:
            self.offset_y_flip = offset_x_flip

    def move(self, delta:tuple):
        self._x += delta[0]; self._y += delta[1]

    def test_for_collisions_with_rect_colliders(self, rects:list, required_flags:list, excluded_flags:list):
        rects_collided_with = []

        for rect in rects:
            can_collide = False
            if len(required_flags) == 0:
                can_collide = True
            else:
                for flag in rect.flags:
                    if flag in required_flags:
                        can_collide = True
            for flag in rect.flags:
                if flag in excluded_flags:
                    can_collide = False
            if not rect.__class__ == self.__class__:
                can_collide = False
            if can_collide:
                if rect.rect.colliderect(self.rect):
                    rects_collided_with.append(rect)
        
        return rects_collided_with

    def test_for_collision_with_rect_collider(self, rect:object, required_flags:list, excluded_flags:list):
        can_collide = False
        if len(required_flags) == 0:
            can_collide = True
        else:
            for flag in rect.flags:
                if flag in required_flags:
                    can_collide = True
        for flag in rect.flags:
            if flag in excluded_flags:
                can_collide = False
        if can_collide:
            if rect.rect.colliderect(self.rect):
                return True
        return False

    def update_position_based_on_rect(self):
        if self.offset_x_flip:
            self._x = self.rect.centerx + self.offset[0]
        else:
            self._x = self.rect.centerx - self.offset[0]
        if self.offset_y_flip:
            self._y = self.rect.centery + self.offset[1]
        else:
            self._y = self.rect.centery - self.offset[1]

    def copy(self):
        return rect_collider(self.top_left, self.bottom_right, self.center, (self._x, self._y), self.flags.copy())

    def calculate_percentage_of_area(self, area:int|float):
        return (self.rect.width * self.rect.height) / area

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, x:int):
        self._x = x
        self.update_rect_based_on_position()

    @y.setter
    def y(self, y:int):
        self._y = y
        self.update_rect_based_on_position()

class ramp_collider:
    __slots__ = ("top_left", "bottom_right", "center", "rect", "offset", "offset_x_flip", "offset_y_flip", "direction", "slope", "flags", "_x", "_y")
    def __init__(self, top_left:tuple, bottom_right:tuple, center:tuple, position:tuple, direction:str, flags:list = []):
        self.top_left = top_left; self.bottom_right = bottom_right; self.center = center

        self.rect = pygame.FRect(top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])

        self.offset = (self.rect.centerx - center[0], self.rect.centery - center[1])
        self.offset_x_flip = False; self.offset_y_flip = False
        
        self.direction = direction
        self.slope = self.rect.height / self.rect.width

        self.flags = flags.copy()

        self._x, self._y = position

        self.update_rect_based_on_position()

    @property
    def position(self):
        return (self._x, self._y)

    def update_rect_based_on_position(self):
        if self.offset_x_flip:
            self.rect.centerx = self._x - self.offset[0]
        else:
            self.rect.centerx = self._x + self.offset[0]
        if self.offset_y_flip:
            self.rect.centery = self._y - self.offset[1]
        else:
            self.rect.centery = self._y + self.offset[1]

    @position.setter
    def position(self, position:tuple):
        self._x, self._y = position
        self.update_rect_based_on_position()

    def set_offset_flips(self, offset_x_flip:bool|None = None, offset_y_flip:bool|None = None):
        if offset_x_flip != None:
            self.offset_x_flip = offset_x_flip
        if offset_y_flip != None:
            self.offset_y_flip = offset_x_flip

    def move(self, delta:tuple):
        self._x += delta[0]; self._y += delta[1]

    def test_for_collision_with_rect_collider(self, rect:rect_collider, required_flags:list, excluded_flags:list):
        can_collide = False
        if len(required_flags) == 0:
            can_collide = True
        else:
            for flag in self.flags:
                if flag in required_flags:
                    can_collide = True
        for flag in self.flags:
            if flag in excluded_flags:
                can_collide = False
        if can_collide:
            if rect.rect.colliderect(self.rect):
                return True
        return False
    
    def get_height(self, rect:rect_collider):
        if self.direction == "right":
            return self.rect.bottom - (rect.rect.right - self.rect.left) * self.slope
        elif self.direction == "left":
            return self.rect.bottom - (self.rect.right - rect.rect.left) * self.slope

    def update_position_based_on_rect(self):
        if self.offset_x_flip:
            self._x = self.rect.centerx + self.offset[0]
        else:
            self._x = self.rect.centerx - self.offset[0]
        if self.offset_y_flip:
            self._y = self.rect.centery + self.offset[1]
        else:
            self._y = self.rect.centery - self.offset[1]

    def copy(self):
        return ramp_collider(self.top_left, self.bottom_right, self.center, (self._x, self._y), self.direction, self.flags.copy())

    def calculate_percentage_of_area(self, area:int|float):
        return (self.rect.width * self.rect.height * 0.5) / area
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, x:int):
        self._x = x
        self.update_rect_based_on_position()

    @y.setter
    def y(self, y:int):
        self._y = y
        self.update_rect_based_on_position()

class mask_collider:
    __slots__ = ("_mask", "mask_rect", "_x", "_y", "offset", "offset_x_flip", "offset_y_flip", "flags")
    def __init__(self, mask:pygame.Mask, position:tuple, offset:tuple = (0, 0), flags:list = []):
        self._mask = mask
        self.mask_rect = mask.get_rect()

        self._x, self._y = position
        self.offset = offset
        self.offset_x_flip = False; self.offset_y_flip = False

        self.mask_rect.center = (self._x + self.offset[0], self._y + self.offset[1])

        self.flags = flags.copy()
    
    @property
    def position(self):
        return (self._x, self._y)
    
    def update_rect_based_on_position(self):
        if self.offset_x_flip:
            self.mask_rect.centerx = self._x - self.offset[0]
        else:
            self.mask_rect.centerx = self._x + self.offset[0]
        if self.offset_y_flip:
            self.mask_rect.centery = self._y - self.offset[1]
        else:
            self.mask_rect.centery = self._y + self.offset[1]

    @position.setter
    def position(self, position:tuple):
        self._x, self._y = position
        self.update_rect_based_on_position()

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, mask:pygame.Mask):
        self._mask = mask
        self.mask_rect = mask.get_rect()

    def set_offset_flips(self, offset_x_flip:bool|None = None, offset_y_flip:bool|None = None):
        if offset_x_flip != None:
            self.offset_x_flip = offset_x_flip
        if offset_y_flip != None:
            self.offset_y_flip = offset_x_flip
    
    def test_for_collision_with_mask_collider(self, mask_collider, required_flags:list, excluded_flags:list):
        can_collide = False
        if len(required_flags) == 0:
            can_collide = True
        else:
            for flag in mask_collider.flags:
                if flag in required_flags:
                    can_collide = True
        for flag in mask_collider.flags:
            if flag in excluded_flags:
                can_collide = False
        if can_collide:
            if mask_collider.mask_rect.colliderect(self.mask_rect):
                if mask_collider._mask.overlap(self._mask, (self.mask_rect.left - mask_collider.mask_rect.left, self.mask_rect.top - mask_collider.mask_rect.top)) != None: 
                    return True
        return False
    
    def copy(self):
        return mask_collider(self.mask, self.set_position, self.offset, self.flags)
    
    def get_overlap_mask(self, mask_collider):
        return self.mask.overlap_mask(mask_collider.mask, (self.mask_rect.left - mask_collider.mask_rect.left, self.mask_rect.top - mask_collider.mask_rect.top))
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, x:int):
        self._x = x
        self.update_rect_based_on_position()

    @y.setter
    def y(self, y:int):
        self._y = y
        self.update_rect_based_on_position()

class collider_sheet:
    def __init__(self):
        self.colliders = {}

    def add_collider(self, collider_name:str, collider:rect_collider|ramp_collider):
        self.colliders[collider_name] = collider

    def check_for_collider(self, collider_name:str):
        return collider_name in self.colliders

    def get_collider(self, collider_name:str):
        return self.colliders[collider_name].copy()

def from_rect_to_mask(rect:pygame.FRect):
    return pygame.Mask(rect.size, True)

def create_blank_mask(size:tuple):
    return pygame.Mask(size)