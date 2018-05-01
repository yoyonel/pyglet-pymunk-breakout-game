"""

"""
import math
import pymunk
from pymunk.vec2d import Vec2d
import random
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType


class Ball(pymunk.Body):
    def __init__(self, space: pymunk.Space, position: Vec2d, collision_type: CollisionType):
        """

        :param space:
        :param position:
        :param collision_type:
        """
        super().__init__(mass=1, moment=pymunk.inf)

        radius = 10
        player_height = 8

        offset_y = player_height + radius

        self.position = position.x, position.y + offset_y

        shape = pymunk.Circle(self, radius=radius)
        shape.elasticity = 1.00
        shape.collision_type = collision_type

        self.spc = space
        self.on_paddle = True

        self.velocity_func = self.constant_velocity

        self.joint = pymunk.GrooveJoint(space.static_body, self, (100, 100 + offset_y), (1180, 100 + offset_y), (0, 0))

        space.add(self, shape, self.joint)

    def shoot(self):
        """

        :return:
        """
        self.on_paddle = False
        self.space.remove(self.joint)
        # random impulsion
        angle = random.uniform(0 + math.pi / 8.0, math.pi - math.pi / 8.0)
        # intensity of the impulse doesn't not really matter
        # because with normalize the velocity (of the ball) after ...
        intensity = 1
        impulse = Vec2d(1, 0).rotated(angle) * intensity
        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.Body.apply_impulse_at_local_point
        self.apply_impulse_at_local_point(impulse)

    def constant_velocity(self, body: pymunk.Body, gravity, damping, dt):
        """
        http://www.pymunk.org/en/latest/pymunk.html#pymunk.Body.velocity_func

        :param body:
        :param gravity:
        :param damping:
        :param dt:
        :return:
        """
        body.velocity = body.velocity.normalized() * 500
