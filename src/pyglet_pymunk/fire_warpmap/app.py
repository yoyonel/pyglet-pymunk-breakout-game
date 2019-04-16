"""

"""
import attr
import _pickle as pickle
import ctypes
import itertools
import numpy as np
from math import cos as cosf
from math import sin as sinf
from math import sqrt
import pathlib

#
import OpenGL.GL.shaders
from OpenGL.GL import *
# from pyglet.gl import *
import pyglet
from pyglet.window import FPSDisplay, key
from pymunk.vec2d import Vec2d
import pymunk
#
# from pyglet_pymunk.fire_warpmap.vertex_array import StereoDepth
from pyglet_pymunk.fire_warpmap.cocos2d_flag import Flag3D

selected = None
selected_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)


class GameWindow(pyglet.window.Window):
    """

    """

    def __init__(
            self,
            warpmap,
            dt_for_physicx,
            space,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        # set window location
        position = Vec2d(300, 50)
        self.set_location(position.x, position.y)
        self.warpmap = warpmap
        self.dt_for_physicx = dt_for_physicx
        self.remain_time_for_updating_physicx = dt_for_physicx
        self.space = space
        # framerate display
        self.fps = FPSDisplay(self)

        ###########################################################################
        self.record_filename = f"/tmp/warp#{4}hz#{self.warpmap.w}#{self.warpmap.h}#{self.warpmap.size}.pkl"
        ###########################################################################

    def on_draw(self):
        self.clear()
        self.fps.draw()

        ###########################################################################
        # Record (dump pickle in file) Warp grid (animation)
        # # 4 Hz
        # if not self.fps.count:
        #     with open(self.record_filename, "ab") as tmp_warp_file:
        #         pickle.dump(self.warpmap.get_web_crossings(), tmp_warp_file)
        ###########################################################################

        self.warpmap.draw_debug(draw_flag=True, draw_web_constraints=True)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.quit_game()

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        mouse_body.position = x, y
        hit = self.space.point_query_nearest((x, y), 10, pymunk.ShapeFilter())
        if hit is not None:
            global selected
            body = hit.shape.body
            rest_length = mouse_body.position.get_distance(body.position)
            stiffness = 1000
            damping = 10
            selected = pymunk.DampedSpring(mouse_body, body, (0, 0), (0, 0), rest_length, stiffness, damping)
            self.space.add(selected)

    def on_mouse_release(self, x, y, button, modifiers):
        global selected
        if selected is not None:
            self.space.remove(selected)
            selected = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        mouse_body.position = x, y

    def update(self, dt):
        """

        :param dt:
        :return:

        """
        # dt: deltatime from display
        self.remain_time_for_updating_physicx -= dt

        while self.remain_time_for_updating_physicx < 0.0:
            self.warpmap.relax(self.dt_for_physicx)
            self.remain_time_for_updating_physicx += self.dt_for_physicx

    def quit_game(self):
        # http://nullege.com/codes/search/pyglet.app.exit
        pyglet.app.exit()


@attr.s
class WarpMap(object):
    h_warpmap: int = attr.ib(default=13)
    w_warpmap: int = attr.ib(default=11)

    offset: np.ndarray = attr.ib(init=False)
    norms: np.ndarray = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._init()

    def _init(self):
        """
        """
        w_warpmap = self.w_warpmap
        h_warpmap = self.h_warpmap

        coef_x = 11.0 / float(w_warpmap)
        coef_y = 13.0 / float(h_warpmap)

        self.offset = np.zeros(
            (w_warpmap, h_warpmap),
            dtype=np.dtype([('x', np.float32, 1),
                            ('y', np.float32, 1),
                            ('xv', np.float32, 1),
                            ('yv', np.float32, 1),
                            ]
                           )
        )
        self.norms = np.array([
            [0., 16.0 * coef_x],
            [16.0 * coef_y, 16.0 * sqrt(2.0) * coef_x]
        ]
        )
        t = t1 = t2 = t3 = 0.0

        max_xv = -10
        max_yv = -10.
        min_xv = +10
        min_yv = +10
        max_lenght2 = 0

        # initialise gelly
        for y in range(h_warpmap):
            yf = float(y)

            for x in range(w_warpmap):
                xf = float(x)

                t += 0.081
                t1 += 0.083
                t2 += 0.085
                t3 += 0.087

                self.offset[x][y]['x'] = float(x << 4) * coef_x
                self.offset[x][y]['y'] = float(y << 4) * coef_y

                self.offset[x][y]['xv'] = 0.0
                self.offset[x][y]['yv'] = 0.0

                is_border = not ((x == 0) or (x == w_warpmap - 1) or (y == 0) or (y == h_warpmap - 1))
                # Deplacement de la grille sauf sur les bords
                if is_border:
                    xv = (sinf(t2 - xf) + cosf(t2 + yf) + sinf(t - yf) - cosf(t + xf)) * coef_x
                    yv = (sinf(t1 - xf) + cosf(t3 + yf) + sinf(t3 - yf) - cosf(t1 + xf)) * coef_y

                    max_xv = max(max_xv, xv)
                    max_yv = max(max_yv, yv)
                    min_xv = min(min_xv, xv)
                    min_yv = min(min_yv, yv)
                    max_lenght2 = max((xv * xv + yv * yv), max_lenght2)

                    self.offset[x][y]['x'] += xv
                    self.offset[x][y]['y'] += yv

        # printf("# min velocity vector : (%1.3f, %1.3f)\n", min_xv, min_yv);
        # printf("# max velocity vector : (%1.3f, %1.3f)\n", max_xv, max_yv);
        # printf("# max velocity length : %1.3f\n", sqrtf(max_lenght2));

    def relax(self, dt):
        """
        Deforme la grille de Warping = > Effet Gel

        :param dt:
        :return:
        """
        sum_norms = 0

        # Update Velocity vectors
        for y in range(1, self.h_warpmap - 1):
            yh = y + 1
            yl = y - 1
            for x in range(1, self.w_warpmap - 1):
                xh = x + 1
                xl = x - 1
                for yi in range(yl, yh + 1):
                    y_norms = abs(yi - y)
                    for xi in range(xl, xh + 1):
                        # Toutes les cases adjacentes (croix+diagonale) (hormis la case centrale (x, y))
                        # 8 cases en tout
                        if (xi != x) or (yi != y):
                            # Current distance between particles
                            Xspring = (self.offset[xi][yi]['x'] - self.offset[x][y]['x'])
                            Yspring = (self.offset[xi][yi]['y'] - self.offset[x][y]['y'])
                            length = sqrt(Xspring * Xspring + Yspring * Yspring)
                            # Initial distance between particles
                            norm = self.norms[abs(xi - x)][y_norms]
                            sum_norms += norm

                            fCoefResistance = 0.001

                            Xspring *= (norm - length) * fCoefResistance
                            Yspring *= (norm - length) * fCoefResistance

                            self.offset[xi][yi]['xv'] += Xspring
                            self.offset[xi][yi]['yv'] += Yspring

        # Mise a jour de la grille, sauf sur les bords
        for y in range(1, self.h_warpmap - 1):
            for x in range(1, self.w_warpmap - 1):
                self.offset[x][y]['x'] += self.offset[x][y]['xv']
                self.offset[x][y]['y'] += self.offset[x][y]['yv']

        return sum_norms

    def draw_debug(self):
        offset = self.offset
        h_warpmap = self.h_warpmap
        w_warpmap = self.w_warpmap

        # glColor3f(0, 1, 0)
        # for y in range(1, h_warpmap - 1):
        #     yh = y + 1
        #     yl = y - 1
        #     for x in range(1, w_warpmap - 1):
        #         xh = x + 1
        #         xl = x - 1
        #         for yi in range(yl, yh + 1):
        #             for xi in range(xl, xh + 1):
        #                 # Toutes les cases adjacentes (croix+diagonale) (hormis la case centrale (x, y))
        #                 # 8 cases en tout
        #                 if (xi != x) or (yi != y):
        #                     pyglet.graphics.draw(2, GL_LINES,
        #                                          ('v2f', (offset[x][y]['x'],
        #                                                   offset[x][y]['y'],
        #                                                   offset[xi][yi]['x'],
        #                                                   offset[xi][yi]['y'],
        #                                                   )))

        # static attach points
        glColor3f(1, 0, 1)
        glPointSize(2)
        for y in range(h_warpmap):
            for x in range(w_warpmap):
                pyglet.graphics.draw(1, GL_POINTS,
                                     ('v2f', (offset[x][y]['x'], offset[x][y]['y'])))


@attr.s
class WarpMapPyMunk(object):
    space = attr.ib()

    h: int = attr.ib(default=13)
    w: int = attr.ib(default=11)

    bs = attr.ib(init=False, default=[])
    static_bs = attr.ib(init=False, default=[])

    size: int = attr.ib(default=32)

    def __attrs_post_init__(self):
        web_group = 1

        for y in range(self.h):
            for x in range(self.w):
                b = pymunk.Body(1, 1)
                # b.position = Vec2d(x, y) * Vec2d(23, 19)
                b.position = Vec2d(x, y) * self.size
                b.velocity_func = self.constant_velocity

                s = pymunk.Circle(b, 15)
                s.filter = pymunk.ShapeFilter(group=web_group)
                s.ignore_draw = True

                self.space.add(b, s)
                self.bs.append(b)

        def add_joint(a, b):
            rl = a.position.get_distance(b.position) * 0.9
            stiffness = 5000. * 0.1
            damping = 100 * 0.1
            j = pymunk.DampedSpring(a, b, (0, 0), (0, 0), rl, stiffness, damping)
            j.max_bias = 1000
            # j.max_force = 50000
            self.space.add(j)

        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                bs_xy = self.bs[x + y * self.w]
                for yi in range(y - 1, y + 2):
                    for xi in range(x - 1, x + 2):
                        if (xi, yi) != (x, y) and ((x - xi) * (y - yi) == 0):
                            add_joint(bs_xy, self.bs[xi + yi * self.w])

        print("len(self.space.constraints): {}".format(len(self.space.constraints)))

        # ATTACH POINTS
        def _static_point(b):
            static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            static_body.position = b.position
            self.static_bs.append(static_body)

            j = pymunk.PivotJoint(static_body, b, static_body.position)
            j.damping = 100
            j.stiffness = 20000
            self.space.add(j)

        self.static_bs = []
        # fisrt and last rows
        for x in range(self.w):
            _static_point(self.bs[x])
            _static_point(self.bs[x + (self.h - 1) * self.w])
        # first and last cols
        for y in range(self.h):
            _static_point(self.bs[y * self.w])
            _static_point(self.bs[(self.w - 1) + y * self.w])

        cooling_map_img = pyglet.image.load(pathlib.Path('datas/cooling_map.png'))
        # self.cooling_map_sprite = pyglet.sprite.Sprite(img=cooling_map_img)
        self.cooling_map_tex = cooling_map_img.get_texture()

        x = (self.w * 4) * 2.0
        y = (self.h * 4) * 2.0
        vlist_arr = [
            0, 0, 1.0, 1.0, 1.0, 0, 0,
            x, 0, 1.0, 1.0, 1.0, 1, 0,
            0, y, 1.0, 1.0, 1.0, 0, 1,
            x, y, 1.0, 1.0, 1.0, 1, 1,
        ]
        self.vlist = pyglet.graphics.vertex_list(
            4,
            ('v2f', list(itertools.chain(*zip(vlist_arr[::7], vlist_arr[1::7])))),
            ('t2f', list(itertools.chain(*zip(vlist_arr[5::7], vlist_arr[6::7]))))
        )

        # http://io7m.com/documents/fso-tta/
        self.vertex_shader_source = """
                #version 130
 
                out vec2 vTexCoord;
                 
                void
                main() {
                  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                  vTexCoord = vec2(gl_MultiTexCoord0);
                }
                """

        self.fragment_shader_source = """                
                #version 130
                
                uniform sampler2D tex0;
                
                in vec2 vTexCoord;
                out vec4 fragColor;
                
                void main() {
                    fragColor = texture(tex0, vTexCoord) * 8;
                }
                """

        self.shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(self.vertex_shader_source, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(self.fragment_shader_source, GL_FRAGMENT_SHADER),
        )

        # self.vao = StereoDepth()
        self.flag = Flag3D()

    @staticmethod
    def constant_velocity(body: pymunk.Body, gravity, damping, dt):
        body_velocity_normalized = body.velocity.normalized()
        #
        body.velocity = body_velocity_normalized * 75

    def get_web_crossings(self):
        return [
            [b.position.x, b.position.y]
            for b in self.bs
        ]

    def draw_debug(self,
                   draw_flag=False,
                   draw_static_attach_points=False,
                   draw_web_crossings=True,
                   draw_web_constraints=False,):
        if draw_flag:
            # self.vao._draw_frame()
            self.flag.update(self.bs)
            glUseProgram(self.shader)
            self.flag.draw()
            glUseProgram(0)

        # static attach points
        if draw_static_attach_points:
            glColor3f(1, 0, 1)
            glPointSize(6)

            a = []
            for b in self.static_bs:
                a += [b.position.x, b.position.y]
                pyglet.graphics.draw(len(a) // 2, GL_POINTS, ('v2f', a))

        # web crossings / bodies
        if draw_web_crossings:
            glColor3f(.1, .8, .05)
            a = []
            for b in self.bs:
                a += [b.position.x, b.position.y]
            glPointSize(4)
            pyglet.graphics.draw(len(a) // 2, GL_POINTS, ('v2f', a))

        # web net / constraints
        if draw_web_constraints:
            a = []
            for j in self.space.constraints:
                a += [j.a.position.x, j.a.position.y, j.b.position.x, j.b.position.y]
            pyglet.graphics.draw(len(a) // 2, GL_LINES, ('v2f', a))

        # # self.cooling_map_sprite.draw()
        #
        # pyglet.graphics.glEnable(GL_TEXTURE_2D)
        # pyglet.graphics.glBindTexture(self.cooling_map_tex.target, self.cooling_map_tex.id)
        # glUseProgram(self.shader)
        # self.vlist.draw(GL_TRIANGLE_STRIP)
        # glUseProgram(0)
        # pyglet.graphics.glDisable(GL_TEXTURE_2D)

    def relax(self, dt):
        # Note that we dont use dt as input into step. That is because the
        # simulation will behave much better if the step size doesnt change
        # between frames.
        # r = 10
        # for x in range(r):
        #     self.space.step(1. / 30. / r)
        self.space.step(dt)
        # self.flag.step(dt)


def main():
    space = pymunk.Space()
    config = pyglet.gl.Config(sample_buffers=1, samples=2, double_buffer=True)
    window = GameWindow(
        WarpMapPyMunk(space, 13, 11),
        1. / 100.,
        space,
        config=config, caption='Fire - WarpMap', resizable=False, fullscreen=False, vsync=False,
    )

    # No limitation on display framerate
    pyglet.clock.schedule_interval_soft(window.update, -1)
    pyglet.clock.set_fps_limit(None)

    pyglet.app.run()


if __name__ == "__main__":
    main()
