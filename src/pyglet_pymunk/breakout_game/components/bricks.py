"""

"""
import pymunk
from pymunk import Vec2d


class Bricks:
    def __init__(self, space: pymunk.Space, collision_type_for_brick, collision_type_for_ball, aspect_ratio):
        """

        :param space:
        :param collision_type_for_brick:
        """
        # self.build_grid(space, collision_type_for_brick, collision_type_for_ball, aspect_ratio)
        self.build_dynamic_grid(space, collision_type_for_brick, collision_type_for_ball, aspect_ratio)

    def build_grid(self, space: pymunk.Space, collision_type_for_brick, collision_type_for_ball, aspect_ratio):
        grid_position = aspect_ratio.scale(90, 500)

        brick_size = aspect_ratio.scale(100, 16)
        brick_width = brick_size.x
        brick_height = brick_size.y

        space_between_brick = aspect_ratio.scale(10, 14)
        x_space_between_brick = space_between_brick.x
        brick_step_x = brick_width + x_space_between_brick

        y_space_between_brick = space_between_brick.y
        brick_step_y = brick_height + y_space_between_brick

        for x in range(10):
            pos_x = grid_position.x + x * brick_step_x
            for y in range(10):
                pos_y = grid_position.y + y * brick_step_y
                # http://www.pymunk.org/en/latest/pymunk.html#pymunk.Body.__init__
                body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                # position
                body.position = pos_x, pos_y
                # shape
                shape = pymunk.Segment(
                    body,
                    (0, 0),
                    aspect_ratio.scale(100, 0),
                    8
                )
                shape.elasticity = 0.98
                shape.collision_type = collision_type_for_brick
                space.add(body, shape)

        handler = space.add_collision_handler(collision_type_for_brick, collision_type_for_ball)
        # http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler.separate
        handler.separate = self._cb_remove_brick

    def build_dynamic_grid(self, space: pymunk.Space, collision_type_for_brick, collision_type_for_ball, aspect_ratio):
        wall_left = 50
        wall_right = 1230

        grid_left_corner = aspect_ratio.scale(wall_left + 40, 500)
        grid_right_corner = aspect_ratio.scale(wall_right - 40, 500 + (16+14)*10)

        nb_bricks = Vec2d(12, 8)

        spaces_between_brick = aspect_ratio.scale_V2d(Vec2d(10, 14))

        grid_size = grid_right_corner - grid_left_corner

        brick_size = (grid_size - (nb_bricks - Vec2d(1, 1)) * spaces_between_brick) / nb_bricks

        brick_steps = brick_size + spaces_between_brick

        for x in range(nb_bricks.x):
            pos_x = grid_left_corner.x + x * brick_steps.x
            for y in range(nb_bricks.y):
                pos_y = grid_left_corner.y + y * brick_steps.y

                # https://github.com/viblo/pymunk/blob/master/examples/breakout.py
                # http://www.pymunk.org/en/latest/pymunk.html#pymunk.Body.__init__
                brick_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
                # position
                brick_body.position = Vec2d(pos_x, pos_y) + brick_size * 0.5

                brick_shape = pymunk.Poly.create_box(brick_body, brick_size)

                brick_shape.elasticity = 0.98
                brick_shape.collision_type = collision_type_for_brick
                space.add(brick_body, brick_shape)

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
