"""

"""
import pymunk
#
from pyglet_pymunk.breakout_game.components.collision_types import CollisionType


class Player(pymunk.Body):
    """

    """
    def __init__(self, space: pymunk.Space, collision_type: CollisionType):
        """

        :param space:
        :param collision_type:
        """
        super().__init__(mass=10, moment=pymunk.inf)
        self.position = 640, 100
        shape = pymunk.Segment(self, (-50, 0), (50, 0), 8)
        shape.elasticity = 1.00
        shape.collision_type = collision_type

        joint = pymunk.GrooveJoint(space.static_body, self, (100, 100), (1180, 100), (0, 0))

        space.add(self, shape, joint)
