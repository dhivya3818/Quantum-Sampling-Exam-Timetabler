import networkx as nx
from collections import Counter
from itertools import combinations

def build_graph(exams, clashes):
    graph = nx.Graph()

    for exam, count in exams.items():
        graph.add_node(exam, size=count)

    for exams_pair, weight in clashes.items():
        exam1, exam2 = exams_pair
        graph.add_edge(exam1, exam2, weight=weight)

    return graph

def get_graph_data(filename):
    stu_file = open("./tests/" + filename + ".stu", 'r')

    clashing_exams = []
    exams_counter = Counter()

    for ind, line in enumerate(stu_file):
        exams = [int(exam) for exam in line.split()]
        if exams not in clashing_exams:
            clashing_exams.append(exams)
        
        exams_counter += Counter(exams)

    clashes = Counter()
    for exams in clashing_exams:
        if len(exams) == 1:
            continue

        clashing_pairs = [((exam1, exam2) if exam1 < exam2 else (exam2, exam1)) for (exam1, exam2) in combinations(exams, 2)]
        clashes += Counter(clashing_pairs)

    graph = build_graph(exams_counter, clashes)

    return graph