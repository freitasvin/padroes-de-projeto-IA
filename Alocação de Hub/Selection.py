import numpy as np
import random

def roulette_wheel_selection(assign_array, hub_array, fitness_values):
    # Calculate the selection probabilities
    fitness_sum = np.sum(fitness_values)
    selection_probabilities = fitness_values / fitness_sum
    
    # Calculate the cumulative probabilities
    cumulative_probabilities = np.cumsum(selection_probabilities)

    
    # Select two individuals from the population
    selected_indices = []
    while len(selected_indices) < 2:
        r = np.random.rand()
        for j in range(len(cumulative_probabilities)):
            if j in selected_indices:
                continue
            if r < cumulative_probabilities[j]:
                selected_indices.append(j)
                break
#     print(selected_indices)
    # Return the selected individuals
    parents_assign_array = [assign_array[i] for i in selected_indices]
    parents_hub_array = [hub_array[i] for i in selected_indices]
    return parents_assign_array, parents_hub_array


def tournament_selection(assign_array, hub_array, fitness_values, tournament_size):
    
    
    
    # Select individuals from the population based on tournament size
    
    fitness_values = np.array(fitness_values)
    selected_indices = [0,0]
    
    while all(x == selected_indices[0] for x in selected_indices):
        selected_indices = []
        for i in range(2):
            tournament_indices = np.random.choice(range(len(assign_array)), tournament_size, replace=False)
            tournament_fitness_values = []
            for index in tournament_indices:
                tournament_fitness_values.append(fitness_values[index])
                selected_index = tournament_indices[np.argmax(tournament_fitness_values)]
            selected_indices.append(selected_index)
    
    # Return the selected individuals
    parents_assign_array = [assign_array[i] for i in selected_indices]
    parents_hub_array = [hub_array[i] for i in selected_indices]
    return parents_assign_array, parents_hub_array

def single_point_crossover_with_repairment(parent_assign, parent_hub, n_hub, flow_matrix, cost_matrix):
    
    offspring_hub = [[0], [0]]
    offspring_assign = [[0], [0]]


    crossover_point = np.random.randint(0, len(parent_assign[0]))

    # Generate the offspring
    offspring_hub[0] = parent_hub[0][:crossover_point] + parent_hub[1][crossover_point:]
    offspring_hub[1] = parent_hub[1][:crossover_point] + parent_hub[0][crossover_point:]
    offspring_assign[0] = parent_assign[0][:crossover_point] + parent_assign[1][crossover_point:]
    offspring_assign[1] = parent_assign[1][:crossover_point] + parent_assign[0][crossover_point:]



    for item in range(2):
        hub_indices = [i for i, x in enumerate(offspring_hub[item]) if x == 1]


        if len(hub_indices) > n_hub:
            while len(hub_indices) > n_hub:
            
                random_index = random.randint(0, len(hub_indices)-1)  # generate random index
                hub_indices.pop(random_index)
        elif len(hub_indices) < n_hub:
            while len(hub_indices) < n_hub:
                all_hub = list(range(len(parent_assign[0])))
                possible_hub = [i for i in all_hub if i not in hub_indices]
                random_index = random.choice(possible_hub)
                hub_indices.append(random_index)
            
            
        
        offspring_hub[item] = [0] * len(parent_assign[0])                                       
                                          
        for index in hub_indices:
            offspring_hub[item][index] = 1
        
    arranged_offspring_assign = []

    # Adjustment function
    for each_offspring_assign, each_offspring_hub in zip(offspring_assign, offspring_hub):

        hub_indices = [i for i, x in enumerate(each_offspring_hub) if x == 1]

        for node in range(len(each_offspring_assign)):
            if each_offspring_hub[node] == 1:
                each_offspring_assign[node] = node
            if each_offspring_hub[node] == 0:
                if each_offspring_assign[node] in hub_indices:
                    continue
                min_cost_index = list(hub_indices)[np.argmin(cost_matrix[list(hub_indices), each_offspring_assign[node]])]
                each_offspring_assign[node] = min_cost_index
            
        arranged_offspring_assign.append(each_offspring_assign)                         
    
    return arranged_offspring_assign, offspring_hub

# Shift
def mutation_shift(arranged_offspring_assign, offspring_hub):
    
    offspring_assign = []
    
    for offspring in arranged_offspring_assign:
#         random_number = np.random.random()
        selected_index = None
#         if random_number < 0.5:
        hub_indices = set(offspring)
        selected_index = np.random.randint(0,len(offspring))
        while selected_index in hub_indices:
            selected_index = np.random.randint(0,9)

        hub_indices = list(hub_indices)
        hub_indices.remove(offspring[selected_index])
        offspring[selected_index] = np.random.choice(hub_indices)
        offspring_assign.append(offspring)

    return offspring_assign, offspring_hub
# Exchange
def mutation_exchange(arranged_offspring_assign, offspring_hub):
    
    offspring_assign = []
    
    for offspring in arranged_offspring_assign:

        hub_indices = set(offspring)
        hub1, hub2  = np.random.choice(list(hub_indices), 2, replace=False)
        node1, node2 = np.random.choice(list((set(range(len(offspring)))) - hub_indices), 2, replace=False)

        node1 = np.random.choice([i for i, x in enumerate(offspring) if x == hub1])
        node2 = np.random.choice([i for i, x in enumerate(offspring) if x == hub2])


        offspring[node1] = hub2
        offspring[node2] = hub1
        
        offspring_assign.append(offspring)

        
    return offspring_assign, offspring_hub

def populate_offspring(population, assign_array, hub_array, n_hub, fitness_values, tournament_size,flow_matrix, cost_matrix):
    
    new_assign_array_set = []
    new_hub_array_set = []
    
    offsprings_assign = []
    offsprings_hub = []
    
    while len(new_assign_array_set) < population:
#         parents_assign, parents_hub = tournament_selection(assign_array, hub_array, fitness_values, tournament_size)
        parents_assign, parents_hub = roulette_wheel_selection(assign_array, hub_array, fitness_values)
        
        arranged_offspring_assign, offspring_hub = single_point_crossover_with_repairment(parents_assign, parents_hub, n_hub, flow_matrix, cost_matrix)
        random_number = np.random.random()
        if random_number < 0.5:
            offspring_assigns, offspring_hubs = mutation_shift(arranged_offspring_assign, offspring_hub)
        else: 
            offspring_assigns, offspring_hubs = mutation_exchange(arranged_offspring_assign, offspring_hub)
        for each_offspring_assign, each_offspring_hub in zip(offspring_assigns, offspring_hubs):
            if len(new_assign_array_set) < population:
                new_assign_array_set.append(each_offspring_assign)
                new_hub_array_set.append(each_offspring_hub)

    return new_assign_array_set, new_hub_array_set