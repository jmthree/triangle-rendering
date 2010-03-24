''' Displays the given triangles in the passed triangle file in
    wireframe format. Backfacing triangles are culled.
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
    ''' Draws a single triangle onto the screen '''
    glLoadIdentity()
    if tri.is_ccw:
        # offsets pyglet setting the center to the bottom left
        glTranslatef(win.width / 2, win.height / 2, 0)
        glBegin(GL_TRIANGLES)
        for vec, col in tri.as_pairs():
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

    # Set up wireframe mode
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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
        for tri in win._triangles:
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
