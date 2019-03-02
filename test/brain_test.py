import pytest # type: ignore
import copy # type: ignore
from src.brain import Brain
from src.board import Board
from src.coordinate import Coordinate

class TestBrain:
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

    def test_brain_can_get_nearest_food(self):
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        assert brain.get_nearest_food() == Coordinate(10,5)

        brain_no_food = self.get_brain(self.main_snake, [], self.width)
        assert brain_no_food.get_nearest_food() is None

    def test_brain_can_get_valid_moves(self):
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        assert brain.get_valid_moves() == ["left", "right", "up"]

    def test_brain_can_avoid_headons(self):

        two_close_snakes = self.main_snake + self.equal_snake
        brain = self.get_brain(two_close_snakes, self.foods, self.width)

        assert brain.get_threatening_snakes_moves() == [
            Coordinate(2,1),
            Coordinate(4,1),
            Coordinate(3,0),
            Coordinate(3,2),
        ]
        assert brain.get_valid_moves() == ["left"]

        snake_and_smol_snek = self.main_snake + self.smol_snek
        unthreatened_brain = self.get_brain(snake_and_smol_snek , self.foods, self.width)
        assert unthreatened_brain.get_threatening_snakes_moves() == []
        assert unthreatened_brain.get_valid_moves() == ["left", "right", "up"]

    def test_brain_can_path_to_nearest_food(self):
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        nearest_food = brain.get_nearest_food()
        assert brain.get_moves_to(nearest_food) == ["right", "down"]

    def test_brain_can_make_decision(self):
        brain = self.get_brain(self.main_snake + self.equal_snake, self.foods, self.width)
        assert brain.get_decision() == "left"

        brain = self.get_brain(self.main_snake, self.foods, self.width)
        assert brain.get_decision() == "right"

    def test_brain_dies_when_stuck(self):
        stuck_snake = list(copy.deepcopy(self.main_snake))
        stuck_snake[0]["body"] = [(1,0), (0,0), (0,1)]

        blocking_snake = list(copy.deepcopy(self.equal_snake))
        blocking_snake[0]["body"] = [(0,2),(1,2),(1,1),(2,1),(2,0),(3,0)] 

        brain = self.get_brain(stuck_snake + blocking_snake, self.foods, self.width)
        assert brain.get_decision() == "left"

    def test_brain_can_get_moves_to_coord(self):
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        assert brain.get_moves_to(Coordinate(9,0)) == ["right", "up"]
        assert brain.get_moves_to(Coordinate(9,2)) == ["right"]
        assert brain.get_moves_to(Coordinate(9,9)) == ["right", "down"]
        assert brain.get_moves_to(Coordinate(2,9)) == ["down"]
        assert brain.get_moves_to(Coordinate(0,9)) == ["down", "left"]
        assert brain.get_moves_to(Coordinate(0,2)) == ["left"]
        assert brain.get_moves_to(Coordinate(0,0)) == ["left", "up"]

    #def test_brain_can_follow_wall(self):
    #    #top wall
    #    snake = copy.deepcopy(self.main_snake)
    #    snake[0]["body"] = [(13,0), (12, 0), (11, 0)]
    #    brain = self.get_brain(snake, self.foods, self.width)
    #    assert brain.follow_wall() == "left"
#
#        snake[0]["body"].reverse()
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "right"
#
#        #left wall
#        snake = copy.deepcopy(self.main_snake)
#        snake[0]["body"] = [(0,2), (0,3), (0,4)]
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "up"
#
#        snake[0]["body"].reverse()
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "down"
#
        #bottom wall
