import dimod
from collections import defaultdict
import dwavebinarycsp
from itertools import combinations, product

class BqmBuilder:

    def __init__(self, graph, num_days, resources, weights=None, one_hot_scale=500, classroom_constraint_scale=100):
        self.graph = graph
        self.num_days = num_days
        self.num_exams = len(graph.nodes)
        self.one_hot_scale = one_hot_scale
        self.classroom_constraint_scale = classroom_constraint_scale
        self.resources = resources
        if 'classrooms' in self.resources:
            self.resources['classrooms'].sort()

        if weights is None:
            self.weights = [16, 8, 4, 2, 1]

    def get_one_hot_constraints(self):
        print("\nAdding one-hot constraints...")
        return [dimod.generators.combinations([f'v_{exam},{k}' for k in range(self.num_days)], 1) for exam in range(self.num_exams)]
    
    def get_minimised_edges(self):
        print("\nAdding minimised edges...")
        J = defaultdict(int)

        for (i, j) in self.graph.edges:
            for day in range(self.num_days):
                for ind, weight in enumerate(self.weights):
                    
                    new_day = day + ind
                    if new_day >= self.num_days:
                        break
                    
                    J[f'v_{i},{day}', f'v_{j},{new_day}'] += weight * self.graph[i][j]["weight"]
                    J[f'v_{j},{day}', f'v_{i},{new_day}'] += weight * self.graph[i][j]["weight"]
        
        return dimod.BQM(J, vartype='BINARY')

    def find_exam_from_tag(self, s):
        start = s.index('_')
        end = s.index(',')
        return int(s[start+1:end])

    def get_classroom_constraints(self):
        print("\nAdding classroom constraints...")

        def check_classroom_constraints(comb):
            exams = [self.find_exam_from_tag(s) for s in comb]
            exams.sort(key=lambda e : self.graph.nodes[e]['size'])
            return all([self.graph.nodes[exams[i]]['size'] <= self.resources['classrooms'][i] for i in range(len(exams))])
        
        csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

        for day in range(self.num_days):

            combs = list(combinations([f'v_{exam},{day}' for exam in range(self.num_exams)], len(self.resources['classrooms'])))
            for comb in combs:

                if not check_classroom_constraints(list(comb)):
                    valid_configurations = set(product([0, 1], repeat=3)) - {(1, 1, 1)}
                    csp.add_constraint(valid_configurations, list(comb))

        return dwavebinarycsp.stitch(csp)

    def get_bqm(self):
        print("\nBuilding BQM...")
        one_hot_bqms = self.get_one_hot_constraints()
        bqm = self.get_minimised_edges()

        for one_hot in one_hot_bqms:
            one_hot.scale(self.one_hot_scale)
            bqm.update(one_hot)

        if "classrooms" in self.resources:
            bqm_classroom = self.get_classroom_constraints()
            bqm_classroom.scale(self.classroom_constraint_scale)
            bqm.update(bqm_classroom)
        
        return bqm
