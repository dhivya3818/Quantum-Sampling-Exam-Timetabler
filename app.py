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

import time
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from src.preprocessor import get_graph_data
from src.bqm_builder import BqmBuilder
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
from src.visualisation import Visualiser
import neal

import pandas as pd

app = Dash(__name__)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
labels = [
    "5 exams, 2 days",
    "5 exams, 2 days with classroom constraints",
    "7 exams, 3 days",
    "7 exams, 3 days with classroom constraints",
    "10 exams, 4 days",
    "10 exams, 4 days with classroom constraints",
    "10 exams, 4 days (low conflict density)",
    "10 exams, 4 days, with classroom constraints (low conflict density)",
    "15 exams, 5 days",
    "15 exams, 5 days with classroom constraints",
    "20 exams, 7 days",
    "20 exams, 7 days with classroom constraints",
    "20 exams, 7 days (low conflict density)",
    "20 exams, 7 days, with classroom constraints (low conflict density)"]

test_data_map = {
    "5 exams, 2 days": "small-01.txt",
    "5 exams, 2 days with classroom constraints": "small-01-cc.txt",
    "7 exams, 3 days": "small-02.txt",
    "7 exams, 3 days with classroom constraints": "small-02-cc.txt",
    "10 exams, 4 days": "small-03.txt",
    "10 exams, 4 days with classroom constraints": "small-03-cc.txt",
    "10 exams, 4 days (low conflict density)": "small-03-dis.txt",
    "10 exams, 4 days, with classroom constraints (low conflict density)": "small-03-cc-dis.txt",
    "15 exams, 5 days": "med-01.txt",
    "15 exams, 5 days with classroom constraints": "med-01-cc.txt",
    "20 exams, 7 days": "med-02.txt",
    "20 exams, 7 days with classroom constraints": "med-02-cc.txt",
    "20 exams, 7 days (low conflict density)": "med-02-dis.txt",
    "20 exams, 7 days, with classroom constraints (low conflict density)": "med-02-cc-dis.txt"}

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                labels,
                labels[0],
                id='xaxis-column'
            ),
            dcc.RadioItems(
                ['Timetable', 'Graph'],
                'Timetable',
                id='graph-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'})]),

    dcc.Loading(
        id="ls-loading",
        children=[dcc.Graph(id='indicator-graphic')],
        type="default",
    )
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('graph-type', 'value'))
def update_graph(xaxis_column_name, graph_type):
    time.sleep(1)
    dataset = test_data_map[xaxis_column_name]
    et_problem = get_graph_data(dataset)
    bqm = BqmBuilder(et_problem).get_bqm()
    # sampler = neal.SimulatedAnnealingSampler()
    # results = sampler.sample(bqm)
    sampler = EmbeddingComposite(DWaveSampler())
    results = sampler.sample(
        bqm,
        num_reads=1000,
        label='Example - Exam Timetabling')

    if graph_type == "Timetable":
        fig = Visualiser(et_problem, results).build_animated_timetable()
    else:
        fig = Visualiser(et_problem, results).build_animated_graph()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
