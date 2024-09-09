import random


def tournament_selection(population, fitness_values, tournament_size):
    
    # Step 1: Detect predetermined numbers of chromosomes are randomly selected from the population
    tournament_candidates = random.sample(range(len(population)), tournament_size)
    # Step 2: Extract index of the chromosome with the best fitness value
    winner_index = max(tournament_candidates, key=lambda i: fitness_values[i])

    return population[winner_index]

def roulette_wheel_selection(population, fitness_values):
    
    # Step 1: Generate random number
    r = random.random()

    # Step 2: Computes the probability of the population
    population_prob = fitness_values / sum(fitness_values)

    # Step 3: Select the chromosome based on a fitness value and cumsum of probs
    cumulative_prob = 0
    winner_index = 0
    for idx, probability in enumerate(population_prob):
        cumulative_prob += probability
        if r <= cumulative_prob:
            winner_index = idx
            break
    
    return population[winner_index]