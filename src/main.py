""" Main file that is run when the game is executed"""
import random

from src import Calico
from src import Agents
import mcts
import csv


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
    #human_play()

    #random_agent_play(100)

    # MCTS agent. parameters as follows: MCTS(Number of games, MCTS iterations)
    #mcts_agent_play(1, 300)

    # Greedy agent. parameters as follows: Greedy(Number of games)
    #greedy_agent_play(10)

    # DQN Agent. Make sure dqn_final.pth present. parameters as follows: DQN(Number of games)
    DQN_agent_play(100)


# !!!!!!!!!!!!!!!!!!!!!!!!! Normal agent plays (and human play) scripts !!!!!!!!!!!!!!!!!!!!!!!
def greedy_agent_play(number_of_games):
    average = 0
    highest = 0
    best_board = None
    lowest = 999999999
    for i in range(1, (number_of_games + 1)):
        print("Starting Game: " + str(i))
        agent = Agents.GreedyAgentRandom(0)
        game = Calico.Calico(1, [agent])
        score = game.start_game(1, [agent])[0][1]
        if score > highest:
            highest = score
            best_board = game.players_board[0]
        if score < lowest:
            lowest = score
        average = calculate_running_average(average, score, i)
        if i % 10 == 0:
            print(average)

    print("\n==== Final Average ====")
    print("     " + str(average))
    print("\n==== Highest Score ====")
    print("     " + str(highest))
    print("\n==== Lowest score ====")
    print("     " + str(lowest))
    # Save the position of the current board
    layout = []  # (id, colour, pattern)
    requirements = []  # (id, requirement)
    cats = []  # (name, pattern1, pattern2)

    for pus in best_board.cats:
        cats.append((pus.name, pus.pattern_1, pus.pattern_2))

    for tile in best_board.board:
        # tile is the tile object
        if tile.normal_tile:
            layout.append((tile.tile_id, tile.colour, tile.pattern))
        else:
            requirements.append((tile.id, tile.requirement))

    print("\n==== Highest Score Layout====")
    print(layout)
    print("==== requirements====")
    print(requirements)
    print("==== Cats ====")
    print(cats)


def mcts_agent_play(number_of_games, iterations):
    average = 0
    highest = 0
    best_board = None
    lowest = 999999999
    for i in range(1, (number_of_games + 1)):
        print("Starting Game: " + str(i))
        agent = mcts.MCTS(0, iterations)
        game = Calico.Calico(1, [agent])
        score = game.start_game(1, [agent])[0][1]
        if score > highest:
            highest = score
            best_board = game.players_board[0]
        if score < lowest:
            lowest = score
        average = calculate_running_average(average, score, i)

    print("\n==== Final Average ====")
    print("     " + str(average))
    print("\n==== Highest Score ====")
    print("     " + str(highest))
    print("\n==== Lowest score ====")
    print("     " + str(lowest))
    # Save the position of the current board
    layout = []  # (id, colour, pattern)
    requirements = []  # (id, requirement)
    cats = []  # (name, pattern1, pattern2)

    for pus in best_board.cats:
        cats.append((pus.name, pus.pattern_1, pus.pattern_2))

    for tile in best_board.board:
        # tile is the tile object
        if tile.normal_tile:
            layout.append((tile.tile_id, tile.colour, tile.pattern))
        else:
            requirements.append((tile.id, tile.requirement))

    print("\n==== Highest Score Layout====")
    print(layout)
    print("==== requirements====")
    print(requirements)
    print("==== Cats ====")
    print(cats)


