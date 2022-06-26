from dimod import Binary, BQM, ConstrainedQuadraticModel, DiscreteQuadraticModel, quicksum
import time
from collections import defaultdict


class CqmBuilder:

    def __init__(self, et_problem, weights=None):
        self.graph = et_problem["graph"]
        self.cqm = ConstrainedQuadraticModel()
        self.num_days = et_problem["num_days"]
        print("num days", self.num_days)
        self.v = {}
        for i in self.graph.nodes:
            self.v[i] = [Binary(f'v_{i},{k}') for k in range(self.num_days)]
        self.num_exams = len(self.graph.nodes)

        if weights is None:
            self.weights = [16, 8, 4, 2, 1]

    def add_one_hot_constraints(self):
        print("\nAdding one-hot constraints...")
        for i in self.graph.nodes:
            self.cqm.add_discrete([f'v_{i},{k}' for k in range(
                self.num_days)], label=f"one-hot-node-{i}")
        # for i in self.graph.nodes:
        #     self.cqm.add_variable(self.num_days, label=i)

    # def add_partition_size_constraint(self):
    #     print("\nAdding partition size constraint...")
    #     for p in range(self.num_days):
    #         self.cqm.add_constraint(quicksum(self.v[i][p] for i in self.graph.nodes) == self.num_exams/self.num_days, label='partition-size-{}'.format(p))

    def set_objective(self):
        print("\nSetting objective...")
        min_edges = []
        J = defaultdict(int)

        for (i, j) in self.graph.edges:
            for day in range(self.num_days):
                for ind, weight in enumerate(self.weights):

                    new_day = day + ind
                    if ind == 0:
                        self.cqm.add_constraint(
                            self.v[i][day] * self.v[j][day] == 0, label="no-clash-{}-{}-day{}".format(i, j, day))
                        # min_edges.append(self.v[i][day] + self.v[j][new_day] + weight * self.graph[i][j]["weight"] * self.v[i][day] * self.v[j][new_day])

                    if new_day >= self.num_days:
                        break

                    J[f'v_{i},{day}',
                      f'v_{j},{new_day}'] += (weight * self.graph[i][j]["weight"])
                    J[f'v_{j},{day}',
                      f'v_{i},{new_day}'] += (weight * self.graph[i][j]["weight"])
                    # min_edges.append(self.v[i][day] + self.v[j][new_day] + weight * self.graph[i][j]["weight"] * self.v[i][day] * self.v[j][new_day])
                    # min_edges.append(self.v[i][new_day] + self.v[j][day] + weight * self.graph[i][j]["weight"] * self.v[i][new_day] * self.v[j][day])

        # print("min edges", min_edges)
        start = time.time()
        # self.cqm.set_objective(sum(min_edges))
        # print("objective min", self.cqm.objective)
        # print("length of min_edges:", len(min_edges))
        # summed_edges = sum(min_edges)
        # print("summed edges", summed_edges)
        # print("Time taken to sum min edges", str((time.time() - start) / 60))
        self.cqm.set_objective(BQM(J, vartype='BINARY'))
        # print("objective J", self.cqm.objective)
        print("Time taken to set objective ", str((time.time() - start) / 60))

    def get_cqm(self):
        print("\nBuilding CQM...")
        self.add_one_hot_constraints()
        # self.add_partition_size_constraint()
        self.set_objective()
        return self.cqm
