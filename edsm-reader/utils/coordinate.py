class Coordinate:
    _x: float
    _y: float
    _z: float

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    def is_outside_limit(self, x_origin: float, y_origin: float, z_origin: float,
                         limit: int) -> bool:
        x_criteria = True
        y_criteria = True
        z_criteria = True
        if (x_origin + limit) > self._x > (x_origin - limit):
            x_criteria = False

        if (y_origin + limit) > self._y > (y_origin - limit):
            y_criteria = False

        if (z_origin + limit) > self._z > (z_origin - limit):
            z_criteria = False

        return x_criteria and y_criteria and z_criteria
