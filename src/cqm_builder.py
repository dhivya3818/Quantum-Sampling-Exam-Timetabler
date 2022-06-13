from dimod import Binary, DiscreteQuadraticModel, quicksum

class CqmBuilder:

    def __init__(self, graph, num_days, weights=None):
        self.graph = graph
        self.dqm = DiscreteQuadraticModel()
        self.num_days = num_days
        self.v = {}
        for i in self.graph.nodes:
            self.v[i] = [Binary(f'v_{i},{k}') for k in self.graph.nodes]
        self.num_exams = len(graph.nodes)

        if weights is None:
            self.weights = [16, 8, 4, 2, 1]

    def add_one_hot_constraints(self):
        print("\nAdding one-hot constraints...")
        # for i in self.graph.nodes:
        #     self.dqm.add_discrete([f'v_{i},{k}' for k in range(self.num_days)], label=f"one-hot-node-{i}")
        for i in self.graph.nodes:
            self.dqm.add_variable(self.num_days, label=i)
    
    def add_partition_size_constraint(self):
        print("\nAdding partition size constraint...")
        for p in range(self.num_days):
            self.dqm.add_constraint(quicksum(self.v[i][p] for i in self.graph.nodes) == self.num_exams/self.num_days, label='partition-size-{}'.format(p))

    def set_objective(self):
        print("\nSetting objective...")        
        min_edges = []

        for (i, j) in self.graph.edges:
            for day in range(self.num_days):
                for ind, weight in enumerate(self.weights):
                    
                    new_day = day + ind
                    # if ind == 0:
                    #     self.dqm.add_constraint(self.v[i][day] * self.v[j][day] == 0, label="no-clash-{}-{}-day{}".format(i, j, day))

                    if new_day >= self.num_days:
                        break
                    
                    # print("egde", self.graph[i])
                    # print("objective", {(day, new_day): weight * self.graph[i][j]["weight"]})
                    self.dqm.set_quadratic(i, j, {(day, new_day): weight * self.graph[i][j]["weight"]})
                    # min_edges.append(self.v[i][day] + self.v[j][day] + weight * self.graph[i][j]["weight"] * self.v[i][day] * self.v[j][day])
        
        # self.cqm.set_objective(sum(min_edges))

    def get_cqm(self):
        print("\nBuilding CQM...")
        self.add_one_hot_constraints()
        # self.add_partition_size_constraint()
        self.set_objective()
        return self.dqm
