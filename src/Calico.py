"""This file contain code that will run the actual game"""
import random
import numpy as np
from src import Board
from src import Tiles
from src import Cats


class Calico:
    """
    Class for the overall game of Calico, this is also the class that the agents
    will interact with when playing the game
    """

    def __init__(self, num_of_players, agents):
        self.agents = agents
        self.num_of_players = num_of_players
        self.tiles_bag = []  # Bag that holds the tiles, that players can draw from to play
        self.shop = []  # Shop that holds available tiles
        self.players_board = []  # Holds the boards for each player
        self.players_stack = []  # Holds the stack for each player
        self.cats = []
        self.setup_game(num_of_players)

    def setup_game(self, num_of_players):
        """
        Function initialises the array with the players boards, the randomly assigned
        tiles they have in their stack, and initialises the shop
        of players
        :param num_of_players:
        :return:
        """

        self.initialise_cats()  # Set up the cats that will be used for this game

        # There is 3 of each pattern for each colour set put this into the bag
        colours = ["Yellow", "Red", "Purple", "Blue", "Green", "Navy"]
        patterns = ["Stripes", "Leaf", "Dots", "Plants", "Four", "Reeds"]
        for c in colours:
            for p in patterns:
                for i in range(3):
                    # Add tuple (colour, pattern)
                    self.tiles_bag.append((c, p))

        random.shuffle(self.tiles_bag)  # Shuffles the bag containing tiles

        for i in range(3):  # Fill the shop up with 3 tiles
            self.shop.append(self.tiles_bag.pop())

        # Sets up the boards and the players stacks
        for i in range(num_of_players):
            # Initialises each players stack with random tiles from bag
            self.players_stack.append([self.tiles_bag.pop(), self.tiles_bag.pop(),
                                       self.tiles_bag.pop()])
            self.players_board.append(Board.Board(i + 1))

        for board in self.players_board:  # Passes the cats for set up
            board.set_cats(self.cats)

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

    def select_board_colour(self, player_id, colour):
        """
        Method that is used to select the board (or mostly used to change the board for a given
        player to another board)
        1-Purple, 2-Blue, 3-Green, 4- Yellow
        """
        self.players_board[player_id].colour_borders(colour)

    def start_game(self, num_of_players, agents):
        """
        Begins the game and loops through all the players giving them a turn to make a play
        :return:
        """
        # If not agents are provided it will be a human player
        if not agents:
            open_moves = True
            while open_moves:
                for player in range(num_of_players):
                    self.human_players(player)
                    if not self.players_board[player].open_positions:
                        open_moves = False
        else:  # We make our agents play the game
            num_of_players = len(agents)  # to prevent any bugs
            open_moves = True
            while open_moves:
                for player in range(num_of_players):
                    # Code here for the choice the agent makes
                    bot = agents[player]
                    state = self
                    answer = bot.get_action(state)
                    # All agent actions returned as (location, tile_indx, shop_indx)
                    location = answer[0]
                    chosen_tile = answer[1]
                    shop_tile = answer[2]
                    self.make_a_move(bot.player_id, location, chosen_tile, shop_tile)

                    # Checks whether game is over
                    if not self.players_board[player].open_positions:
                        open_moves = False
        if len(agents) > 1:
            # return self.calculate_scores()
            return self.winner_id()
        else:
            return self.return_score()

    def make_a_move(self, player_id, location, chosen_tile, shop_tile):
        """
        Plays the move that for the given player (prevents a lot of manual
        move making for the agents
        :param player_id:
        :param location:
        :param chosen_tile:
        :param shop_tile:
        :return:
        """
        board = self.get_my_board(player_id)  # Get the board
        my_stack = self.get_my_stack(player_id)  # Get the players stack
        tile = my_stack.pop(chosen_tile)  # Pop their chosen tile

        # Tile is (colour, pattern) tuple so tile[0] = colour, and tile[1] = pattern
        board.add_tile(location, tile[0], tile[1])  # Place chosen tile

        my_stack.append(self.shop.pop(shop_tile))  # Pop from shop and add to stack
        self.shop.append(self.tiles_bag.pop())  # Add random tile from bag to shop

    def human_players(self, player):
        board = self.players_board[player]  # gets the board for the respective players
        current_stack = self.players_stack[player]
        print("It's player " + str(player) + "'s move, your stack of tiles is")
        print("Open positions: ", board.open_positions)
        print("Your tiles: " + str(self.players_stack[player]))
        chosen_tile, chosen_location = self.get_user_inputs(board)

        colour = current_stack[chosen_tile][0]
        pattern = current_stack[chosen_tile][1]
        board.add_tile(chosen_location, colour, pattern)
        current_stack.pop(chosen_tile)

        # The user now needs to select a new tile from the shop
        print("The shop has: " + str(self.shop))
        select = int(input("Select a tile from the shop(1-3): "))
        current_stack.append(self.shop.pop(select - 1))  # Pop from shop and add to stack
        self.shop.append(self.tiles_bag.pop())  # Add random tile from bag to shop

    @classmethod
    def get_user_inputs(cls, board):
        """
        Collects the tile and the location that the user wants to play. Then checks that they
        are valid, if invalid they are prompted again, else return the chosen tile and the move
        :return:
        """
        while True:
            chosen_tile = int(input("Enter your chosen tile(1-3):"))
            if chosen_tile > 3 or chosen_tile < 1:
                print("Invalid option you only have 3 card (1-3)")
            else:
                break

        while True:
            chosen_location = int(input("Enter a tile location:"))
            if chosen_location not in board.open_positions:
                print("Invalid move please pick a valid position")
            else:
                break
        return (chosen_tile - 1), chosen_location

    def return_score(self):
        """
        return just the scores nothing else
        :return:
        """
        scores = []
        for board in self.players_board:
            # (name , score)
            scores.append((board.player_num, board.get_score()))  # Add it in
        return scores

    def calculate_scores(self):
        """
        Gets the scores of all the players, determines the winner and returns all the score
        :return:
        """
        scores = []
        for board in self.players_board:
            # (name , score)
            scores.append((board.player_num, board.get_score()))  # Add it in

        scores.sort(key=lambda a: a[1], reverse=True)  # Sort them in order of who wins

        # Craft the string that will be returned
        position_names = ["\nFourth Place: ", "\nThird Place: ", "\nSecond Place: ",
                          "\nFirst Place: "]
        final_log = "=====!! End Of Game !!====="
        for player in scores:
            final_log += position_names.pop() + "Player " + str(player[0]) + \
                         "!  Score: " + str(player[1])

        return final_log

    def single_player_give_game_info(self):
        """
        Called only at the end of the game.
        This method returns all the information about the game back to the user, for example
        the final score, the cats and their tiles, the number of buttons and specific ones scored
        the design tiles present, and finally the board layout.
        """
        board = self.get_my_board(0)
        info = []

        # Quick summary
        info.append(board.get_score())
        info.append(board.get_buttons_score())
        info.append(board.get_cat_score())
        info.append(board.get_design_score())
        info.append(board.board_colour)

        # Buttons info
        buttons = board.buttons  # Gets the buttons dictionary
        info.append(buttons["Red"])
        info.append(buttons["Purple"])
        info.append(buttons["Yellow"])
        info.append(buttons["Blue"])
        info.append(buttons["Green"])
        info.append(buttons["Navy"])
        info.append(board.count_rainbows())

        # Design Tile Info
        info.append(board.board[17].requirement)
        info.append(board.board[17].check_design_goal_reached())
        info.append(board.board[25].requirement)
        info.append(board.board[25].check_design_goal_reached())
        info.append(board.board[30].requirement)
        info.append(board.board[30].check_design_goal_reached())

        # Cat info
        info.append(board.cats[0].name)
        info.append(board.cats[0].num_of_cats)
        info.append(board.cats[0].pattern_1)
        info.append(board.cats[0].pattern_2)
        info.append(board.cats[1].name)
        info.append(board.cats[1].num_of_cats)
        info.append(board.cats[1].pattern_1)
        info.append(board.cats[1].pattern_2)
        info.append(board.cats[2].name)
        info.append(board.cats[2].num_of_cats)
        info.append(board.cats[2].pattern_1)
        info.append(board.cats[2].pattern_2)

        return info

    def winner_id(self):
        """
        Returns the ID of the winner
        """
        scores = []
        csv_output = []
        for board in self.players_board:
            # (name , score)
            scores.append((self.agents[board.player_num - 1].player_name, board.get_score()))  # Add it in
            csv_output.append(self.agents[board.player_num - 1].player_name)
            csv_output.append(board.get_score())
        scores.sort(key=lambda a: a[1])
        csv_output.append(scores.pop()[0])
        return csv_output

    def get_my_stack(self, player_id):
        """
        Given the players id, return their respective stack!
        :param player_id:
        :return:
        """
        return self.players_stack[player_id]

    def get_my_board(self, player_id):
        """
        Given a players ID return their respective board!
        :param player_id:
        :return:
        """
        return self.players_board[player_id]

    #########################################################################
    # #################   Code for DQN Ignore It ############################

    @classmethod
    def colour_info_to_one_hot(cls, colour):
        """
       Converts the string of colour into a one-hot encoded version
       :param colour:
       :return:
       """
        word_colours = ["Yellow", "Red", "Purple", "Blue", "Green", "Navy"]
        encoded_colour = []
        for word in word_colours:
            if word == colour:
                encoded_colour.append(1)
            else:
                encoded_colour.append(0)

        return encoded_colour

    @classmethod
    def patter_info_to_one_hot(cls, pattern):
        """
        Converts the string of pattern into a one-hot encoded version
        :param pattern:
        :return:
        """
        # [Stripes, Leaf, Dots, Plants, Four, Reeds]
        encoded_pattern = []
        word_patterns = ["Stripes", "Leaf", "Dots", "Plants", "Four", "Reeds"]
        for word in word_patterns:
            if word == pattern:
                encoded_pattern.append(1)
            else:
                encoded_pattern.append(0)

        return encoded_pattern

    @classmethod
    def requirement_to_one_one(cls, requirement):
        """
        Converts the string requirements into a one-hot encoded version
        :param requirement:
        :return:
        """
        encoded_requirements = []
        word_req = ["NotEqual", "aaa-bbb", "aa-bb-cc", "aaaa-bb", "aaa-bb-c", "aa-bb-c-d"]
        for req in word_req:
            if requirement == req:
                encoded_requirements.append(1)
            else:
                encoded_requirements.append(0)
        return encoded_requirements

    def get_state(self):
        state = []  # Array that will hold the 3D state of the game
        board = self.get_my_board(0)
        stack = self.get_my_stack(0)

        # Add the cats to the game state
        cats = board.cats
        for cat in cats:
            cat1_info = self.patter_info_to_one_hot(cat.pattern_1)
            state.append(cat1_info)
            cat2_info = self.patter_info_to_one_hot(cat.pattern_2)
            state.append(cat2_info)

        # Add the board positions 0 means open position
        for tile in board.board:
            if isinstance(tile, Tiles.DesignGoalTile):
                # In situation where it's a design tile we need to add its requirements
                state.append(self.requirement_to_one_one(tile.requirement))
            elif tile.colour is None or tile.pattern is None:
                state.append([0, 0, 0, 0, 0, 0])  # Free colour
                state.append([0, 0, 0, 0, 0, 0])  # Free pattern
            else:
                info1 = self.colour_info_to_one_hot(tile.colour)
                info2 = self.patter_info_to_one_hot(tile.pattern)
                state.append(info1)
                state.append(info2)

        # Add the player stack
        for tile in stack:
            info1 = self.colour_info_to_one_hot(tile[0])
            info2 = self.patter_info_to_one_hot(tile[1])
            state.append(info1)
            state.append(info2)

        # Add the shop stack
        for tile in self.shop:
            info1 = self.colour_info_to_one_hot(tile[0])
            info2 = self.patter_info_to_one_hot(tile[1])
            state.append(info1)
            state.append(info2)

        arr = np.array(state)
        flat_state = arr.flatten()
        return flat_state

    def get_action_state(self):
        og_open = [8, 9, 10, 11, 12, 15, 16, 18, 19, 22, 23, 24, 26, 29, 31, 32,
                   33, 36, 37, 38, 39, 40]
        open_pos = self.get_my_board(0).open_positions
        moves = []
        counter = 1
        for tile in og_open:
            if tile not in open_pos:
                for i in range(9):
                    counter += 1
            else:
                for i in range(9):
                    moves.append(counter)
                    counter += 1

        return moves

    def reset(self):
        """
        Method to reset the game, for when an AI wants to play a new game
        """
        num_of_players = self.num_of_players
        agents = self.agents
        self.__init__(num_of_players, agents)  # Reset the game to new
        return self.get_state()

    def step(self, action):
        """
        For the DQN given an action, complete the action. Then return the following:
        the next state, the reward, and whether the game is done
        """
        # Convert the action to action we use
        action_map = self.dqn_convert_move()
        play = action_map[action]  # Get action that the game understands
        location = play[0]
        tile = play[1]
        shop = play[2]

        my_board = self.get_my_board(0)
        initial_score = my_board.get_score()
        done = False
        self.make_a_move(0, location, tile, shop)

        reward = my_board.get_score() - initial_score

        if not my_board.open_positions:
            done = True

        next_state = self.get_state()

        return next_state, reward, done

    def get_invalid_actions(self):
        board = self.get_my_board(0)
        current_open = board.open_positions
        og_open = [8, 9, 10, 11, 12, 15, 16, 18, 19, 22, 23, 24, 26, 29, 31, 32,
                   33, 36, 37, 38, 39, 40]
        counter = 0
        invalid_pos = []
        for pos in og_open:
            if pos not in current_open:  # Not a valid move then add it array
                for i in range(9):
                    invalid_pos.append(counter)
                    counter += 1
            else:
                for i in range(9):
                    counter += 1

        return invalid_pos

    def dqn_convert_move(self):
        # Convert the output to a playable move
        hold_actions = [(8, 0, 0), (8, 0, 1), (8, 0, 2), (8, 1, 0), (8, 1, 1), (8, 1, 2),
                        (8, 2, 0), (8, 2, 1), (8, 2, 2), (9, 0, 0), (9, 0, 1), (9, 0, 2),
                        (9, 1, 0), (9, 1, 1), (9, 1, 2), (9, 2, 0), (9, 2, 1), (9, 2, 2),
                        (10, 0, 0), (10, 0, 1), (10, 0, 2), (10, 1, 0), (10, 1, 1), (10, 1, 2),
                        (10, 2, 0), (10, 2, 1), (10, 2, 2), (11, 0, 0), (11, 0, 1), (11, 0, 2),
                        (11, 1, 0), (11, 1, 1), (11, 1, 2), (11, 2, 0), (11, 2, 1), (11, 2, 2),
                        (12, 0, 0), (12, 0, 1), (12, 0, 2), (12, 1, 0), (12, 1, 1), (12, 1, 2),
                        (12, 2, 0), (12, 2, 1), (12, 2, 2), (15, 0, 0), (15, 0, 1), (15, 0, 2),
                        (15, 1, 0), (15, 1, 1), (15, 1, 2), (15, 2, 0), (15, 2, 1), (15, 2, 2),
                        (16, 0, 0), (16, 0, 1), (16, 0, 2), (16, 1, 0), (16, 1, 1), (16, 1, 2),
                        (16, 2, 0), (16, 2, 1), (16, 2, 2), (18, 0, 0), (18, 0, 1), (18, 0, 2),
                        (18, 1, 0), (18, 1, 1), (18, 1, 2), (18, 2, 0), (18, 2, 1), (18, 2, 2),
                        (19, 0, 0), (19, 0, 1), (19, 0, 2), (19, 1, 0), (19, 1, 1), (19, 1, 2),
                        (19, 2, 0), (19, 2, 1), (19, 2, 2), (22, 0, 0), (22, 0, 1), (22, 0, 2),
                        (22, 1, 0), (22, 1, 1), (22, 1, 2), (22, 2, 0), (22, 2, 1), (22, 2, 2),
                        (23, 0, 0), (23, 0, 1), (23, 0, 2), (23, 1, 0), (23, 1, 1), (23, 1, 2),
                        (23, 2, 0), (23, 2, 1), (23, 2, 2), (24, 0, 0), (24, 0, 1), (24, 0, 2),
                        (24, 1, 0), (24, 1, 1), (24, 1, 2), (24, 2, 0), (24, 2, 1), (24, 2, 2),
                        (26, 0, 0), (26, 0, 1), (26, 0, 2), (26, 1, 0), (26, 1, 1), (26, 1, 2),
                        (26, 2, 0), (26, 2, 1), (26, 2, 2), (29, 0, 0), (29, 0, 1), (29, 0, 2),
                        (29, 1, 0), (29, 1, 1), (29, 1, 2), (29, 2, 0), (29, 2, 1), (29, 2, 2),
                        (31, 0, 0), (31, 0, 1), (31, 0, 2), (31, 1, 0), (31, 1, 1), (31, 1, 2),
                        (31, 2, 0), (31, 2, 1), (31, 2, 2), (32, 0, 0), (32, 0, 1), (32, 0, 2),
                        (32, 1, 0), (32, 1, 1), (32, 1, 2), (32, 2, 0), (32, 2, 1), (32, 2, 2),
                        (33, 0, 0), (33, 0, 1), (33, 0, 2), (33, 1, 0), (33, 1, 1), (33, 1, 2),
                        (33, 2, 0), (33, 2, 1), (33, 2, 2), (36, 0, 0), (36, 0, 1), (36, 0, 2),
                        (36, 1, 0), (36, 1, 1), (36, 1, 2), (36, 2, 0), (36, 2, 1), (36, 2, 2),
                        (37, 0, 0), (37, 0, 1), (37, 0, 2), (37, 1, 0), (37, 1, 1), (37, 1, 2),
                        (37, 2, 0), (37, 2, 1), (37, 2, 2), (38, 0, 0), (38, 0, 1), (38, 0, 2),
                        (38, 1, 0), (38, 1, 1), (38, 1, 2), (38, 2, 0), (38, 2, 1), (38, 2, 2),
                        (39, 0, 0), (39, 0, 1), (39, 0, 2), (39, 1, 0), (39, 1, 1), (39, 1, 2),
                        (39, 2, 0), (39, 2, 1), (39, 2, 2), (40, 0, 0), (40, 0, 1), (40, 0, 2),
                        (40, 1, 0), (40, 1, 1), (40, 1, 2), (40, 2, 0), (40, 2, 1), (40, 2, 2)]

        mapped_actions = {}
        num = 0
        for n in hold_actions:
            mapped_actions[num] = n
            num += 1
        return mapped_actions

    def get_valid_moves(self):
        board = self.get_my_board(0)
        og_open = [8, 9, 10, 11, 12, 15, 16, 18, 19, 22, 23, 24, 26, 29, 31, 32,
                   33, 36, 37, 38, 39, 40]
        valid_moves = []
        open_pos = board.open_positions
        counter = 0
        for pos in og_open:
            if pos in open_pos:
                for i in range(9):
                    valid_moves.append(counter)
                    counter += 1
            else:
                for i in range(9):
                    counter += 1

        return valid_moves
