class Coordinate:
    _x: float
    _y: float
    _z: float

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    def is_outside_limit(self, x_origin: float, y_origin: float, z_origin: float,
                         radius: int) -> bool:
        '''
        check if coordinates (x, y, z) set within class are outside a radius
        :param x_origin: x center coordinate
        :param y_origin: y center coordinate
        :param z_origin: z center coordinate
        :param radius: the radius of exclusion
        :return: True if coordinates are within (False by default)
        '''
        if radius != 0:
            x_criteria = True
            y_criteria = True
            z_criteria = True
            if (x_origin + radius) > self._x > (x_origin - radius):
                x_criteria = False

            if (y_origin + radius) > self._y > (y_origin - radius):
                y_criteria = False

            if (z_origin + radius) > self._z > (z_origin - radius):
                z_criteria = False

            return x_criteria and y_criteria and z_criteria
        return False
