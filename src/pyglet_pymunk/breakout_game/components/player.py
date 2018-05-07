"""

"""
import pymunk
from pymunk.vec2d import Vec2d
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType


class Player(pymunk.Body):
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

        player_width = 100
        player_height = 16
        player_half_width = player_width // 2
        player_half_height = player_height // 2

        player_position = Vec2d(640, wall_bottom + player_height * 3)
        self.position = aspect_ratio.scale_V2d(player_position)

        shape = pymunk.Segment(
            self,
            aspect_ratio.scale(-player_half_width, 0),
            aspect_ratio.scale(+player_half_width, 0),
            aspect_ratio.scale_s(player_half_height)
        )

        shape.elasticity = 1.00
        shape.collision_type = collision_type

        self.joint_groove_a = aspect_ratio.scale(wall_left + player_half_width * 1.50, player_position.y)
        self.joint_groove_b = aspect_ratio.scale(wall_right - player_half_width * 1.50, player_position.y)
        self.joint_anchor = aspect_ratio.scale(0, 0)
        self.joint = pymunk.GrooveJoint(
            space.static_body,
            self,
            self.joint_groove_a,
            self.joint_groove_b,
            self.joint_anchor,
        )

        space.add(self, shape, self.joint)
