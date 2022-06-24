import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd

from dwave.system.samplers import DWaveSampler
import minorminer
from src.bqm_builder import BqmBuilder
from src.preprocessor import get_graph_data

# ---------------------boxplot-------------------------------------------------------------------------
# data = [{"Minimum Energy": min_energy, "Dataset": "small-02", "Type": "Quantum Annealing"} for min_energy in [12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817, 12.67605633802817]]

# data.extend([{"Minimum Energy": min_energy, "Dataset": "small-02-cc", "Type": "Quantum Annealing"} for min_energy in [6.124137931034454, 5.875862068965546, 6.758620689655174, 6.344827586206861, 6.124137931034454, 6.758620689655174, 6.124137931034483, 5.324137931034471, 6.34482758620689, 6.620689655172384]])

# data.extend([{"Minimum Energy": min_energy, "Dataset": "med-01", "Type": "Quantum Annealing"} for min_energy in [5.8267973856209245, 9.68954248366014, 8.019607843137297, 7.928104575163445, 10.303921568627452, 10.8823529411765, 7.535947712418306, 7.277777777777764, 11.25816993464051, 7.1666666666667]])

# data.extend([{"Minimum Energy": min_energy, "Dataset": "med-01-cc", "Type": "Quantum Annealing"} for min_energy in [129.85947712418306, 138.27450980392143, 146.30392156862752, 112.43790849673212, 145.16339869281057, 121.40196078431387, 125.07516339869267, 118.1111111111112, 141.5294117647062, 115.39869281045765]])

# data.extend([{"Minimum Energy": min_energy, "Dataset": "small-02", "Type": "Simulated Annealing"} for min_energy in [12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905, 12.676056338027905]])

# data.extend([{"Minimum Energy": min_energy, "Dataset": "small-02-cc", "Type": "Simulated Annealing"} for min_energy in [5.296551724137771, 5.296551724137771, 5.296551724137771, 5.296551724138226, 5.296551724138226, 5.2965517241379985, 5.296551724137771, 5.296551724137771, 5.2965517241379985, 5.296551724138226]])

# data.extend([{"Minimum Energy": min_energy, "Dataset": "med-01", "Type": "Simulated Annealing"} for min_energy in [5.568627450978852, 5.9575163398686755, 5.614379084966345, 5.088235294117453, 5.349673202613417, 5.307189542482433, 5.477124183004776, 5.699346405227175, 5.503267973854804, 5.52941176470415]])

# data.extend([{"Minimum Energy": min_energy, "Dataset": "med-01-cc", "Type": "Simulated Annealing"} for min_energy in [7.732026143795338, 8.464052287586128, 10.392156862754746, 15.960784313726435, 12.4575163398722, 25.290849673211596, 11.238562091511085, 13.062091503271404, 13.787581699355542, 9.058823529418987]])

 
# fig = px.box(data, x="Dataset", y="Minimum Energy", color="Type")
# fig.show()
# plt.savefig("boxplot.png")
#-----------------------------------------------------------------------------------------------------

# df = pd.read_csv('fyp-data-_1_.csv')
# print(df.columns)
# df = df[["Dataset", "SA min energy :(", "Chimera - min energy"]]
# df = df.dropna(axis=0)

# new_list = []

# for ind, row in df.iterrows():
#     new_list.append({"Dataset": row["Dataset"], "Minimum Energy": row["SA min energy :("], "Type": "Simulated Annealing"})
#     if row["Dataset"] == "small-03-cc":
#         new_list.append({"Dataset": row["Dataset"], "Minimum Energy": 102.38493, "Type": "Quantum Annealing"})
#     else:
#         new_list.append({"Dataset": row["Dataset"], "Minimum Energy": row["Chimera - min energy"], "Type": "Quantum Annealing"})

# new_df = pd.DataFrame(new_list)
# fig = px.line(new_df, x="Dataset", y="Minimum Energy", color="Type", markers=True)
# fig.show()
# plt.savefig("line.png")


#----------------------------------------------------------------------------------------------------

# df = pd.read_csv('fyp-data-_1_.csv')
# df = df[["Dataset", "Unnamed: 13", "SA time"]]
# df = df.dropna(axis=0)

# new_list = []

# for ind, row in df.iterrows():
#     new_list.append({"Dataset": row["Dataset"], "Computation Time": row["SA time"], "Type": "Simulated Annealing"})
#     new_list.append({"Dataset": row["Dataset"], "Computation Time": float(row["Unnamed: 13"])/1000000, "Type": "Quantum Annealing"})

# new_df = pd.DataFrame(new_list)
# fig = px.line(new_df, x="Dataset", y="Computation Time", color="Type", markers=True)
# fig.update_layout(legend_x=1, legend_y=1)
# fig.show()

#--------------------------------------------------------------------------------------------------------------

# df = pd.read_csv('fyp-data-_1_.csv')
# df = df[["Dataset"]]
# df.drop([5, 12, 13, 14, 16, 17, 18], axis=0, inplace=True)
# df = df.dropna(axis=0)
# print(df)
# new_list = []

# for ind, row in df.iterrows():
#     print("Dataset", row["Dataset"])
#     et_problem = get_graph_data(row["Dataset"] + ".txt")
#     bqm = BqmBuilder(et_problem).get_bqm()

