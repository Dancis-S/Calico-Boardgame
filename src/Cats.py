"""Module for defining the Cat class used in the Calico game.

Each Cat object represents a cat in the game with specific attributes like name, score, etc.
"""

class Cat:
    def __init__(self, name: str, score: int, num_of_tiles: int):
        """
        Initialize a new Cat with a name, score, and the number of tiles.

        :param name: The name of the cat.
        :param score: The score associated with the cat.
        :param num_of_tiles: The number of tiles needed for the cat.
        """
        self.name = name
        self.score = score
        self.num_of_tiles = num_of_tiles
        self.pattern_1 = None
        self.pattern_2 = None
        self.num_of_cats = 0

    def get_patterns(self) -> list:
        """
        Get the patterns assigned to this cat.

        :return: A list containing the patterns of this cat.
        """
        return [self.pattern_1, self.pattern_2]
