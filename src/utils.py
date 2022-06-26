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
