# Copyright 2022 Dhivya Ravindran
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
import dwave.inspector
import neal
from dwave.system.composites import EmbeddingComposite, FixedEmbeddingComposite
from dwave.system.samplers import DWaveSampler
from dwave.system import LeapHybridSampler
from utils import write_to_file
from preprocessor import get_graph_data
from bqm_builder import BqmBuilder
from cqm_builder import CqmBuilder
from timetable import Timetable
from greedy import SteepestDescentSampler
import sys, getopt

def sample_and_get_results(type, qm, et_problem, filename, write=False):

    if type == "sa":
        print("\nSending to Classical Sampler...")
        sampler = neal.SimulatedAnnealingSampler()
        results = sampler.sample(qm, num_reads=1000)

    elif type =="qa":
        print("\nSending to Quantum Sampler...")
        sampler = EmbeddingComposite(DWaveSampler())
        results = sampler.sample(qm, num_reads=1000, label='Exam Timetabling (Quantum Sampler)')

    elif type == "post":
        print("\nSending to Quantum Sampler...")
        sampler = EmbeddingComposite(DWaveSampler())
        qpu_results = sampler.sample(qm, num_reads=100, answer_mode='raw', label='Example - Exam Timetabling')
        print("\nSending to postprocessor...")
        results = SteepestDescentSampler().sample(qm, initial_samples=qpu_results, num_reads=100)

    elif type == "leap":
        print("\nSending to Leap's Hybrid Solver...")
        sampler = LeapHybridSampler()
        results = sampler.sample(qm)

    elif type == "hybrid":
        print("\nSending to dwave-hybrid sampler...")
        workflow = hybrid.LoopUntilNoImprovement(
            hybrid.RacingBranches(
            hybrid.InterruptableTabuSampler(),
            hybrid.EnergyImpactDecomposer(size=50, rolling=True, rolling_history=0.75, traversal='bfs')
            | hybrid.QPUSubproblemAutoEmbeddingSampler()
            | hybrid.SplatComposer()) | hybrid.ArgMin(), convergence=3)
        sampler = hybrid.HybridSampler(workflow)
        results = sampler.sample(qm)

    else:
        print("\nSending to Kerberos Sampler...")
        results = hybrid.KerberosSampler().sample(qm) 

    if type == "qa":
        dwave.inspector.show(results)
        
    # for ind, record in enumerate(reversed(results.record)):
    #     if ind % 100 != 0:
    #         continue
    #     sample = record.sample
        # for k in range(et_problem["num_days"]):
        #     print("Day {}:".format(k + 1), [i for i in et_problem["graph"].nodes if sample[results.variables.index(f'v_{i},{k}')] == 1])

    best_sample = results.first.sample
    timetable = Timetable(et_problem, best_sample).check_validity()
    print("\nFinal Timetable")
    for k in range(et_problem["num_days"]):
        print("Day {}:".format(k + 1), [i for i in et_problem["graph"].nodes if best_sample[f'v_{i},{k}'] == 1])

    if write:
        write_to_file(best_sample, filename + "-" + type, et_problem["num_days"], et_problem["graph"].nodes)

    print("\nFinal result - Energy {}".format(results.first.energy))
    return timetable


if __name__ == "__main__":
    filename = "small-01.txt"
    solver = "qa"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:s:",["filename=","solver="])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-f", "--filename"):
            filename = arg
        elif opt in ("-s", "--solver"):
            solver = arg
        else:
            print("Invalid argument")

    print("\nSolving for problem {}...".format(filename))
    et_problem = get_graph_data(filename)
    if solver == "leap":
        qm = CqmBuilder(et_problem).get_cqm()
    else: 
        qm = BqmBuilder(et_problem).get_bqm()
    timetable = sample_and_get_results(solver, qm, et_problem, filename)