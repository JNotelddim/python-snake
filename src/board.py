"""Board Module"""
import copy
from typing import Tuple, List
from src.coordinate import Coordinate
from src.snake import Snake

class Board:
    """Track the cooardinates for all snakes and food in the game."""
    def __init__(self, data):
        self._data = data
        self._snakes = None
        self._foods = None

    @property
    def snakes(self) -> List[Snake]:
        """Retreive the list of snakes from the board data."""
        if self._snakes is None:
            snakes = [Snake(snake_data) for snake_data in self._data['snakes']]
            self._snakes = snakes
        return self._snakes

    @property
    def foods(self) -> List[Coordinate]:
        """Retreive the list of food from the board data."""
        if self._foods is None:
            self._foods = [Coordinate(food_data) for food_data in self._data['food']]
        return self._foods

    @property
    def width(self) -> int:
        """Get width of the board -- note: it's a square."""
        return self._data['width']

    def is_coordinate_in_bounds(self, coordinate) -> bool:
        """Check whether or not the Coordinate is within the bounds of the Board."""
        is_wall = (coordinate.x == -1 or coordinate.x == self.width
                   or coordinate.y == -1 or coordinate.y == self.width)
        return not is_wall

    def get_other_snakes(self, exclude_id) -> List[Snake]:
        """Get the List of Snakes whose IDs don't match the given ID."""
        return [snake for snake in self.snakes if snake.id != exclude_id]

    def advance_snake_along_path(self, snake_id: str, path: List[Coordinate]):
        """Return a new board with our snake advanced along given path."""
        new_board = copy.deepcopy(self)
        return new_board.__help_advance_snake_along_path(snake_id, path)

    def __help_advance_snake_along_path(self, snake_id: str, path: List[Coordinate]):
        """Do the actual advancement of the snake along the path."""
        me = next((snake for snake in self.snakes if snake.id == snake_id), None)
        if not me:
            raise ValueError("No snake for given id!")

        me.coordinates += path
        me.coordinates = me.coordinates[len(path):]
        me.coordinates.reverse()
        me.coordinates.append(me.coordinates[-1])

        print("new coords:")
        for coord in me.coordinates:
            print(coord)
        return self
