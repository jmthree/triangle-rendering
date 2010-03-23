import sys

from pyglet import window
from pyglet.gl import *

from shapes import *
from util import load_triangle_file

WINDOW_WIDTH  = 1024
WINDOW_HEIGHT = 768

def draw_triangle(win, triangle):
    ''' Draws a single triangle onto the screen '''
    glLoadIdentity()
    if triangle.is_ccw:
        shaded = triangle.flat_shade(vector(0, 0, -1))
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

    triangles = load_triangle_file(name, args)
    win._triangles = triangles

    # Initialize the opengl camera
#    @win.event
#    def on_resize(width, height):
        #glViewport(0, 0, width, height)
#        glMatrixMode(GL_PROJECTION)
#        glLoadIdentity()
#        glOrtho(0, width,
#                0, height,
#                -width, width)
#        glOrtho(width / -2, width / 2,
#                height / -2, WINDOW_HEIGHT / 2,
#                width / -2, width / 2)
#        gluPerspective(45, width / height, -2 * width, width * 2)
#        glMatrixMode(GL_MODELVIEW)

    @win.event
    def on_key_press(key, modifier):
        if key == window.key.LEFT:
            win.__moving_left = True
        elif key == window.key.RIGHT:
            win.__moving_right = True
        elif key == window.key.UP:
            win.__moving_up = True
        elif key == window.key.DOWN:
            win.__moving_down = True
        elif key == window.key.PLUS:
            win.__scale_up = True
        elif key == window.key.MINUS:
            win.__scale_down = True

    @win.event
    def on_key_release(key, modifier):
        if key == window.key.LEFT:
            del(win.__moving_left)
        elif key == window.key.RIGHT:
            del(win.__moving_right)
        elif key == window.key.UP:
            del(win.__moving_up)
        elif key == window.key.DOWN:
            del(win.__moving_down)
        elif key == window.key.PLUS:
            del(win.__scale_up)
        elif key == window.key.MINUS:
            del(win.__scale_down)

    @win.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for tri in sorted(win._triangles,
                lambda t1, t2: min(t1.v0.z, t1.v1.z, t1.v2.z) < min(t2.v0.z, t2.v1.z, t2.v2.z) and -1 or 1):
            draw_triangle(win, tri)

    def execute_transforms(dt):
        transforms = [lambda t: t]
        if hasattr(win, '__moving_left'):
            transforms.append(lambda t: t.rotate_y(-3))
        elif hasattr(win, '__moving_right'):
            transforms.append(lambda t: t.rotate_y(3))

        if hasattr(win, '__moving_up'):
            transforms.append(lambda t: t.rotate_x(-3))
        elif hasattr(win, '__moving_down'):
            transforms.append(lambda t: t.rotate_x(3))

        if hasattr(win, '__scale_up'):
            transforms.append(lambda t: t.scale(1.1))
        elif hasattr(win, '__scale_down'):
            transforms.append(lambda t: t.scale(0.9))

        transform = reduce(lambda f, g: lambda t: g(f(t)), transforms)
        win._triangles = map(transform, win._triangles)

    pyglet.clock.schedule(execute_transforms)
    pyglet.app.run()


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
