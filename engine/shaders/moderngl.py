import pygame
import array
import moderngl
from ..core.default_constants import QUAD_BUFFER

DEFAULT_SWIZZLING = "BGRA"

#texture group -> handles texture (including memory management)
class texture_group:
    def __init__(self, gl_context:moderngl.Context):
        self.gl_context = gl_context

        self.textures:dict[str:moderngl.Texture] = {}
        self.is_texture_permanent:dict[str:bool] = {}
        self.texture_memory_assignments:dict[str:int] = {}

    def create_texture_from_surface(self, name:str, surface:pygame.Surface, memory_hash:int|None = None, permanent:bool = False, swizzling:str = "BGRA"):
        texture = self.gl_context.texture(surface.get_size(), 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = swizzling
        texture.write(surface.get_view("1"))
        
        self.textures[name] = texture
        self.is_texture_permanent[name] = permanent
        self.texture_memory_assignments[name] = None

        if memory_hash != None:
            texture.use(memory_hash)
            self.texture_memory_assignments[name] = memory_hash

    def assign_texture_to_memory(self, name:str, memory_hash:int):
        self.textures[name].use(memory_hash)
        self.texture_memory_assignments[name] = memory_hash

    def clear_all_assigned_textures(self):
        for name in self.textures:
            if self.is_texture_permanent[name] == False:
                self.textures[name].release()
                self.texture_memory_assignments[name] = None

    def clear_texture(self, name:str):
        self.textures[name].release()
        self.texture_memory_assignments[name] = None

    def get_texture_memory_assignment(self, name:str):
        return self.texture_memory_assignments[name]

#shader -> wrapper for the moderngl program module
class shader:
    def __init__(self, gl_context:moderngl.Context, texture_group:texture_group, vertex_shader:str, fragment_shader:str):
        vertex_shader_file = open(vertex_shader)
        fragment_shader_file = open(fragment_shader)

        self.program = gl_context.program(vertex_shader=vertex_shader_file.read(), fragment_shader=fragment_shader_file.read())
        self.texture_group = texture_group

        vertex_shader_file.close()
        fragment_shader_file.close()

    def update_uniforms(self, expected_textures:list, **kwargs):
        for texture_name in expected_textures:
            self.program[texture_name] = self.texture_group.get_texture_memory_assignment(texture_name)
    
        for uniform in kwargs:
            self.program[uniform] = kwargs[uniform]

#gl_render_object -> render object for moderngl rendering
class gl_render_object:
    def __init__(self, gl_context:moderngl.Context, shader:shader):
        self.gl_context = gl_context
        
        self.shader = shader

        self.quad_buffer = gl_context.buffer(data = array.array("f", QUAD_BUFFER))

        self.vertex_array = gl_context.vertex_array(shader.program, [(self.quad_buffer, "2f 2f", "vertex", "texture_coordinates")])

    def update(self):
        self.vertex_array.render(mode=moderngl.TRIANGLE_STRIP)