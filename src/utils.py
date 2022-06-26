import networkx as nx


def write_to_file(sample, filename, num_days, exams):
    timetable = []
    for k in range(num_days):
        timetable.extend(["{}\t{}\n".format(str(i).zfill(4), k)
                         for i in exams if sample[f'v_{i},{k}'] == 1])

    file = open("output/{}.sol".format(filename), "w")
    file.writelines(timetable)
    file.close()


def get_conflict_density(graph):
    adj_matrix = nx.adjacency_matrix(graph).todense().tolist()
    conflict_matrix = [[int(x > 0) for x in row] for row in adj_matrix]
    return sum(row.count(1)
               for row in conflict_matrix) / (len(conflict_matrix) ** 2)
