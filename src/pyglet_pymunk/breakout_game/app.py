"""

"""
import pymunkoptions

pymunkoptions.options["debug"] = False
import pyglet

from pyglet_pymunk.breakout_game.components.gamewindow import GameWindow


def main():
    window = GameWindow(1280, 900, 'Breakout game', resizable=False)
    pyglet.clock.schedule_interval(window.update, 1 / 60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
