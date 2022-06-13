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

import hybrid
import networkx as nx
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
from dwave.system import LeapHybridBQMSampler, LeapHybridCQMSampler, LeapHybridDQMSampler
from bqm_builder import BqmBuilder
from cqm_builder import CqmBuilder
from preprocessor import get_graph_data
from postprocessor import write_to_file
import dwave.inspector
import neal
from dimod import ExactSolver
import itertools
from visualisation import Visualiser
from solution import Timetable
import matplotlib.pyplot as plt
print("\nGetting graph data")
filename = "med-04.txt"
et_problem = get_graph_data(filename)
graph = et_problem["graph"]
num_students = et_problem["num_students"]
num_days = et_problem["num_days"]
resources = et_problem["resources"]
print("num students", num_students)
# def anneal_sched_custom_2():
#     return (
#         (0.0, 0.0),  # Start the anneal (time 0.0) at 0.0 (min)
#         (5.0, 0.5),  # After 5us, set the anneal setting to 50%
#         (20.0, 1.0)  # After 20us, set the anneal setting to 100% (max)
#     )

# def anneal_sched_custom_1():
#     return [(0.0,0.0),(10.0,0.5),(110.0,0.5),(120.0,1.0)]  # After 5µs, set the anneal setting to 100% (max)

print("graph:", graph)
print("num exams:", len(graph.nodes))
print("sizes", nx.get_node_attributes(graph, "size"))
# pos = nx.spring_layout(graph, k=0.45)
# nx.draw(graph, pos, node_color="#ABD7EB", edgecolors="black", node_size=1000, font_size=10, labels=nx.get_node_attributes(graph, "size"), with_labels=True)
# nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "weight"))
# plt.savefig("graph.png")
# print("\nGetting BQM with builder...")
bqm = BqmBuilder(et_problem).get_bqm()

# print("bqm", bqm)
# # cqm = CqmBuilder(graph, num_days).get_cqm()

def get_conflict_density(graph):
    adj_matrix = nx.adjacency_matrix(graph).todense().tolist()
    conflict_matrix = [[int(x > 0) for x in row] for row in adj_matrix]
    return sum(row.count(1) for row in conflict_matrix) / (len(conflict_matrix) ** 2)

print("conflict density:", get_conflict_density(graph))
ranges = [1, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
def sample_and_get_results(type, bqm):

    if type == "sa":
        print("\nSending to Classical Sampler...")
        sampler = neal.SimulatedAnnealingSampler()
        results = sampler.sample(bqm)
    elif type =="qa":
        print("\nSending to Quantum Sampler...")
        sampler = EmbeddingComposite(DWaveSampler(solver={'topology__type': 'pegasus'}))
        # results = sampler.sample(bqm, num_reads=1000, anneal_schedule=anneal_sched_custom_1(), chain_strength=5000, label='Example - Exam Timetabling')
        results = sampler.sample(bqm, num_reads=1000, label='Example - Exam Timetabling')
    else:
        print("\nSending to Hybrid Sampler...")
        # sampler = LeapHybridBQMSampler()
        # results = sampler.sample(bqm)
        results = hybrid.KerberosSampler().sample(bqm) 
        write_to_file(results.first.sample, filename, num_days, graph.nodes)
        # print("results:", results)
        # feasible_result = results.filter(lambda row: row.is_feasible)
        # if feasible_result is not Empty:
        #     write_to_file(results.filter(lambda row: row.is_feasible).first.sample, filename, num_days, graph.nodes)       
    # results = sampler.sample(bqm, num_reads=num_reads, chain_strength=scale*20, label='Example - Exam Timetabling')
    
    if type == "qa":
        dwave.inspector.show(results)
    min_energies = []
    asceding_energies = list(reversed(results.record))
    # for ind, record in enumerate(reversed(results.record)):
    for range in ranges:
        range_energies = asceding_energies[0:range]
        min_energy = min([r.energy for r in range_energies])
        min_energies.append(min_energy)
        # print("\n Iteration {} - Energy: {}".format(ind, record.energy))
        # sample = record.sample
        # for k in range(num_days):
        #     print("Day {}:".format(k + 1), [i for i in graph.nodes if sample[results.variables.index(f'v_{i},{k}')] == 1])

    best_sample = results.first.sample

    print("\nFinal result - Energy {}".format(results.first.energy))
    # timetable = Timetable(et_problem, best_sample)
    # # validity_checks = timetable.check_validity()
    # fig = Visualiser(et_problem, results).build_animated_graph()
    # fig.show()

    return ranges, min_energies

ranges, min_energies = sample_and_get_results("qa", bqm)
