import math
import array

DEFAULT_COLORKEY = (0, 0, 0)
MAX_RADIANS = math.pi * 2
QUAD_BUFFER = array.array("f", [-1.0, 1.0, 0.0, 0.0, #top left
                                1.0, 1.0, 1.0, 0.0, #top right
                                -1.0, -1.0, 0.0, 1.0, #bottom left
                                1.0, -1.0, 1.0, 1.0 #bottom right  
                                ])