def random_agent_play(number_of_games):
    agent = Agents.RandomAgent(0)
    agents = [agent]
    average = 0
    highest = 0
    best_board = None
    lowest = 999999999
    for i in range(1, (number_of_games + 1)):
        print("Starting Game: " + str(i))
        game = Calico.Calico(1, agents)
        game.select_board_colour(0, 3)
        score = game.start_game(1, agents)[0][1]
        if score > highest:
            highest = score
            best_board = game.players_board[0]
        if score < lowest:
            lowest = score
        average = calculate_running_average(average, score, i)
        if i % 100 == 0:
            print(f"Average: {average}")

    print("\n==== Final Average ====")
    print("     " + str(average))
    print("\n==== Highest Score ====")
    print("     " + str(highest))
    print("\n==== Lowest score ====")
    print("     " + str(lowest))

    print("==== Best Board ====")
    # Save the position of the current board
    layout = []  # (id, colour, pattern)
    requirements = []  # (id, requirement)
    cats = []  # (name, pattern1, pattern2)

    for pus in best_board.cats:
        cats.append((pus.name, pus.pattern_1, pus.pattern_2))

    for tile in best_board.board:
        # tile is the tile object
        if tile.normal_tile:
            layout.append((tile.tile_id, tile.colour, tile.pattern))
        else:
            requirements.append((tile.id, tile.requirement))
    print("\n==== Highest Score Layout====")
    print(layout)
    print("==== requirements====")
    print(requirements)
    print("==== Cats ====")
    print(cats)


def DQN_agent_play(number_of_games):
    agent = Agents.DQNAgent()
    agents = [agent]
    average = 0
    highest = 0
    best_board = None
    lowest = 999999999
    for i in range(1, (number_of_games + 1)):
        print("Starting Game: " + str(i))
        game = Calico.Calico(1, agents)
        game.select_board_colour(0, 3)
        score = game.start_game(1, agents)[0][1]
        if score > highest:
            highest = score
            best_board = game.players_board[0]
        if score < lowest:
            lowest = score
        average = calculate_running_average(average, score, i)
        if i % 100 == 0:
            print(f"Average: {average}")

    print("\n==== Final Average ====")
    print("     " + str(average))
    print("\n==== Highest Score ====")
    print("     " + str(highest))
    print("\n==== Lowest score ====")
    print("     " + str(lowest))

    print("==== Best Board ====")
    # Save the position of the current board
    layout = []  # (id, colour, pattern)
    requirements = []  # (id, requirement)
    cats = []  # (name, pattern1, pattern2)

    for pus in best_board.cats:
        cats.append((pus.name, pus.pattern_1, pus.pattern_2))

    for tile in best_board.board:
        # tile is the tile object
        if tile.normal_tile:
            layout.append((tile.tile_id, tile.colour, tile.pattern))
        else:
            requirements.append((tile.id, tile.requirement))
    print("\n==== Layout====")
    print(layout)
    print("==== requirements====")
    print(requirements)
    print("==== Cats ====")
    print(cats)


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


# !!!!!!!! Scripts for project below, might not work unless you make some changes in code !!!!!!!!!!

