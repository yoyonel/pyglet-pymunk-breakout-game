"""

"""
from enum import Enum, auto
import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk import Vec2d
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType
from pyglet_pymunk.breakout_game.components.ball import Ball
from pyglet_pymunk.breakout_game.components.paddle import Paddle
from pyglet_pymunk.breakout_game.components.walls import Walls
from pyglet_pymunk.breakout_game.components.bricks import Bricks


batch = pyglet.graphics.Batch()


class ActionCommand(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    SHOOT = auto()
    RESET_GAME = auto()


class GameEngine:
    """

    """

    def __init__(self, aspect_ratio):
        self.aspect_ratio = aspect_ratio

        self.space = pymunk.Space()
        self.options = DrawOptions()

        self.nb_balls = 1

        self._init_dynamic_body()
        self._add_collision_handler_for_paddle_ball()
        #
        self.walls = Walls(self.space, CollisionType.BALL, CollisionType.BOTTOM, self.reset_game, aspect_ratio)
        self.bricks = Bricks(self.space, CollisionType.BRICK, CollisionType.BALL, aspect_ratio)

    def _init_dynamic_body(self):
        self.player = Paddle(
            self.space,
            CollisionType.PLAYER,
            self.aspect_ratio,
            mass=100
        )

        self.balls = [
            Ball(
                self.space,
                self.player.position,
                CollisionType.BALL,
                self.aspect_ratio,
                mass=1.0,
                paddle=self.player
            )
            for _ in range(self.nb_balls)
        ]

    def _add_collision_handler_for_paddle_ball(self):
        #
        def pre_solve(arbiter, space, data):
            # We want to update the collision normal to make the bounce direction
            # dependent of where on the paddle the ball hits. Note that this
            # calculation isn't perfect, but just a quick example.
            set_ = arbiter.contact_point_set
            if len(set_.points) > 0:
                paddle_shape = arbiter.shapes[0]
                width = (paddle_shape.b - paddle_shape.a).x
                delta = (paddle_shape.body.position - set_.points[0].point_a.x).x
                angle = delta / width / 2
                # angle = 0.26 if angle > 0 else -0.25
                # print("angle: {}".format(angle))
                normal = Vec2d(0, 1).rotated(angle)
                set_.normal = normal
                set_.points[0].distance = 0
            arbiter.contact_point_set = set_
            return True

        h = self.space.add_collision_handler(
            CollisionType.PLAYER,
            CollisionType.BALL
        )
        h.pre_solve = pre_solve

    def on_draw(self):
        self.space.debug_draw(self.options)

        ball = self.balls[0]
        segment_q = ball.segment_q
        if segment_q:
            contact_shape = ball.segment_q.shape
            if contact_shape:
                # https://github.com/viblo/pymunk/blob/master/examples/using_sprites_pyglet.py
                pv1 = ball.position
                # TODO: work for bricks not for walls (left, right, top)
                pv2 = (Vec2d(contact_shape.bb.left,
                             contact_shape.bb.top) +
                       Vec2d(contact_shape.bb.right,
                             contact_shape.bb.bottom)
                       ) * 0.5
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                     ('v2f', (pv1.x, pv1.y, pv2.x, pv2.y)),
                                     ('c3f', (.05, .3, .9) * 2)
                                     )
                batch.draw()

    def update_velocity(self, velocity):
        self.player.velocity = velocity
        for ball in self.balls:
            if ball.on_paddle:
                ball.velocity = velocity

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
                velocity = self.aspect_ratio.scale(500, 0)
            if command == ActionCommand.MOVE_LEFT:
                velocity = self.aspect_ratio.scale(-500, 0)
            if command == ActionCommand.SHOOT:
                for ball in self.balls:
                    if ball.on_paddle:
                        ball.shoot()

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
