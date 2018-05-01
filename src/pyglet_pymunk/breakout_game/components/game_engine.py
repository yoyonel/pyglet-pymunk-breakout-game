"""

"""
from enum import Enum, auto
import pymunk
from pymunk.pyglet_util import DrawOptions
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType
from pyglet_pymunk.breakout_game.components.ball import Ball
from pyglet_pymunk.breakout_game.components.player import Player
from pyglet_pymunk.breakout_game.components.walls import Walls
from pyglet_pymunk.breakout_game.components.bricks import Bricks


class ActionCommand(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SHOOT = auto()
    RESET_GAME = auto()


class GameEngine:
    """

    """

    def __init__(self):
        self.space = pymunk.Space()
        self.options = DrawOptions()

        self._init_dynamic_body()
        #
        self.walls = Walls(self.space, CollisionType.BALL, CollisionType.BOTTOM, self.reset_game)
        self.bricks = Bricks(self.space, CollisionType.BRICK, CollisionType.BALL)

    def _init_dynamic_body(self):
        self.player = Player(self.space, CollisionType.PLAYER)
        self.ball = Ball(self.space, self.player.position, CollisionType.BALL)

    def on_draw(self):
        self.space.debug_draw(self.options)

    def update_velocity(self, velocity):
        self.player.velocity = velocity
        if self.ball.on_paddle:
            self.ball.velocity = velocity

    def on_action_command_press(self, command: ActionCommand):
        """

        :param command:
        :return:
        """
        if command == ActionCommand.RESET_GAME:
            self.reset_game()
        else:
            velocity = None

            # paddle
            if command == ActionCommand.MOVE_RIGHT:
                velocity = 500, 0
            if command == ActionCommand.MOVE_LEFT:
                velocity = -500, 0
            if command == ActionCommand.SHOOT:
                if self.ball.on_paddle:
                    self.ball.shoot()

            if velocity is not None:
                self.update_velocity(velocity)

    def on_action_command_release(self, command: ActionCommand):
        if command in (ActionCommand.MOVE_RIGHT, ActionCommand.MOVE_LEFT):
            self.update_velocity((0, 0))

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
