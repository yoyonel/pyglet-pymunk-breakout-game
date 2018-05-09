"""

"""
import pyglet
from pyglet.window import FPSDisplay, key
#
from pyglet_pymunk.breakout_game.components.game_engine import GameEngine, ActionCommand

map_key_command = {
        key.RIGHT: ActionCommand.MOVE_RIGHT,
        key.LEFT: ActionCommand.MOVE_LEFT,
        key.SPACE: ActionCommand.SHOOT,
        key.R: ActionCommand.RESET_GAME,
        key.P: ActionCommand.PAUSE_GAME,
    }


class GameWindow(pyglet.window.Window):
    """

    """
    def __init__(
            self,
            aspect_ratio,
            dt_for_physicx,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        # set window location
        position = aspect_ratio.scale(300, 50)
        self.set_location(position.x, position.y)
        # framerate display
        self.fps = FPSDisplay(self)
        self.engine = GameEngine(aspect_ratio, dt_for_physicx)
        self.dt_for_physicx = dt_for_physicx
        self.remain_time_for_updating_physicx = dt_for_physicx

    def on_draw(self):
        self.clear()
        self.engine.on_draw()
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        try:
            self.engine.on_action_command_press(map_key_command[symbol])
        except KeyError:
            if symbol == key.ESCAPE:
                self.quit_game()

    def on_key_release(self, symbol, modifiers):
        try:
            self.engine.on_action_command_release(map_key_command[symbol])
        except KeyError:
            pass

    def update(self, dt):
        """

        :param dt:
        :return:

        """
        # dt: deltatime from display
        self.remain_time_for_updating_physicx -= dt

        while self.remain_time_for_updating_physicx < 0.0:
            self.engine.update(self.dt_for_physicx)
            self.remain_time_for_updating_physicx += self.dt_for_physicx

    def quit_game(self):
        # http://nullege.com/codes/search/pyglet.app.exit
        pyglet.app.exit()
