import pytest # type: ignore
import copy # type: ignore
from src.brain import Brain
from src.board import Board
from src.coordinate import Coordinate
from src.cerebellum import Cerebellum

class TestCerebellum:
    width: int = 15
    main_snake = [{
        "body": [(2, 2), (2,3), (3,3)],
        "health": 10,
        "id": "asdf1234"
    }]
    #don't try to use equal_snake and smol_snek in the same game (they're in the same spot)
    equal_snake = [{
        "body": [(3, 1), (4,1), (4,2)],
        "health": 10,
        "id": "fdfdssdsssdfd"
    }]
    smol_snek = [{
        "body": [(3, 1), (4,1)],
        "health": 10,
        "id": "fdfdssds"
    }]
    foods = [
        ((10, 5)),
        ((6, 12))
    ]

    def get_brain(self, snakes, foods, width):
        board = Board({
            "snakes": snakes,
            "food": foods,
            "width": width,
            "height": width,
        })
        return Brain(board.snakes[0].id, board)

    def test_cerebellum_get_path(self):
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        cereb = Cerebellum(brain.me, brain.board, "breadth_first")
        path = cereb.get_path(Coordinate(10,6))
        assert path == [
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
            Coordinate(10,5),
            Coordinate(10,6)
        ]

    def test_cerebellum_breadth_first_path(self):
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        cereb = Cerebellum(brain.me, brain.board, "breadth_first")
        path = cereb.get_path(Coordinate(10,5))

        assert path == [
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

        path_2 = cereb.get_path(Coordinate(0,5))

        assert path_2 == [
            Coordinate(1,2),
            Coordinate(0,2),
            Coordinate(0,3),
            Coordinate(0,4),
            Coordinate(0,5)
        ]

