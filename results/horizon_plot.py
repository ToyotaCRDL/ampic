# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import xml.etree.ElementTree as ET

fig_dir = os.getcwd() + "/figs/"
plt.rcParams["font.size"] = 14
savefig_type = ".pdf"
# savefig_type = ".png"
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

# horizon_ar = [1, 2, 4, 6]
horizon_ar = [1, 2, 4, 6, 8, 10]
seed_ar = [1, 2, 3, 4, 5]

# seed_ar = [1, 2, 3, 4]

mean_velocity_ar = np.zeros((len(horizon_ar), len(seed_ar), 3600))
wait_rate_ar = np.zeros((len(horizon_ar), len(seed_ar), 3600))
wait_time_ar = np.zeros((len(horizon_ar), len(seed_ar)))
hamiltonian_ar = np.zeros((len(horizon_ar), len(seed_ar), 3600))
co2_ar = np.zeros((len(horizon_ar), len(seed_ar), 3600))


dir_name = "/case009/p023/gc_s7_horizon"


local_mean_velocity_ar = np.zeros((len(seed_ar), 3600))
local_dir_name = "/case009/p023/lc_s7"

# %%

for s, seed in enumerate(seed_ar):
    for h, horizon in enumerate(horizon_ar):
        dir = dir_name + str(horizon_ar[h]) + "_seed" + str(seed_ar[s]) + "/w00000"
        print(dir)
        mean_velocity_ar[h, s:] = read_stats_raw(dir)[0]
        wait_rate_ar[h, s, :] = read_stats_raw(dir)[2]
        wait_time_ar[h, s] = read_stats_raw(dir)[3]
        hamiltonian_ar[h, s, :] = read_stats_raw(dir)[4]
        co2_ar[h, s, :] = read_stats_raw(dir)[5]


for s, seed in enumerate(seed_ar):
    dir = local_dir_name + "_seed" + str(seed_ar[s]) + "/w00000"
    print(dir)
    local_mean_velocity_ar[s:] = read_stats_raw(dir)[0]


# %%
mean_velocity_mean_time = np.mean(mean_velocity_ar, axis=2)
mean_velocity_mean_time_mean_seed = np.mean(mean_velocity_mean_time, axis=1)
mean_velocity_mean_time_std_seed = np.std(mean_velocity_mean_time, axis=1)

wait_rate_mean_time = np.mean(wait_rate_ar, axis=2)
wait_rate_mean_time_mean_seed = np.mean(wait_rate_mean_time, axis=1)
wait_rate_mean_time_std_seed = np.std(wait_rate_mean_time, axis=1)

wait_time_mean_seed = np.mean(wait_time_ar, axis=1)
wait_time_std_seed = np.std(wait_time_ar, axis=1)

hamiltonian_mean_time = np.mean(hamiltonian_ar, axis=2)
hamiltonian_mean_time_mean_seed = np.mean(hamiltonian_mean_time, axis=1)
hamiltonian_mean_time_std_seed = np.std(hamiltonian_mean_time, axis=1)

co2_mean_time = np.mean(co2_ar, axis=2)
co2_mean_time_mean_seed = np.mean(co2_mean_time, axis=1)
co2_mean_time_std_seed = np.std(co2_mean_time, axis=1)

local_mean_velocity_mean_time = np.mean(local_mean_velocity_ar, axis=1)
local_mean_velocity_mean_time_mean_seed = np.mean(local_mean_velocity_mean_time)


# %%
plt.figure()
plt.errorbar(
    horizon_ar,
    co2_mean_time_mean_seed,
    yerr=co2_mean_time_std_seed / np.sqrt(len(seed_ar)),
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
# plt.scatter(1, local_co2_mean_time_mean_seed)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Prediction horizon")
plt.ylabel("CO2 emission [kg/s]")
plt.savefig(
    fig_dir + "co2_mean_seed_10x10_p023_interval7_sweep_horizon" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)


# %%
plt.figure()
plt.errorbar(
    horizon_ar,
    mean_velocity_mean_time_mean_seed,
    yerr=mean_velocity_mean_time_std_seed / np.sqrt(len(seed_ar)),
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
# plt.scatter(1, local_mean_velocity_mean_time_mean_seed)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Prediction horizon")
plt.ylabel("Mean velocity [m/s]")
plt.savefig(
    fig_dir
    + "mean_velocity_mean_seed_10x10_p023_interval7_sweep_horizon"
    + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

# %%
plt.figure()
plt.errorbar(
    horizon_ar,
    wait_rate_mean_time_mean_seed,
    yerr=wait_rate_mean_time_std_seed / np.sqrt(len(seed_ar)),
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Prediction horizon")
plt.ylabel("Waiting vehicle ratio")
plt.savefig(
    fig_dir + "wait_rate_mean_seed_10x10_p023_interval7_sweep_horizon" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

# %%
plt.figure()
plt.errorbar(
    horizon_ar,
    wait_time_mean_seed,
    yerr=wait_time_std_seed / np.sqrt(len(seed_ar)),
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Prediction horizon")
plt.ylabel("Wait time [s]")
plt.savefig(
    fig_dir + "wait_time_mean_seed_10x10_p023_interval7_sweep_horizon" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)
# %%
plt.figure()
plt.errorbar(
    horizon_ar,
    hamiltonian_mean_time_mean_seed,
    yerr=hamiltonian_mean_time_std_seed / np.sqrt(len(seed_ar)),
    color=cm.tab10(0 / 10),
    alpha=0.8,
)
plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
plt.legend()
plt.xlabel("Prediction horizon")
plt.ylabel("Sum of squared vehicle bias")
plt.savefig(
    fig_dir + "hamiltonian_mean_seed_10x10_p023_interval7_sweep_horizon" + savefig_type,
    bbox_inches="tight",
    dpi=300,
)

# %%
