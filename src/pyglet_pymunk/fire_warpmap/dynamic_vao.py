import pyglet
from OpenGL.GL import *
from ctypes import pointer, sizeof

window = pyglet.window.Window(width=800, height=800)

''' update function  '''
c = 0


def update(dt):
    global c
    c += 1
    data = calc_point(c)
    # if there's only on VBO, you can comment out the 'glBindBuffer' call
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(data), data)


pyglet.clock.schedule(update)

''' draw function  '''


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0, 0, 0)

    glVertexPointer(2, GL_FLOAT, 0, 0)
    glDrawArrays(GL_POINTS, 0, 2)


''' calculate coordinates given counter 'c' '''


def calc_point(c):
    data = (GLfloat * 4)(*[500 + c, 100 + c, 300 + c, 200 + c])
    return data


''' setup points '''


def setup_initial_points(c):
    vbo_id = GLuint()
    glGenBuffers(1, pointer(vbo_id))

    data = calc_point(c)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glBufferData(GL_ARRAY_BUFFER, sizeof(data), data, GL_DYNAMIC_DRAW)

    return vbo_id


############################################

vbo_id = setup_initial_points(c)

glClearColor(0.2, 0.4, 0.5, 1.0)
glEnableClientState(GL_VERTEX_ARRAY)

glPointSize(100)
pyglet.app.run()
