"""

"""
import math
import pymunk
from pymunk.vec2d import Vec2d
import random
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType


class Ball(pymunk.Body):
    def __init__(
            self,
            space: pymunk.Space,
            player_position: Vec2d,
            collision_type: CollisionType,
            aspect_ratio,
            mass=1,
            player=None,
    ):
        """

        :param space:
        :param player_position:
        :param collision_type:
        :param aspect_ratio:
        :param mass:
        :param player:
        """
        super().__init__(mass=mass, moment=pymunk.inf)

        self.aspect_ratio = aspect_ratio

        radius = 20

        player_height = 16
        player_half_height = player_height

        ball_position = Vec2d(
            player_position.x,
            player_position.y + aspect_ratio.scale_s(player_half_height + radius)
        )
        self.position = ball_position

        shape = pymunk.Circle(self, radius=aspect_ratio.scale_s(radius))
        shape.elasticity = 0.98
        shape.collision_type = collision_type

        self.spc = space
        self.on_paddle = True

        self.velocity_func = self.constant_velocity

        self.joint = pymunk.GrooveJoint(
            space.static_body,
            self,
            Vec2d(player.joint_groove_a.x, ball_position.y),
            Vec2d(player.joint_groove_b.x, ball_position.y),
            Vec2d(0, 0),
        )
        space.add(self, shape, self.joint)

        self.ball_speed = 500

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
        body.velocity = body.velocity.normalized() * self.aspect_ratio.scale_s(self.ball_speed)
