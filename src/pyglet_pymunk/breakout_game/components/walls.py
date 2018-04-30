"""

"""
import pymunk


class Walls:
    def __init__(
            self, space: pymunk.Space,
            collision_type_for_ball,
            collision_type_for_bottom,
            cb_reset_game,
    ):
        """

        :param space:
        :param collision_type_for_ball:
        :param collision_type_for_bottom:
        :param cb_reset_game: call back function to reset game
        """

        left = pymunk.Segment(space.static_body, (50, 110), (50, 800), 2)
        top = pymunk.Segment(space.static_body, (50, 800), (1230, 800), 2)
        right = pymunk.Segment(space.static_body, (1230, 110), (1230, 800), 2)

        left.elasticity = 0.98
        right.elasticity = 0.98
        top.elasticity = 0.98

        bottom = pymunk.Segment(space.static_body, (50, 50), (1230, 50), 2)
        bottom.sensor = True
        bottom.collision_type = collision_type_for_bottom

        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler
        handler = space.add_collision_handler(collision_type_for_ball, collision_type_for_bottom)
        handler.begin = self.reset_game
        self.cb_reset_game = cb_reset_game

        space.add(left, top, right, bottom)

    def reset_game(self, arbiter, space, data) -> bool:
        """
        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler

        :param arbiter:
        :param space:
        :param data:
        :return:
        """
        self.cb_reset_game()
        return True
