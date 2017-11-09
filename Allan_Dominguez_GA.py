from deap import base, creator, tools
import random


# DEFAULTS
GAME_LENGTH = 70
MEMORY_DEFAULT = 3
N_GEN = 5
PWR = 3
POP_SIZE = 100


# playing a game (represented as a bit string)
def play_ind(bits):
    score = 0
    # opp_sc = 0
    for p1, p2 in zip(bits[0::2], bits[1::2]):
        if p1 == '1':
            if p2 == '1':
                score += 3
                # opp_sc += 3
            else:
                score += 0
                # opp_sc += 5
        else:
            if p2 == '1':
                score += 5
                # opp_sc += 0
            else:
                score += 1
                # opp_sc += 1
    return score


# build a game (bit string) from 2 players (i1, i2)
def eval_two(i1, i2, p=MEMORY_DEFAULT):

    # history setup; all D for even start
    game = ''
    i = 0
    while i < p:
        game += '00'
        i += 1

    # build string based on the 2 individuals (strategies)
    t = 0
    depth = p * 2   # length of string history of p memory depth
    while t < GAME_LENGTH:
        ith = get_ith(game[-depth:], p)
        game += str(i1[ith])
        game += str(i2[ith])
        t += 1

    # get score of first player
    p1 = play_ind(game)
    return p1,


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


# function to return the bit passed
def single_bit(bit):
    return bit


# Create the toolbox with the right parameters
def create_toolbox(num_bits):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Initialize the toolbox
    toolbox = base.Toolbox()

    # Generate attributes
    toolbox.register("attr_bool", random.randint, 0, 1)

    # Initialises a Defector individual
    toolbox.register("defector", single_bit, 0)
    toolbox.register("def_ind", tools.initRepeat, creator.Individual, toolbox.defector, num_bits)

    # Initialises a Cooperator individual
    toolbox.register("cooperator", single_bit, 1)
    toolbox.register("coop_ind", tools.initRepeat, creator.Individual, toolbox.cooperator, num_bits)

    # Initialize structures
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, num_bits)

    # Define the population to be a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Register the eval2 (evaluate) operator
    toolbox.register("eval2", eval_two)

    # Register the crossover operator
    toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=0.5)

    # Register a mutation operator
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)

    # Operator for selecting individuals for breeding
    toolbox.register("select", tools.selRoulette)

    return toolbox


# determine 'a' in formula: a * f + b
def a_scale(avg, mnm):
    return avg/(avg-mnm)


# determine 'b' in formula: a * f + b
def b_scale(avg, mnm):
    return (-mnm)*(avg/(avg-mnm))


# evaluates fitness of each individual in population
def eval_pop_fit(population, toolbox=create_toolbox(4**PWR)):
    c = len(population)
    avg = 0
    mnm = 1000

    # get raw fitness of each individual by playing against all other
    # individuals in population
    fits = []
    for i in population:
        score = 0
        for j in population:
            e1 = toolbox.eval2(i, j, PWR)
            score += e1[0]
        ind_avg = score/c
        fits.append(ind_avg)
        avg += ind_avg

    # calculate the scaled fitness and return that list
    avg = avg/c
    a = a_scale(avg, mnm)
    b = b_scale(avg, mnm)
    fits2 = []
    for x in fits:
        f = a * x + b
        fits2.append((f,))
    return fits2


# main function to generate a strategy
def strategy_gen(pwr=3):
    num_bits = 4 ** pwr
    global PWR
    PWR = pwr

    toolbox = create_toolbox(num_bits)

    random.seed(7)

    population = toolbox.population(n=POP_SIZE)

    # add a Defector and Cooperator to population
    # defector = toolbox.def_ind()
    # population.append(defector)
    # cooperator = toolbox.coop_ind()
    # population.append(cooperator)

    prob_cross, prob_mute = 0.5, 0.2

    num_generations = N_GEN

    print('\nStarting the evolution process')

    # Evaluate the entire population
    f = eval_pop_fit(population, toolbox)

    for ind, fit in zip(population, f):
        ind.fitness.values = fit
        print("Individual: ", ind)
        print("Fitness: ", fit)

    print('\nEvaluated', len(population), 'individuals')

    # Iterate through generations
    for g in range(num_generations):
        print("\n===== Generation", g)

        # Select the next generation individuals
        n = len(population)
        offspring = toolbox.select(population, n)

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

        # Re-evaluate all individuals
        # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        f2 = eval_pop_fit(offspring, toolbox)

        # fitnesses = map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, f2):
            ind.fitness.values = fit

        print('Re-evaluated', len(offspring), 'individuals')

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

    for pop in population:
        print("Individual:", pop)
        print("Fitness: ", pop.fitness.values[0])

    best_ind = tools.selBest(population, 1)[0]
    print('\nBest individual:\n', best_ind)
    print('\nFitness:', best_ind.fitness.values[0])

    return best_ind


if __name__ == "__main__":
    strategy_gen()

