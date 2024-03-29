# %%
import os
import xml.etree.ElementTree as ET

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.size"] = 14

savefig_type = ".png"
savefig_type = ".pdf"

fig_dir = os.getcwd() + "/figs/"
casename5 = "case033"
casename6 = "case034"
casename7 = "case035"
casename8 = "case036"
casename9 = "case037"
casename10 = "case038"
casename15 = "case039"
casename20 = "case040"
casename25 = "case041"


# %%
def read_stats(dir_name):
    fn1 = os.getcwd() + dir_name
    fn2 = "/values.dat"
    fn3 = "/statistic.xml"
    df_values = pd.read_csv(fn1 + fn2, skiprows=2, header=None)

    cutoff_time = 500
    # cutoff_time = 1500

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

dirs_p = [
    "p005",
    "p01",
    "p015",
    "p02",
    "p025",
    "p03",
    "p0325",
    "p035",
    "p0375",
    "p04",
    "p0425",
    "p045",
    "p0475",
    "p05",
    "p06",
    "p07",
    "p08",
]
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

vals_p = [
    0.05,
    0.1,
    0.15,
    0.2,
    0.25,
    0.3,
    0.325,
    0.35,
    0.375,
    0.4,
    0.425,
    0.45,
    0.475,
    0.5,
    0.6,
    0.7,
    0.8,
]
vals_l = np.array([0.0])
vals_g = np.array([0.0])

# case_list = [casename5,casename10,casename15,casename20,casename25]
case_list = [
    casename5,
    casename6,
    casename7,
    casename8,
    casename9,
    casename10,
    casename15,
    casename20,
    casename25,
]

size_list = [
    "5x5",
    "6x6",
    "7x7",
    "8x8",
    "9x9",
    "10x10",
    "15x15",
    "20x20",
    "25x25",
]

size_list_num = [5, 6, 7, 8, 9, 10, 15, 20, 25]

stats_g = np.zeros((len(case_list), len(dirs_p), len(dirs_gw), len(dirs_g), 6))

stats_l = np.zeros((len(case_list), len(dirs_p), len(dirs_lw), len(dirs_l), 6))

# %%
for c, casename_ in enumerate(case_list):
    for i, dp in enumerate(dirs_p):
        for j, dgw in enumerate(dirs_gw):
            for k, dg in enumerate(dirs_g):
                dir_name_g = "/" + casename_ + "/" + dp + "/" + dg + "/" + dgw
                # print(dir_name_g)
                stats_g[c, i, j, k, :] = read_stats(dir_name_g)
                print(stats_g[c, i, j, k, :])

        for j, dlw in enumerate(dirs_lw):
            for k, dl in enumerate(dirs_l):
                dir_name_l = "/" + casename_ + "/" + dp + "/" + dl + "/" + dlw
                stats_l[c, i, j, k, :] = read_stats(dir_name_l)
                print(stats_l[c, i, j, k, :])


# %%
stats_g_sm = np.mean(stats_g, axis=3)
stats_l_sm = np.mean(stats_l, axis=3)
stats_g_ss = np.std(stats_g, axis=3)
stats_l_ss = np.std(stats_l, axis=3)

# %%
figname = "global_various_N_reg"

# %%

plt.figure()
plt.plot(size_list_num,np.mean(stats_g_sm[:, 0:5, 0, 2], axis=1).flatten()/np.mean(stats_l_sm[:, 0:5, 0, 2], axis=1).flatten())
plt.xlabel("Network size")
plt.ylabel("Relative waiting vehicle ratio")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.savefig(fig_dir + figname + casename_ + "waterate_gl.png", bbox_inches="tight", dpi=300
)

# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.errorbar(
        vals_p,
        stats_g_sm[j, :, 0, 5],
        label=c,
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_g_ss[j, :, 0, 5],
    )
    plt.errorbar(
        vals_p,
        stats_l_sm[j, :, 0, 5],
        label="",
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_l_ss[j, :, 0, 5],
        linestyle="dashdot",
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("CO2 emission [kg/s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "co2" + savefig_type, bbox_inches="tight", dpi=300
)


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.errorbar(
        vals_p,
        stats_g_sm[j, :, 0, 5] / size_list_num[j],
        label=c,
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_g_ss[j, :, 0, 5] / size_list_num[j],
    )
    plt.errorbar(
        vals_p,
        stats_l_sm[j, :, 0, 5] / size_list_num[j],
        label="",
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_l_ss[j, :, 0, 5] / size_list_num[j],
        linestyle="dashdot",
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Scaled CO2 emission [kg/s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "co2-s" + savefig_type, bbox_inches="tight", dpi=300
)


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.errorbar(
        vals_p,
        stats_g_sm[j, :, 0, 5] / size_list_num[j] ** 2,
        label=c,
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_g_ss[j, :, 0, 5] / size_list_num[j] ** 2,
    )
    plt.errorbar(
        vals_p,
        stats_l_sm[j, :, 0, 5] / size_list_num[j] ** 2,
        label="",
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_l_ss[j, :, 0, 5] / size_list_num[j] ** 2,
        linestyle="dashdot",
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Scaled CO2 emission [kg/s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "co2-s2" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%

plt.figure()
for j, c in enumerate(size_list):
    plt.errorbar(
        vals_p,
        stats_g_sm[j, :, 0, 0],
        label=c,
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_g_ss[j, :, 0, 0],
    )
    plt.errorbar(
        vals_p,
        stats_l_sm[j, :, 0, 0],
        label="",
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_l_ss[j, :, 0, 0],
        linestyle="dashdot",
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Mean velocity [m/s]")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "vmean" + savefig_type, bbox_inches="tight", dpi=300
)


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.errorbar(
        vals_p,
        stats_g_sm[j, :, 0, 2],
        label=c,
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_g_ss[j, :, 0, 2],
    )
    plt.errorbar(
        vals_p,
        stats_l_sm[j, :, 0, 2],
        label="",
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_l_ss[j, :, 0, 2],
        linestyle="dashdot",
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Waiting vehicle ratio")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "waitrate" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.errorbar(
        vals_p,
        stats_g_sm[j, :, 0, 4],
        label=c,
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_g_ss[j, :, 0, 4],
    )
    plt.errorbar(
        vals_p,
        stats_l_sm[j, :, 0, 4],
        label="",
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        yerr=stats_l_ss[j, :, 0, 4],
        linestyle="dashdot",
    )
plt.xlabel("Scaled vehicle generation rate")
# plt.ylabel("Hamiltonian")
plt.ylabel("Sum of squared vehicle bias")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "hamiltonian" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
stats_rel = stats_g / stats_l
stats_rel_seedmean = np.mean(stats_rel, axis=3)
stats_rel_seedstd = np.std(stats_rel, axis=3)

stats_rel_seed_p_mean = np.mean(stats_rel, axis=(3, 1))
stats_rel_seed_p_std = np.std(stats_rel, axis=(3, 1))


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.plot(
        vals_p,
        stats_rel_seedmean[j, :, 0, 5],
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        label=c,
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Relative CO2 emission")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "co2_comp" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.plot(
        vals_p,
        stats_rel_seedmean[j, :, 0, 0],
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        label=c,
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Relative mean velocity")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "vmean_comp" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%


plt.figure()
for j, c in enumerate(size_list):
    plt.plot(
        vals_p,
        stats_rel_seedmean[j, :, 0, 2],
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        label=c,
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Relative waiting vehicle ratio")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "waitrate_comp" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
plt.figure()
for j, c in enumerate(size_list):
    plt.plot(
        vals_p,
        stats_rel_seedmean[j, :, 0, 4],
        color=cm.viridis(j / len(size_list)),
        alpha=0.7,
        label=c,
    )
plt.xlabel("Scaled vehicle generation rate")
plt.ylabel("Relative sum of squared vehicle bias")
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.savefig(
    fig_dir + figname + casename_ + "hamiltonian_comp" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

