"""

"""
from pymunk.vec2d import Vec2d


class AspectRatio:
    """

    """
    def __init__(self, src_sizes: Vec2d, dst_sizes: Vec2d):
        self.aspect_ratio = Vec2d(
            dst_sizes[0] / src_sizes[0],
            dst_sizes[1] / src_sizes[1],
        )   # type: Vec2d

    def scale(self, x, y) -> Vec2d:
        return Vec2d(
            int(x * self.aspect_ratio[0]),
            int(y * self.aspect_ratio[1]),
        )

    def scale_V2d(self, v: Vec2d) -> Vec2d:
        return self.scale(v.x, v.y)

    def scale_s(self, scalar: float) -> float:
        return self.scale(scalar, 0).x


class DtRatio:
    """

    """
    def __init__(self, dt_for_display: float, dt_for_physicx: float):
        self.dt_for_display = dt_for_display
        self.dt_for_physicx = dt_for_physicx
        self.dt_ratio = dt_for_physicx / dt_for_display

    def scale(self, dt) -> float:
        return dt * self.dt_ratio