#        snake = copy.deepcopy(self.main_snake)
#        snake[0]["body"] = [(1,14), (2,14), (3,14)]
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "left"
#
#        snake[0]["body"].reverse()
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "right"
#
#        #right wall
#        snake = copy.deepcopy(self.main_snake)
#        snake[0]["body"] = [(14,12), (14,11), (14,10)]
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "down"
#
#        snake[0]["body"].reverse()
#        brain = self.get_brain(snake, self.foods, self.width)
#        assert brain.follow_wall() == "up"



    def test_brain_can_follow_tail(self):
        snake = copy.deepcopy(self.main_snake)
        snake[0]["body"] = [(6,5), (6,6), (7,6), (7,7,)]
        brain = self.get_brain(snake, self.foods, self.width)
        assert brain.follow_tail() == ["down", "right"]

        snake[0]["body"].reverse()
        brain = self.get_brain(snake, self.foods, self.width)
        assert brain.follow_tail() == ["up", "left"]

        snake = copy.deepcopy(self.main_snake)
        snake[0]["body"] = [(6,5), (6,6), (7,6), (7,7,), (7,8), (6,8), (5,8), (4,8)]
        brain = self.get_brain(snake, self.foods, self.width)
        assert brain.follow_tail() == ["down", "left"]

        snake[0]["body"].reverse()
        brain = self.get_brain(snake, self.foods, self.width)
        assert brain.follow_tail() == ["up", "right"]


#    def test_brain_can_circle_perimeter(self):
#        assert 1 == 2

#    def test_brain_can_go_to_nearest_wall(self):
#        #quadrant 1
#        q1_snake = copy.deepcopy(self.main_snake)
#        q1_snake[0]["body"] = [(12, 1), (13, 1), (13, 2)]
#        q1_brain = self.get_brain(q1_snake, self.foods, self.width)
#        assert q1_brain.go_to_nearest_wall() == "up"
#
#        q1_snake[0]["body"].reverse()
#        q1_brain = self.get_brain(q1_snake, self.foods, self.width)
#        assert q1_brain.go_to_nearest_wall() == "right"
#
#        #quadrant 2
#        q2_snake = copy.deepcopy(q1_snake)
#        q2_snake[0]["body"] = [(2, 1), (1, 1), (1, 2)]
#        q2_brain = self.get_brain(q2_snake, self.foods, self.width)
#        assert q2_brain.go_to_nearest_wall() == "up"
#
#        q2_snake[0]["body"].reverse()
#        q2_brain = self.get_brain(q2_snake, self.foods, self.width)
#        assert q2_brain.go_to_nearest_wall() == "left"
#
#        #quadrant 3
#        q3_snake = copy.deepcopy(q1_snake)
#        q3_snake[0]["body"] = [(1, 12), (1, 13), (2, 13)]
#        q3_brain = self.get_brain(q3_snake, self.foods, self.width)
#        assert q3_brain.go_to_nearest_wall() == "left"
#
#        q3_snake[0]["body"].reverse()
#        q3_brain = self.get_brain(q3_snake, self.foods, self.width)
#        assert q3_brain.go_to_nearest_wall() == "down"
#
#        #quadrant 4
#        q4_snake = copy.deepcopy(q1_snake)
#        q4_snake[0]["body"] = [(12, 13), (13, 13,), (13, 12)]
#        q4_brain = self.get_brain(q4_snake, self.foods, self.width)
#        assert q4_brain.go_to_nearest_wall() == "down"
#
#        q4_snake[0]["body"].reverse()
#        q4_brain = self.get_brain(q4_snake, self.foods, self.width)
#        assert q4_brain.go_to_nearest_wall() == "right"

    def test_brain_can_tell_if_snake_is_greatest_length(self):
        #snake = copy.deepcopy(self.main_snake)
        #snake[0]["body"] = [(6,5), (6,6), (7,6), (7,7,)]
        brain = self.get_brain(self.main_snake, self.foods, self.width)
        assert brain.get_snake_is_safe_length() == True

        brain = self.get_brain(self.main_snake+self.smol_snek, self.foods, self.width)
        assert brain.get_snake_is_safe_length() == False

        brain = self.get_brain(self.main_snake+self.equal_snake, self.foods, self.width)
        assert brain.get_snake_is_safe_length() == False

        bigger_snek = copy.deepcopy(self.main_snake)
        bigger_snek[0]["body"] = [(2,2), (2,3), (3,3), (3,4)]
        brain = self.get_brain(bigger_snek+self.smol_snek, self.foods, self.width)
        assert brain.get_snake_is_safe_length() == True

        brain = self.get_brain(self.smol_snek+bigger_snek, self.foods, self.width)
        assert brain.get_snake_is_safe_length() == False
