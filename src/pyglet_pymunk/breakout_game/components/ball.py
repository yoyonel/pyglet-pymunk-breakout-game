"""

"""
import math
import pymunk
from pymunk.vec2d import Vec2d
import random
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType
from pyglet_pymunk.breakout_game.components.paddle import Paddle
#
from pyglet_pymunk.breakout_game.components.aspect_ratio import AspectRatio


class Ball(pymunk.Body):
    def __init__(
            self,
            space: pymunk.Space,
            paddle_position: Vec2d,
            collision_type: CollisionType,
            aspect_ratio: AspectRatio,
            mass: float=1,
            paddle: Paddle=None,
    ):
        """

        :param space:
        :param paddle_position:
        :param collision_type:
        :param aspect_ratio:
        :param mass:
        :param paddle:
        """
        super().__init__(mass=mass, moment=pymunk.inf)

        self.aspect_ratio = aspect_ratio

        self.radius = 16 * 1

        paddle_height = 16
        paddle_half_height = paddle_height

        ball_position = Vec2d(
            paddle_position.x,
            paddle_position.y + aspect_ratio.scale_s(paddle_half_height + self.radius)
        )
        self.position = ball_position

        shape = pymunk.Circle(self, radius=aspect_ratio.scale_s(self.radius))
        shape.elasticity = 0.98
        shape.collision_type = collision_type
        shape.filter = pymunk.ShapeFilter(categories=2 << collision_type)

        self.spc = space
        self.on_paddle = True

        self.velocity_func = self.constant_velocity

        self.joint = pymunk.GrooveJoint(
            space.static_body,
            self,
            Vec2d(paddle.groove_joint.groove_a.x, ball_position.y),
            Vec2d(paddle.groove_joint.groove_b.x, ball_position.y),
            Vec2d(0, 0),
        )
        space.add(self, shape, self.joint)

        self.ball_speed = 500

        self.segments_q = []
        self.points_on_ball = []

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
        intensity = 500
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
        body_velocity_normalized = body.velocity.normalized()
        #
        body.velocity = body_velocity_normalized * self.aspect_ratio.scale_s(self.ball_speed)

        self.raycast_ball_over_the_world(body.position, body_velocity_normalized)

    def raycast_ball_over_the_world(
            self,
            ball_position,
            ball_velocity_normalized
    ):
        shapes_filter = pymunk.ShapeFilter(
            # mask=pymunk.ShapeFilter.ALL_MASKS
            mask=pymunk.ShapeFilter.ALL_MASKS ^ (2 << CollisionType.BALL)
        )

        body_velocity_normalized_ortho = ball_velocity_normalized.rotated(+math.pi / 2.0)

        ball_radius_scaled = self.aspect_ratio.scale_s(self.radius * 1.00)

        self.points_on_ball = [
            ball_position + body_velocity_normalized_ortho * ball_radius_scaled,
            ball_position - body_velocity_normalized_ortho * ball_radius_scaled,
            ball_position + ball_velocity_normalized * ball_radius_scaled
        ]

        wall_left = 50
        wall_right = 1230
        wall_top = 800
        wall_bottom = 50
        raycast_distance = self.aspect_ratio.scale(
            wall_right - wall_left,
            wall_top - wall_bottom
        ).length

        self.segments_q = [
            self.space.segment_query_first(
                point_on_ball,
                point_on_ball + ball_velocity_normalized * raycast_distance,
                1,
                shapes_filter,
            )
            for point_on_ball in self.points_on_ball
        ]
