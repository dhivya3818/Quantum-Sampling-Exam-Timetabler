import itertools
from collections import Counter


class Timetable:

    def __init__(self, et_problem, record):
        self.num_days = et_problem["num_days"]
        self.graph = et_problem["graph"]
        self.resources = et_problem["resources"]
        self.timetable = self.make_timetable(record)

    def make_timetable(self, record):
        timetable = {}

        for k in range(self.num_days):
            timetable[k +
                      1] = [i for i in self.graph.nodes if record[f'v_{i},{k}'] == 1]

        return timetable

    def print_timetable(self):
        for day, exams in self.timetable.items():
            print("Day {}: {}".format(day, exams))

    def check_hard_clashes(self):
        penalty = 0

        for _, exams in self.timetable.items():
            for (course1, course2) in itertools.combinations(exams, 2):
                if self.graph.has_edge(course1, course2):
                    print("\nCLASH between exams {} and {}: weight {}".format(
                        course1, course2, self.graph[course1][course2]["weight"]))
                    penalty += self.graph[course1][course2]["weight"]

        return penalty

    def check_classroom_constraints(self):
        days = []

        for day, exams in self.timetable.items():
            if len(exams) > len(self.resources['classrooms']):
                days.append(day)
                continue

            exams.sort(key=lambda e: self.graph.nodes[e]['size'])
            available_classrooms = self.resources['classrooms'][-len(exams):]
            if not all([self.graph.nodes[exams[i]]['size'] <=
                       available_classrooms[i] for i in range(len(exams))]):
                days.append(day)

        return days

    def check_one_hot(self):
        allocated_exams = itertools.chain(*self.timetable.values())
        count_allocated_exams = Counter(allocated_exams)
        return len(count_allocated_exams) == len(self.graph.nodes) and all(
            count == 1 for count in count_allocated_exams.values())

    def check_validity(self):
        valid_solution = []

        print("\nChecking all exams allocated exactly once...")
        if not self.check_one_hot():
            print("\nSolution fails check: exams not allocated exactly once!")
            valid_solution.append("C1")

        print("\nChecking no clashing exams are on the same day...")
        penalty = self.check_hard_clashes()
        if penalty > 0:
            print("\nSolution fails check: penalty " + str(penalty))
            valid_solution.append("C2")

        if len(self.resources) != 0:
            print("\nChecking solution satisfies classroom constraints...")
            days = self.check_classroom_constraints()
            if len(days) > 0:
                print(
                    "\nSolution fails check: classroom constraints broken on days {}".format(days))
                valid_solution.append("C4")

        # if valid_solution:
        #     print("\nSolution passes all constraint checks!")

        return valid_solution
