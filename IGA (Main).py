import random
import pandas as pd
import numpy as np
from NEH_alg import completion_time
from Instance import read_instance, read_excel
from Population import initial_population, fitness_evaluation, neh_chromosome, generate_random_population
from Selection import tournament_selection, roulette_wheel_selection
from Crossover import two_points_crossover, partially_mapped_crossover, similar_job_order_crossover, linear_order_crossover
from Mutation import arbitrary_three_job, arbitrary_two_job, shift_change
import plotly.figure_factory as ff

def improved_genetic_algorithm(p_ij, n_jobs, n_machines, population_size, crossover_prob, mutation_prob, roulette_wheel_prob, tournament_prob, two_point_prob,
                               pmx_prob, sjox_prob, lox_prob, three_job_prob, two_job_prob, shift_change_prob, mutation_multiplier,
                               num_generations, gen_limit_reassign, gen_limit_mutation_prob, tournament_size):
    countmut = 0
    cntrndpop = 0  
    k = 1
    M = [None]

    Populations = {}

    # Step 0: Create Initial Population (Ps - 1 Randomly Generated + NEH Heuristic Solution)
    pop = initial_population(population_size, neh_chromosome(p_ij, n_machines, n_jobs), n_jobs)

    # Build P(k)
    Populations[k] = pop
    
    # Step 1: Fitness Evaluation based on Objective Function for each individual in Population
    # Evaluate objective function for each chromosome in population
    fitness_values = [fitness_evaluation(completion_time(chromosome, p_ij, n_machines).max()) for chromosome in Populations[k]]
            
    # Sort the list of tuples based on the values
    sorted_fitness_values = sorted(list(zip(Populations[k], fitness_values)), key=lambda x: x[1], reverse=True)

    # Select two best chromosomes based on fitness value then Update M(k)
    X_star = sorted_fitness_values[0][0]
    X_double_star = sorted_fitness_values[1][0]
    
    # Step 2: Set Current Best Makespan as Mk
    M.insert(k, completion_time(X_star, p_ij, n_machines).max())
    print(f"best Makespan at first: {M[1]}")
    
    while k < num_generations:
        # Step 3: Evaluate a condition to avoid premature convergence and escape local optimum and Update Counter
        if M[k] == M[k-1]:
            countmut += 1
            cntrndpop += 1
        else:
            countmut = 0
            cntrndpop = 0 

        # Step 4: Define Inside loop counter to generate new population
        q = 0
        new_pop = []
        
        while q < (population_size / 2):
            
            # Step 5 : Selection Operations ---> Generate random number and choose the method based on the probabilities
            r = random.random()
            if r <= tournament_prob:
                x_1, x_2 = [tournament_selection(Populations[k], fitness_values, tournament_size) for _ in range(2)]
            else:
                x_1, x_2 = [roulette_wheel_selection(Populations[k], fitness_values) for _ in range(2)]
                
            # Step 6: Crossover Operations ---> Generate 2 random numbers to perform crossover and choose the method based on the probabilities
            r = random.random()
            if r <= crossover_prob:
                r = random.random()
                if r <= two_point_prob:
                    x_prime_1, x_prime_2 = two_points_crossover(x_1, x_2)
                elif two_point_prob < r <= two_point_prob + pmx_prob:
                    x_prime_1, x_prime_2 = partially_mapped_crossover(x_1, x_2)
                elif two_point_prob + pmx_prob < r <= two_point_prob + pmx_prob + sjox_prob:
                    x_prime_1, x_prime_2 = similar_job_order_crossover(x_1, x_2)
                else:
                    x_prime_1, x_prime_2 = linear_order_crossover(x_1, x_2)
            else:
                x_prime_1, x_prime_2 = x_1, x_2
                    
            # Step 7: Mutation Operations ---> Generate 2 random numbers to perform mutation and choose the method based on the probabilities
            r = random.random()
            if r <= mutation_prob:
                r = random.random()
                if r <= three_job_prob:
                    x_zegond_1, x_zegond_2 = arbitrary_three_job(x_prime_1), arbitrary_three_job(x_prime_2)
                elif three_job_prob < r <= three_job_prob + two_job_prob:
                    x_zegond_1, x_zegond_2 = arbitrary_two_job(x_prime_1), arbitrary_two_job(x_prime_2)
                else:
                    x_zegond_1, x_zegond_2 = shift_change(x_prime_1), shift_change(x_prime_2)       
                new_pop.extend([x_zegond_1, x_zegond_2])
                q += 1
            else:
                x_zegond_1, x_zegond_2 = x_prime_1, x_prime_2
                new_pop.extend([x_zegond_1, x_zegond_2])
                q += 1
            # Step 8: Update q and break the loop

        if len(new_pop) > len(Populations[k]):
            new_pop = sorted(new_pop, key= lambda x: completion_time(x, p_ij, n_machines).max())[:population_size]
        
        # Step 9: Check if countmut > Gm  
        if countmut > gen_limit_mutation_prob:
            mutation_prob *= mutation_multiplier

        # Step 10: Check if cntrndpop > Gp
        if cntrndpop > gen_limit_reassign:
            # Generate new population (size = 0.75 * population size)
            new_gen_size = int(0.75 * population_size)
            new_gen = [generate_random_population(n_jobs) for _ in range(new_gen_size)]
            
            # Insert new generated population instead of worst 75 percent of initial Population
            new_pop = sorted(new_pop, key= lambda x: completion_time(x, p_ij, n_machines).max())[:len(new_pop) - new_gen_size]
            new_pop.extend(new_gen)


        # Step 11: Update X_star and X_double_star and Mk in P(k)
        fitness_values = [fitness_evaluation(completion_time(chromosome, p_ij, n_machines).max()) for chromosome in Populations[k]]
        C_max = [completion_time(chromosome, p_ij, n_machines).max() for chromosome in Populations[k]]
        sorted_fitness_values = sorted(list(zip(Populations[k], fitness_values)), key=lambda x: x[1], reverse=True)
        sorted_obj_val = sorted(list(zip(Populations[k], C_max)), key=lambda x: x[1])
        X_star = sorted_fitness_values[0][0]
        X_double_star = sorted_fitness_values[1][0]
        M.insert(k, completion_time(X_star, p_ij, n_machines).max())
        best_C_max = sorted_obj_val[0][1]
        best_schedule = sorted_obj_val[0][0]
        
        # Step 12: Elitist Strategy
        new_pop = sorted(new_pop, key= lambda x: completion_time(x, p_ij, n_machines).max())[:len(new_pop) - 2]
        new_pop.extend([X_star, X_double_star])
        
        # Step 13: Update Counter and create P(k+1)
        k += 1        
        Populations[k] = new_pop
        fitness_values = [fitness_evaluation(completion_time(chromosome, p_ij, n_machines).max()) for chromosome in Populations[k]]

    print(f"Makespan after While loop: {best_C_max}")
    print(f"Given Sequence: {best_schedule}")

    return best_schedule, best_C_max

