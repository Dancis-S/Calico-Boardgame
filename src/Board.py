"""This file contain code related to setting up the board"""
import copy
import random
from src import Tiles, Cats


class Board:
    """Represents the game board, managing its tiles, cats, and other game elements."""

    def __init__(self, player_num: int):
        """Initialize the board for a given player."""
        self.board_colour = "Test"  # This will be set properly in colour_borders
        self.open_positions = [8, 9, 10, 11, 12, 15, 16, 18, 19, 22, 23, 24, 26, 29, 31, 32,
                               33, 36, 37, 38, 39, 40]
        self.buttons = {"Red": 0, "Yellow": 0, "Purple": 0, "Blue": 0, "Green": 0, "Navy": 0}
        self.cats = []
        self.player_num = player_num
        self.board = []

        self.populate_board()
        self.initialise_tiles()
        self.initialise_cats()
        self.colour_borders(player_num)

    def populate_board(self):
        """Populate the board with normal and design goal tiles."""
        for i in range(49):
            self.board.append(Tiles.NormalTile(i))

        requirements = ["NotEqual", "aaa-bbb", "aa-bb-cc", "aaaa-bb", "aaa-bb-c", "aa-bb-c-d"]
        random.shuffle(requirements)
        for idx, req in zip([17, 25, 30], requirements):
            self.board[idx] = Tiles.DesignGoalTile(idx, req)

    def set_cats(self, cats):
        """Set the cat objects for the board."""
        self.cats = copy.deepcopy(cats)

    def initialise_tiles(self):
        """Initialize connections between tiles."""
        for i in range(49):
            self._set_tile_neighbors(i)

    def _set_tile_neighbors(self, i):
        """Set up neighbors for a specific tile."""
        tile = self.board[i]
        offset = 0 if i % 14 >= 7 else -1

        tile.west = None if i % 7 == 0 else self.board[i - 1]
        tile.east = None if i % 7 == 6 else self.board[i + 1]
        tile.north_west = None if i - 7 + offset < 0 else self.board[i - 7 + offset]
        tile.north_east = None if i - 6 + offset < 0 else self.board[i - 6 + offset]
        tile.south_west = None if i + 7 + offset > 48 else self.board[i + 7 + offset]
        tile.south_east = None if i + 8 + offset > 48 else self.board[i + 8 + offset]

    def colour_borders(self, player_num: int):
        """Color the borders of the board based on player number."""

        colours = ["Yellow", "Red", "Purple", "Blue", "Green", "Navy"]
        patterns = ["Stripes", "Leaf", "Dots", "Plants", "Four", "Reeds"]
        borders = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42, 43, 44, 45, 46, 47, 48, 41, 34, 27,
                   20, 13]

        # Board configuration setup
        board_configs = {
            1: self._get_purple_board(),
            2: self._get_blue_board(),
            3: self._get_green_board(),
            4: self._get_yellow_board()
        }

        chosen_board = board_configs.get(player_num, self._get_purple_board())
        self.board_colour = "Random" if player_num not in board_configs else colours[player_num - 1]

        for i, (colour_idx, pattern_idx) in enumerate(chosen_board):
            self.board[borders[i]].colour = colours[colour_idx]
            self.board[borders[i]].pattern = patterns[pattern_idx]

    def _get_purple_board(self):
        return [(0, 3), (1, 2), (2, 3), (0, 1), (3, 0), (1, 4), (4, 2), (3, 4), (5, 0),
                (4, 1), (1, 5), (3, 2), (2, 1), (0, 4), (2, 0), (5, 1), (4, 3), (0, 5),
                (2, 2), (5, 4), (4, 0), (1, 1), (3, 3), (5, 5)]

    def _get_blue_board(self):
        return [(1, 5), (0, 0), (3, 5), (1, 1), (2, 4), (0, 3), (4, 0), (4, 3), (5, 4), (3, 1),
                (2, 0), (0, 2), (2, 3), (3, 4), (1, 3), (5, 1), (4, 5), (1, 2), (3, 0), (5, 3),
                (4, 4), (0, 1), (2, 5), (5, 2)]

    def _get_green_board(self):
        return [(5, 1), (0, 5), (4, 1), (5, 0), (2, 4), (0, 2), (3, 5), (2, 2), (1, 4), (3, 0),
                (0, 3), (2, 5), (4, 0), (5, 2), (4, 4), (1, 0), (3, 1), (5, 3), (4, 5), (1, 2),
                (3, 4), (0, 0), (2, 1), (1, 3)]

    def _get_yellow_board(self):
        return [(4, 4), (5, 3), (0, 0), (2, 2), (5, 5), (4, 1), (1, 4), (1, 1), (2, 5), (0, 2),
                (4, 3), (5, 4), (3, 5), (2, 1), (0, 5), (3, 2), (1, 0), (2, 3), (0, 4), (3, 1),
                (1, 5), (4, 2), (5, 0), (3, 3)]

    def add_tile(self, tile_id: int, colour: str, pattern: str):
        """Add a tile with specified colour and pattern to the board."""
        tile = self.board[tile_id]
        tile.colour = colour
        tile.pattern = pattern
        self.open_positions.remove(tile_id)
        self.check_and_add_buttons(tile_id)
        self.check_and_add_cat(tile_id)

    def check_and_add_buttons(self, tile_id: int):
        """Check and add buttons based on the newly added tile."""
        tile = self.board[tile_id]
        count = 1
        colour = tile.colour
        visited_tiles = [tile_id]  # Keeps track of visited nodes
        cache_neighbors = []

        # Loop through all the matching neighbors
        while True:
            neighbors = tile.get_neighbors()
            neighbors = list(filter(lambda item: item is not None, neighbors))  # Remove any None
            # Loop through all neighbors, add where colour matches and tile isn't visited
            for n in neighbors:
                # Checks if it is a Design tile, then we just skip this neighbor
                if isinstance(n, Tiles.DesignGoalTile):
                    continue

                # If it touches an already complete pattern it becomes part of the pattern
                # In-order to be scored, it as to be a separate group!
                if n.colour == colour and n.part_of_button:
                    count = 0
                    tile.part_of_button = True

                # If it is a free matching tile, then add it to cache
                if n.colour == colour and n.tile_id not in visited_tiles and not n.part_of_button:
                    cache_neighbors.append(n.tile_id)  # Add id of tile with matching colour

            if not cache_neighbors:  # If there is no more nodes to visit then break
                break

            # Move to the next node, increment count, add its id to visited
            tile = self.board[cache_neighbors.pop()]
            count += 1
            visited_tiles.append(tile.tile_id)

        if count >= 3:  # if there is more than 3 then we group them together.
            self.buttons[colour] += 1  # increment the amount of that colour buttons
            for n in visited_tiles:
                self.board[n].part_of_button = True

    def check_and_add_cat(self, tile_id: int):
        """Check and add cats based on the newly added tile."""
        tile = self.board[tile_id]
        count = 1
        pattern = tile.pattern
        visited_tiles = [tile_id]  # Keeps track of visited nodes
        cache_neighbors = []

        # Loop through all the matching neighbors
        while True:
            neighbors = tile.get_neighbors()
            neighbors = list(filter(lambda item: item is not None, neighbors))  # Remove any None
            # Loop through all neighbors, add where pattern matches and tile hasn't been visited
            for n in neighbors:
                # Checks if it is a Design tile, then we just skip this neighbor
                if isinstance(n, Tiles.DesignGoalTile):
                    continue

                # If it touches an already complete pattern it becomes part of the pattern
                # In-order to be scored, it as to be a separate group!
                if n.pattern == pattern and n.part_of_pattern:
                    count = 0
                    tile.part_of_pattern = True  # join the already done tile

                # If it is a free matching tile, then add it to cache
                if n.pattern == pattern and (n.tile_id not in visited_tiles) and not \
                        n.part_of_pattern and n.tile_id not in cache_neighbors:
                    cache_neighbors.append(n.tile_id)  # Add id of tile with matching pattern

            if not cache_neighbors:  # If there is no more nodes to visit then break
                break

            # Move to the next node, increment count, add its id to visited
            tile = self.board[cache_neighbors.pop()]
            count += 1
            visited_tiles.append(tile.tile_id)

        # Get the amount required for the given cat, if it is met then we set all the visited
        # To be part of the pattern
        cat = self.cats[0]
        for kitten in self.cats:  # Find the cat with the matching pattern
            if pattern in kitten.get_patterns():
                cat = kitten

        if count >= cat.num_of_tiles:  # if there is enough tiles increment num_of_cats
            cat.num_of_cats += 1
            for n in visited_tiles:
                self.board[n].part_of_pattern = True

    def count_rainbows(self) -> int:
        """Count the number of rainbows scored on the board."""
        return min(self.buttons.values())

    def get_score(self) -> int:
        """Calculate and return the total score for the board."""
        return self._calculate_design_score() + self._calculate_button_score() \
            + self._calculate_cat_score()

    def _calculate_design_score(self) -> int:
        """Calculate the score obtained from design tiles."""
        return sum(self.board[idx].check_design_goal_reached() for idx in [17, 25, 30])

    def _calculate_button_score(self) -> int:
        """Calculate the score obtained from buttons."""
        return sum(val * 3 for val in self.buttons.values()) + self.count_rainbows() * 3

    def _calculate_cat_score(self) -> int:
        """Calculate the score obtained from cats."""
        return sum(cat.num_of_cats * cat.score for cat in self.cats)

    def initialise_cats(self):
        """Initialise cats for the board game."""
        millie = Cats.Cat("Millie", 3, 3)
        tibbit = Cats.Cat("Tibbit", 5, 4)
        coconut = Cats.Cat("Coconut", 7, 5)
        cira = Cats.Cat("Cira", 9, 6)
        gwen = Cats.Cat("Gwen", 11, 7)
        bag_of_cats = [millie, tibbit, coconut, cira, gwen]
        random.shuffle(bag_of_cats)  # Shuffle the cats to randomly assign them

        for i in range(3):
            self.cats.append(bag_of_cats.pop())  # Randomly add cats to the array

        # Now assign each cat 2 random pattern
        patterns = ["Stripes", "Leaf", "Dots", "Plants", "Four", "Reeds"]
        random.shuffle(patterns)
        for n in self.cats:
            n.pattern_1 = patterns.pop()
            n.pattern_2 = patterns.pop()

    # ... Implementation for _get_purple_board, _get_blue_board, etc.
