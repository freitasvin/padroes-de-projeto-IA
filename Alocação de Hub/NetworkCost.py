class NetworkCost:
    ALPHA_VALUES = {50000: 1, 100000: 0.8, 200000: 0.6}
    INTERCEPT_VALUES = {50000: 0, 100000: 10000, 200000: 30000}

    @staticmethod
    def flow_loc(interhub_flow):
        for threshold, alpha in NetworkCost.ALPHA_VALUES.items():
            if interhub_flow < threshold:
                intercept = NetworkCost.INTERCEPT_VALUES[threshold]
                return alpha, intercept
        raise ValueError('Invalid interhub flow')

    @staticmethod
    def distribution_collection_cost(solution, flow_matrix, cost_matrix):
        total_distribution_cost = 0
        
    @staticmethod
    def inter_hub_cost(solution, flow_matrix, cost_matrix):
        inter_hub_cost = 0
        hub_indices = set(solution)
        
    @staticmethod
    def total_cost(solution, flow_matrix, cost_matrix):
        total_cost = (
            NetworkCost.distribution_collection_cost(solution, flow_matrix, cost_matrix) +
            NetworkCost.inter_hub_cost(solution, flow_matrix, cost_matrix)
        )
        return total_cost