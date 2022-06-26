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

import networkx as nx
from collections import Counter
from itertools import combinations

timeslots = {
    "hec-s-92-2": 18,
    "hec-s-92": 18,
    "car-f-92": 32,
    "ute-s-92": 10,
    "yor-f-83-3": 21,
    "tre-s-92": 23,
    "lse-f-91": 18,
    "uta-s-92-2": 35,
    "sta-f-83-3": 35,
    "sta-f-83": 13,
    "pur-s-93": 42,
    "kfu-s-93": 20,
    "ear-f-83": 24,
    "car-f-92": 32,
    "car-s-91": 35}


def build_graph(exams, clashes):
    graph = nx.Graph()

    for exam, count in exams.items():
        graph.add_node(exam, size=count)

    for exams_pair, weight in clashes.items():
        exam1, exam2 = exams_pair
        graph.add_edge(exam1, exam2, weight=weight)

    return graph


def get_graph_data(filename):

    # Determine if file is from test_data or toronto_benchmark_data
    if filename[-3:] == "txt":
        file_path = filename
    else:
        file_path = "toronto_benchmark_data/" + filename
        num_days = timeslots[filename[:-4]]
        resources = {}
        starting_index = 0

    # Open input file
    input_file = open("./timetabling_problems/" + file_path, 'r')
    input_lines = input_file.readlines()

    # Get parameters num_days and classrooms if file is from test_data folder
    if filename[-3:] == "txt":
        num_days = input_lines[0].split()[1]
        if input_lines[1].split()[0] != "classrooms":
            resources = {}
            starting_index = 1
        else:
            resources = {"classrooms": list(
                map(int, input_lines[1].split()[1:]))}
            starting_index = 2

    exams_counter = Counter()
    clashes = Counter()

    # Tally sizes of each class and number of each clash
    for i in range(starting_index, len(input_lines)):
        line = input_lines[i]
        exams = [int(exam) for exam in line.split()]
        exams_counter += Counter(exams)

        if len(exams) == 1:
            continue

        clashing_pairs = [
            ((exam1, exam2) if exam1 < exam2 else (
                exam2, exam1)) for (
                exam1, exam2) in combinations(
                exams, 2)]
        clashes += Counter(clashing_pairs)

    graph = build_graph(exams_counter, clashes)
    return {
        "graph": graph,
        "num_days": int(num_days),
        "resources": resources,
        "num_students": (
            len(input_lines) -
            starting_index)}
