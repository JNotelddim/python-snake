"""Brain Module"""
import math # type: ignore
from operator import itemgetter
from typing import List, Optional
from src.snake import Snake
from src.board import Board
from src.coordinate import Coordinate
from src.cerebellum import Cerebellum


class Brain:
    """Control which move the snake makes."""
    def __init__(self, my_id: str, board: Board) -> None:
        self.hunger_threshold = 45
        self.board: Board = board
        self.my_id: str = my_id
        self.other_snakes: List[Snake] = self.board.get_other_snakes(my_id)
        self.me: Snake = next((snake for snake in self.board.snakes if snake.id == my_id))
        self.cerebellum = Cerebellum(self.me, self.board)

    def get_decision(self) -> str:
        """Get the move which the snake will make this turn."""
        valid_moves = self.get_valid_moves()
        decision = None
        tail = self.me.coordinates[-1]

        # in case the head is right next to the tail, if there aren't any valid moves, move towards tail
        if not valid_moves:
            path = self.cerebellum.get_path(tail)
            if not path:
                return self.follow_tail()[0]
            return self.get_moves_to(path[0])[0]

        if not self.get_snake_is_safe_length() or self.me.health < self.hunger_threshold:
            nearest_food = self.get_nearest_food()
            if nearest_food is not None:
                path_to_nearest_food = self.cerebellum.get_path(nearest_food)
                moves_for_first_path_step = self.get_moves_to(path_to_nearest_food[0])
                #TODO: keep checking
                decision = next((move for move in moves_for_first_path_step if move in valid_moves), None)

        else:
            tail_path = self.cerebellum.get_path(tail)
            if tail_path is None or len(tail_path) == 0:
                return self.follow_tail()[0]

            first_in_tail_path = tail_path[0]
            loop_moves = self.get_moves_to(first_in_tail_path)

            if loop_moves:
                decision = next((move for move in loop_moves if move in valid_moves), None)
 
        if not decision:
            decision = valid_moves[0]

        return decision
 
    def get_valid_moves(self) -> List[str]:
        """Return the moves which won't immediately get the snake killed."""
        moves = self.get_valid_moves_helper(True)

        if not moves or not len(moves):
            moves = self.get_valid_moves_helper(False)
        return moves

    def get_valid_moves_helper(self, avoid_collisions: bool) -> List[str]:
        """Return moves which are deemed valid, option to not avoid headons"""
        moves = ["left", "right", "up", "down"]
        valid_moves = []
        collision_coordinates = [coordinate for snake in self.board.snakes for coordinate in snake.coordinates] #snake.coordinates[:-1]]
        if avoid_collisions:
            collision_coordinates = collision_coordinates + self.get_threatening_snakes_moves()

        #remove this snake's tail from array of "invalid moves"
        tail = self.me.coordinates[-1]
        if tail in collision_coordinates:
            collision_coordinates.remove(tail)

        for move in moves:
            move_coordinate = getattr(self.me.head, "get_"+move)()
            if self.board.is_coordinate_in_bounds(move_coordinate) and move_coordinate not in collision_coordinates:
                valid_moves.append(move)

        return valid_moves


    def get_nearest_food(self) -> Optional[Coordinate]:
        """Get the food item which has coordinates closest to this snake's head."""
        closest_food = (Coordinate((0,0)), 9999.0)

        for food in self.board.foods:
            x_diff = self.me.head.x - food.x
            y_diff = self.me.head.y - food.y
            distance = math.sqrt( x_diff * x_diff + y_diff * y_diff )

            if distance < closest_food[1]:
                closest_food = (food, distance)

        if closest_food[1] == 9999.0:
            return None

        return closest_food[0]

    def get_threatening_snakes_moves(self) -> List[Coordinate]:
        """Get the coordinates which will result in head-on collisions.""" 
        #note, we can ignore snakes smaller than us.
        danger_snakes = [snake for snake in self.board.get_other_snakes(self.my_id) if len(snake.coordinates) >= len(self.me.coordinates)]
        return [snake_moves for snake in danger_snakes for snake_moves in snake.get_all_moves()]

    def follow_tail(self) -> List[str]:
        """Get moves for getting to tail."""
        tail = self.me.coordinates[-1]
        return self.get_moves_to(tail)

    def get_moves_to(self, coord: Coordinate) -> List[str]:
        """Get move options for getting to given coordinate."""
        options = []
        x_diff = self.me.head.x - coord.x
        y_diff = self.me.head.y - coord.y

        if x_diff > 0:
            options.append('left')
        elif x_diff < 0:
            options.append('right')

        if y_diff > 0:
            options.append('up')
        elif y_diff < 0:
            options.append('down')

        if abs(y_diff) > abs(x_diff):
            options.reverse()
        return options

    def get_snake_is_safe_length(self) -> bool:
        """Get whether snake is longest on board (by 2)."""
        for snake in self.other_snakes:
            if len(snake.coordinates) > len(self.me.coordinates) - 2:
                return False

        return True
