import random
from NEH_alg import neh

# Create individual in a population
def generate_random_population(num_jobs):
    chromosome = random.sample(range(num_jobs), num_jobs)
    return chromosome

# Create NEH Heuristic Solution
def neh_chromosome(p_ij, n_machines, n_jobs):
    seq = neh(p_ij, n_machines, n_jobs)[0]
    return seq

# Create Initial Population (Ps - 1 Randomly Generated + NEH Heuristic Solution)
def initial_population(population_size, neh_sequence, n_jobs):
    size = n_jobs
    population = [generate_random_population(size) for _ in range(population_size - 1)]   
    population.append(neh_sequence)   
    return population

# Calculate fitness value for each individual: (1 / Cmax)
def fitness_evaluation(obj_fun):
    fitness = 1 / obj_fun
    return fitness