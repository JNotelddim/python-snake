import pytest # type: ignore
from src.board import Board
from src.coordinate import Coordinate
from src.snake import Snake

class TestBoard:
    def get_board(self):
        width = 15
        snakes = [{
            "body": [(2, 2), (2,3), (3,3)],
            "health": 10,
            "id": "asdf1234"
        }]
        foods = [
            (10, 5),
            (6, 12)
        ]
        return Board({
            "snakes": snakes,
            "food": foods,
            "width": width
        })

    def test_create_board(self):
        assert type(Board({})).__name__ == "Board"

    def test_board_has_snakes(self):
        board = self.get_board()
        assert board.snakes == [Snake({
            "body": [(2, 2), (2,3), (3,3)],
            "health": 10,
            "id": "asdf1234"
        })]

    def test_board_has_foods(self):
        assert self.get_board().foods == [
            Coordinate(10, 5),
            Coordinate(6, 12)
        ]

    def test_board_has_width(self):
        assert self.get_board().width == 15

    def test_coordinate_is_in_bounds(self):
        board = self.get_board()

        coordinate = Coordinate(-1,0)
        assert board.is_coordinate_in_bounds(coordinate) == False

        coordinate = Coordinate(0,-1)
        assert board.is_coordinate_in_bounds(coordinate) == False

        coordinate = Coordinate(15, 0)
        assert board.is_coordinate_in_bounds(coordinate) == False

        coordinate = Coordinate(0, 15)
        assert board.is_coordinate_in_bounds(coordinate) == False

        coordinate = Coordinate(0, 14)
        assert board.is_coordinate_in_bounds(coordinate) == True

        coordinate = Coordinate(14, 0)
        assert board.is_coordinate_in_bounds(coordinate) == True

    def test_board_can_advance_snake(self):
        board = self.get_board()

        path = [
            Coordinate(3,2),
            Coordinate(4,2),
            Coordinate(5,2),
            Coordinate(6,2),
            Coordinate(7,2),
            Coordinate(8,2),
            Coordinate(9,2),
            Coordinate(10,2),
            Coordinate(10,3),
            Coordinate(10,4),
            Coordinate(10,5)
        ]

        new_board = board.advance_snake_along_path(board.snakes[0].id, path)
        new_snake_coords = new_board.snakes[0].coordinates
        assert new_snake_coords[0] == Coordinate(10,5)
        assert new_snake_coords[1] == Coordinate(10,4)
        assert new_snake_coords[2] == Coordinate(10,3)
        assert new_snake_coords[3] == Coordinate(10,3)
        assert len(new_snake_coords) == 4
