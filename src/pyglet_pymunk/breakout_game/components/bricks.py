"""

"""
import pymunk


class Bricks:
    def __init__(self, space: pymunk.Space, collision_type_for_brick, collision_type_for_ball):
        """

        :param space:
        :param collision_type_for_brick:
        """
        brick_width = 100
        brick_height = 16

        x_space_between_brick = 10
        brick_step_x = brick_width + x_space_between_brick

        y_space_between_brick = 14
        brick_step_y = brick_height + y_space_between_brick

        for x in range(10):
            pos_x = x*brick_step_x + 90
            for y in range(10):
                pos_y = y*brick_step_y + 500
                # http://www.pymunk.org/en/latest/pymunk.html#pymunk.Body.__init__
                body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                # position
                body.position = pos_x, pos_y
                # shape
                # shape = pymunk.Poly.create_box(body, (brick_width, brick_height))
                shape = pymunk.Segment(body, (0, 0), (100, 0), 8)
                shape.elasticity = 1.00
                shape.collision_type = collision_type_for_brick
                space.add(body, shape)

        handler = space.add_collision_handler(collision_type_for_brick, collision_type_for_ball)
        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler.separate
        handler.separate = self._cb_remove_brick

    def _cb_remove_brick(self, arbiter: pymunk.Arbiter, space: pymunk.Space, data):
        """
        callback function

        :param arbiter:
        :param space:
        :param data:
        :return:
        """
        brick_shape = arbiter.shapes[0]
        space.remove(brick_shape, brick_shape.body)
