"""This file contain code that will run the actual game"""
import random
from src.core import Board, Cats
from src.core import Tiles


class Calico:
    """
    Class for the overall game of Calico
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

    def get_user_inputs(board):
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
