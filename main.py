import axelrod as axl
from deap import base, creator, tools
import random, re

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
    return play_ind(individual),


# playing a bit string strategy
def play_ind(bits):
    score = 0
    for p1, p2 in zip(bits[0::2], bits[1::2]):
        if p1 == 1:
            if p2 == 1:
                score += 3
            else:
                score += 0
        else:
            if p2 == 1:
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
    toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.5)

    # Register a mutation operator
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    # Operator for selecting individuals for breeding
    toolbox.register("select", tools.selRoulette)   # based on fitness

    return toolbox


if __name__ == "__main__":
    num_bits = 64

    toolbox = create_toolbox(num_bits)

    random.seed(7)

    population = toolbox.population(n=12)

    prob_cross, prob_mute = 0.5, 0.2

    num = input("How many generations? ")

    num_generations = int(re.search(r'\d+', num).group())

    print('\nStarting the evolution process')

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    print('\nEvaluated', len(population), 'individuals')

    # Iterate through generations
    for g in range(num_generations):
        print("\n===== Generation", g)

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        print(len(offspring))

        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            # Cross two individuals
            if random.random() < prob_cross:
                toolbox.mate(child1, child2)

                # "Forget" the fitness values of the children
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation
        for mutant in offspring:
            # Mutate an individual
            if random.random() < prob_mute:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print('Re-evaluated', len(invalid_ind), 'individuals')

        # The population is entirely replaced by the offspring
        population[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in population]

        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print('Min =', min(fits), ', Max =', max(fits))
        print('Average =', round(mean, 2), ', Standard deviation =',
              round(std, 2))

    print("\n==== End of evolution")

    best_ind = tools.selBest(population, 1)[0]
    print('\nBest individual:\n', best_ind)
    print('\nFitness:', play_ind(best_ind))