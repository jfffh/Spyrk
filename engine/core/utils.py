import time
import random
import math
from . import default_constants

def get_shortest_distance_in_radians(radians_1:int|float, radians_2:int|float):
    difference = (radians_2 - radians_1) % default_constants.MAX_RADIANS
    return 2 * difference % default_constants.MAX_RADIANS - difference

def interpolate(point_1:int|float, point_2:int|float, buffer:int|float):
    return (point_2 - point_1) * buffer

def get_distance(position_1:tuple, position_2:tuple):
    return abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1])

def get_euclidian_distance(position_1:tuple, position_2:tuple):
    return math.dist(position_1, position_2)

def clamp(value:int|float, min_value:int|float, max_value:float):
    return min(max(value, min_value), max_value)

def generate_3_point_bezier_curve(point_0:tuple, point_1:tuple, control_point:tuple, increments:float = 0.1):
    dist_0 = ((control_point[0] - point_0[0]), (control_point[1] - point_0[1]))
    dist_1 = ((point_1[0] - control_point[0]), (point_1[1] - control_point[1]))

    bezier_points = []

    i = 0
    while i <= 1:
        mid_point_0 = (point_0[0] + (dist_0[0] * i), point_0[1] + (dist_0[1] * i))
        mid_point_1 = (control_point[0] + (dist_1[0] * i), control_point[1] + (dist_1[1] * i))
        point = (mid_point_0[0] + (mid_point_1[0] - mid_point_0[0]) * i, mid_point_0[1] + (mid_point_1[1] - mid_point_0[1]) * i)
        bezier_points.append(point)
        i += increments

    return bezier_points

class index:
    def __init__(self):
        self.objects = {}

    def index_object(self, type:str, object:object):
        self.objects[type] = object

    def check_for_object(self, type:str):
        return type in self.objects
    
    def get_object(self, type:str):
        return self.objects[type]

def random_integer(min:int, max:int):
    if min == max:
        return min
    else:
        return random.randint(min, max)
    
def cap_normalized_velocity(speed_x:int, speed_y:int, capped_velocity:int|float):
    direction = math.atan2(speed_y, speed_x)
    velocity = math.hypot(speed_x, speed_y)
    if velocity > capped_velocity:
        velocity = capped_velocity
    return (math.cos(direction) * velocity, math.sin(direction) * velocity)

class fps_counter:
    def __init__(self):
        self.last_fps_check = time.perf_counter()
        self.fps = "None"
        self.frames_since_last_check = 0

    def update(self):
        self.frames_since_last_check += 1
        if time.perf_counter() - self.last_fps_check > 1:
            self.fps = self.frames_since_last_check
            self.frames_since_last_check = 0
            self.last_fps_check = time.perf_counter()