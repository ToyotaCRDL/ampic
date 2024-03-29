# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import xml.etree.ElementTree as ET

fig_dir = os.getcwd() + "/figs/"

savefig_type = ".pdf"
# savefig_type = ".png"
# %%


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i] * 0.9, np.round(y[i], decimals=3), ha="center")


def read_stats_raw(dir_name):
    fn1 = os.getcwd() + dir_name
    fn2 = "/values.dat"
    fn3 = "/statistic.xml"
    df_values = pd.read_csv(fn1 + fn2, skiprows=2, header=None)

    vmean = df_values[3]
    hamiltonian = df_values[4]
    sigterm = df_values[6]
    waitrate = df_values[7]
    co2 = df_values[8]
    # elapsedtime = df_values[9]
    elapsedtime = df_values[10]

    tree = ET.ElementTree(file=fn1 + fn3)
    root = tree.getroot()
    vts = root.find("vehicleTripStatistics")
    waittime = float(vts.attrib["waitingTime"])

    return (
        np.array(vmean),
        np.array(sigterm),
        np.array(waitrate),
        np.array(waittime),
        np.array(hamiltonian),
        np.array(elapsedtime),
        np.array(co2),
    )


# %%

dirs_0 = [
    "gc_s60_seed1_greedy_nr1",
    "gc_s60_seed2_greedy_nr1",
    "gc_s60_seed3_greedy_nr1",
    "gc_s60_seed4_greedy_nr1",
    "gc_s60_seed5_greedy_nr1",
]

# dirs_0 = [
#     "gc_s60_seed1_greedy",
#     "gc_s60_seed2_greedy",
#     "gc_s60_seed3_greedy",
#     "gc_s60_seed4_greedy",
#     "gc_s60_seed5_greedy",
# ]


# dirs_1 = [
#     "gc_s60_seed1_sa10",
#     "gc_s60_seed2_sa10",
#     "gc_s60_seed3_sa10",
#     "gc_s60_seed4_sa10",
#     "gc_s60_seed5_sa10",
# ]

dirs_1 = [
    "gc_s60_seed1",
    "gc_s60_seed2",
    "gc_s60_seed3",
    "gc_s60_seed4",
    "gc_s60_seed5",
]


# dirs_2 = [
#     "gc_s60_seed1_hb3",
#     "gc_s60_seed2_hb3",
#     "gc_s60_seed3_hb3",
#     "gc_s60_seed4_hb3",
#     "gc_s60_seed5_hb3",
# ]

# dirs_2 = [
#     "gc_s60_seed1_hb2",
#     "gc_s60_seed2_hb2",
#     "gc_s60_seed3_hb2",
#     "gc_s60_seed4_hb2",
#     "gc_s60_seed5_hb2",
# ]

# dirs_2 = [
#     "gc_s60_seed1_hb",
#     "gc_s60_seed2_hb",
#     "gc_s60_seed3_hb",
#     "gc_s60_seed4_hb",
#     "gc_s60_seed5_hb",
# ]


dirs_2 = [
    "gc_s60_seed1_qa",
    "gc_s60_seed2_qa",
    "gc_s60_seed3_qa",
    "gc_s60_seed4_qa",
    "gc_s60_seed5_qa",
]


dir_name = ["Greedy", "SA", "QA"]
# dir_name = ["Greedy", "SA", "Hybrid"]
bar_place = [0, 1, 2]


# %%

stats_0 = np.zeros((len(dirs_0), 3600))
stats_1 = np.zeros((len(dirs_1), 3600))
stats_2 = np.zeros((len(dirs_2), 3600))
# stats_3 = np.zeros((len(dirs_2), 3600))

for k, dg in enumerate(dirs_0):
    dir_name_0 = "/case042/p023/" + dg + "/w00000"
    # dir_name_0 = '/case042/p023/' + dg + '/t00'
    # print(dir_name_0)
    stats_0[k, :] = read_stats_raw(dir_name_0)[6]
    print(stats_0)

