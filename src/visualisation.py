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

from datetime import datetime, timedelta
from matplotlib.pyplot import colorbar
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx


class Visualiser:

    def __init__(self, et_problem, results):
        self.graph = et_problem["graph"]
        self.results = results
        self.num_days = et_problem["num_days"]
        self.num_exams = len(self.graph.nodes)
        self.best_sample = self.results.first.sample
        self.final_iteration = len(results)

    def visualise_result(
            self,
            sample_data,
            sample,
            iteration,
            title,
            last_one=False):
        exams_set = []
        for k in range(self.num_days):
            if not last_one:
                exams = [i for i in range(
                    self.num_exams) if sample[self.results.variables.index(f'v_{i},{k}')] == 1]
            else:
                exams = [
                    i for i in range(
                        self.num_exams) if sample[f'v_{i},{k}'] == 1]

            time = datetime.strptime("01/01/21", "%d/%m/%y")
            for e in exams:
                edges = self.graph.edges(e)
                other_nodes = [
                    node1 if node2 == e else node2 for (
                        node1, node2) in edges]
                clashes = sum([self.graph[e][node]['weight']
                              if node in exams else 0 for node in other_nodes])
                end_time = time + timedelta(days=60)

                if e in exams_set:
                    exams_str = "Exam " + str (e) + " (duplicate)"
                else:
                    exams_set.append(e)
                    exams_str = "Exam " + str(e)

                sample_data.append(
                    dict(
                        Day="Day {}".format(
                            k + 1),
                        Start=time,
                        End=end_time,
                        Exam=exams_str,
                        Clashes=clashes,
                        Iteration=iteration,
                        Title=title))
                time = end_time + timedelta(days=15)

    def get_sample_data(self):
        sample_data = []
        for ind, record in enumerate(reversed(self.results.record)):
            if ind % 100 != 0:
                continue

            title = "Iteration {} - Energy: {}".format(ind, record.energy)
            sample = record.sample
            self.visualise_result(sample_data, sample, ind, title)

        title = "Iteration {} - Energy {}".format(
            self.final_iteration, self.results.first.energy)
        self.visualise_result(sample_data, self.best_sample, 1000, title, True)
        return sample_data

    def build_animated_timetable(self):
        sample_data = self.get_sample_data()
        max_clashes = max(sample_data, key=lambda x: x['Clashes'])["Clashes"]
        fig = px.timeline(
            sample_data,
            animation_frame="Iteration",
            animation_group="Exam",
            x_start="Start",
            x_end="End",
            y="Day",
            title="Exam Timetabling Optimisation",
            text="Exam",
            color="Clashes",
            color_continuous_scale='temps',
            range_color=(
                0,
                max_clashes),
            hover_data={
                "Iteration": False,
                "Start": False,
                "End": False,
                "Day": False,
                "Exam": True,
                "Clashes": True})
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(visible=False)
        fig.update_traces(textposition='inside')
        fig.update_layout(transition = {'duration': 1000}, uniformtext_minsize=50)
        return fig

    def get_node_trace(self, node_x, node_y, day, exams):
        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            name=f"Day {day}",
            marker=dict(
                size=12,
                line_width=2),
            hovertemplate='<b>Exam</b>: %{text}<extra></extra>',
            text=list(exams)
        )

    def get_edge_trace(self, edge_x, edge_y, edge_colors, text=None):
        if text is None:
            text = []
        return go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1.8, color=edge_colors),
            hovertemplate="%{text}",
            text=text,
            mode='lines',
            showlegend=False)

    def build_animated_graph(self):
        graph_with_pos = nx.spring_layout(self.graph, 2)
        edge_x = []
        edge_y = []
        for edge in self.graph.edges():
            x0, y0 = graph_with_pos[edge[0]]
            x1, y1 = graph_with_pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        frames = []

        for ind, record in enumerate(reversed(self.results.record)):
            if ind % 100 != 0:
                continue
            fig = go.Figure()

            exams_per_day = [[e for e in graph_with_pos.keys() if record.sample[self.results.variables.index(
                f'v_{e},{d}')] == 1] for d in range(self.num_days)]

            edge_x = []
            edge_y = []
            edge_x_clash = []
            edge_y_clash = []
            clashes_text = []
            for edge in self.graph.edges():
                x0, y0 = graph_with_pos[edge[0]]
                x1, y1 = graph_with_pos[edge[1]]
                if any([edge[0] in exams and edge[1]
                       in exams for exams in exams_per_day]):
                    edge_x_clash.extend([x0, x1, None])
                    edge_y_clash.extend([y0, y1, None])
                    clashes_text.append(
                        "Clash between exams " +
                        "{} and {}".format(
                            edge[0],
                            edge[1]))
                else:

                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])

            fig.add_trace(
                self.get_edge_trace(
                    edge_x_clash,
                    edge_y_clash,
                    "red",
                    clashes_text))
            fig.add_trace(self.get_edge_trace(edge_x, edge_y, "grey"))

            for ind, exams in enumerate(exams_per_day):
                node_x, node_y = zip(*[graph_with_pos[e] for e in exams])
                fig.add_trace(
                    self.get_node_trace(
                        list(node_x),
                        list(node_y),
                        ind + 1,
                        exams))

        return fig
