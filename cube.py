import pyglet
from pyglet.gl import *

vertices = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]

colors =   [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]

def polygon(a, b, c, d):
#    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    for i in [a, b, c, d]:
        glColor3f(*colors[i])
        glVertex3f(*vertices[i])
    glEnd()

def color_cube():
    polygon(0, 3, 2, 1)
    polygon(2, 3, 7, 6)
    polygon(0, 4, 7, 3)
    polygon(1, 2, 6, 5)
    polygon(4, 5, 6, 7)
    polygon(0, 1, 5, 4)

theta = [0.0, 0.0, 0.0]
axis = 2

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(theta[0], 1, 0, 0)
    glRotatef(theta[1], 0, 1, 0)
    glRotatef(theta[2], 0, 0, 1)

    color_cube()

def reshape(x, y):
    glViewport(0, 0, x, y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if (x <= y):
        glOrtho(-2, 2, -2 * (y / x), 2 * (y / x), -10, 10)
    else:
        glOrtho(-2 * (x / y), 2 * (x / y), -2, 2, -10, 10)
    glMatrixMode(GL_MODELVIEW)

def spin_cube(dt):
    theta[axis] += 50 * dt
    if theta[axis] > 360:
        theta[axis] -= 360

def on_key(symbol, modifier):
    global axis
    if symbol == pyglet.window.key.A:
        axis = 0
    elif symbol == pyglet.window.key.S:
        axis = 1
    elif symbol == pyglet.window.key.D:
        axis = 2

def main():
    win = pyglet.window.Window(512, 512)
    win.on_resize = reshape
    win.on_draw = display
    win.on_key_press = on_key
    pyglet.clock.schedule(spin_cube)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()

if __name__ == "__main__": main()
