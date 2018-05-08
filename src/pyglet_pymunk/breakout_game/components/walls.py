"""

"""
import pymunk


class Walls:
    def __init__(
            self, space: pymunk.Space,
            collision_type_for_ball,
            collision_type_for_bottom,
            cb_loose_ball,
            aspect_ratio
    ):
        """

        :param space:
        :param collision_type_for_ball:
        :param collision_type_for_bottom:
        :param cb_loose_ball: call back function to reset game
        """

        left = pymunk.Segment(
            space.static_body,
            aspect_ratio.scale(50, 50),
            aspect_ratio.scale(50, 800),
            2
        )
        top = pymunk.Segment(
            space.static_body,
            aspect_ratio.scale(50, 800),
            aspect_ratio.scale(1230, 800),
            2
        )
        right = pymunk.Segment(
            space.static_body,
            aspect_ratio.scale(1230, 50),
            aspect_ratio.scale(1230, 800),
            2
        )

        left.elasticity = 1.0
        right.elasticity = 1.0
        top.elasticity = 1.0

        bottom = pymunk.Segment(
            space.static_body,
            aspect_ratio.scale(50, 50),
            aspect_ratio.scale(1230, 50),
            2
        )
        bottom.sensor = True
        bottom.collision_type = collision_type_for_bottom

        left.filter = pymunk.ShapeFilter(categories=2 << collision_type_for_bottom)
        right.filter = pymunk.ShapeFilter(categories=2 << collision_type_for_bottom)
        top.filter = pymunk.ShapeFilter(categories=2 << collision_type_for_bottom)
        bottom.filter = pymunk.ShapeFilter(categories=2 << collision_type_for_bottom)

        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler
        handler = space.add_collision_handler(collision_type_for_ball, collision_type_for_bottom)
        handler.begin = self.reset_game
        self.cb_loose_ball = cb_loose_ball

        space.add(left, top, right, bottom)

    def reset_game(self, arbiter, space, data) -> bool:
        """
        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler

        :param arbiter:
        :param space:
        :param data:
        :return:
        """
        self.cb_loose_ball(self)
        return True
