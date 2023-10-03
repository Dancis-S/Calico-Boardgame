"""This file contain code related to setting up the board"""
import copy
import random
from src import Tiles
from src import Cats


# Initialises the board creating the 7 * 7 grid and stores them in array for quick access
class Board:
    def __init__(self, player_num):
        self.board_colour = "Test"
        self.open_positions = [8, 9, 10, 11, 12, 15, 16, 18, 19, 22, 23, 24, 26, 29, 31, 32,
                               33, 36, 37, 38, 39, 40]
        self.buttons = {"Red": 0, "Yellow": 0, "Purple": 0, "Blue": 0, "Green": 0, "Navy": 0}
        self.cats = []  # List that will hold array of the 3 cats
        self.player_num = player_num  # Determines which board player gets
        self.board = []  # Holds all the tile space that are on the board
        self.populate_board()
        self.initialise_tiles()
        self.initialise_cats()
        self.colour_borders(player_num)  # We need to put player number here after

    def populate_board(self):
        """
        Adds the tiles (nodes) that will be used to represent the board
        :return:
        """
        for i in range(49):
            self.board.append(Tiles.NormalTile(i))

        # Insert the Design Pattern tiles in 17,25,30 (we start from 0 not 1)
        requirements = ["NotEqual", "aaa-bbb", "aa-bb-cc", "aaaa-bb", "aaa-bb-c", "aa-bb-c-d"]
        random.shuffle(requirements)  # Randomize the requirements
        self.board[17] = Tiles.DesignGoalTile(17, requirements.pop())
        self.board[25] = Tiles.DesignGoalTile(25, requirements.pop())
        self.board[30] = Tiles.DesignGoalTile(30, requirements.pop())

    def set_cats(self, cats):
        """
        Method used to pass the cats from the higher class to the lower class
        """
        self.cats = copy.deepcopy(cats)

    def initialise_tiles(self):
        """
        Creates the connections (edges) between the tiles (nodes)
        :return:
        """
        for i in range(49):
            tile = self.board[i]
            # Check which part of the board we are in and determines offset
            if i % 14 >= 7:  # left most is full hexagon
                offset = 0
            else:  # left most is half hexagon
                offset = -1

            # set up the west connection
            if i % 7 == 0:
                tile.west = None
            else:
                tile.west = self.board[i - 1]

            # set up the east connection
            if i % 7 == 6:
                tile.east = None
            else:
                tile.east = self.board[i + 1]

            # North-west set up
            if i - 7 + offset < 0 or (offset == -1 and i % 7 == 0):
                tile.north_west = None
            else:
                tile.north_west = self.board[i - 7 + offset]

            # North-east set up
            if i - 6 + offset < 0 or (offset == 0 and i % 7 == 6):
                tile.north_east = None
            else:
                tile.north_east = self.board[i - 6 + offset]

            # South West set up
            if i + 7 + offset > 48 or (offset == -1 and i % 7 == 0):
                tile.south_west = None
            else:
                tile.south_west = self.board[i + 7 + offset]

            # South East set up
            if i + 8 + offset > 48 or (offset == 0 and i % 7 == 6):
                tile.south_east = None
            else:
                tile.south_east = self.board[i + 8 + offset]

    def colour_borders(self, player_num):
        """
        Depending on the players number (i.e. which board the player gets) the
        boarders are initialised with their respective colour and pattern
        :param player_num:
        :return:
        """
        # To reduce the amount of code required
        # Yellow-0, red-1, purple-2, blue-3, green-4, navy-5
        # stripes-0, leaf-1, dots-2, plants-3, four-4, Reeds-5
        colours = ["Yellow", "Red", "Purple", "Blue", "Green", "Navy"]
        patterns = ["Stripes", "Leaf", "Dots", "Plants", "Four", "Reeds"]
        borders = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42, 43, 44,
                   45, 46, 47, 48, 41, 34, 27, 20, 13]
        # (colour, pattern)
        purple_board = [(0, 3), (1, 2), (2, 3), (0, 1), (3, 0), (1, 4), (4, 2), (3, 4), (5, 0),
                        (4, 1), (1, 5), (3, 2), (2, 1), (0, 4), (2, 0), (5, 1), (4, 3), (0, 5),
                        (2, 2), (5, 4), (4, 0), (1, 1), (3, 3), (5, 5)]

        blue_board = [(1, 5), (0, 0), (3, 5), (1, 1), (2, 4), (0, 3), (4, 0), (4, 3), (5, 4),
                      (3, 1),
                      (2, 0), (0, 2), (2, 3), (3, 4), (1, 3), (5, 1), (4, 5), (1, 2), (3, 0),
                      (5, 3),
                      (4, 4), (0, 1), (2, 5), (5, 2)]

        green_board = [(5, 1), (0, 5), (4, 1), (5, 0), (2, 4), (0, 2), (3, 5), (2, 2), (1, 4),
                       (3, 0),
                       (0, 3), (2, 5), (4, 0), (5, 2), (4, 4), (1, 0), (3, 1), (5, 3), (4, 5),
                       (1, 2),
                       (3, 4), (0, 0), (2, 1), (1, 3)]

        yellow_board = [(4, 4), (5, 3), (0, 0), (2, 2), (5, 5), (4, 1), (1, 4), (1, 1), (2, 5),
                        (0, 2),
                        (4, 3), (5, 4), (3, 5), (2, 1), (0, 5), (3, 2), (1, 0), (2, 3), (0, 4),
                        (3, 1),
                        (1, 5), (4, 2), (5, 0), (3, 3)]

        if player_num == 1:
            chosen_board = purple_board
            self.board_colour = "Purple"
        elif player_num == 2:
            chosen_board = blue_board
            self.board_colour = "Blue"
        elif player_num == 3:
            chosen_board = green_board
            self.board_colour = "Green"
        elif player_num == 4:
            chosen_board = yellow_board
            self.board_colour = "Yellow"
        else:  # Default to purple board
            self.board_colour = "Random"
            print("Im in Random")
            chosen_board = purple_board

        for n in range(len(borders)):  # Applies the chosen colours and patterns
            self.board[borders[n]].colour = colours[chosen_board[n][0]]
            self.board[borders[n]].pattern = patterns[chosen_board[n][1]]

    def add_tile(self, tile_id, colour, pattern):
        """
        This function takes as an input the board position, tile colour, tile pattern
        and then places the given tile into
        :return:
        """
        tile = self.board[tile_id]
        tile.colour = colour
        tile.pattern = pattern
        self.open_positions.remove(tile_id)
        self.check_and_add_buttons(
            tile_id)  # Calls the function to check whether we have gained a button
        self.check_and_add_cat(tile_id)  # Calls function to check whether cat is scored

    def check_and_add_buttons(self, tile_id):
        """
        Each time a new tile is added, search to see if there is a connection of nodes with
        the same colour. (if there is more than 3 then we call method that adds button to the board)
        :param tile_id:
        :return:
        """
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

    def check_and_add_cat(self, tile_id):

        """
        Each time a new tile is added, we get its pattern and the properties from the
        respective cat. We then see if it fulfills the required number of tiles needed
        inorder to score a cat. If scored we increment the num_of_cats variable in the
        respective cat object.
        :return:
        """
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

    def count_rainbows(self):
        """
        Function that will calculate how many rainbows the player has scored in their
        board and then return it.
        :return:
        """
        return min(list(self.buttons.values()))

    def get_score(self):
        """
        At the end of the game this function is called, it calculates the players score
        based on the design tiles completed, the buttons scored, and the cats scored.
        :return:
        """
        score = 0

        # Design tile scores obtained
        score += self.board[17].check_design_goal_reached()  # Tile 17
        score += self.board[25].check_design_goal_reached()  # Tile 25
        score += self.board[30].check_design_goal_reached()  # Tile 30

        # Adds the scores from the button (don't forget to check for rainbows)
        score += self.count_rainbows() * 3  # Adds the score of the rainbow
        values = list(self.buttons.values())
        for n in values:
            score += 3 * n

        # Cats scored
        score += self.cats[0].num_of_cats * self.cats[0].score  # Cat 1
        score += self.cats[1].num_of_cats * self.cats[1].score  # Cat 2
        score += self.cats[2].num_of_cats * self.cats[2].score  # Cat 3

        return score

    def get_cat_score(self):
        """
        Return the score that has been obtained due to the cats
        """
        score = 0
        score += self.cats[0].num_of_cats * self.cats[0].score  # Cat 1
        score += self.cats[1].num_of_cats * self.cats[1].score  # Cat 2
        score += self.cats[2].num_of_cats * self.cats[2].score  # Cat 3
        return score

    def get_design_score(self):
        """
        Return the score that has been obtained from the design tiles
        """
        score = 0
        score += self.board[17].check_design_goal_reached()  # Tile 17
        score += self.board[25].check_design_goal_reached()  # Tile 25
        score += self.board[30].check_design_goal_reached()  # Tile 30
        return score

    def get_buttons_score(self):
        """
        Returns the amount of score obtained from buttons, including the rianbow
        """
        score = 0
        # Adds the scores from the button (don't forget to check for rainbows)
        score += self.count_rainbows() * 3  # Adds the score of the rainbow
        values = list(self.buttons.values())
        for n in values:
            score += 3 * n

        return score

    def initialise_cats(self):
        """
               Initialises the cats for the board game by randomly picking 3 cats out of the 5,
               and the randomly assigning them 2 patterns.
               :return:
               """
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
