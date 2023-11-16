import numpy as np
import NetworkCost as nc

class InitialSolution:
    def __init__(self, flow_matrix, n_hub, n_node, population):
        self.flow_matrix = flow_matrix
        self.n_hub = n_hub
        self.n_node = n_node
        self.population = population
        self.assign_array_set = []
        self.hub_array_set = []

    def create_initial_solution(self):
        pass

    def calculate_fitness(self, cost_matrix):
        fitness_values = []
        for individual in self.assign_array_set:
            fitness_values.append(nc.total_cost(individual, self.flow_matrix, cost_matrix))
        return fitness_values

    def calculate_total_flow(self):
        total_flow = []
        for node in range(self.n_node):
            flow = 0
            for other_node in range(self.n_node):
                if node != other_node:
                    flow += self.flow_matrix[node][other_node]
                    flow += self.flow_matrix[other_node][node]
            total_flow.append(flow)
        return total_flow

    def calculate_node_index(self, total_flow):
        return [i for _, i in sorted(zip(total_flow, range(len(total_flow))), reverse=True)]

    def calculate_two_thirds_biggest_flow_index(self, node_index):
        return node_index[:int(len(node_index) * (1/3))]

class WeightedFlowBasedInitialSolution(InitialSolution):
    def create_initial_solution(self):
        total_flow = self.calculate_total_flow()
        node_index = self.calculate_node_index(total_flow)
        two_thirds_biggest_flow_index = self.calculate_two_thirds_biggest_flow_index(node_index)

        for individual in range(self.population):
            assign_array = [0] * self.n_node
            hub_array = [0] * self.n_node

            if individual < int(self.population * (1/3)):
                hubs = np.random.choice(two_thirds_biggest_flow_index, self.n_hub, replace=False)
            else:
                hubs = np.random.choice(self.n_node, self.n_hub, replace=False)

            for item in range(len(assign_array)):
                for hub in hubs:
                    if item == hub:
                        assign_array[item] = hub

            for item in range(len(assign_array)):
                if item not in set(hubs):
                    assign_array[item] = int(np.random.choice(hubs))

            for item in range(len(assign_array)):
                if assign_array[item] == item:
                    hub_array[item] = 1
                else:
                    hub_array[item] = 0

            self.assign_array_set.append(assign_array)
            self.hub_array_set.append(hub_array)

class RandomInitialSolution(InitialSolution):
    def create_initial_solution(self):
        for individual in range(self.population):
            assign_array = [0] * self.n_node
            hub_array = [0] * self.n_node
            hubs = np.random.choice(self.n_node, self.n_hub, replace=False)

            for item in range(len(assign_array)):
                for hub in hubs:
                    if item == hub:
                        assign_array[item] = hub

            for item in range(len(assign_array)):
                if item not in set(hubs):
                    assign_array[item] = int(np.random.choice(hubs))

            for item in range(len(assign_array)):
                if assign_array[item] == item:
                    hub_array[item] = 1
                else:
                    hub_array[item] = 0

            self.assign_array_set.append(assign_array)
            self.hub_array_set.append(hub_array)
