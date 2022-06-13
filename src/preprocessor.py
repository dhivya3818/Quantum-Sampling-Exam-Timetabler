import networkx as nx
from collections import Counter
from itertools import combinations

timeslots = {"hec-s-92-2":18, "hec-s-92":18 }

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
        file_path = "test_data/" + filename
    else:
        file_path = "toronto_benchmark_data/" + filename
        num_days = timeslots[filename[:-3]]
        resources = {}
        starting_index = 0

    # Open input file
    input_file = open("./timetabling_data/" + file_path, 'r')
    input_lines = input_file.readlines()
    
    # Get parameters num_days and classrooms if file is from test_data folder
    if filename[-3:] == "txt":
        num_days = input_lines[0].split()[1]
        if input_lines[1].split()[0] != "classrooms":
            resources = {}
            starting_index = 1
        else:
            resources = { "classrooms": list(map(int, input_lines[1].split()[1:]))}
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

        clashing_pairs = [((exam1, exam2) if exam1 < exam2 else (exam2, exam1)) for (exam1, exam2) in combinations(exams, 2)]
        clashes += Counter(clashing_pairs)

    graph = build_graph(exams_counter, clashes)

    et_problem = { "graph": graph, "num_days": int(num_days), "resources": resources, "num_students": (len(input_lines) - starting_index)}
    return et_problem