# !!!!!!!!!!!!!!! CSV File games all agents + all the solos !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def all_agents_1000():
    agents = [Agents.DQNAgent(), Agents.RandomAgent(1), Agents.GreedyAgentRandom(2),
              mcts.MCTS(3, 300)]

    with open(f'all_agents_1000.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        for i in range(1000):
            try:
                game = Calico.Calico(4, agents)
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game.select_board_colour(2, numbers[2])
                game.select_board_colour(3, numbers[3])
                game_info = game.start_game(4, agents)
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of All Agents complete.")


def DQN_agent_10000():
    agent = Agents.DQNAgent()

    with open(f'DQN_agent_results_10000.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        for i in range(10000):
            try:
                game = Calico.Calico(1, [agent])
                game.select_board_colour(0, random.choice(range(1, 5)))
                game.start_game(1, [agent])
                game_info = game.single_player_give_game_info()
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of DQN complete.")


def MCTS_300_agent_10000():
    agent = mcts.MCTS(0, 300)

    with open(f'MCTS_agent_results_10000.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        for i in range(10000):
            try:
                game = Calico.Calico(1, [agent])
                game.select_board_colour(0, random.choice(range(1, 5)))
                game.start_game(1, [agent])
                game_info = game.single_player_give_game_info()
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of MCTS complete.")


def MCTS_10_to_1000():
    """
    This function will run 100 games of MCTS at different intervals, and then append each game's result
    to a separate CSV file for the corresponding interval.
    """
    import csv
    intervals = [10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    for number in intervals:
        mcts_agent = mcts.MCTS(0, number)
        print("Starting interval: " + str(number))

        with open(f'mcts_results_{number}.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            for i in range(100):  # Play the 100 games with those intervals
                try:
                    game = Calico.Calico(1, [mcts_agent])
                    game.select_board_colour(0, random.choice(range(1, 5)))
                    game.start_game(1, [mcts_agent])
                    game_info = game.single_player_give_game_info()
                    writer.writerow(
                        [i + 1] + game_info)  # Write game number and game info to the CSV file
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
        print(f"Interval {number} finished.")


def random_agent_10000():
    import csv

    agent = Agents.RandomAgent(0)

    with open(f'random_agent_results_10000.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        for i in range(10000):
            try:
                game = Calico.Calico(1, [agent])
                game.select_board_colour(0, random.choice(range(1, 5)))
                game.start_game(1, [agent])
                game_info = game.single_player_give_game_info()
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of greedy complete.")


def greedy_agent_10000():
    import csv

    agent = Agents.GreedyAgentRandom(0)

    with open(f'greedy_agent_results_3000.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        for i in range(10000):  # Play the 100 games with those intervals
            try:
                game = Calico.Calico(1, [agent])
                game.select_board_colour(0, random.choice(range(1, 5)))
                game.start_game(1, [agent])
                game_info = game.single_player_give_game_info()
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of greedy complete.")


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 1 v 1 agent scripts !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def greedy_vs_mcts():
    with open(f'Greedy_VS_MCTS.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000):
            try:
                greedy_agent = Agents.GreedyAgentRandom(0)
                mcts_agent = mcts.MCTS(1, 300)
                game = Calico.Calico(2, [greedy_agent, mcts_agent])
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, [greedy_agent, mcts_agent])
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of Greedy VS MCTS complete.")


def greedy_vs_greedy():
    with open(f'Greedy_VS_Greedy.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(10000):
            if i % 100 == 0: print("Progress: " + str(i))
            try:
                greedy_agent = Agents.GreedyAgentRandom(0)
                second_greedy = Agents.GreedyAgentRandom(1)
                game = Calico.Calico(2, [greedy_agent, second_greedy])
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, [greedy_agent, second_greedy])
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of Greedy VS Greedy complete.")


def random_vs_mcts():
    agents = [Agents.RandomAgent(0), mcts.MCTS(1, 300)]
    with open(f'Random_VS_MCTS.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000):
            try:
                game = Calico.Calico(2, agents)
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, agents)
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of Random VS MCTS complete.")


def DQN_vs_mcts():
    agents = [Agents.DQNAgent(), mcts.MCTS(1, 300)]
    with open(f'DQN_VS_MCTS.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000):
            try:
                game = Calico.Calico(2, agents)
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, agents)
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of DQN VS MCTS complete.")


def DQN_vs_random():
    agents = [Agents.DQNAgent(), Agents.RandomAgent(1)]
    with open(f'DQN_VS_Random.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000):
            try:
                game = Calico.Calico(2, agents)
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, agents)
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of DQN VS Random complete.")


def DQN_vs_greedy():
    agents = [Agents.DQNAgent(), Agents.GreedyAgentRandom(1)]
    with open(f'DQN_VS_Greedy.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000):
            try:
                game = Calico.Calico(2, agents)
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, agents)
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of DQN VS Greedy complete.")


def Random_vs_greedy():
    agents = [Agents.RandomAgent(0), Agents.GreedyAgentRandom(1)]
    with open(f'Random_vs_Greedy.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for i in range(1000):
            try:
                game = Calico.Calico(2, agents)
                numbers = [1, 2, 3, 4]
                random.shuffle(numbers)
                game.select_board_colour(0, numbers[0])
                game.select_board_colour(1, numbers[1])
                game_info = game.start_game(2, agents)
                writer.writerow(
                    [i + 1] + game_info)  # Write game number and game info to the CSV file
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    print(f"Simulation of Random VS Greedy complete.")


def calculate_running_average(previous_avg, new_num, n):
    return ((previous_avg * (n - 1)) + new_num) / n


main()
