import axelrod as axl
from deap import base, creator, tools
import random

# --- AXELROD EXAMPLE ---
# players = (axl.Cooperator(), axl.Alternator())
# match = axl.Match(players, 5)
# match.play()
#
# print(match.result)
# print(match.final_score())
# print(match.winner())
#
# print("-----------------------------")
#
# competitors = [axl.Cooperator(), axl.Defector(), axl.TitForTat(), axl.Grudger()]
# tournament = axl.Tournament(competitors, turns=3, repetitions=1)
# res = tournament.play(keep_interactions=True)
#
# print("\nInteractions between players")
# matches = []
# for player_index, interaction in sorted(res.interactions.items()):
#     player1 = tournament.players[player_index[0]]
#     player2 = tournament.players[player_index[1]]
#     match = axl.Match((player1, player2), turns=3)
#     match.result = interaction[0]
#     matches.append(match)
#
# print("\nPlayers ranked")
# c = 1
# for p in res.ranked_names:
#     print("%d: %s" % (c, p))
#     c += 1

# plot = axl.Plot(res)
# p = plot.boxplot()
# p.show()


# Fitness Function
def fit_func(individual):
    if len(individual) == 64:
        return 0


# playing a bit string strategy
def play_ind(bits):
    score = 0
    for p1, p2 in zip(bits[0::2], bits[1::2]):
        if p1 == '1':
            if p2 == '1':
                score += 3
            else:
                score += 0
        else:
            if p2 == '1':
                score += 5
            else:
                score += 1
    return score


# Create the toolbox with the right parameters
def create_toolbox(num_bits):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Initialize the toolbox
    toolbox = base.Toolbox()

    # Generate attributes
    toolbox.register("attr_bool", random.randint, 0, 1)

    # Initialize structures
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, num_bits)

    # Define the population to be a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register the evaluation operator
    toolbox.register("evaluate", fit_func)

    # Register the crossover operator
    toolbox.register("mate", tools.cxTwoPoint)

    # Register a mutation operator
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    # Operator for selecting individuals for breeding
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox