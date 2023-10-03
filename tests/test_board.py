"""Tests for the Board module"""
import unittest
from src import Board
from src import Cats


class TestBoard(unittest.TestCase):

    def test_open_positions(self):
        """
        Tests that when we add a tile to the board, that position is removed from
        the open positions array. In this test tile with id 8 is added, so 8 should be
        removed from open positions
        :return:
        """
        board = Board.Board(1)
        board.add_tile(8, "Red", "Dots")
        self.assertFalse(8 in board.open_positions)

    def test_tile_8_is_empty(self):
        """
        Tests that tile 8 has no info in it (is a blank tile)
        :return:
        """
        board = Board.Board(1)
        self.assertEqual(board.board[8].colour, None)

    def test_add_to_tile_8(self):
        """
        Tests that the add tile adds the tile correctly
        :return:
        """
        board = Board.Board(1)
        board.add_tile(8, "Red", "Dots")
        info = board.board[8].colour + board.board[8].pattern
        self.assertEqual(info, "RedDots")

    def test_creating_board(self):
        """
        Tests that the
        :return:
        """
        board = Board.Board(1)
        length = len(board.board)
        msg = "The length is: " + str(length) + "!!"
        self.assertTrue(length == 49, msg)

    def test_get_id(self):
        """
        Tests that we are able to get the ID of a tile.
        :return:
        """
        board = Board.Board(1)
        tile_id = board.board[0].tile_id
        self.assertEqual(tile_id, 0, "The ID produced is:" + str(tile_id))

    # Tests that the east is initialised properly
    def test_navigate_along_east(self):
        """
        Tests that we are able to navigate along the east direction. This means that
        the east connections are correctly initialised.
        :return:
        """
        board = Board.Board(1)
        node = board.board[0]
        hold_id = node.tile_id
        # Go move east through the tiles
        while node.east is not None:
            node = node.east
            hold_id = node.tile_id
        self.assertEqual(hold_id, 6, "The ID produced is: " + str(hold_id))

    # Test that the west connection are correct and can be traversed
    def test_navigate_along_west(self):
        """
        Tests that we are able to move along the west direction. This means that
        the west connections are correctly initialised
        :return:
        """
        board = Board.Board(1)
        node = board.board[48]
        hold_id = node.tile_id
        # Move west until we can no more
        while node.west is not None:
            node = node.west
            hold_id = node.tile_id
        self.assertEqual(hold_id, 42, "The ID produced is: " + str(hold_id))

    def test_purple_borders(self):
        """
        Tests the border for the purple board is drawn correct by iterating over the nodes,
        gathering the colour and pattern and then comparing to make sure it is correctly drawn

        :return: Whether the purple border is drawn correct
        """
        board = Board.Board(1)  # Purple board is 1
        border = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42, 43, 44,
                  45, 46, 47, 48, 41, 34, 27, 20, 13]
        test = ""
        for n in border:
            test += str(board.board[n].colour)
            test += str(board.board[n].pattern)

        correct = "YellowPlantsRedDotsPurplePlantsYellowLeafBlueStripesRedFourGreenDots" \
                  "BlueFourNavyStripesGreenLeafRedReedsBlueDotsPurpleLeafYellowFourPurpleStripes" \
                  "NavyLeafGreenPlantsYellowReedsPurpleDotsNavyFourGreenStripesRedLeafBluePlants" \
                  "NavyReeds"
        self.assertEqual(test, correct, "Test outputs: " + test)

    def test_blue_borders(self):
        """
        Tests the border for the blue board is drawn correct by iterating over the nodes,
        gathering the colour and pattern and then comparing to make sure it is correctly drawn

        :return: Whether the blue border is drawn correct
        """
        board = Board.Board(2)  # Blue board is 2
        border = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42, 43, 44,
                  45, 46, 47, 48, 41, 34, 27, 20, 13]
        test = ""
        for n in border:
            test += str(board.board[n].colour)
            test += str(board.board[n].pattern)

        correct = "RedReedsYellowStripesBlueReedsRedLeafPurpleFourYellowPlantsGreenStripesGreenPlants" \
                  "NavyFourBlueLeafPurpleStripesYellowDotsPurplePlantsBlueFourRedPlantsNavyLeafGreenReeds" \
                  "RedDotsBlueStripesNavyPlantsGreenFourYellowLeafPurpleReedsNavyDots"
        self.assertEqual(test, correct, "Test outputs: " + test)

    def test_green_borders(self):
        """
        Tests the border for the purple board is drawn correct by iterating over the nodes,
        gathering the colour and pattern and then comparing to make sure it is correctly drawn

        :return: Whether the purple border is drawn correct
        """
        board = Board.Board(3)  # Green board is 3
        border = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42, 43, 44,
                  45, 46, 47, 48, 41, 34, 27, 20, 13]
        test = ""
        for n in border:
            test += str(board.board[n].colour)
            test += str(board.board[n].pattern)

        correct = "NavyLeafYellowReedsGreenLeafNavyStripesPurpleFourYellowDotsBlueReedsPurpleDots" \
                  "RedFourBlueStripesYellowPlantsPurpleReedsGreenStripesNavyDotsGreenFourRedStripes" \
                  "BlueLeafNavyPlantsGreenReedsRedDotsBlueFourYellowStripesPurpleLeafRedPlants"
        self.assertEqual(test, correct, "Test outputs: " + test)

    def test_yellow_borders(self):
        """
        Tests the border for the purple board is drawn correct by iterating over the nodes,
        gathering the colour and pattern and then comparing to make sure it is correctly drawn

        :return: Whether the purple border is drawn correct
        """
        board = Board.Board(4)  # Yellow board is 4
        border = [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28, 35, 42, 43, 44,
                  45, 46, 47, 48, 41, 34, 27, 20, 13]
        test = ""
        for n in border:
            test += str(board.board[n].colour)
            test += str(board.board[n].pattern)

        correct = "GreenFourNavyPlantsYellowStripesPurpleDotsNavyReedsGreenLeafRedFourRedLeaf" \
                  "PurpleReedsYellowDotsGreenPlantsNavyFourBlueReedsPurpleLeafYellowReedsBlueDots" \
                  "RedStripesPurplePlantsYellowFourBlueLeafRedReedsGreenDotsNavyStripesBluePlants"
        self.assertEqual(test, correct, "Test outputs: " + test)

    def test_adding_button(self):
        """
        Tests to see that a connection of 3 or more tiles with the same colour, results
        in a button being added to the button dictionary
        :return:
        """
        board = Board.Board(1)
        board.add_tile(23, "Blue", "Dots")
        board.add_tile(24, "Blue", "Plants")
        board.add_tile(31, "Blue", "Four")
        blue_button_count = board.buttons.get("Blue")
        self.assertEqual(blue_button_count, 1)

    def test_adding_button_2(self):
        """
        Tests to see that a connection of 3 or more tiles with the same colour, results
        in a button being added to the button dictionary.
        This time only checking that each button has their "button" instance variable changed
        :return:
        """
        board = Board.Board(1)
        board.add_tile(40, "Blue", "Dots")
        board.add_tile(26, "Blue", "Plants")
        board.add_tile(33, "Blue", "Four")
        blue_button_count = board.buttons.get("Blue")
        statement = board.board[40].part_of_button and board.board[33].part_of_button and\
                    board.board[26].part_of_button and blue_button_count == 1

        self.assertTrue(statement)

    def test_adding_to_existing_pattern(self):
        """
        given that there is already a group (a button), when we add another matching tile, it should
        just become part of the group and should not add a new button
        :return:
        """
        board = Board.Board(1)
        board.add_tile(23, "Blue", "Dots")
        board.add_tile(24, "Blue", "Plants")
        board.add_tile(31, "Blue", "Four")
        board.add_tile(37, "Blue", "Four")
        blue_button_count = board.buttons.get("Blue")
        self.assertEqual(blue_button_count, 1)

    def test_adding_to_existing_pattern_2(self):
        """
        Check that when we have already 1 group (1 button) consisting of 3 tiles, and we
        have 2 tiles that are disconnected to the group, but we then place 1 tile that connects
        the 2 disconnected tiles. The functions should make sure it does not count the 2 disconnected
        and 1 new as a new group, as they are technically touching another group therefore they
        should be put together with the other group, and the count for buttons should not change!
        :return:
        """
        board = Board.Board(1)
        board.add_tile(23, "Blue", "Dots")
        board.add_tile(22, "Blue", "Plants")
        board.add_tile(16, "Blue", "Four")
        board.add_tile(32, "Blue", "Four")
        board.add_tile(33, "Blue", "Four")
        board.add_tile(24, "Blue", "Four")
        blue_button_count = board.buttons.get("Blue")
        # Check that the button count is 1 AND the furthest button added to same group
        statement = blue_button_count == 1 and board.board[33].part_of_button
        self.assertTrue(statement)

    def test_adding_to_existing_pattern_3(self):
        """
        Once again checks what happens when adding 1 tile connects multiple different groups
        together. (should only results in 1 button)
        :return:
        """
        board = Board.Board(1)
        board.add_tile(23, "Blue", "Dots")
        board.add_tile(22, "Blue", "Plants")
        board.add_tile(32, "Blue", "Four")
        board.add_tile(39, "Blue", "Four")
        board.add_tile(11, "Blue", "Four")
        board.add_tile(18, "Blue", "Four")
        board.add_tile(24, "Blue", "Four")
        blue_button_count = board.buttons.get("Blue")
        # should still only be 1
        self.assertEqual(blue_button_count, 1)

    def test_cats_are_initialised(self):
        """
        Tests that the 3 cats are correctly initialised where they all contain a
        pattern.
        :return:
        """
        board = Board.Board(1)
        set_up_correct = True
        if len(board.cats) != 3:
            set_up_correct = False
        for cat in board.cats:
            arr = cat.get_patterns()
            if len(arr) != 2:
                set_up_correct = False

        self.assertTrue(set_up_correct)

    def test_cats_contain_different_patterns(self):
        """
        Tests that there are no duplicated patterns for each cat
        :return:
        """
        board = Board.Board(1)
        hold_cats = []
        set_up_correct = True
        for cat in board.cats:
            if cat.pattern_1 in hold_cats or cat.pattern_2 in hold_cats \
                    or cat.pattern_1 == cat.pattern_2:
                set_up_correct = False
            else:
                hold_cats.append(cat.pattern_1)
                hold_cats.append(cat.pattern_2)
        self.assertTrue(set_up_correct)

    def test_adding_random_cat(self):
        """
        Tests that we can correctly add a random cat
        :return:
        """
        # Given that the highest cat is a group of 7 we will just use that
        board = Board.Board(1)
        # Now we get the pattern we need
        cat = board.cats[2]
        pattern = cat.pattern_2  # Get the second pattern from the second cat
        board.add_tile(23, "Blue", pattern)
        board.add_tile(22, "Red", pattern)
        board.add_tile(32, "Blue", pattern)
        board.add_tile(39, "Red", pattern)
        board.add_tile(11, "Blue", pattern)
        board.add_tile(18, "Red", pattern)
        board.add_tile(24, "Blue", pattern)
        num_of_cats = cat.num_of_cats
        # should still only be 1
        self.assertEqual(num_of_cats, 1,
                         "Pattern was: " + pattern + " and required length was: " + str(cat.num_of_tiles))

    def test_adding_random_cat_redundant_1(self):
        """
        Tests that we can correctly add a random cat
        :return:
        """
        # Given that the highest cat is a group of 7 we will just use that
        board = Board.Board(1)
        # Now we get the pattern we need
        cat = board.cats[2]
        pattern = cat.pattern_2  # Get the second pattern from the second cat
        board.add_tile(23, "Blue", pattern)
        board.add_tile(22, "Red", pattern)
        board.add_tile(32, "Blue", pattern)
        board.add_tile(39, "Red", pattern)
        board.add_tile(11, "Blue", pattern)
        board.add_tile(18, "Red", pattern)
        board.add_tile(24, "Blue", pattern)
        num_of_cats = cat.num_of_cats
        # should still only be 1
        self.assertEqual(num_of_cats, 1,
                         "Pattern was: " + pattern + " and required length was: " + str(cat.num_of_tiles))

    def test_adding_random_cat_redundant_2(self):
        """
        Tests that we can correctly add a random cat
        :return:
        """
        # Given that the highest cat is a group of 7 we will just use that
        board = Board.Board(1)
        # Now we get the pattern we need
        cat = board.cats[2]
        pattern = cat.pattern_2  # Get the second pattern from the second cat
        board.add_tile(23, "Blue", pattern)
        board.add_tile(22, "Red", pattern)
        board.add_tile(32, "Blue", pattern)
        board.add_tile(39, "Red", pattern)
        board.add_tile(11, "Blue", pattern)
        board.add_tile(18, "Red", pattern)
        board.add_tile(24, "Blue", pattern)
        num_of_cats = cat.num_of_cats
        # should still only be 1
        self.assertEqual(num_of_cats, 1,
                         "Pattern was: " + pattern + " and required length was: " + str(cat.num_of_tiles))

    def test_adding_random_cat_redundant_3(self):
        """
        Tests that we can correctly add a random cat
        :return:
        """
        # Given that the highest cat is a group of 7 we will just use that
        board = Board.Board(1)
        # Now we get the pattern we need
        cat = board.cats[2]
        pattern = cat.pattern_2  # Get the second pattern from the second cat
        board.add_tile(23, "Blue", pattern)
        board.add_tile(22, "Red", pattern)
        board.add_tile(32, "Green", pattern)
        board.add_tile(39, "Red", pattern)
        board.add_tile(11, "Blue", pattern)
        board.add_tile(18, "Navy", pattern)
        board.add_tile(24, "Blue", pattern)
        num_of_cats = cat.num_of_cats
        # should still only be 1
        self.assertEqual(num_of_cats, 1,
                         "Pattern was: " + pattern + " and required length was: " + str(cat.num_of_tiles))

    def test_get_score_for_complete_board(self):
        """
        Tests that the correct score is returned for a specific board
        Score should be 27
        3 buttons (1 blue, 1 navy, 1 purple)
        2 cats (gwen plants , coconut four)
        :return:
        """
        board = Board.Board(1)
        board.board[17].requirement = "aa-bb-cc"
        board.board[25].requirement = "aa-bb-c-d"
        board.board[30].requirement = "aaaa-bb"

        tibbit = Cats.Cat("Tibbit", 5, 4)
        tibbit.pattern_1 = "Stripes"
        tibbit.pattern_2 = "Reeds"
        coconut = Cats.Cat("Coconut", 7, 5)
        coconut.pattern_1 = "Four"
        coconut.pattern_2 = "Dots"
        gwen = Cats.Cat("Gwen", 11, 7)
        gwen.pattern_1 = "Leaf"
        gwen.pattern_2 = "Plants"
        board.cats.clear()  # Empty cats to set custom cats
        board.cats.append(tibbit)
        board.cats.append(gwen)
        board.cats.append(coconut)
        # Add the 2 tiles
        board.add_tile(8, 'Purple', 'Plants')
        board.add_tile(9, 'Red', 'Plants')
        board.add_tile(10, 'Navy', 'Plants')
        board.add_tile(11, 'Yellow', 'Plants')
        board.add_tile(12, 'Blue', 'Dots')
        board.add_tile(15, 'Blue', 'Four')
        board.add_tile(16, 'Yellow', 'Plants')
        board.add_tile(18, 'Blue', 'Leaf')
        board.add_tile(19, 'Blue', 'Plants')
        board.add_tile(22, 'Red', 'Plants')
        board.add_tile(23, 'Green', 'Plants')
        board.add_tile(24, 'Blue', 'Plants')
        board.add_tile(26, 'Yellow', 'Plants')
        board.add_tile(29, 'Green', 'Plants')
        board.add_tile(31, 'Purple', 'Dots')
        board.add_tile(32, 'Purple', 'Four')
        board.add_tile(33, 'Navy', 'Plants')
        board.add_tile(36, 'Purple', 'Plants')
        board.add_tile(37, 'Purple', 'Leaf')
        board.add_tile(38, 'Navy', 'Four')
        board.add_tile(39, 'Purple', 'Four')
        board.add_tile(40, 'Navy', 'Four')

        open_positions = board.open_positions
        score = board.get_score()
        buttons = board.buttons
        pos17_score = board.board[17].check_design_goal_reached()
        pos25_score = board.board[25].check_design_goal_reached()
        pos30_score = board.board[30].check_design_goal_reached()
        pos30_neighbors = []
        for n in board.board[30].get_neighbors():
            pos30_neighbors.append((n.tile_id, n.colour, n.pattern))
        rainbows = board.count_rainbows()
        cat1 = board.cats[0].num_of_cats
        cats2 = board.cats[1].num_of_cats
        cats3 = board.cats[2].num_of_cats

        board_info = "==== Board Info ===="
        board_info += "\nScore = " + str(score) + "\nOpen positions: " + str(open_positions)
        board_info += "\nButtons = " + str(buttons) + "\nRainbows = " + str(rainbows) + \
                      "\nPos 17 = " + str(pos17_score)
        board_info += "\nPos 25 = " + str(pos25_score) + "\nPos 30 score = " + str(pos30_score)
        board_info += "\nCat 1 (tibbit) = " + str(cat1) + "\nCat 2 (gwen) =" + str(
            cats2) + "\nCat 3 (coconut) = " + str(cats3)
        self.assertEqual(score, 27, board_info)

    def test_get_score_for_complete_board_2(self):
        """
        Tests that the correct score is returned for a specific board
        Score should be 53
        3 buttons (1 blue, 1 blue, 1 red)
        2 cats (gwen four , tibbit leaf)
        17 aa-bb-cc only pattern complete
        25 aaaa-bb colour and pattern complete
        30 aaa-bb-c only pattern complete
        :return:
        """
        board = Board.Board(1)
        board.board[17].requirement = "aa-bb-cc"
        board.board[25].requirement = "aaaa-bb"
        board.board[30].requirement = "aaa-bb-c"

        tibbit = Cats.Cat("Tibbit", 5, 4)
        tibbit.pattern_1 = "Plants"
        tibbit.pattern_2 = "Leaf"
        cira = Cats.Cat("Cira", 9, 6)
        cira.pattern_1 = "Reeds"
        cira.pattern_2 = "Dots"
        gwen = Cats.Cat("Gwen", 11, 7)
        gwen.pattern_1 = "Four"
        gwen.pattern_2 = "Stripes"
        board.cats.clear()  # Empty cats to set custom cats
        board.cats.append(tibbit)
        board.cats.append(gwen)
        board.cats.append(cira)
        # Add the 25 tiles
        tiles = [(8, 'Red', 'Reeds'), (9, 'Navy', 'Leaf'), (10, 'Red', 'Four'), (11, 'Red', 'Dots'),
                 (12, 'Green', 'Four'), (15, 'Purple', 'Leaf'), (16, 'Green', 'Leaf'), (18, 'Blue', 'Four'),
                 (19, 'Navy', 'Four'), (22, 'Blue', 'Dots'), (23, 'Navy', 'Reeds'), (24, 'Blue', 'Reeds'),
                 (26, 'Navy', 'Four'), (29, 'Yellow', 'Dots'), (31, 'Purple', 'Stripes'), (32, 'Blue', 'Reeds'),
                 (33, 'Blue', 'Four'), (36, 'Navy', 'Reeds'), (37, 'Red', 'Reeds'), (38, 'Yellow', 'Reeds'),
                 (39, 'Yellow', 'Dots'), (40, 'Purple', 'Plants')]
        for n in tiles:
            board.add_tile(n[0], n[1], n[2])

        open_positions = board.open_positions
        score = board.get_score()
        buttons = board.buttons
        pos17_score = board.board[17].check_design_goal_reached()
        pos25_score = board.board[25].check_design_goal_reached()
        pos30_score = board.board[30].check_design_goal_reached()
        pos30_neighbors = []
        for n in board.board[30].get_neighbors():
            pos30_neighbors.append((n.tile_id, n.colour, n.pattern))
        rainbows = board.count_rainbows()
        cat1 = board.cats[0].num_of_cats
        cats2 = board.cats[1].num_of_cats
        cats3 = board.cats[2].num_of_cats

        board_info = "==== Board Info ===="
        board_info += "\nScore = " + str(score) + "\nOpen positions: " + str(open_positions)
        board_info += "\nButtons = " + str(buttons) + "\nRainbows = " + str(rainbows) + \
                      "\nPos 17 = " + str(pos17_score)
        board_info += "\nPos 25 = " + str(pos25_score) + "\nPos 30 score = " + str(pos30_score)
        board_info += "\nCat 1 (tibbit) = " + str(cat1) + "\nCat 2 (gwen) =" + str(
            cats2) + "\nCat 3 (cira) = " + str(cats3)
        self.assertEqual(score, 62, board_info)

    def test_get_score_for_complete_board_3(self):
        """
        Tests that the correct score is returned for a specific board
        This is a losing board so itt should score 0
        17 'aaa-bbb' None
        25 'aaaa-bb' None
        30 'aa-bb-c-d' None
        :return:
        """
        board = Board.Board(1)
        board.board[17].requirement = 'aaa-bbb'
        board.board[25].requirement = "aaaa-bb"
        board.board[30].requirement = 'aa-bb-c-d'

        tibbit = Cats.Cat("Tibbit", 5, 4)
        tibbit.pattern_1 = "Four"
        tibbit.pattern_2 = "Stripes"
        cira = Cats.Cat("Cira", 9, 6)
        cira.pattern_1 = "Reeds"
        cira.pattern_2 = "Plants"
        coconut = Cats.Cat("Coconut", 7, 5)
        coconut.pattern_1 = "Dots"
        coconut.pattern_2 = "Leaf"
        board.cats.clear()  # Empty cats to set custom cats
        board.cats.append(tibbit)
        board.cats.append(coconut)
        board.cats.append(cira)
        # Add the 25 tiles
        tiles = [(8, 'Purple', 'Reeds'), (9, 'Green', 'Stripes'), (10, 'Yellow', 'Reeds'), (11, 'Blue', 'Stripes'),
                 (12, 'Red', 'Four'), (15, 'Green', 'Leaf'), (16, 'Red', 'Reeds'), (18, 'Purple', 'Plants'),
                 (19, 'Yellow', 'Reeds'), (22, 'Blue', 'Four'), (23, 'Green', 'Four'), (24, 'Purple', 'Stripes'),
                 (26, 'Green', 'Leaf'), (29, 'Red', 'Leaf'), (31, 'Yellow', 'Leaf'), (32, 'Blue', 'Dots'),
                 (33, 'Purple', 'Stripes'), (36, 'Navy', 'Leaf'), (37, 'Blue', 'Four'), (38, 'Yellow', 'Stripes'),
                 (39, 'Green', 'Four'), (40, 'Yellow', 'Reeds')]
        for n in tiles:
            board.add_tile(n[0], n[1], n[2])

        open_positions = board.open_positions
        score = board.get_score()
        buttons = board.buttons
        pos17_score = board.board[17].check_design_goal_reached()
        pos25_score = board.board[25].check_design_goal_reached()
        pos30_score = board.board[30].check_design_goal_reached()
        pos30_neighbors = []
        for n in board.board[30].get_neighbors():
            pos30_neighbors.append((n.tile_id, n.colour, n.pattern))
        rainbows = board.count_rainbows()
        cat1 = board.cats[0].num_of_cats
        cats2 = board.cats[1].num_of_cats
        cats3 = board.cats[2].num_of_cats

        board_info = "==== Board Info ===="
        board_info += "\nScore = " + str(score) + "\nOpen positions: " + str(open_positions)
        board_info += "\nButtons = " + str(buttons) + "\nRainbows = " + str(rainbows) + \
                      "\nPos 17 = " + str(pos17_score)
        board_info += "\nPos 25 = " + str(pos25_score) + "\nPos 30 score = " + str(pos30_score)
        board_info += "\nCat 1 (tibbit) = " + str(cat1) + "\nCat 2 (coconut) =" + str(
            cats2) + "\nCat 3 (cira) = " + str(cats3)
        self.assertEqual(score, 0, board_info)

    def test_get_score_for_complete_board_4(self):
        """
        Tests that the correct score is returned for a specific board
        This is should score a total of 35, with following buttons: 2 yellow, 2 red,
        1 blue, 1 navy, 1 green
        17 'aaa-bb-c' colour only (7)
        25 'aaaa-bb' None
        30 'aa-bb-cc' colour only (7)
        NO cats
        :return:
        """
        board = Board.Board(1)
        board.board[17].requirement = 'aaa-bb-c'
        board.board[25].requirement = "aaaa-bb"
        board.board[30].requirement = 'aa-bb-cc'

        tibbit = Cats.Cat("Tibbit", 5, 4)
        tibbit.pattern_1 = "Reeds"
        tibbit.pattern_2 = "Plants"
        cira = Cats.Cat("Cira", 9, 6)
        cira.pattern_1 = "Dots"
        cira.pattern_2 = "Stripes"
        coconut = Cats.Cat("Coconut", 7, 5)
        coconut.pattern_1 = "Four"
        coconut.pattern_2 = "Leaf"
        board.cats.clear()  # Empty cats to set custom cats
        board.cats.append(tibbit)
        board.cats.append(coconut)
        board.cats.append(cira)
        # Add the 25 tiles
        tiles = [(8, 'Green', 'Plants'), (9, 'Blue', 'Plants'), (10, 'Blue', 'Leaf'), (11, 'Yellow', 'Plants'),
                 (12, 'Red', 'Plants'), (15, 'Green', 'Leaf'), (16, 'Yellow', 'Leaf'), (18, 'Navy', 'Dots'),
                 (19, 'Red', 'Four'), (22, 'Yellow', 'Leaf'), (23, 'Yellow', 'Stripes'), (24, 'Blue', 'Four'),
                 (26, 'Purple', 'Four'), (29, 'Red', 'Reeds'), (31, 'Navy', 'Four'), (32, 'Navy', 'Four'),
                 (33, 'Yellow', 'Stripes'), (36, 'Red', 'Leaf'), (37, 'Navy', 'Four'), (38, 'Purple', 'Leaf'),
                 (39, 'Red', 'Reeds'), (40, 'Yellow', 'Reeds')]
        for n in tiles:
            board.add_tile(n[0], n[1], n[2])

        open_positions = board.open_positions
        score = board.get_score()
        buttons = board.buttons
        pos17_score = board.board[17].check_design_goal_reached()
        pos25_score = board.board[25].check_design_goal_reached()
        pos30_score = board.board[30].check_design_goal_reached()
        pos30_neighbors = []
        for n in board.board[30].get_neighbors():
            pos30_neighbors.append((n.tile_id, n.colour, n.pattern))
        rainbows = board.count_rainbows()
        cat1 = board.cats[0].num_of_cats
        cats2 = board.cats[1].num_of_cats
        cats3 = board.cats[2].num_of_cats

        board_info = "==== Board Info ===="
        board_info += "\nScore = " + str(score) + "\nOpen positions: " + str(open_positions)
        board_info += "\nButtons = " + str(buttons) + "\nRainbows = " + str(rainbows) + \
                      "\nPos 17 = " + str(pos17_score)
        board_info += "\nPos 25 = " + str(pos25_score) + "\nPos 30 score = " + str(pos30_score)
        board_info += "\nCat 1 (tibbit) = " + str(cat1) + "\nCat 2 (coconut) = " + str(
            cats2) + "\nCat 3 (cira) = " + str(cats3)
        self.assertEqual(score, 35, board_info)


if __name__ == '__main__':
    unittest.main()
