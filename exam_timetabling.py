# Copyright [2022] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Things to do:
 - Please name this file <demo_name>.py
 - Fill in [yyyy] and [name of copyright owner] in the copyright (top line)
 - Add demo code below
 - Format code so that it conforms with PEP 8
"""

import networkx as nx
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
from bqm_builder import BqmBuilder
from preprocessor import get_graph_data

# Overall model variables: problem size
num_days = 18
# num_days = 3

# graph = nx.Graph()

# course_sizes = [40, 60, 25, 40, 30, 22, 25]
# for i in range(num_exams):
#     graph.add_node(i, size=course_sizes[i])

# resources = { 'classrooms': [30, 60, 30] }

# graph.add_edge(0, 1, weight=35)
# graph.add_edge(0, 5, weight=3)
# graph.add_edge(1, 2, weight=3)
# graph.add_edge(2, 4, weight=5)
# graph.add_edge(3, 4, weight=15)
# graph.add_edge(5, 6, weight=12)

# stu_file = open("./tests/hec-s-92-2.stu", 'r')
# crs_file = open("./tests/EdHEC92.sol", 'r')

# common_classes = []

# for ind, line in enumerate(stu_file):
#     classes = line.split()

#     if classes not in common_classes:
#         common_classes.append(classes)

# solution = {}
# for line in crs_file.readlines():
#     split_line = line.strip().split()
#     if int(split_line[1]) in solution:
#         arr = solution[int(split_line[1])]
#         arr.append(split_line[0])
#         solution[int(split_line[1])] = arr
#     else:
#         solution[int(split_line[1])] = [split_line[0]]

# clashes = {}

# def add_to_clashes(course1, course2):

#     if course1 not in clashes:
#         clashes[course1] = {}

#     if course2 in clashes[course1]:
#         clashes[course1][course2] += 1
#     else:
#         clashes[course1][course2] = 1

# for classes in common_classes:
#     if len(classes) == 1:
#         continue

#     for courses in itertools.combinations(classes, 2):
#         (course1, course2) = courses
#         course1 = int(str(course1)[-2:])
#         course2 = int(str(course2)[-2:])

#         add_to_clashes(course1, course2)
#         add_to_clashes(course2, course1)


# # Find composite index into 1D list for (exam_index, day_index)
# def get_index(exam_index, day_index):
#     # return (exam_index - 1) * num_days + day_index
#     return exam_index * num_days + day_index

# # Inverse of get_index - given a composite index in a 1D list, return the
# # exam_index and day_index
# def get_exam_and_day(index):
#     exam_index, day_index = divmod(index, num_days)
#     return exam_index, day_index

# csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

# def sums_to_one(*args):
#     print("SUMS TO ONE:", args)
#     return sum(args) == 1

# for exam in range(num_exams):
#     exam_days = {f'v_{exam},{day}' for day in range(num_days)}
#     print("exam days", exam_days)
#     csp.add_constraint(sums_to_one, exam_days)

#-------------------------------------------------------------------------------

print("\nGetting graph data")
graph = get_graph_data("hec-s-92-2")
num_exams = len(graph.nodes)
resources = {}

print("\nGetting BQM with builder...")
bqm = BqmBuilder(graph, num_days, resources).get_bqm()

print("\nSending to DWave Sampler...")
sampler = EmbeddingComposite(DWaveSampler())
results = sampler.sample(bqm, num_reads=1000, label='Example - Exam Timetabling')
   
for ind, record in enumerate(reversed(results.record)):
    if ind % 400 != 0:
        continue

    print("\n Iteration {} - Energy: {}".format(ind, record.energy))
    sample = record.sample
    for k in range(num_days):
        print("Day {}:".format(k + 1), [i for i in range(num_exams) if sample[results.variables.index(f'v_{i},{k}')] == 1])

sample = results.first.sample
print("\nFinal result - Energy {}".format(results.first.energy))
for k in range(num_days):
    print("Day {}:".format(k + 1), [i for i in range(num_exams) if sample[f'v_{i},{k}'] == 1])
#-----------------------------------------------------------------------------------------------
# csp.add_constraint(sums_to_one, exam_days)
# print("added constraint", exam)
# for i in range(num_exams):
#     cqm.add_discrete([f'v_{i},{k}' for k in range(num_days)], label=f"one-hot-node-{i}")

# print("\nAdding partition size constraint...")
# for p in range(num_days):
#     cqm.add_constraint(quicksum(v[n][p] for n in range(num_exams)) == num_exams/num_days, label='partition-size-{}'.format(p))

# min_edges = []
# for (i, j) in graph.edges:
#     for p in range(num_days):
#         break
#         # print("weight", v[i][p])
#         # print("objective:", graph[i][j]["weight"]*v[i][p]*v[j][p])
#         # TODO: Add how to weigh the different constraints differently
#         # min_edges.append(v[i - 1][p]+v[j - 1][p]+clashes[i][j]*v[i - 1][p]*v[j - 1][p])
#         # cqm.add_constraint(v[i - 1][p] * v[j - 1][p] == 0, label="no-clash-{}-{}-day{}".format(i, j, p))

# cqm.set_objective(sum(min_edges))
# sampler = LeapHybridCQMSampler()

# print("\nSending to the solver...")
    
# # Solve the CQM problem using the solver
# sampleset = sampler.sample_cqm(cqm, label='Example - Graph Partitioning')
# sample = sampleset.filter(lambda row: row.is_feasible).first.sample
# print("Feasible Sample:", sample)

# print("\nBuilding schedule and checking constraints...\n")

# for k in range(num_days):
#     partition = [i + 1 for i in range(num_exams) if sample[f'v_{i},{k}'] == 1]
#     print("Day {}:".format(k + 1), [i + 1 for i in range(num_exams) if sample[f'v_{i},{k}'] == 1])
#     for courses in itertools.combinations(partition, 2):
#         (course1, course2) = courses
#         if course2 in clashes[course1]:
#             print("CLASH! of exams {} and {} of {}".format(course1, course2, clashes[course1][course2]))
# print("Solution:", solution)

#--------------------------------------------------------------------------------
# Hard constraint: Each exam has to be scheduled once
# csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
# print("print csp before", csp)
# for exam in range(num_exams):
#     exam_days = {get_index(exam, day) for day in range(num_days)}
#     csp.add_constraint(sums_to_one, exam_days)
#     # print("added constraint", exam)

# bqm = dwavebinarycsp.stitch(csp)

# Hard constraint: Students can only sit for 1 exam in a timeslot
# J = defaultdict(int)

# for exam in range(num_exams):
#     for day in range(num_days):
#         index = get_index(exam, day)
#         clashing_exams = clashes[exam + 1]

#         for clash in clashing_exams:
#             clash_index = get_index(clash, day)
#             J[index, clash_index] = clashing_exams[clash]

# bqm = BinaryQuadraticModel.from_qubo(J)

# print("print clashes only bqm", bqm)

# Q matrix assign the cost term, the J matrix
# Q = deepcopy(J)

# # Solve the problem, and use the offset to scale the energy
# bqm = BinaryQuadraticModel.from_qubo(Q)

# print("\nSending problem to quantum sampler...")
# # sampler = LeapHybridSampler()
# sampler = EmbeddingComposite(DWaveSampler())
# results = sampler.sample(bqm, num_reads=10, label='Example - Exam Timetabling')
# sample = results.first.sample

# print("Sample set:")
# print(results)

# print("Best Sample:")
# print(sample)

# print("\nBuilding schedule and checking constraints...\n")
# sched = [get_exam_and_day(j) for j in range(num_exams * num_days) if sample[j] == 1]

# for i in range(num_days):
#     print("Day i:", [k for (k, j) in sched if j == i])

# print("Day 0:", [i for (i, j) in sched if j == 0])
# print("Day 1:", [i for (i, j) in sched if j == 1]) 
# print("Day 2:", [i for (i, j) in sched if j == 2]) 
