# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import xml.etree.ElementTree as ET

savefig_type = ".png"
savefig_type = ".pdf"

fig_dir = os.getcwd() + "/figs/"
casename = "case046"


# %%


def read_stats_raw(dir_name):
    fn1 = os.getcwd() + dir_name
    fn2 = "/values.dat"
    fn3 = "/statistic.xml"
    df_values = pd.read_csv(fn1 + fn2, skiprows=2, header=None)

    vmean = df_values[3]
    sigterm = df_values[6]
    waitrate = df_values[7]
    co2 = df_values[8]
    hamiltonian = df_values[4]

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
        np.array(co2),
    )


# %%
dirs_g = [
    "gc_s60_seed1",
    "gc_s60_seed2",
    "gc_s60_seed3",
    "gc_s60_seed4",
    "gc_s60_seed5",
]
dirs_l = [
    "lc_s60_seed1",
    "lc_s60_seed2",
    "lc_s60_seed3",
    "lc_s60_seed4",
    "lc_s60_seed5",
]
dirs_r = ["rand_seed1", "rand_seed2", "rand_seed3", "rand_seed4", "rand_seed5"]
dirs_p = [
    "pattern_seed1",
    "pattern_seed2",
    "pattern_seed3",
    "pattern_seed4",
    "pattern_seed5",
]
dirs_p2 = [
    "pattern2_seed1",
    "pattern2_seed2",
    "pattern2_seed3",
    "pattern2_seed4",
    "pattern2_seed5",
]
# dirs_g = ['gc_s60_seed1', 'gc_s60_seed2']
# dirs_l = ['lc_s60_seed1', 'lc_s60_seed2']

p_name = "p045"


# %%
stats_g = np.zeros((len(dirs_g), 3600))
stats_l = np.zeros((len(dirs_l), 3600))
stats_r = np.zeros((len(dirs_r), 3600))
stats_p = np.zeros((len(dirs_p), 3600))
stats_p2 = np.zeros((len(dirs_p), 3600))

for k, dg in enumerate(dirs_g):
    dir_name_g = "/case046/" + p_name + "/" + dg + "/w00000"
    # print(dir_name_g)
    stats_g[k, :] = read_stats_raw(dir_name_g)[5]
    print(stats_g)

for k, dl in enumerate(dirs_l):
    dir_name_l = "/case046/" + p_name + "/" + dl + "/t00"
    stats_l[k, :] = read_stats_raw(dir_name_l)[5]
    print(stats_l)

for k, dl in enumerate(dirs_r):
    dir_name_r = "/case046/" + p_name + "/" + dl + "/f05"
    stats_r[k, :] = read_stats_raw(dir_name_r)[5]
    print(stats_r)

for k, dl in enumerate(dirs_p):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p[k, :] = read_stats_raw(dir_name_p)[5]
    print(stats_p)

for k, dl in enumerate(dirs_p2):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p2[k, :] = read_stats_raw(dir_name_p)[5]
    print(stats_p2)


