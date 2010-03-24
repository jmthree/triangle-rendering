''' Displays the given triangles in the passed triangle file
    as an object with flat surface shading. The triangles are
    rendered in an order such that occulusion is taken into account
'''

import sys

from pyglet import window
from pyglet.gl import *
from pyglet.window import key

from shapes import *
from util import load_triangle_file

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 768

def draw_triangle(win, tri):
    ''' Draws a single shaded triangle onto the screen '''
    glLoadIdentity()
    if tri.is_ccw:
        shaded = tri.flat_shade(vector(0, 0, -1))
        # offsets pyglet setting the center to the bottom left
        glTranslatef(win.width / 2, win.height / 2, 0)
        glBegin(GL_TRIANGLES)
        for vec, col in shaded.as_pairs():
            glColor3f(*col)
            glVertex3f(vec.x, vec.y, 0)
        glEnd()

def main(name, args):
    ''' Creates the main window, initializes the OpenGL
        environment, and draws the triangles
    '''
    win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    win._keys = set([])

    triangles = load_triangle_file(name, args)
    win._triangles = triangles

    @win.event
    def on_key_press(key, modifier):
        win._keys.add(key)

    @win.event
    def on_key_release(key, modifier):
        if key in win._keys:
            win._keys.remove(key)

    @win.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Sort the triangles first by the furthest Z value
        def sort_by_z(tri1, tri2):
            min_tri1 = min(tri1.v0.z, tri1.v1.z, tri1.v2.z)
            min_tri2 = min(tri2.v0.z, tri2.v1.z, tri2.v2.z)
            return [1, -1][min_tri1 < min_tri2]
        for tri in sorted(win._triangles, sort_by_z):
            draw_triangle(win, tri)

    def execute_transforms(dt):
        transforms = [lambda t: t]
        if key.LEFT in win._keys:
            transforms.append(lambda t: t.rotate_y(-3))
        elif key.RIGHT in win._keys:
            transforms.append(lambda t: t.rotate_y(3))

        if key.UP in win._keys:
            transforms.append(lambda t: t.rotate_x(-3))
        elif key.DOWN in win._keys:
            transforms.append(lambda t: t.rotate_x(3))

        if key.PLUS in win._keys:
            transforms.append(lambda t: t.scale(1.1))
        elif key.MINUS in win._keys:
            transforms.append(lambda t: t.scale(0.9))

        transform = reduce(lambda f, g: lambda t: g(f(t)), transforms)
        win._triangles = map(transform, win._triangles)

    pyglet.clock.schedule(execute_transforms)
    pyglet.app.run()

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
