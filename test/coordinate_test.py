import pytest # type: ignore

from src.coordinate import Coordinate

class TestCoordinate:
    DEFAULT_X = 5
    DEFAULT_Y = 6

    def get_coordinate(self):
        coordinate = (self.DEFAULT_X, self.DEFAULT_Y)
        return Coordinate(coordinate)

    def test_create_coordinate(self):
        assert type(Coordinate(5, 5)).__name__ == 'Coordinate'

    def test_coordinate_has_x(self):
        assert self.get_coordinate().x == self.DEFAULT_X

    def test_coordinate_has_y(self):
        assert self.get_coordinate().y == self.DEFAULT_Y

    def test_coordinate_can_provide_up_coordinate(self):
        coordinate = (self.DEFAULT_X, self.DEFAULT_Y - 1)
        up_coordinate = Coordinate(coordinate)
        assert self.get_coordinate().get_up() == up_coordinate

    def test_coordinate_can_provide_down_coordinate(self):
        coordinate = (self.DEFAULT_X, self.DEFAULT_Y + 1)
        down_coordinate = Coordinate(coordinate)
        assert self.get_coordinate().get_down() == down_coordinate

    def test_coordinate_can_provide_right_coordinate(self):
        coordinate = (self.DEFAULT_X + 1, self.DEFAULT_Y)
        right_coordinate = Coordinate(coordinate)
        assert self.get_coordinate().get_right() == right_coordinate

    def test_coordinate_can_provide_left_coordinate(self):
        coordinate = (self.DEFAULT_X - 1, self.DEFAULT_Y)
        left_coordinate = Coordinate(coordinate)
        assert self.get_coordinate().get_left() == left_coordinate

    def test_immutability_of_coordinates(self):
        coordinate = self.get_coordinate()
        with pytest.raises(AttributeError):
            coordinate.x = coordinate.x - 1
        with pytest.raises(AttributeError):
            coordinate.y = coordinate.y + 1

    def test_coordinates_can_be_compared(self):
        coordinate_a = Coordinate(4,5)
        coordinate_b = Coordinate(4,5)
        # Coordinate objects are unique.
        assert coordinate_a is not coordinate_b
        # Coordinates are comparable based on x and y values.
        assert coordinate_a == coordinate_b

        coordinate_c = Coordinate(5,4)
        assert coordinate_a != coordinate_c

        coordinate_d = (coordinate_a.x, coordinate_a.y)
        # Coordinates can only be compared against other coordinates.
        assert (coordinate_a == coordinate_d) is not True
        assert coordinate_a != coordinate_d

    def test_coordinate_can_get_distance_to_other_coordinates(self):
        a = Coordinate(0,0)
        b = Coordinate(0,5)
        assert a.get_distance_from(b) == 5

        b = Coordinate(0,10)
        assert a.get_distance_from(b) == 10

        b = Coordinate(5,0)
        assert a.get_distance_from(b) == 5

        b = Coordinate(3,4)
        assert a.get_distance_from(b) == 5

        b = Coordinate(6,8)
        assert a.get_distance_from(b) == 10

        a = Coordinate(5,5)
        b = Coordinate(23, 29)
        assert a.get_distance_from(b) == 30