#     qpu = DWaveSampler(solver={'topology__type': 'chimera'})
#     minor_embedding = minorminer.find_embedding(list(bqm.quadratic.keys()), qpu.edgelist)
#     if len(minor_embedding) > 0:
#         new_list.append({"Dataset": row["Dataset"], "Max Chain Length": len(max(minor_embedding.values(), key=lambda x: len(x))), "Type": "Chimera"})

#     qpu = DWaveSampler(solver={'topology__type': 'pegasus'})
#     minor_embedding = minorminer.find_embedding(list(bqm.quadratic.keys()), qpu.edgelist)
#     new_list.append({"Dataset": row["Dataset"], "Max Chain Length": len(max(minor_embedding.values(), key=lambda x: len(x))), "Type": "Pegasus"})

#     minor_embedding = minorminer.find_embedding(list(bqm.quadratic.keys()), qpu.edgelist, chainlength_patience=100)
#     new_list.append({"Dataset": row["Dataset"], "Max Chain Length": len(max(minor_embedding.values(), key=lambda x: len(x))), "Type": "Pegasus (CLP 100)"})

# new_df = pd.DataFrame(new_list)
# print("new df", new_df)
# fig = px.line(new_df, x="Dataset", y="Max Chain Length", color="Type", markers=True)
# fig.update_layout(legend_x=1, legend_y=1)
# fig.show()

# -----------------------------------------------------------------------------------------------------------

# s = [0.5, 0.4, 0.3, 0.2, 0.1, 0.09, 0.08, 0.07]
# min_energy = [8.6, 8.65, 8.5, 8.3, 7.77, 5.93, 10.06, 10.52]

# new_df = []

# for i in range(len(s)):
#     new_df.append({"s": s[i], "Minimum Energy": min_energy[i]})

# new_df = pd.DataFrame(new_df)
# print("new df", new_df)
# fig = px.line(new_df, x="s", y="Minimum Energy", markers=True, log_x=True)
# fig.update_layout(legend_x=1, legend_y=1)
# fig.show()

# s = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
# min_energy = [10.82, 11.209, 8.42, 7.19, 7.84, 9.29]

# new_df = []

# for i in range(len(s)):
#     new_df.append({"s": s[i], "Minimum Energy": min_energy[i]})

# new_df = pd.DataFrame(new_df)
# print("new df", new_df)
# fig = px.line(new_df, x="s", y="Minimum Energy", markers=True, log_x=True)
# fig.update_layout(legend_x=1, legend_y=1)
# fig.update_traces(line_color='#ff0000')
# fig.show()

#----------------------------------------------------------------------------------------------------

# df = pd.read_csv('tableConvert.com_vpw09w.csv')
# print(df.columns)
# # print(df.columns)
# # df = df[["Dataset", "SA min energy :(", "Chimera - min energy"]]
# # df = df.dropna(axis=0)

# new_list = []

# for ind, row in df.iterrows():
#     new_list.append({"Dataset": row["Dataset"], "Minimum Energy": row["SA"], "Type": "SA"})
#     if row["Initial QA"] != "-":
#         new_list.append({"Dataset": row["Dataset"], "Minimum Energy": row["Initial QA"], "Type": "QA (Initial)"})
#     new_list.append({"Dataset": row["Dataset"], "Minimum Energy": row["Final QA"], "Type": "QA (Final)"})
# new_df = pd.DataFrame(new_list)
# fig = px.line(new_df, x="Dataset", y="Minimum Energy", color="Type", markers=True)
# fig.update_layout(font=dict(size=20))
# fig.show()
# plt.savefig("line.png")

# new_list = []

# print("\nSending to postprocessor...")
# post_results_noqpu = SteepestDescentSampler().sample(bqm, num_reads=100)

# for ind, record in enumerate(post_results_noqpu.record):
#     new_list.append({"Sample": ind + 1, "Energy": record.energy, "Type": "Classical samples"})

# for ind, record in enumerate(post_results.record):
#     new_list.append({"Sample": ind + 1, "Energy": record.energy, "Type": "Postprocessed Quantum samples"})

# new_df = pd.DataFrame(new_list)
# fig = px.line(new_df, x="Sample", y="Energy", color="Type", markers=True)
# fig.update_layout(font=dict(size=20))
# fig.show()
# plt.savefig("line.png")


df = pd.read_csv('convertcsv.csv')

print(df.columns)
# print(df.columns)

df = df.drop([2, 5, 7, 10, 11], axis=0)

new_list = []

for ind, row in df.iterrows():
    new_list.append({"Dataset": row["Dataset"] + "-" + str(row["Version"]), "Energy (Best Solution)": float(row["dwave-hybrid"]), "Type": "dwave-hybrid"})
    new_list.append({"Dataset": row["Dataset"] + "-" + str(row["Version"]), "Energy (Best Solution)": float(row["kerberos"]), "Type": "Kerberos"})


new_df = pd.DataFrame(new_list)
fig = px.line(new_df, x="Dataset", y="Energy (Best Solution)", color="Type", markers=True)
fig.update_layout(font=dict(size=20))
fig.show()
plt.savefig("line.png")