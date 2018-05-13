"""

"""
import pymunkoptions
pymunkoptions.options["debug"] = False
import pyglet
from pymunk.vec2d import Vec2d
#
from pyglet_pymunk.breakout_game.components.aspect_ratio import AspectRatio
from pyglet_pymunk.breakout_game.components.game_window import GameWindow


def main():
    original_size = Vec2d(1280, 900)

    config = pyglet.gl.Config(sample_buffers=1, samples=2, double_buffer=True)

    # target_size = Vec2d(800, 600)
    target_size = Vec2d(1280, 900)
    aspect_ratio = AspectRatio(original_size, target_size)

    dt_for_physicx = 1 / 50.0   # constant dt for physic engine

    window_size = aspect_ratio.scale_V2d(original_size)
    window = GameWindow(aspect_ratio,
                        dt_for_physicx,
                        window_size[0], window_size[1],
                        config=config,
                        caption='Breakout game',
                        resizable=False, fullscreen=False, vsync=False)

    # No limitation on display framerate
    pyglet.clock.schedule_interval_soft(window.update, -1)
    pyglet.clock.set_fps_limit(None)

    pyglet.app.run()


if __name__ == "__main__":
    main()
