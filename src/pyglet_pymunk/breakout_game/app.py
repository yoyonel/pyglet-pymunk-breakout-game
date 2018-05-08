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
    target_size = Vec2d(800, 600)
    aspect_ratio = AspectRatio(original_size, target_size)
    dt_for_physicx = 1 / 50.0

    window_size = aspect_ratio.scale_V2d(original_size)
    window = GameWindow(aspect_ratio, dt_for_physicx,
                        window_size[0], window_size[1], 'Breakout game', resizable=False)

    pyglet.clock.schedule_interval(window.update, dt_for_physicx)

    pyglet.app.run()


if __name__ == "__main__":
    main()
