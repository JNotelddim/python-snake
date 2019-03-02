"""Pathfinding Module"""
import pdb
import copy
from queue import Queue
from typing import List, Optional
from src.snake import Snake
from src.board import Board
from src.coordinate import Coordinate


class Cerebellum:
    """Find paths to given coordinates."""
    def __init__(self, me: Snake, board: Board, selected_algorithm: Optional[str] = None) -> None:
        self.selected_algorithm: str = selected_algorithm if selected_algorithm is not None else "breadth_first"
        self.me = me
        self.board: Board = copy.deepcopy(board)

    def get_path(self, coordinate: Optional[Coordinate] = None, coordinates: Optional[List[Coordinate]] = None) -> List[Coordinate]:
        """Find path to given coordinate/coordinates based on pathfinder's selected algorithm."""

        if coordinates is None:
            if coordinate is None:
                return []
            coordinates = [coordinate]

        path: List[Coordinate] = []

        if self.selected_algorithm == 'breadth_first':
            path = self.__get_breadth_first_path(coordinates)

#        elif self.selected_algorithm == 'djikstra\'s':
#            path = self.__get_djikstras_path(coordinates)

#        elif self.selected_algorithm == 'a*':
#            path = self.__get_a_star_path(coordinates)

        return path

    def __get_breadth_first_path(self, coordinates: List[Coordinate], board: Optional[Board] = None) -> List[Coordinate]:
        """Find path using breadth-first algorithm."""

        #pick location from grid (self.me.head)
        #expand that location by looking at neighbours
        #any unvisited neighbours are added to "unexplored" and "visited" set

        board = self.board if not board else board
        start = self.me.head

        unexplored: Queue = Queue()
        unexplored.put(start)
        came_from: dict = {}
        came_from[str(start)] = None

        collision_coordinates = [coordinate for snake in board.snakes for coordinate in snake.coordinates]

        #remove this snake's tail from array of "invalid moves"
        tail = self.me.coordinates[-1]
        if tail in collision_coordinates:
            collision_coordinates.remove(tail)


        matched = False
        while not unexplored.empty():
            current = unexplored.get()

            if any(coord == current for coord in coordinates):
                if current != tail:
                    from_path = self.__get_path_from_current(current, start, came_from)
                    tail_path = self.__get_breadth_first_path([tail], board.advance_snake_along_path(self.me.id, from_path))
                    if tail_path:
                        matched = True
                        break
                else:
                    matched = True
                    break

            valid_move_coordinatees = [coord for coord in current.get_neighbours() if board.is_coordinate_in_bounds(coord) and coord not in collision_coordinates]
            #also need to account for snakebodies

            for neighbour in valid_move_coordinatees:
                if not str(neighbour) in came_from:
                    unexplored.put(neighbour)
                    came_from[str(neighbour)] = current

        if current is not None and matched:
            path = self.__get_path_from_current(current, start, came_from)
            return path
        else:
            return []

#    def __get_djikstras_path(self, coordinates: List[Coordinate]) -> List[Coordinate]:
#        """Find path using djikstra's algorithm."""
#
#        raise NotImplementedError("Gotta write the code first!")
#        return []
#
#    def __get_a_star_path(self, coordinates: List[Coordinate]) -> List[Coordinate]:
#        """Find path using A* algorithm."""
#
#        raise NotImplementedError("Gotta write the code first!")
#        return []

    def __get_path_from_current(self, current: Coordinate, start: Coordinate, came_from: dict) -> List[Coordinate]:
        """Given end coord and "came-from" list, return the list of coordinates leading back to start."""
        path = []
        while current != start: 
            path.append(current)
            current = came_from[str(current)]
        path.reverse() # optional

        return path
