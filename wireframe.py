import sys
import pyglet
from os import path
from pyglet.gl import *

from shapes import *
from util import load_triangle_file

def draw_triangles(triangles):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    for triangle in triangles:
        if triangle.is_ccw:
            glLoadIdentity()
            glBegin(GL_TRIANGLES)
            for vec, col in triangle.as_pairs():
                glColor3f(*col)
                glVertex3f(*vec)
            glEnd()

theta = [0.0, 0.0, 0.0]

def on_key_press(button, modifiers):
    global theta
    if button == pyglet.window.key.LEFT:
        theta[0] -= 1
    elif button == pyglet.window.key.RIGHT:
        theta[0] += 1

def main(name, args):
    triangles = load_triangle_file(name, args)
    window = pyglet.window.Window()
    window.on_key_press = on_key_press
    widthRatio = window.width / (window.height * 1.0)
    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-256 * widthRatio, 256 * widthRatio, -256, 256, -256, 256)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glEnable(GL_CULL_FACE)
    #glPolygonMode(GL_FRONT, GL_LINE)
    #glPolygonMode(GL_BACK, GL_LINE)
    #glCullFace(GL_BACK)
    def on_draw():
        draw_triangles(triangles)
    draw_triangles(triangles)
    #window.on_draw = on_draw

    pyglet.app.run()


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
