"""

"""
import attr
import pymunk
from pymunk.vec2d import Vec2d
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType


@attr.s
class GroovJoint:
    groove_a: Vec2d = attr.ib()
    groove_b: Vec2d = attr.ib()
    anchor: Vec2d = attr.ib(default=Vec2d())


class Paddle(pymunk.Body):
    """

    """
    def __init__(
            self,
            space: pymunk.Space,
            collision_type: CollisionType,
            aspect_ratio,
            mass=10
    ):
        """

        :param space:
        :param collision_type:
        :param aspect_ratio:
        :param mass:
        """
        super().__init__(mass=mass, moment=pymunk.inf)

        wall_left = 50
        wall_right = 1230
        wall_bottom = 50

        paddle_width = 100
        paddle_height = 16
        paddle_half_width = paddle_width // 2
        paddle_half_height = paddle_height // 2

        paddle_position = Vec2d(640, wall_bottom + paddle_height * 3)
        self.position = aspect_ratio.scale_V2d(paddle_position)

        shape = pymunk.Segment(
            self,
            aspect_ratio.scale(-paddle_half_width, 0),
            aspect_ratio.scale(+paddle_half_width, 0),
            aspect_ratio.scale_s(paddle_half_height)
        )
        # shape = pymunk.Poly.create_box(self, (paddle_width, paddle_height))

        shape.elasticity = 1.00
        shape.collision_type = collision_type
        shape.filter = pymunk.ShapeFilter(categories=2 << collision_type)

        self.groove_joint = GroovJoint(
            aspect_ratio.scale(wall_left + paddle_half_width * 1.50, paddle_position.y),
            aspect_ratio.scale(wall_right - paddle_half_width * 1.50, paddle_position.y),
        )

        self.joint = pymunk.GrooveJoint(
            space.static_body,
            self,
            self.groove_joint.groove_a,
            self.groove_joint.groove_b,
            self.groove_joint.anchor,
        )

        space.add(self, shape, self.joint)