def gantt_chart(jobs, sequence, p_ij, n_machines, n_jobs):
    plot = {}
    c_ij = completion_time(sequence, p_ij, n_machines)
    for i in range(n_machines):
        plot[i + 1] = {}
        for idx, j in enumerate(sequence):
            plot[i + 1][j] = c_ij[i][idx + 1]

    df = pd.DataFrame()
    for m, j_ in plot.items():
        for j in j_.keys():
            df_tmp = pd.DataFrame([dict(Job="Job "+str(j), Task= "Machine "+str(m), Start= plot[m][j] - jobs[j][m-1], Finish=plot[m][j])])
            df = pd.concat([df, df_tmp], ignore_index=True)
            
    colors = {}
    for j in range(n_jobs):
        colors['Job '+str(j)] = 'rgb'+str(tuple(np.random.choice(range(256), size=3)))

    fig = ff.create_gantt(df, group_tasks=True, index_col='Job',show_colorbar=True,
                        showgrid_x=True, showgrid_y=True, title='IGA Sequence Gantt Chart', colors= colors)
    fig.update_layout(xaxis_type='linear')
    
    return fig 

# Define Required Parameters
p_s = 70          # Population size
p_c = 0.9         # Probability of crossover
p_m = 0.4         # Probability of mutation
p_ro = 0.2        # Probability for roulette wheel selection
p_to = 0.8        # Probability for tournament selection
p_t = 0.7         # Probability for two-point crossover
p_p = 0.125       # Probability for PMX crossover
p_sj = 0.05       # Probability for SJOX crossover
p_l = 0.125       # Probability for LOX crossover
p_3j = 0.05       # Probability for arbitrary three-job change mutation
p_2j = 0.15       # Probability for arbitrary two-job change mutation
p_sh = 0.8        # Probability for shift change mutation
multiplier = 1.2  # A constant Mutation multiplier
n_gen = 1000      # Number of generations
g_p = 200         # Generation limit for population re-assignment
g_m = 150         # Generation limit for changing mutation probability
tournament_size = 13

# jobs, p_ij, n_j, n_m = read_instance('Instances/VFR10_5_9_Gap.txt')
jobs, p_ij, n_j, n_m = read_instance('VFR10_5_9_Gap.txt')
schedule, obj = improved_genetic_algorithm(p_ij= p_ij, n_jobs= n_j, n_machines= n_m,
                                           population_size= p_s,
                                           crossover_prob= p_c,
                                           mutation_prob= p_m,
                                           roulette_wheel_prob= p_ro,
                                           tournament_prob= p_to,
                                           two_point_prob= p_t,
                                           pmx_prob= p_p,
                                           sjox_prob= p_sj,
                                           lox_prob= p_l,
                                           three_job_prob= p_3j,
                                           two_job_prob= p_2j,
                                           shift_change_prob= p_sh,
                                           mutation_multiplier= multiplier,
                                           num_generations= n_gen,
                                           gen_limit_reassign= g_p,
                                           gen_limit_mutation_prob=g_m,
                                           tournament_size= tournament_size)

plot = gantt_chart(jobs, schedule, p_ij, n_m, n_j)
plot.show()