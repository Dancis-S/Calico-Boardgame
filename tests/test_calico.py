""" Contains tests for the Calico class """
import unittest
from src import Calico


class TestCalico(unittest.TestCase):

    def test_tile_bag_filled(self):
        """
        Test to see that the bag contains 102 playable tiles that the player
        can get. (initial(108) - shop(3) - 1player(3) = 102)
        :return:
        """
        game = Calico.Calico(1, [])
        bag_amount = len(game.tiles_bag)
        self.assertEqual(bag_amount, 102, "Bag contains: " + str(bag_amount))

    def test_setup_shop(self):
        """
        Test that makes sure that the shop is set up properly at the start of
        the game
        :return:
        """
        game = Calico.Calico(2, [])
        shop_count = len(game.shop)
        self.assertEqual(shop_count, 3, "Shop contains: " + str(shop_count))

    def test_3_board_setup(self):
        """
        Tests that 3 boards are initialised for the 3 players
        :return:
        """
        game = Calico.Calico(3, [])
        num_of_boards = len(game.players_board)
        self.assertEqual(num_of_boards, 3, "Num of boards: " + str(num_of_boards))

    def test_2_player_stack_setup(self):
        """
        Tests that the stack for 2 player set up is initialised properly, where
        each player has 3 playable tiles randomly assigned to them (does not
        test for randomness, just that they get 3 tiles each)
        :return:
        """
        game = Calico.Calico(2, [])
        player1 = len(game.players_stack[0])
        player2 = len(game.players_stack[1])
        player_count = len(game.players_stack)
        self.assertTrue(player1 == player2 and player_count == 2)


if __name__ == '__main__':
    unittest.main()
