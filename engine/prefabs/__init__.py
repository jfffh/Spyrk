import os

__all__ = ["VERTEX_PATH", "FRAGMENT_PATH", "gfx", "algorithms"]

path = os.path.relpath(__file__).replace(os.sep, "/").removesuffix("/__init__.py")
VERTEX_PATH = path + "/shaders/vertex.glsl"
FRAGMENT_PATH = path + "/shaders/fragment.glsl"

from . import gfx
from . import algorithms