for k, dg in enumerate(dirs_1):
    # dir_name_1 = '/case042/p023/' + dg + '/w00000'
    dir_name_1 = "/case042/p023/" + dg + "/w00000"
    # print(dir_name_1)
    stats_1[k, :] = read_stats_raw(dir_name_1)[6]
    print(stats_1)

for k, dl in enumerate(dirs_2):
    # dir_name_2 = '/case042/p023/' + dl + '/w00000'
    dir_name_2 = "/case042/p023/" + dl + "/w00000"
    stats_2[k, :] = read_stats_raw(dir_name_2)[6]
    print(stats_2)

# for k, dl in enumerate(dirs_3):
#     # dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     stats_3[k, :] = read_stats_raw(dir_name_3)[0]
#     print(stats_3)


# # %%

# # plt.plot(np.mean(stats_0, axis=0), label="local mean",
#     #  color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_0, axis=0), label="sa NR 10",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_1, axis=0), label="sa mean",
#          color=cm.tab10(1/10), alpha=0.8)
# plt.plot(np.mean(stats_2, axis=0), label="qa mean",
#          color=cm.tab10(2/10), alpha=0.8)
# plt.plot(np.mean(stats_3, axis=0), label="hybrid mean",
#          color=cm.tab10(3/10), alpha=0.8)
# plt.grid(color='gray', linestyle='dotted', linewidth=0.5)
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Mean velocity [m/s]")
# # plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
# plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
#             bbox_inches='tight', dpi=300)


# %%

stats_0_time_mean = np.mean(stats_0, axis=0)
stats_0_time_mean_seed_mean = np.mean(stats_0_time_mean)
stats_0_time_mean_seed_std = np.std(stats_0_time_mean)

stats_1_time_mean = np.mean(stats_1, axis=0)
stats_1_time_mean_seed_mean = np.mean(stats_1_time_mean)
stats_1_time_mean_seed_std = np.std(stats_1_time_mean)

stats_2_time_mean = np.mean(stats_2, axis=0)
stats_2_time_mean_seed_mean = np.mean(stats_2_time_mean)
stats_2_time_mean_seed_std = np.std(stats_2_time_mean)

# stats_3_time_mean = np.mean(stats_3, axis=0)
# stats_3_time_mean_seed_mean = np.mean(stats_3_time_mean)
# stats_3_time_mean_seed_std = np.std(stats_3_time_mean)

stats_time_mean_seed_mean_ar = [
    stats_0_time_mean_seed_mean,
    stats_1_time_mean_seed_mean,
    stats_2_time_mean_seed_mean,
]


# stats_time_mean_seed_mean_ar = [
#     stats_0_time_mean_seed_mean, stats_1_time_mean_seed_mean, stats_2_time_mean_seed_mean, stats_3_time_mean_seed_mean]

stats_time_mean_seed_std_ar = [
    stats_0_time_mean_seed_std / len(dirs_0),
    stats_1_time_mean_seed_std / len(dirs_1),
    stats_2_time_mean_seed_std / len(dirs_2),
    # stats_3_time_mean_seed_std/len(dirs_3)
]


