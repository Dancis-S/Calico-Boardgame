""" Main file that is run when the game is executed"""
import random

from src import Calico

def main():
    """
    The code is unfortunately not user-friendly uncomment a function you would like to try.
    You can mess with the number of games and iterations (mcts only).
    Feel free to try the other functions (such as the 1v1 games) they might work, but be warned
    they don't produce console output they will produce a csv file similar to those submitted.
    All the functions put in the main function will work, but other functions you might want to
    try might require some code to be changed in Calico but most should work.
    """
    # For humans to play can be solo or multiplayer (no agents)
    human_play()

def human_play():
    while True:
        num_of_players = int(input("Enter the number of players: "))
        if num_of_players > 4 or num_of_players < 1:
            print("Invalid Number pick ")
        else:
            break

    print("Beginning game for " + str(num_of_players) + " players!")
    game = Calico.Calico(num_of_players, [])
    game.start_game(num_of_players, [])  # Calls the method to start the game

main()
