"""Snake Module"""
from typing import List, Optional
from src.coordinate import Coordinate

class Snake:
    """Define properties and functionality of a Snake."""
    def __init__(self, data: dict) -> None:
        self._data = data
        self._coordinates: Optional[List[Coordinate]] = None

    def __eq__(self, other: object) -> bool:
        """Return true if the snake id, health, and coordinates match."""
        if not isinstance(other, Snake):
            return NotImplemented
        return self.id == other.id

    def __str__(self) -> str:
        return str(self.id) + "; " + str(self.health) + "; " + str(self.coordinates)

    @property
    def id(self) -> str:
        """Get the id of the snake."""
        return self._data["id"]

    @property
    def coordinates(self) -> List[Coordinate]:
        """Get the List of Coordinates which describes the location of this Snake."""
        if not self._coordinates:
            self._coordinates = [Coordinate(coordinate_tuple) for coordinate_tuple in self._data['body']]
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates

    @property
    def head(self) -> Coordinate:
        """Get the coordinate which represents the location of this Snake's head."""
        return self.coordinates[0]

    @property
    def body(self) -> List[Coordinate]:
        """Get the List of Coordinates which respresents this Snake's body (not head)."""
        return self.coordinates[1:]

    @property
    def health(self) -> int:
        """Get the number of health points this Snake currently has."""
        return self._data['health']

    def contains_coordinate(self, coordinate) -> bool:
        """Get whether or not the given Coordinate is within this Snake."""
        return coordinate in self.coordinates

    def get_all_moves(self) -> List[Coordinate]:
        """Get list of coordinates for left, right, up, down, of the snake's head - regardless of whether or not it kills the snake."""
        return self.head.get_neighbours()