plt.bar(
    bar_place,
    stats_time_mean_seed_mean_ar,
    yerr=stats_time_mean_seed_std_ar,
    tick_label=dir_name,
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
ax = plt.gca()
addlabels(bar_place, stats_time_mean_seed_mean_ar)
# plt.bar_2abel(["SA", "QA"])
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Mean velocity [m/s]")
# plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
plt.ylabel("CO2 emission [kg/s]")
plt.savefig(
    fig_dir + "case042_co2_mean_10x10_p023_lcsaqa_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


print(stats_time_mean_seed_mean_ar)
print(stats_time_mean_seed_std_ar)


# %%
stats_0 = np.zeros((len(dirs_0), 3600))
stats_1 = np.zeros((len(dirs_1), 3600))
stats_2 = np.zeros((len(dirs_2), 3600))
# stats_3 = np.zeros((len(dirs_2), 3600))

for k, dg in enumerate(dirs_0):
    dir_name_0 = "/case042/p023/" + dg + "/w00000"
    # dir_name_0 = '/case042/p023/' + dg + '/t00'
    # print(dir_name_0)
    stats_0[k, :] = read_stats_raw(dir_name_0)[0]
    print(stats_0)

for k, dg in enumerate(dirs_1):
    # dir_name_1 = '/case042/p023/' + dg + '/w00000'
    dir_name_1 = "/case042/p023/" + dg + "/w00000"
    # print(dir_name_1)
    stats_1[k, :] = read_stats_raw(dir_name_1)[0]
    print(stats_1)

for k, dl in enumerate(dirs_2):
    # dir_name_2 = '/case042/p023/' + dl + '/w00000'
    dir_name_2 = "/case042/p023/" + dl + "/w00000"
    stats_2[k, :] = read_stats_raw(dir_name_2)[0]
    print(stats_2)

# for k, dl in enumerate(dirs_3):
#     # dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     stats_3[k, :] = read_stats_raw(dir_name_3)[0]
#     print(stats_3)


# # %%

# # plt.plot(np.mean(stats_0, axis=0), label="local mean",
#     #  color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_0, axis=0), label="sa NR 10",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_1, axis=0), label="sa mean",
#          color=cm.tab10(1/10), alpha=0.8)
# plt.plot(np.mean(stats_2, axis=0), label="qa mean",
#          color=cm.tab10(2/10), alpha=0.8)
# plt.plot(np.mean(stats_3, axis=0), label="hybrid mean",
#          color=cm.tab10(3/10), alpha=0.8)
# plt.grid(color='gray', linestyle='dotted', linewidth=0.5)
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Mean velocity [m/s]")
# # plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
# plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
#             bbox_inches='tight', dpi=300)


# %%

stats_0_time_mean = np.mean(stats_0, axis=0)
stats_0_time_mean_seed_mean = np.mean(stats_0_time_mean)
stats_0_time_mean_seed_std = np.std(stats_0_time_mean)

stats_1_time_mean = np.mean(stats_1, axis=0)
stats_1_time_mean_seed_mean = np.mean(stats_1_time_mean)
stats_1_time_mean_seed_std = np.std(stats_1_time_mean)

stats_2_time_mean = np.mean(stats_2, axis=0)
stats_2_time_mean_seed_mean = np.mean(stats_2_time_mean)
stats_2_time_mean_seed_std = np.std(stats_2_time_mean)

# stats_3_time_mean = np.mean(stats_3, axis=0)
# stats_3_time_mean_seed_mean = np.mean(stats_3_time_mean)
# stats_3_time_mean_seed_std = np.std(stats_3_time_mean)

stats_time_mean_seed_mean_ar = [
    stats_0_time_mean_seed_mean,
    stats_1_time_mean_seed_mean,
    stats_2_time_mean_seed_mean,
]


# stats_time_mean_seed_mean_ar = [
#     stats_0_time_mean_seed_mean, stats_1_time_mean_seed_mean, stats_2_time_mean_seed_mean, stats_3_time_mean_seed_mean]

stats_time_mean_seed_std_ar = [
    stats_0_time_mean_seed_std / len(dirs_0),
    stats_1_time_mean_seed_std / len(dirs_1),
    stats_2_time_mean_seed_std / len(dirs_2),
    # stats_3_time_mean_seed_std/len(dirs_3)
]


plt.bar(
    bar_place,
    stats_time_mean_seed_mean_ar,
    yerr=stats_time_mean_seed_std_ar,
    tick_label=dir_name,
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
ax = plt.gca()
addlabels(bar_place, stats_time_mean_seed_mean_ar)
# plt.bar_2abel(["SA", "QA"])
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Mean velocity [m/s]")
# plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
plt.ylabel("Mean velocity [m/s]")
plt.savefig(
    fig_dir + "case042_vmean_mean_10x10_p023_lcsaqa_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


print(stats_time_mean_seed_mean_ar)
print(stats_time_mean_seed_std_ar)


# %%
stats_0 = np.zeros((len(dirs_0), 3600))
stats_1 = np.zeros((len(dirs_1), 3600))
stats_2 = np.zeros((len(dirs_2), 3600))
# stats_3 = np.zeros((len(dirs_2), 3600))

for k, dg in enumerate(dirs_0):
    dir_name_0 = "/case042/p023/" + dg + "/w00000"
    # dir_name_0 = '/case042/p023/' + dg + '/t00'
    # print(dir_name_0)
    stats_0[k, :] = read_stats_raw(dir_name_0)[2]
    print(stats_0)

for k, dg in enumerate(dirs_1):
    # dir_name_1 = '/case042/p023/' + dg + '/w00000'
    dir_name_1 = "/case042/p023/" + dg + "/w00000"
    # print(dir_name_1)
    stats_1[k, :] = read_stats_raw(dir_name_1)[2]
    print(stats_1)

for k, dl in enumerate(dirs_2):
    # dir_name_2 = '/case042/p023/' + dl + '/w00000'
    dir_name_2 = "/case042/p023/" + dl + "/w00000"
    stats_2[k, :] = read_stats_raw(dir_name_2)[2]
    print(stats_2)

# for k, dl in enumerate(dirs_3):
#     # dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     stats_3[k, :] = read_stats_raw(dir_name_3)[2]
#     print(stats_3)


# plt.plot(np.mean(stats_0, axis=0), label="sa",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_1, axis=0), label="qa",
#          color=cm.tab10(1/10), alpha=0.8)
# plt.plot(np.mean(stats_2, axis=0), label="hb-1",
#          color=cm.tab10(2/10), alpha=0.8)
# plt.plot(np.mean(stats_3, axis=0), label="hb-2",
#          color=cm.tab10(3/10), alpha=0.8)
# plt.grid(color='gray', linestyle='dotted', linewidth=0.5)
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Waiting vehicle ratio")
# # plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
# plt.savefig(fig_dir+"waitrate_10x10_p023_qasa_seed_mean"+savefig_type,
#             bbox_inches='tight', dpi=300)

# %%

stats_0_time_mean = np.mean(stats_0, axis=0)
stats_0_time_mean_seed_mean = np.mean(stats_0_time_mean)
stats_0_time_mean_seed_std = np.std(stats_0_time_mean)

stats_1_time_mean = np.mean(stats_1, axis=0)
stats_1_time_mean_seed_mean = np.mean(stats_1_time_mean)
stats_1_time_mean_seed_std = np.std(stats_1_time_mean)

stats_2_time_mean = np.mean(stats_2, axis=0)
stats_2_time_mean_seed_mean = np.mean(stats_2_time_mean)
stats_2_time_mean_seed_std = np.std(stats_2_time_mean)

# stats_3_time_mean = np.mean(stats_3, axis=0)
# stats_3_time_mean_seed_mean = np.mean(stats_3_time_mean)
# stats_3_time_mean_seed_std = np.std(stats_3_time_mean)

stats_time_mean_seed_mean_ar = [
    stats_0_time_mean_seed_mean,
    stats_1_time_mean_seed_mean,
    stats_2_time_mean_seed_mean,
    # stats_3_time_mean_seed_mean
]

stats_time_mean_seed_std_ar = [
    stats_0_time_mean_seed_std / len(dirs_0),
    stats_1_time_mean_seed_std / len(dirs_1),
    stats_2_time_mean_seed_std / len(dirs_2),
    # stats_3_time_mean_seed_std/len(dirs_3)
]


plt.bar(
    bar_place,
    stats_time_mean_seed_mean_ar,
    yerr=stats_time_mean_seed_std_ar,
    tick_label=dir_name,
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
# plt.bar_label(stats_time_mean_seed_mean_ar)
addlabels(bar_place, stats_time_mean_seed_mean_ar)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.ylabel("Waiting vehicle ratio")
plt.savefig(
    fig_dir + "case042_waitrate_mean_10x10_p023_saqa_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


print(stats_time_mean_seed_mean_ar)
print(stats_time_mean_seed_std_ar)


# %%
stats_0 = np.zeros((len(dirs_0), 3600))
stats_1 = np.zeros((len(dirs_1), 3600))
stats_2 = np.zeros((len(dirs_2), 3600))
# stats_3 = np.zeros((len(dirs_2), 3600))

for k, dg in enumerate(dirs_0):
    dir_name_0 = "/case042/p023/" + dg + "/w00000"
    # dir_name_0 = '/case042/p023/' + dg + '/t00'
    # print(dir_name_0)
    stats_0[k, :] = read_stats_raw(dir_name_0)[3]
    print(stats_0)

for k, dg in enumerate(dirs_1):
    # dir_name_1 = '/case042/p023/' + dg + '/w00000'
    dir_name_1 = "/case042/p023/" + dg + "/w00000"
    # print(dir_name_1)
    stats_1[k, :] = read_stats_raw(dir_name_1)[3]
    print(stats_1)

for k, dl in enumerate(dirs_2):
    # dir_name_2 = '/case042/p023/' + dl + '/w00000'
    dir_name_2 = "/case042/p023/" + dl + "/w00000"
    stats_2[k, :] = read_stats_raw(dir_name_2)[3]
    print(stats_2)

# for k, dl in enumerate(dirs_3):
#     # dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     stats_3[k, :] = read_stats_raw(dir_name_3)[2]
#     print(stats_3)


# plt.plot(np.mean(stats_0, axis=0), label="sa",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_1, axis=0), label="qa",
#          color=cm.tab10(1/10), alpha=0.8)
# plt.plot(np.mean(stats_2, axis=0), label="hb-1",
#          color=cm.tab10(2/10), alpha=0.8)
# plt.plot(np.mean(stats_3, axis=0), label="hb-2",
#          color=cm.tab10(3/10), alpha=0.8)
# plt.grid(color='gray', linestyle='dotted', linewidth=0.5)
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Waiting vehicle ratio")
# # plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
# plt.savefig(fig_dir+"waitrate_10x10_p023_qasa_seed_mean"+savefig_type,
#             bbox_inches='tight', dpi=300)

# %%

stats_0_time_mean = np.mean(stats_0, axis=0)
stats_0_time_mean_seed_mean = np.mean(stats_0_time_mean)
stats_0_time_mean_seed_std = np.std(stats_0_time_mean)

stats_1_time_mean = np.mean(stats_1, axis=0)
stats_1_time_mean_seed_mean = np.mean(stats_1_time_mean)
stats_1_time_mean_seed_std = np.std(stats_1_time_mean)

stats_2_time_mean = np.mean(stats_2, axis=0)
stats_2_time_mean_seed_mean = np.mean(stats_2_time_mean)
stats_2_time_mean_seed_std = np.std(stats_2_time_mean)

# stats_3_time_mean = np.mean(stats_3, axis=0)
# stats_3_time_mean_seed_mean = np.mean(stats_3_time_mean)
# stats_3_time_mean_seed_std = np.std(stats_3_time_mean)

stats_time_mean_seed_mean_ar = [
    stats_0_time_mean_seed_mean,
    stats_1_time_mean_seed_mean,
    stats_2_time_mean_seed_mean,
    # stats_3_time_mean_seed_mean
]

stats_time_mean_seed_std_ar = [
    stats_0_time_mean_seed_std / len(dirs_0),
    stats_1_time_mean_seed_std / len(dirs_1),
    stats_2_time_mean_seed_std / len(dirs_2),
    # stats_3_time_mean_seed_std/len(dirs_3)
]


plt.bar(
    bar_place,
    stats_time_mean_seed_mean_ar,
    yerr=stats_time_mean_seed_std_ar,
    tick_label=dir_name,
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
# plt.bar_label(stats_time_mean_seed_mean_ar)
addlabels(bar_place, stats_time_mean_seed_mean_ar)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.ylabel("Wait time [s]")
plt.savefig(
    fig_dir + "case042_waittime_mean_10x10_p023_saqa_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


print(stats_time_mean_seed_mean_ar)


# %%
stats_0 = np.zeros((len(dirs_0), 3600))
stats_1 = np.zeros((len(dirs_1), 3600))
stats_2 = np.zeros((len(dirs_2), 3600))
# stats_3 = np.zeros((len(dirs_2), 3600))

for k, dg in enumerate(dirs_0):
    dir_name_0 = "/case042/p023/" + dg + "/w00000"
    # dir_name_0 = '/case042/p023/' + dg + '/t00'
    # print(dir_name_0)
    stats_0[k, :] = read_stats_raw(dir_name_0)[4]
    print(stats_0)

for k, dg in enumerate(dirs_1):
    # dir_name_1 = '/case042/p023/' + dg + '/w00000'
    dir_name_1 = "/case042/p023/" + dg + "/w00000"
    # print(dir_name_1)
    stats_1[k, :] = read_stats_raw(dir_name_1)[4]
    print(stats_1)

for k, dl in enumerate(dirs_2):
    # dir_name_2 = '/case042/p023/' + dl + '/w00000'
    dir_name_2 = "/case042/p023/" + dl + "/w00000"
    stats_2[k, :] = read_stats_raw(dir_name_2)[4]
    print(stats_2)

# for k, dl in enumerate(dirs_3):
#     # dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     dir_name_3 = '/case042/p023/' + dl + '/w00000'
#     stats_3[k, :] = read_stats_raw(dir_name_3)[2]
#     print(stats_3)


# plt.plot(np.mean(stats_0, axis=0), label="sa",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_1, axis=0), label="qa",
#          color=cm.tab10(1/10), alpha=0.8)
# plt.plot(np.mean(stats_2, axis=0), label="hb-1",
#          color=cm.tab10(2/10), alpha=0.8)
# plt.plot(np.mean(stats_3, axis=0), label="hb-2",
#          color=cm.tab10(3/10), alpha=0.8)
# plt.grid(color='gray', linestyle='dotted', linewidth=0.5)
# plt.legend()
# plt.xlabel("time [s]")
# plt.ylabel("Waiting vehicle ratio")
# # plt.savefig(fig_dir+"vmean_10x10_p023_saqa_seed_mean"+savefig_type,
# plt.savefig(fig_dir+"waitrate_10x10_p023_qasa_seed_mean"+savefig_type,
#             bbox_inches='tight', dpi=300)


# %%

stats_0_time_mean = np.mean(stats_0, axis=0)
stats_0_time_mean_seed_mean = np.mean(stats_0_time_mean)
stats_0_time_mean_seed_std = np.std(stats_0_time_mean)

stats_1_time_mean = np.mean(stats_1, axis=0)
stats_1_time_mean_seed_mean = np.mean(stats_1_time_mean)
stats_1_time_mean_seed_std = np.std(stats_1_time_mean)

stats_2_time_mean = np.mean(stats_2, axis=0)
stats_2_time_mean_seed_mean = np.mean(stats_2_time_mean)
stats_2_time_mean_seed_std = np.std(stats_2_time_mean)

# stats_3_time_mean = np.mean(stats_3, axis=0)
# stats_3_time_mean_seed_mean = np.mean(stats_3_time_mean)
# stats_3_time_mean_seed_std = np.std(stats_3_time_mean)

stats_time_mean_seed_mean_ar = [
    stats_0_time_mean_seed_mean,
    stats_1_time_mean_seed_mean,
    stats_2_time_mean_seed_mean,
    # stats_3_time_mean_seed_mean
]

stats_time_mean_seed_std_ar = [
    stats_0_time_mean_seed_std / len(dirs_0),
    stats_1_time_mean_seed_std / len(dirs_1),
    stats_2_time_mean_seed_std / len(dirs_2),
    # stats_3_time_mean_seed_std/len(dirs_3)
]


plt.bar(
    bar_place,
    stats_time_mean_seed_mean_ar,
    yerr=stats_time_mean_seed_std_ar,
    tick_label=dir_name,
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
# plt.bar_label(stats_time_mean_seed_mean_ar)
addlabels(bar_place, stats_time_mean_seed_mean_ar)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
# plt.ylabel("Hamiltonian")
plt.ylabel("Sum of squared vehicle bias")
plt.savefig(
    fig_dir + "case042_hamiltonian_mean_10x10_p023_saqa_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

print(stats_time_mean_seed_mean_ar)
print(stats_time_mean_seed_std_ar)


# %%

stats_0 = np.zeros((len(dirs_0), 3600))
stats_1 = np.zeros((len(dirs_1), 3600))
stats_2 = np.zeros((len(dirs_2), 3600))
# stats_3 = np.zeros((len(dirs_2), 3600))

for k, dg in enumerate(dirs_0):
    dir_name_0 = "/case042/p023/" + dg + "/w00000"
    # dir_name_0 = '/case042/p023/' + dg + '/t00'
    # print(dir_name_0)
    stats_0[k, :] = read_stats_raw(dir_name_0)[5]
    print(stats_0)

for k, dg in enumerate(dirs_1):
    # dir_name_1 = '/case042/p023/' + dg + '/w00000'
    dir_name_1 = "/case042/p023/" + dg + "/w00000"
    # print(dir_name_1)
    stats_1[k, :] = read_stats_raw(dir_name_1)[5]
    print(stats_1)

for k, dl in enumerate(dirs_2):
    # dir_name_2 = '/case042/p023/' + dl + '/w00000'
    dir_name_2 = "/case042/p023/" + dl + "/w00000"
    stats_2[k, :] = read_stats_raw(dir_name_2)[5]
    print(stats_2)

stats_0_time_mean = np.mean(stats_0, axis=0)
stats_0_time_mean_seed_mean = np.mean(stats_0_time_mean)
stats_0_time_mean_seed_std = np.std(stats_0_time_mean)

stats_1_time_mean = np.mean(stats_1, axis=0)
stats_1_time_mean_seed_mean = np.mean(stats_1_time_mean)
stats_1_time_mean_seed_std = np.std(stats_1_time_mean)

stats_2_time_mean = np.mean(stats_2, axis=0)
stats_2_time_mean_seed_mean = np.mean(stats_2_time_mean)
stats_2_time_mean_seed_std = np.std(stats_2_time_mean)


stats_time_mean_seed_mean_ar = [
    stats_0_time_mean_seed_mean,
    stats_1_time_mean_seed_mean,
    stats_2_time_mean_seed_mean,
]

stats_time_mean_seed_std_ar = [
    stats_0_time_mean_seed_std / len(dirs_0),
    stats_1_time_mean_seed_std / len(dirs_1),
    stats_2_time_mean_seed_std / len(dirs_2),
]


plt.bar(
    bar_place,
    stats_time_mean_seed_mean_ar,
    yerr=stats_time_mean_seed_std_ar,
    tick_label=dir_name,
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
# plt.bar_label(stats_time_mean_seed_mean_ar)
addlabels(bar_place, stats_time_mean_seed_mean_ar)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.ylabel("Elapsed time [s]")
plt.savefig(
    fig_dir + "case042_elapsedtime_mean_10x10_p023_saqa_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

print(stats_time_mean_seed_mean_ar)
print(stats_time_mean_seed_std_ar)
# %%
