import time
import numpy as np
import matplotlib.pyplot as plt
import NetworkCost as nc
import Replacement as rep1
import InitialSolution as isol
import Selection as ns2

def genetic_algorithm(n_node, n_hub, population, cost_matrix, flow_matrix, initial_solution, termination_time):
    
    objIsol = isol()
    final_best_cost = float('inf')
    final_best_solution = None
    
    best_solution_list = []
    final_best_solution_list = []
    final_best_cost_list = []
    time_stamp = []
    
    if initial_solution == 'flowbased':
        assign_array, hub_array = objIsol.weighted_flowbased_initial_solution_GA(flow_matrix, n_hub, n_node, population)
    elif initial_solution == 'costbased':
        assign_array, hub_array = objIsol.weighted_costbased_initial_solution_GA(cost_matrix, n_hub, n_node, population)
    else:
        assign_array, hub_array = objIsol.random_initial_solution_GA(n_hub, n_node, population)
    
    updated = 0
    start_time = time.time()
    current_time = start_time
    
    while current_time - start_time < termination_time:
        
        # calculate fitness value
        fitness_values = objIsol.calculate_fitness(assign_array, flow_matrix, cost_matrix)
        
        best_cost = float('inf')
        best_solution = None
        
        for index, cost in enumerate(fitness_values):
            if cost < best_cost:
                best_cost = cost
                best_solution = assign_array[index]
          
        # create set of new generation population through selection and reproduction
        new_assign_array_set, new_hub_array_set = populate_offspring(population, assign_array, hub_array, n_hub, fitness_values, 10, flow_matrix, cost_matrix)
        
        # apply replacement strategy to get new generation
        new_generation_assign, new_generation_hub = rep1.combination_replacement(new_assign_array_set, new_hub_array_set, assign_array, hub_array, flow_matrix, cost_matrix, fitness_values)
        
        best_solution_list.append(best_solution)
        
        if best_cost < final_best_cost:
            final_best_cost = best_cost
            final_best_solution = best_solution.copy()
            best_iteration = len(best_solution_list) - 1
            updated += 1
            
        final_best_solution_list.append(final_best_solution)
        final_best_cost_list.append(final_best_cost)
        
        assign_array = new_generation_assign.copy()
        hub_array = new_generation_hub.copy()
        
        current_time = time.time()
        time_stamp.append(current_time - start_time)
    

    fig, ax = plt.subplots()
    ax.plot(range(len(final_best_solution_list)), [nc.total_cost(best_solution, flow_matrix, cost_matrix) for best_solution in final_best_solution_list])
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Total Cost (Final Best Solution)')
    ax.set_title('Final Best Solution')
    
    plt.show()

    return final_best_solution, final_best_cost, best_iteration, updated, final_best_cost_list, time_stamp

def populate_offspring(population, assign_array, hub_array, n_hub, fitness_values, tournament_size,flow_matrix, cost_matrix):
    
    new_assign_array_set = []
    new_hub_array_set = []
    
    offsprings_assign = []
    offsprings_hub = []
    
    while len(new_assign_array_set) < population:
#         parents_assign, parents_hub = tournament_selection(assign_array, hub_array, fitness_values, tournament_size)
        roulette_selection = ns2.RouletteWheelSelection()
        parents_assign, parents_hub = ns2.roulette_wheel_selection(assign_array, hub_array, fitness_values)
        
        arranged_offspring_assign, offspring_hub = ns2.single_point_crossover_with_repairment(parents_assign, parents_hub, n_hub, flow_matrix, cost_matrix)
        random_number = np.random.random()
        if random_number < 0.5:
            offspring_assigns, offspring_hubs = ns2.mutation_shift(arranged_offspring_assign, offspring_hub)
        else: 
            offspring_assigns, offspring_hubs = ns2.mutation_exchange(arranged_offspring_assign, offspring_hub)
        for each_offspring_assign, each_offspring_hub in zip(offspring_assigns, offspring_hubs):
            if len(new_assign_array_set) < population:
                new_assign_array_set.append(each_offspring_assign)
                new_hub_array_set.append(each_offspring_hub)

    return new_assign_array_set, new_hub_array_set