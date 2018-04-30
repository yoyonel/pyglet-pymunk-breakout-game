"""

"""
import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions
import sys

from pyglet_pymunk.breakout_game.components.collision_types import collision_types
from pyglet_pymunk.breakout_game.components.ball import Ball
from pyglet_pymunk.breakout_game.components.player import Player
from pyglet_pymunk.breakout_game.components.walls import Walls
from pyglet_pymunk.breakout_game.components.bricks import Bricks


class GameWindow(pyglet.window.Window):
    """

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set window location
        self.set_location(300, 50)
        # framerate display
        self.fps = FPSDisplay(self)

        self.space = pymunk.Space()
        self.options = DrawOptions()

        self._init_dynamic_body()
        #
        self.walls = Walls(self.space, collision_types["ball"], collision_types["bottom"], self.reset_game)
        self.bricks = Bricks(self.space, collision_types["brick"], collision_types["ball"])

    def _init_dynamic_body(self):
        self.player = Player(self.space, collision_types["player"])
        self.ball = Ball(self.space, self.player.position, collision_types["ball"])

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options)
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        # paddle
        if symbol == key.RIGHT:
            self.player.velocity = 600, 0
        if symbol == key.LEFT:
            self.player.velocity = -600, 0

        # ball
        # ball stick to the paddle (at start/reset)
        if symbol in (key.RIGHT, key.LEFT):
            if self.ball.on_paddle:
                self.ball.velocity = self.player.velocity
        if symbol == key.SPACE:
            if self.ball.on_paddle:
                self.ball.shoot()

        if symbol == key.R:
            self.reset_game()

        if symbol == key.ESCAPE:
            self.quit_game()

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.RIGHT, key.LEFT):
            self.player.velocity = 0, 0

        if symbol in (key.RIGHT, key.LEFT):
            if self.ball.on_paddle:
                self.ball.velocity = 0, 0

    def reset_game(self):
        # remove ball, player
        for shape in self.space.shapes:
            is_not_walls = shape.body != self.space.static_body
            is_not_bricks = shape.body.body_type != pymunk.Body.KINEMATIC
            if is_not_walls and is_not_bricks:
                self.space.remove(shape.body, shape)
        # remove constraints
        for constraint in self.space.constraints:
            self.space.remove(constraint)
        #
        self._init_dynamic_body()

    def update(self, dt):
        """

        :param dt:
        :return:
        """
        self.space.step(1 / 50.0)
        # self.space.step(dt)

    def quit_game(self):
        # http://nullege.com/codes/search/pyglet.app.exit
        pyglet.app.exit()
