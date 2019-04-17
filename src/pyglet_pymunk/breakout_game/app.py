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

    # TODO: Find a way to test if multisample (AA) is available
    config = pyglet.gl.Config(
        sample_buffers=0,   # The number of multisample buffers.
        samples=0,          # The number of samples per pixel,
                            # or 0 if there are no multisample
        double_buffer=True  # Specify the presence of a back-buffer
                            # for every color buffer.
    )

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
