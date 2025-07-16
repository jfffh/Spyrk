#version 330 core

in vec2 vertex;
in vec2 texture_coordinates;
out vec2 uvs;

void main() {
    uvs = texture_coordinates;
    gl_Position = vec4(vertex.x, vertex.y, 0.0, 1.0);
};