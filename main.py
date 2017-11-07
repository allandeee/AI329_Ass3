import axelrod as axl
from deap import base, creator, tools
import random, re

# DEFAULTS
GAME_LENGTH = 70
MEMORY_DEFAULT = 3


# Fitness Function
def fit_func(individual):
    return play_ind(individual),


# playing a bit string strategy
def play_ind(bits):
    score = 0
    opp_sc = 0
    for p1, p2 in zip(bits[0::2], bits[1::2]):
        if p1 == '1':
            if p2 == '1':
                score += 3
                opp_sc += 3
            else:
                score += 0
                opp_sc += 5
        else:
            if p2 == '1':
                score += 5
                opp_sc += 0
            else:
                score += 1
                opp_sc += 1
    return score, opp_sc


def eval_two(i1, i2, p=MEMORY_DEFAULT):

    # history setup; all C for even start
    game = ''
    i = 0
    while i < p:
        game += '11'
        i += 1

    # build string based on the 2 individuals (strategies)
    t = 0
    depth = p * 2   # length of string history of p memory depth
    while t < GAME_LENGTH:
        ith = get_ith(game[-depth:], p)
        game += str(i1[ith])
        game += str(i2[ith])
        t += 1

    # get scores of individuals
    p1, p2 = play_ind(game)
    return p1,p2


# get the index of the the next move (from strategy bit string)
def get_ith(hist, mem_depth=MEMORY_DEFAULT):
    pairs = ['11', '10', '01', '00']
    vals = []
    for c1, c2 in zip(hist[0::2], hist[1::2]):
        pair = c1 + c2
        vals.append(pairs.index(pair))
    i = 0
    ith = 0
    while i < mem_depth:
        ith += vals[i] * 4 ** (mem_depth - (i + 1))
        i += 1
    return ith


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

    toolbox.register("eval2", eval_two)

    # Register the crossover operator
    toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.5)

    # Register a mutation operator
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    # Operator for selecting individuals for breeding
    toolbox.register("select", tools.selTournament)   # based on fitness

    return toolbox


def off_sel(population):
    n = len(population)
    return toolbox.select(population, n, n)


if __name__ == "__main__":
    num = input("What depth? ")
    pwr = int(re.search(r'\d+', num).group())
    num_bits = 4**pwr

    toolbox = create_toolbox(num_bits)

    random.seed(7)

    population = toolbox.population(n=4)

    prob_cross, prob_mute = 0.5, 0.2

    num_generations = 10

    print('\nStarting the evolution process')

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, population))
    # ^ restructure that
    f = []
    for i1, i2 in zip(population[::2], population[1::2]):
        e1, e2 = toolbox.eval2(i1,i2,pwr)
        f.append((e1,))
        f.append((e2,))

    for ind, fit in zip(population, f):
        ind.fitness.values = fit

    print('\nEvaluated', len(population), 'individuals')

    # Iterate through generations
    for g in range(num_generations):
        print("\n===== Generation", g)

        # Select the next generation individuals
        offspring = off_sel(population)

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
        f2 = []
        for i1, i2 in zip(offspring[::2], offspring[1::2]):
            e1, e2 = toolbox.eval2(i1, i2, pwr)
            f.append((e1,))
            f.append((e2,))
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, f2):
            ind.fitness.values = fit

        print('Re-evaluated', len(offspring), 'individuals')

        # The population is entirely replaced by the offspring
        population[:] = offspring
        print(population)

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