vmean_g_60 = np.convolve(np.mean(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vmean_l_60 = np.convolve(np.mean(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vmean_r_60 = np.convolve(np.mean(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vmean_p_60 = np.convolve(np.mean(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vmean_p2_60 = np.convolve(np.mean(stats_p2, axis=0), np.ones(120) / 120, mode="valid")

vstd_g_60 = np.convolve(np.std(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vstd_l_60 = np.convolve(np.std(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vstd_r_60 = np.convolve(np.std(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vstd_p_60 = np.convolve(np.std(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vstd_p2_60 = np.convolve(np.std(stats_p2, axis=0), np.ones(120) / 120, mode="valid")


x_range = np.arange(0, 3481)
# x_range = np.arange(1, 3600)
plt.plot(vmean_g_60, label="AMPIC", color=cm.tab10(0 / 10), alpha=0.8)
plt.fill_between(
    x_range,
    vmean_g_60 + vstd_g_60,
    vmean_g_60 - vstd_g_60,
    color=cm.tab10(0 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_l_60, label="local", color=cm.tab10(1 / 10), alpha=0.8, linestyle="dashdot"
)
plt.fill_between(
    x_range,
    vmean_l_60 + vstd_l_60,
    vmean_l_60 - vstd_l_60,
    color=cm.tab10(1 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_r_60, label="random", color=cm.tab10(2 / 10), alpha=0.8, linestyle="dotted"
)
plt.fill_between(
    x_range,
    vmean_r_60 + vstd_r_60,
    vmean_r_60 - vstd_r_60,
    color=cm.tab10(2 / 10),
    alpha=0.2,
)
# plt.plot(
#     vmean_p_60, label="pattern", color=cm.tab10(3 / 10), alpha=0.8, linestyle="dashed"
# )
# plt.fill_between(
#     x_range,
#     vmean_p_60 + vstd_p_60,
#     vmean_p_60 - vstd_p_60,
#     color=cm.tab10(3 / 10),
#     alpha=0.2,
# )
plt.plot(
    vmean_p2_60,
    # label="pattern 2",
    label="pattern",
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.8,
    linestyle="dashed",
)
plt.fill_between(
    x_range,
    vmean_p2_60 + vstd_p2_60,
    vmean_p2_60 - vstd_p2_60,
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.2,
)
# plt.plot(np.mean(stats_g, axis=0), label="global mean",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_l, axis=0), label="local mean",
#          color=cm.tab10(1/10), alpha=0.8)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("CO2 emission [kg/s]")
# plt.savefig(fig_dir+"vmean_sapporo_p012_seed_mean" + savefig_type,
plt.savefig(
    fig_dir + casename + p_name + "CO2_sapporo_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
stats_g = np.zeros((len(dirs_g), 3600))
stats_l = np.zeros((len(dirs_l), 3600))
stats_r = np.zeros((len(dirs_r), 3600))
stats_p = np.zeros((len(dirs_p), 3600))
stats_p2 = np.zeros((len(dirs_p), 3600))

for k, dg in enumerate(dirs_g):
    dir_name_g = "/case046/" + p_name + "/" + dg + "/w00000"
    # print(dir_name_g)
    stats_g[k, :] = read_stats_raw(dir_name_g)[0]
    print(stats_g)

for k, dl in enumerate(dirs_l):
    dir_name_l = "/case046/" + p_name + "/" + dl + "/t00"
    stats_l[k, :] = read_stats_raw(dir_name_l)[0]
    print(stats_l)

for k, dl in enumerate(dirs_r):
    dir_name_r = "/case046/" + p_name + "/" + dl + "/f05"
    stats_r[k, :] = read_stats_raw(dir_name_r)[0]
    print(stats_r)

for k, dl in enumerate(dirs_p):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p[k, :] = read_stats_raw(dir_name_p)[0]
    print(stats_p)

for k, dl in enumerate(dirs_p2):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p2[k, :] = read_stats_raw(dir_name_p)[0]
    print(stats_p2)


vmean_g_60 = np.convolve(np.mean(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vmean_l_60 = np.convolve(np.mean(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vmean_r_60 = np.convolve(np.mean(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vmean_p_60 = np.convolve(np.mean(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vmean_p2_60 = np.convolve(np.mean(stats_p2, axis=0), np.ones(120) / 120, mode="valid")

vstd_g_60 = np.convolve(np.std(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vstd_l_60 = np.convolve(np.std(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vstd_r_60 = np.convolve(np.std(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vstd_p_60 = np.convolve(np.std(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vstd_p2_60 = np.convolve(np.std(stats_p2, axis=0), np.ones(120) / 120, mode="valid")


x_range = np.arange(0, 3481)
# x_range = np.arange(1, 3600)
plt.plot(vmean_g_60, label="AMPIC", color=cm.tab10(0 / 10), alpha=0.8)
plt.fill_between(
    x_range,
    vmean_g_60 + vstd_g_60,
    vmean_g_60 - vstd_g_60,
    color=cm.tab10(0 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_l_60, label="local", color=cm.tab10(1 / 10), alpha=0.8, linestyle="dashdot"
)
plt.fill_between(
    x_range,
    vmean_l_60 + vstd_l_60,
    vmean_l_60 - vstd_l_60,
    color=cm.tab10(1 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_r_60, label="random", color=cm.tab10(2 / 10), alpha=0.8, linestyle="dotted"
)
plt.fill_between(
    x_range,
    vmean_r_60 + vstd_r_60,
    vmean_r_60 - vstd_r_60,
    color=cm.tab10(2 / 10),
    alpha=0.2,
)
# plt.plot(
#     vmean_p_60, label="pattern", color=cm.tab10(3 / 10), alpha=0.8, linestyle="dashed"
# )
# plt.fill_between(
#     x_range,
#     vmean_p_60 + vstd_p_60,
#     vmean_p_60 - vstd_p_60,
#     color=cm.tab10(3 / 10),
#     alpha=0.2,
# )
# plt.plot(
#     vmean_p2_60,
#     label="pattern 2",
#     color=cm.tab10(4 / 10),
#     alpha=0.8,
#     linestyle="dashed",
# )
# plt.fill_between(
#     x_range,
#     vmean_p2_60 + vstd_p2_60,
#     vmean_p2_60 - vstd_p2_60,
#     color=cm.tab10(4 / 10),
#     alpha=0.2,
# )
plt.plot(
    vmean_p2_60,
    # label="pattern 2",
    label="pattern",
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.8,
    linestyle="dashed",
)
plt.fill_between(
    x_range,
    vmean_p2_60 + vstd_p2_60,
    vmean_p2_60 - vstd_p2_60,
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.2,
)
# plt.plot(np.mean(stats_g, axis=0), label="global mean",
#          color=cm.tab10(0/10), alpha=0.8)
# plt.plot(np.mean(stats_l, axis=0), label="local mean",
#          color=cm.tab10(1/10), alpha=0.8)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Mean velocity [m/s]")
# plt.savefig(fig_dir+"vmean_sapporo_p012_seed_mean" + savefig_type,
plt.savefig(
    fig_dir + casename + p_name + "vmean_sapporo_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
stats_g = np.zeros((len(dirs_g), 3600))
stats_l = np.zeros((len(dirs_l), 3600))
stats_r = np.zeros((len(dirs_r), 3600))
stats_p = np.zeros((len(dirs_p), 3600))
stats_p2 = np.zeros((len(dirs_p2), 3600))

for k, dg in enumerate(dirs_g):
    dir_name_g = "/case046/" + p_name + "/" + dg + "/w00000"
    # print(dir_name_g)
    stats_g[k, :] = read_stats_raw(dir_name_g)[2]
    print(stats_g)

for k, dl in enumerate(dirs_l):
    dir_name_l = "/case046/" + p_name + "/" + dl + "/t00"
    stats_l[k, :] = read_stats_raw(dir_name_l)[2]
    print(stats_l)

for k, dl in enumerate(dirs_r):
    dir_name_r = "/case046/" + p_name + "/" + dl + "/f05"
    stats_r[k, :] = read_stats_raw(dir_name_r)[2]
    print(stats_r)

for k, dl in enumerate(dirs_p):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p[k, :] = read_stats_raw(dir_name_p)[2]
    print(stats_p)

for k, dl in enumerate(dirs_p2):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p2[k, :] = read_stats_raw(dir_name_p)[2]
    print(stats_p2)


vmean_g_60 = np.convolve(np.mean(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vmean_l_60 = np.convolve(np.mean(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vmean_r_60 = np.convolve(np.mean(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vmean_p_60 = np.convolve(np.mean(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vmean_p2_60 = np.convolve(np.mean(stats_p2, axis=0), np.ones(120) / 120, mode="valid")


vstd_g_60 = np.convolve(np.std(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vstd_l_60 = np.convolve(np.std(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vstd_r_60 = np.convolve(np.std(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vstd_p_60 = np.convolve(np.std(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vstd_p2_60 = np.convolve(np.std(stats_p2, axis=0), np.ones(120) / 120, mode="valid")


x_range = np.arange(0, 3481)
# x_range = np.arange(1, 3600)
plt.plot(vmean_g_60, label="AMPIC", color=cm.tab10(0 / 10), alpha=0.8)
plt.fill_between(
    x_range,
    vmean_g_60 + vstd_g_60,
    vmean_g_60 - vstd_g_60,
    color=cm.tab10(0 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_l_60, label="local", color=cm.tab10(1 / 10), alpha=0.8, linestyle="dashdot"
)
plt.fill_between(
    x_range,
    vmean_l_60 + vstd_l_60,
    vmean_l_60 - vstd_l_60,
    color=cm.tab10(1 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_r_60, label="random", color=cm.tab10(2 / 10), alpha=0.8, linestyle="dotted"
)
plt.fill_between(
    x_range,
    vmean_r_60 + vstd_r_60,
    vmean_r_60 - vstd_r_60,
    color=cm.tab10(2 / 10),
    alpha=0.2,
)
# plt.plot(
#     vmean_p_60, label="pattern", color=cm.tab10(3 / 10), alpha=0.8, linestyle="dashed"
# )
# plt.fill_between(
#     x_range,
#     vmean_p_60 + vstd_p_60,
#     vmean_p_60 - vstd_p_60,
#     color=cm.tab10(3 / 10),
#     alpha=0.2,
# )
# plt.plot(
#     vmean_p2_60,
#     label="pattern 2",
#     color=cm.tab10(4 / 10),
#     alpha=0.8,
#     linestyle="dashed",
# )
# plt.fill_between(
#     x_range,
#     vmean_p2_60 + vstd_p2_60,
#     vmean_p2_60 - vstd_p2_60,
#     color=cm.tab10(4 / 10),
#     alpha=0.2,
# )
plt.plot(
    vmean_p2_60,
    # label="pattern 2",
    label="pattern",
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.8,
    linestyle="dashed",
)
plt.fill_between(
    x_range,
    vmean_p2_60 + vstd_p2_60,
    vmean_p2_60 - vstd_p2_60,
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.2,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Waiting vehicle ratio")
# plt.savefig(fig_dir+"vmean_sapporo_p012_seed_mean" + savefig_type,
plt.savefig(
    fig_dir + casename + p_name + "waitrate_sapporo_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
stats_g = np.zeros((len(dirs_g), 3600))
stats_l = np.zeros((len(dirs_l), 3600))
stats_r = np.zeros((len(dirs_r), 3600))
stats_p = np.zeros((len(dirs_p), 3600))
stats_p2 = np.zeros((len(dirs_p2), 3600))

for k, dg in enumerate(dirs_g):
    dir_name_g = "/case046/" + p_name + "/" + dg + "/w00000"
    # print(dir_name_g)
    stats_g[k, :] = read_stats_raw(dir_name_g)[4]
    print(stats_g)

for k, dl in enumerate(dirs_l):
    dir_name_l = "/case046/" + p_name + "/" + dl + "/t00"
    stats_l[k, :] = read_stats_raw(dir_name_l)[4]
    print(stats_l)

for k, dl in enumerate(dirs_r):
    dir_name_r = "/case046/" + p_name + "/" + dl + "/f05"
    stats_r[k, :] = read_stats_raw(dir_name_r)[4]
    print(stats_r)

for k, dl in enumerate(dirs_p):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p[k, :] = read_stats_raw(dir_name_p)[4]
    print(stats_p)

for k, dl in enumerate(dirs_p2):
    dir_name_p = "/case046/" + p_name + "/" + dl + "/f09"
    stats_p2[k, :] = read_stats_raw(dir_name_p)[4]
    print(stats_p2)

vmean_g_60 = np.convolve(np.mean(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vmean_l_60 = np.convolve(np.mean(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vmean_r_60 = np.convolve(np.mean(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vmean_p_60 = np.convolve(np.mean(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vmean_p2_60 = np.convolve(np.mean(stats_p2, axis=0), np.ones(120) / 120, mode="valid")


vstd_g_60 = np.convolve(np.std(stats_g, axis=0), np.ones(120) / 120, mode="valid")
vstd_l_60 = np.convolve(np.std(stats_l, axis=0), np.ones(120) / 120, mode="valid")
vstd_r_60 = np.convolve(np.std(stats_r, axis=0), np.ones(120) / 120, mode="valid")
vstd_p_60 = np.convolve(np.std(stats_p, axis=0), np.ones(120) / 120, mode="valid")
vstd_p2_60 = np.convolve(np.std(stats_p2, axis=0), np.ones(120) / 120, mode="valid")


x_range = np.arange(0, 3481)
# x_range = np.arange(1, 3600)
plt.plot(vmean_g_60, label="AMPIC", color=cm.tab10(0 / 10), alpha=0.8)
plt.fill_between(
    x_range,
    vmean_g_60 + vstd_g_60,
    vmean_g_60 - vstd_g_60,
    color=cm.tab10(0 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_l_60, label="local", color=cm.tab10(1 / 10), alpha=0.8, linestyle="dashdot"
)
plt.fill_between(
    x_range,
    vmean_l_60 + vstd_l_60,
    vmean_l_60 - vstd_l_60,
    color=cm.tab10(1 / 10),
    alpha=0.2,
)
plt.plot(
    vmean_r_60, label="random", color=cm.tab10(2 / 10), alpha=0.8, linestyle="dotted"
)
plt.fill_between(
    x_range,
    vmean_r_60 + vstd_r_60,
    vmean_r_60 - vstd_r_60,
    color=cm.tab10(2 / 10),
    alpha=0.2,
)
# plt.plot(
#     vmean_p_60, label="pattern", color=cm.tab10(3 / 10), alpha=0.8, linestyle="dashed"
# )
# plt.fill_between(
#     x_range,
#     vmean_p_60 + vstd_p_60,
#     vmean_p_60 - vstd_p_60,
#     color=cm.tab10(3 / 10),
#     alpha=0.2,
# )
# plt.plot(
#     vmean_p2_60,
#     label="pattern 2",
#     color=cm.tab10(4 / 10),
#     alpha=0.8,
#     linestyle="dashed",
# )
# plt.fill_between(
#     x_range,
#     vmean_p2_60 + vstd_p2_60,
#     vmean_p2_60 - vstd_p2_60,
#     color=cm.tab10(3 / 10),
#     alpha=0.2,
# )
plt.plot(
    vmean_p2_60,
    # label="pattern 2",
    label="pattern",
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.8,
    linestyle="dashed",
)
plt.fill_between(
    x_range,
    vmean_p2_60 + vstd_p2_60,
    vmean_p2_60 - vstd_p2_60,
    color=cm.tab10(3 / 10),
    # color=cm.tab10(4 / 10),
    alpha=0.2,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Time [s]")
# plt.ylabel("Hamiltonian")
plt.ylabel("Sum of squared vehicle bias")
# plt.savefig(fig_dir+"vmean_sapporo_p012_seed_mean" + savefig_type,
plt.savefig(
    fig_dir + casename + p_name + "hamiltonian_sapporo_seed_mean" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%


def read_stats(dir_name):
    fn1 = os.getcwd() + dir_name
    fn2 = "/values.dat"
    fn3 = "/statistic.xml"
    df_values = pd.read_csv(fn1 + fn2, skiprows=2, header=None)

    cutoff_time = 500
    cutoff_time = 1800
    # cutoff_time = 2000

    vmean = df_values[3]
    hamiltonian = df_values[4]
    sigterm = df_values[6]
    waitrate = df_values[7]
    co2 = df_values[8]
    vmean_mean = vmean[cutoff_time:-1].mean()
    hamiltonian_mean = hamiltonian[cutoff_time:-1].mean()
    sigterm_mean = sigterm[cutoff_time:-1].mean()
    waitrate_mean = waitrate[cutoff_time:-1].mean()
    co2_mean = co2[cutoff_time:-1].mean()

    tree = ET.ElementTree(file=fn1 + fn3)
    root = tree.getroot()
    vts = root.find("vehicleTripStatistics")
    waittime = float(vts.attrib["waitingTime"])

    return vmean_mean, sigterm_mean, waitrate_mean, waittime, hamiltonian_mean, co2_mean


# %%

# dirs_p = ['p012', 'p023', 'p034', 'p045', 'p056', 'p067', 'p078']
# vals_p = [0.12, 0.23, 0.34, 0.45, 0.56, 0.67, 0.78]

dirs_p = [
    "p012",
    "p023",
    "p025",
    "p028",
    "p031",
    "p034",
    "p037",
    "p041",
    "p045",
    "p056",
    "p067",
    "p078",
]

vals_p = [0.12, 0.23, 0.25, 0.28, 0.31, 0.34, 0.37, 0.41, 0.45, 0.56, 0.67, 0.78]

dirs_g = [
    "gc_s60_seed1",
    "gc_s60_seed2",
    "gc_s60_seed3",
    "gc_s60_seed4",
    "gc_s60_seed5",
]
dirs_gw = ["w00000"]
dirs_l = [
    "lc_s60_seed1",
    "lc_s60_seed2",
    "lc_s60_seed3",
    "lc_s60_seed4",
    "lc_s60_seed5",
]
dirs_lw = ["t00"]
dirs_r = ["rand_seed1", "rand_seed2", "rand_seed3", "rand_seed4", "rand_seed5"]
dirs_rw = ["f05"]
dirs_p_ = [
    "pattern_seed1",
    "pattern_seed2",
    "pattern_seed3",
    "pattern_seed4",
    "pattern_seed5",
]
dirs_pw = ["f09"]

dirs_p2 = [
    "pattern2_seed1",
    "pattern2_seed2",
    "pattern2_seed3",
    "pattern2_seed4",
    "pattern2_seed5",
]
dirs_p2w = ["f09"]


vals_l = np.array([0.0])
vals_g = np.array([0.0])

stats_g = np.zeros((len(dirs_p), len(dirs_gw), len(dirs_g), 6))
stats_l = np.zeros((len(dirs_p), len(dirs_lw), len(dirs_l), 6))
stats_r = np.zeros((len(dirs_p), len(dirs_rw), len(dirs_g), 6))
stats_p = np.zeros((len(dirs_p), len(dirs_pw), len(dirs_l), 6))
stats_p2 = np.zeros((len(dirs_p), len(dirs_pw), len(dirs_l), 6))

# %%
for i, dp in enumerate(dirs_p):
    for j, dgw in enumerate(dirs_gw):
        for k, dg in enumerate(dirs_g):
            dir_name_g = "/" + casename + "/" + dp + "/" + dg + "/" + dgw
            # print(dir_name_g)
            stats_g[i, j, k, :] = read_stats(dir_name_g)
            print(stats_g[i, j, k, :])

    for j, dlw in enumerate(dirs_lw):
        for k, dl in enumerate(dirs_l):
            dir_name_l = "/" + casename + "/" + dp + "/" + dl + "/" + dlw
            stats_l[i, j, k, :] = read_stats(dir_name_l)
            print(stats_l[i, j, k, :])

    for j, drw in enumerate(dirs_rw):
        for k, dr in enumerate(dirs_r):
            dir_name_r = "/" + casename + "/" + dp + "/" + dr + "/" + drw
            stats_r[i, j, k, :] = read_stats(dir_name_r)
            print(stats_r[i, j, k, :])

    for j, dpw in enumerate(dirs_pw):
        for k, dp_ in enumerate(dirs_p_):
            dir_name_p = "/" + casename + "/" + dp + "/" + dp_ + "/" + dpw
            stats_p[i, j, k, :] = read_stats(dir_name_p)
            print(stats_p[i, j, k, :])

    for j, dpw in enumerate(dirs_p2w):
        for k, dp_ in enumerate(dirs_p2):
            dir_name_p = "/" + casename + "/" + dp + "/" + dp_ + "/" + dpw
            stats_p2[i, j, k, :] = read_stats(dir_name_p)
            print(stats_p2[i, j, k, :])


# %%
stats_g_sm = np.mean(stats_g, axis=2)
stats_l_sm = np.mean(stats_l, axis=2)
stats_r_sm = np.mean(stats_r, axis=2)
stats_p_sm = np.mean(stats_p, axis=2)
stats_p2_sm = np.mean(stats_p2, axis=2)

stats_g_ss = np.std(stats_g, axis=2)
stats_l_ss = np.std(stats_l, axis=2)
stats_r_ss = np.std(stats_r, axis=2)
stats_p_ss = np.std(stats_p, axis=2)
stats_p2_ss = np.std(stats_p2, axis=2)

p_inv = [1 / p for p in vals_p]
figname = "global_sapporo_various_p"


# %%
plt.figure()
plt.errorbar(p_inv[1:], stats_g_sm[1:, 0, 5], label="AMPIC", yerr=stats_g_ss[1:, 0, 5])
plt.errorbar(
    p_inv[1:],
    stats_l_sm[1:, 0, 5],
    label="local",
    yerr=stats_l_ss[1:, 0, 5],
    linestyle="dashdot",
)
plt.errorbar(
    p_inv[1:],
    stats_r_sm[1:, 0, 5],
    label="random",
    yerr=stats_r_ss[1:, 0, 5],
    linestyle="dotted",
)
# plt.errorbar(
#     p_inv[1:],
#     stats_p_sm[1:, 0, 5],
#     label="pattern",
#     yerr=stats_p_ss[1:, 0, 5],
#     linestyle="dashed",
# )
# plt.errorbar(
#     p_inv[1:],
#     stats_p2_sm[1:, 0, 5],
#     label="pattern 2",
#     yerr=stats_p2_ss[1:, 0, 5],
#     linestyle="dashed",
# )
plt.errorbar(
    p_inv[1:],
    stats_p2_sm[1:, 0, 5],
    label="pattern",
    yerr=stats_p2_ss[1:, 0, 5],
    linestyle="dashed",
)
plt.xlabel("Vehicle generation rate")
plt.ylabel("CO2 emission [kg/s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename + "co2" + savefig_type, bbox_inches="tight", dpi=300
)


# %%
plt.figure()
plt.errorbar(p_inv[1:], stats_g_sm[1:, 0, 0], label="AMPIC", yerr=stats_g_ss[1:, 0, 0])
plt.errorbar(
    p_inv[1:],
    stats_l_sm[1:, 0, 0],
    label="local",
    yerr=stats_l_ss[1:, 0, 0],
    linestyle="dashdot",
)
plt.errorbar(
    p_inv[1:],
    stats_r_sm[1:, 0, 0],
    label="random",
    yerr=stats_r_ss[1:, 0, 0],
    linestyle="dotted",
)
# plt.errorbar(
#     p_inv[1:],
#     stats_p_sm[1:, 0, 0],
#     label="pattern",
#     yerr=stats_p_ss[1:, 0, 0],
#     linestyle="dashed",
# )
# plt.errorbar(
#     p_inv[1:],
#     stats_p2_sm[1:, 0, 0],
#     label="pattern 2",
#     yerr=stats_p2_ss[1:, 0, 0],
#     linestyle="dashed",
# )
plt.errorbar(
    p_inv[1:],
    stats_p2_sm[1:, 0, 0],
    label="pattern",
    yerr=stats_p2_ss[1:, 0, 0],
    linestyle="dashed",
)
# plt.plot(vals_p, stats_g_sm[:, 0, 0], label="AMPIC")
# plt.plot(vals_p, stats_l_sm[:, 0, 0], label="local")
# plt.title(figname)
# plt.xlabel("p values")
plt.xlabel("Vehicle generation rate")
plt.ylabel("Mean velocity [m/s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename + "vmean" + savefig_type, bbox_inches="tight", dpi=300
)

# %%
plt.figure()
plt.errorbar(p_inv[1:], stats_g_sm[1:, 0, 3], label="AMPIC", yerr=stats_g_ss[1:, 0, 3])
plt.errorbar(
    p_inv[1:],
    stats_l_sm[1:, 0, 3],
    label="local",
    yerr=stats_l_ss[1:, 0, 3],
    linestyle="dashdot",
)
plt.errorbar(
    p_inv[1:],
    stats_r_sm[1:, 0, 3],
    label="random",
    yerr=stats_r_ss[1:, 0, 3],
    linestyle="dotted",
)
# plt.errorbar(
#     p_inv[1:],
#     stats_p_sm[1:, 0, 3],
#     label="pattern",
#     yerr=stats_p_ss[1:, 0, 3],
#     linestyle="dashed",
# )
# plt.errorbar(
#     p_inv[1:],
#     stats_p2_sm[1:, 0, 3],
#     label="pattern 2",
#     yerr=stats_p2_ss[1:, 0, 3],
#     linestyle="dashed",
# )
plt.errorbar(
    p_inv[1:],
    stats_p2_sm[1:, 0, 3],
    label="pattern",
    yerr=stats_p2_ss[1:, 0, 3],
    linestyle="dashed",
)
# plt.plot(p_inv, stats_g_sm[:, 0, 3], label="AMPIC")
# plt.plot(p_inv, stats_l_sm[:, 0, 3], label="local")
# plt.title(figname)
# plt.xlabel("p values")
plt.xlabel("Vehicle generation rate")
plt.ylabel("Mean waiting time [s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename + "waittime" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
plt.figure()
plt.errorbar(p_inv[1:], stats_g_sm[1:, 0, 2], label="AMPIC", yerr=stats_g_ss[1:, 0, 2])
plt.errorbar(
    p_inv[1:],
    stats_l_sm[1:, 0, 2],
    label="local",
    yerr=stats_l_ss[1:, 0, 2],
    linestyle="dashdot",
)
plt.errorbar(
    p_inv[1:],
    stats_r_sm[1:, 0, 2],
    label="random",
    yerr=stats_r_ss[1:, 0, 2],
    linestyle="dotted",
)
# plt.errorbar(
#     p_inv[1:],
#     stats_p_sm[1:, 0, 2],
#     label="pattern",
#     yerr=stats_p_ss[1:, 0, 2],
#     linestyle="dashed",
# )
# plt.errorbar(
#     p_inv[1:],
#     stats_p2_sm[1:, 0, 2],
#     label="pattern 2",
#     yerr=stats_p2_ss[1:, 0, 2],
#     linestyle="dashed",
# )

plt.errorbar(
    p_inv[1:],
    stats_p2_sm[1:, 0, 2],
    label="pattern",
    yerr=stats_p2_ss[1:, 0, 2],
    linestyle="dashed",
)
# plt.plot(p_inv, stats_g_sm[:, 0, 2], label="AMPIC")
# plt.plot(p_inv, stats_l_sm[:, 0, 2], label="local")
# plt.title(figname)
# plt.xlabel("p values")
plt.xlabel("Vehicle generation rate")
plt.ylabel("Waiting vehicle ratio")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename + "waitrate" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
plt.figure()
plt.errorbar(p_inv[1:], stats_g_sm[1:, 0, 4], label="AMPIC", yerr=stats_g_ss[1:, 0, 4])
plt.errorbar(
    p_inv[1:],
    stats_l_sm[1:, 0, 4],
    label="local",
    yerr=stats_l_ss[1:, 0, 4],
    linestyle="dashdot",
)
plt.errorbar(
    p_inv[1:],
    stats_r_sm[1:, 0, 4],
    label="random",
    yerr=stats_r_ss[1:, 0, 4],
    linestyle="dotted",
)
# plt.errorbar(
#     p_inv[1:],
#     stats_p_sm[1:, 0, 4],
#     label="pattern",
#     yerr=stats_p_ss[1:, 0, 4],
#     linestyle="dashed",
# )
# plt.errorbar(
#     p_inv[1:],
#     stats_p2_sm[1:, 0, 4],
#     label="pattern 2",
#     yerr=stats_p2_ss[1:, 0, 4],
#     linestyle="dashed",
# )
plt.errorbar(
    p_inv[1:],
    stats_p2_sm[1:, 0, 4],
    label="pattern",
    yerr=stats_p2_ss[1:, 0, 4],
    linestyle="dashed",
)
# plt.title(figname)
# plt.xlabel("p values")
plt.xlabel("Vehicle generation rate")
# plt.ylabel("Hamiltonian")
plt.ylabel("Sum of squared vehicle bias")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename + "hamiltonian" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

# %%
