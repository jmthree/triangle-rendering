import sys

from pyglet import window
from pyglet.gl import *

from shapes import *
from util import load_triangle_file

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 768

def draw_triangle(triangle):
    ''' Draws a single triangle onto the screen '''
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    for vec, col in triangle.as_pairs():
        glColor3f(*col)
        glVertex3f(vec.x, vec.y, 0)
    glEnd()

def main(name, args):
    ''' Creates the main window, initializes the OpenGL
        environment, and draws the triangles
    '''
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    ratio = WINDOW_WIDTH / (WINDOW_HEIGHT * 1.0)

    triangles = load_triangle_file(name, args)
    valid_triangles = [tri for tri in triangles if tri.is_ccw]

    # Initialize the opengl camera
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(WINDOW_WIDTH / -2, WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / -2, WINDOW_HEIGHT / 2,
            WINDOW_WIDTH / -2, WINDOW_HEIGHT / 2)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    for tri in valid_triangles:
        draw_triangle(tri)

    pyglet.app.run()


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
