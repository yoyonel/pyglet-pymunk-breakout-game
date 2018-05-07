"""

"""
import pymunkoptions
pymunkoptions.options["debug"] = False
import pyglet
from pymunk.vec2d import Vec2d
#
from pyglet_pymunk.breakout_game.components.game_window import GameWindow


class AspectRatio:
    def __init__(self, src_sizes: Vec2d, dst_sizes: Vec2d):
        self.aspect_ratio = Vec2d(
            dst_sizes[0] / src_sizes[0],
            dst_sizes[1] / src_sizes[1],
        )   # type: Vec2d

    def scale(self, x, y) -> Vec2d:
        return Vec2d(
            int(x * self.aspect_ratio[0]),
            int(y * self.aspect_ratio[1]),
        )

    def scale_V2d(self, v: Vec2d) -> Vec2d:
        return self.scale(v.x, v.y)

    def scale_s(self, scalar: float) -> float:
        return self.scale(scalar, 0).x


def main():
    original_size = Vec2d(1280, 900)
    target_size = Vec2d(800, 600)
    aspect_ratio = AspectRatio(original_size, target_size)

    window_size = aspect_ratio.scale_V2d(original_size)
    window = GameWindow(aspect_ratio, window_size[0], window_size[1], 'Breakout game', resizable=False)

    dt_for_physicx = 1 / 50.0
    pyglet.clock.schedule_interval(window.update, dt_for_physicx)

    pyglet.app.run()


if __name__ == "__main__":
    main()
