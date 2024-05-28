from __future__ import absolute_import, print_function

import csv
import random
import sys

import numpy as np
import pandas as pd
import traci  # noqa
from sumolib import checkBinary  # noqa

from .controller import global_controller
from .network import traffic_network
from .network_values import network_values
from .statistics import statistics

#########################################################
# interface to traci(sumo)
#########################################################


def setPhase_all(netw, ph):
    for id in netw.tlsid:
        if id in ph:
            traci.trafficlight.setPhase(id, str(ph[id]))


def getPhase_all(netw):
    ph = {}
    for id in netw.tlsid:
        ph[id] = traci.trafficlight.getPhase(id)
    return ph


#########################################################
# set phases of traffic lights
#########################################################


def set_green(netw, tr):
    ph = {}
    for id, p01 in tr.items():
        p0, p1 = p01
        ph[id] = p1
    setPhase_all(netw, ph)


def set_red(netw, tr):
    ph = {}
    for id, p01 in tr.items():
        p0, p1 = p01
        if p0 == p1:
            ph[id] = p1
        else:
            ph[id] = 2
    setPhase_all(netw, ph)


def set_yellow(netw, tr):
    ph = {}
    for id, p01 in tr.items():
        p0, p1 = p01
        if p0 == p1:
            ph[id] = p1
        else:
            ph[id] = p0 + 3
    setPhase_all(netw, ph)


def set_next_transition(netw, ph_prev, ph_next):
    tr = {}
    ph = {}
    for id in netw.tlsid:
        p0 = ph_prev[id]
        if id in ph_next:
            p1 = ph_next[id]
        else:
            p1 = p0
        tr[id] = (p0, p1)
        ph[id] = p1
    return ph, tr


#########################################################
# controllers
#########################################################


#########################################################
# interface to global_controller
#########################################################
def get_x_array(netw, xVal):
    x = np.empty(netw.L)
    for i, node in enumerate(netw.nodid):
        id = str(node)
        x[i] = xVal[id]
    return x


def get_sigma_array(netw, tls):
    sigma = np.empty(netw.L)
    for i, node in enumerate(netw.nodid):
        id = str(node)
        if id in tls:
            sigma[i] = -int(2 * int(tls[id]) - 1)
        else:
            sigma[i] = 1
    return sigma


def computeHamiltonian(gcon, netw_v, weight, tlsprev, tlsnow):
    x_ = get_x_array(gcon.netw, netw_v.xVal)
    sigma = get_sigma_array(gcon.netw, tlsnow)
    sigma_ = get_sigma_array(gcon.netw, tlsprev)
    hamiltonian, xsquared, sigmasquared = gcon.get_hamiltonian(
        x_, sigma, sigma_, weight
    )
    return hamiltonian, xsquared, sigmasquared


#########################################################
# random control with param
#########################################################
def randomControlParam(netw, tlsprev, freq):
    sigma_prev = get_sigma_array(netw, tlsprev)
    rand_array = np.random.rand(netw.L)
    sigma = np.array(
        [
            sigma_prev[i] if rand_array[i] > freq else -sigma_prev[i]
            for i in range(netw.L)
        ]
    )

    ph = {}
    for i, node in enumerate(netw.nodid):
        ph[str(node)] = int((-sigma[i] + 1) / 2)
    return ph


#########################################################
# pattern control
#########################################################
def patternControl(netw, tlsprev, freq, count):
    sigma_prev = get_sigma_array(netw, tlsprev)

    if freq == 0:
        sigma = sigma_prev
    else:
        N = int(1 / freq)
        if count % N == 0:
            count = 1
            sigma = -np.array(sigma_prev)
        else:
            count = count + 1
            sigma = sigma_prev

    ph = {}
    for i, node in enumerate(netw.nodid):
        ph[str(node)] = int((-sigma[i] + 1) / 2)
    return ph, count


#########################################################
# local control
#########################################################


def localControl(netw, xVal, carThreshold):
    ph = {}
    for id in netw.tlsid:
        if xVal[id] > carThreshold:
            ph[id] = 0
        if xVal[id] < -carThreshold:
            ph[id] = 1
    return ph


#########################################################
# global control
#########################################################


def globalControl(gcon, netw_v, tlsprev, weight, weight_mode, h):
    gcon.set_parameters(netw_v.a_0, netw_v.a_1, netw_v.o_g_global)
    x_ = get_x_array(gcon.netw, netw_v.xVal)
    sigma_ = get_sigma_array(gcon.netw, tlsprev)
    # assert (h == 1)
    if h == 1:
        sigma = gcon.global_control(x_, sigma_, weight, weight_mode)
    else:
        sigma = gcon.global_control_horizon(x_, sigma_, weight, weight_mode, horizon=h)

    ph = {}
    for i, node in enumerate(gcon.netw.nodid):
        ph[str(node)] = int((-sigma[i] + 1) / 2)
        # ph[str(node)] = str(int((-sigma[i]+1)/2))
    return ph


#########################################################
# log control
#########################################################


def logControl(df_tls_log, step):
    ph = dict(df_tls_log.loc[step])
    return ph


class simulator:
    def __init__(self, **kwargs):
        # Prefix of network data
        self.networkData = kwargs["input"]
        # Data path
        self.dataPath = kwargs.get("path", "")

        # input files
        self.sumoCfg = self.dataPath + self.networkData + ".sumocfg"
        self.input_fname_xml = self.dataPath + self.networkData + ".net.xml"
        self.input_fname_route = self.dataPath + self.networkData + ".rou.xml"

        self.input_fname_tls_log = kwargs["tls"]

        # output files
        self.fname_value = kwargs.get("fname_value", "values.dat")
        self.fname_tls = kwargs.get("output_fname_tls", "traffic_lights.dat")
        self.fname_tls_csv = kwargs.get(
            "output_fname_tls_csv", "traffic_lights_log.csv"
        )

        # Minimum interval between signal changes (unit s, integer)
        self.stepInterval = kwargs["step_interval"]

        self.secs_yellow = kwargs.get("secs_yellow", 3)
        self.secs_red = kwargs.get("secs_red", 3)
        self.nored = kwargs.get("nored", False)

        if not self.nored:
            assert self.secs_yellow + self.secs_red < self.stepInterval

        # simulation steps (unit s, integer)
        self.stepFinish = kwargs["step_end"]

        # threshold for local control
        self.carThreshold = kwargs["threshold"]

        # parameter for global control (dimensionless)
        #  (weight of cost for frequent sigal changes)
        self.weight = kwargs["weight"]
        self.weight_mode = kwargs["weight_mode"]

        # reference density of cars (# of cars par m)
        self.densityRef = kwargs.get("densityRef", 0.05)

        # reference speed of cars (in m/s)
        self.speedRef = kwargs.get("speedRef", 12)

        # reference number of cars (# of cars)
        self.numRef = self.densityRef * self.speedRef * self.stepInterval

        # reference length (m)
        self.lenRef = self.speedRef * self.stepInterval

        self.freq = kwargs["freq"]
        self.count = 1

        self.seed = kwargs["seed"]

        self.controller = kwargs["controller"]
        self.horizon = kwargs["horizon"]
        self.solver = kwargs["solver"]
        self.numreads = kwargs["numreads"]

        # if self.controller == "4" and self.horizon > 1:
        #     print("multiple horizon. step interval is ", self.stepInterval)
        #     self.stepInterval = int(self.stepInterval / self.horizon)

        if kwargs["nogui"]:
            self.sumoBinary = checkBinary("sumo")
        else:
            self.sumoBinary = checkBinary("sumo-gui")

    #########################################################
    # display
    #########################################################

    def display_global_message(self, m):
        traci.poi.setParameter("global", "text", str(m))

    def display_tls_values(self, d):
        for id in d:
            i = self.netw.nodid.index(id)
            traci.poi.setParameter("tls_" + id, "text", f"[{i}]" + str(d[id]))

    def display_edge_values(self, d):
        _d = {}

        for e in d:
            u, v = e
            i, j = self.netw.nodid.index(u), self.netw.nodid.index(v)
            if u > v:
                w = u
                u = v
                v = w
            s = _d.get((u, v), "")
            if s != "":
                s += "\n"
            _d[(u, v)] = s + f"({i}, {j})\n" + str(d[e])

        for e in _d:
            u, v = e
            traci.poi.setParameter(f"edge_{u}_{v}", "text", _d[e])

    def display_network_values(self, gcon, netw, netw_v, tlsprev):
        self.display_global_message(
            f"rate: {netw_v.rate_global:.3f}={netw_v.sum_exit}/{netw_v.green_count}"
        )

        gcon.set_parameters(netw_v.a_0, netw_v.a_1, netw_v.o_g_global)
        x_ = get_x_array(netw, netw_v.xVal)
        sigma_ = get_sigma_array(netw, tlsprev)
        gcon.build_ising(x_, sigma_, self.weight, self.weight_mode)

        d_tls = {}
        for i, id in enumerate(netw.nodid):
            x = netw_v.xVal[id]
            h = gcon.ising_h[i]
            s = tlsprev[id]
            d_tls[id] = "\n".join([f"state: {s}", f"x: {x:.5f}", f"h: {h:.5f}"])

        d_edge = {}
        for i, e in enumerate(netw.G.edges):
            u, v = e
            # eid = netw.G.edges[u, v]["id"]
            # c = netw_v.exit_count.get(eid, 0)
            i, j = self.netw.nodid.index(u), self.netw.nodid.index(v)
            Aji = gcon.A[j, i]
            Jji = gcon.ising_J[j, i]

            # o = netw_v.o_g[j, i]
            # on = netw_v.on_g[j, i]
            # os = o * on
            # rate = c / (on + 1e-10)
            a_0 = netw_v.a_0[j, i]
            a_1 = netw_v.a_1[j, i]
            state = netw.G.edges[u, v]["state"]

            # lane = eid + "_0"
            # l = traci.lane.getLength(lane)
            # rate_normalized = (
            #     rate / netw_v.numRef / (l / netw_v.lenRef) * netw_v.stepInterval
            # )
            # rate_global_normalized = (
            #     netw_v.rate_global
            #     / netw_v.numRef
            #     / (l / netw_v.lenRef)
            #     * netw_v.stepInterval
            # )

            d_edge[e] = "\n".join(
                [
                    f"state: {state}",
                    # f"{o:.3f}={os:.3f}/{on}",
                    f"a: {a_0:.3f}, {a_1: .3f}",
                    # f"a_0: {a_0:.3f}",
                    # f"a_1: {a_1:.3f}",
                    # f"exit: {c}\nrate: {rate:.3f}",
                    # f"rate_n: {rate_normalized:.3f}",
                    # f"rate_gn: {rate_global_normalized:.3f}",
                    f"A: {Aji:.5f}" f"J: {Jji:.5f}",
                ]
            )
            # d_edge[e] = f"rate={rate:.2f}={c}/{on}"

        self.display_tls_values(d_tls)
        self.display_edge_values(d_edge)

    #########################################################
    # run
    #########################################################

    def run(self):
        ########################################
        # Initialization
        ########################################

        random.seed(self.seed)
        np.random.seed(self.seed)

        traci.start(
            [
                self.sumoBinary,
                "-c",
                self.sumoCfg,
                "--tripinfo-output",
                "tripinfo.xml",
                "--statistic-output",
                "statistic.xml",
                "-g",
                self.dataPath + "view_HY_0402.xml",
                "--seed",
                str(self.seed),
            ]
        )

        ########################################
        # network and statistics
        ########################################

        netw = traffic_network(self.input_fname_xml)
        self.netw = netw
        L = netw.L

        netw_v = network_values(
            netw,
            L,
            float(self.stepInterval),
            self.numRef,
            self.lenRef,
            self.input_fname_route,
        )
        stat = statistics()

        ########################################
        # display
        ########################################

        traci.poi.add("global", -10, -10, color=(255, 0, 0))
        for id in netw.nodid:
            x, y = netw.pos[id]
            traci.poi.add("tls_" + id, x + 10, y + 10, color=(255, 0, 0))
        for u, v in netw.G.edges:
            if u < v:
                xu, yu = netw.pos[u]
                xv, yv = netw.pos[v]
                print(u, v, xu, xv, yu, yv)
                traci.poi.add(
                    f"edge_{u}_{v}",
                    (xu + xv) / 2 + 10,
                    (yu + yv) / 2 + 10,
                    color=(255, 0, 0),
                )

        ########################################
        # controller
        ########################################

        controller_name = {
            "1": "random",
            "2": "pattern",
            "3": "local",
            "4": "global",
            "5": "log",
        }[self.controller]

        oc = self.controller
        if oc == "1":
            print("random control")
        elif oc == "2":
            print("pattern control")
        elif oc == "3":
            print("local control")
        elif oc == "4":
            print("global control")
        elif oc == "5":
            print("log control")

        gcon = global_controller(netw, self.solver, self.numreads)

        if oc == "5":
            with open(self.input_fname_tls_log, "r") as f:
                self.df_tls_log = pd.read_csv(f, header=0, index_col=0)
                self.df_tls_log.columns = netw.tlsid

        ########################################
        # output headers
        ########################################

        header = (
            "controller="
            + controller_name
            + " horizon="
            + str(self.horizon)
            + " threshold="
            + str(self.carThreshold)
            + "\n"
        )
        stat.init_file(self.fname_value, header=header)

        with open(self.fname_tls, "w") as fl:
            fl.write(
                "step interval="
                + str(self.stepInterval)
                + " number of tls="
                + str(len(netw.tlsid))
                + "\n"
            )
        with open(self.fname_tls_csv, "w", newline="") as fl:
            writer = csv.writer(fl)
            writer.writerow([""] + [tls for tls in netw.tlsid])

        ########################################
        # Main iteration
        ########################################
        step = 0

        ph_init = {id: 0 for id in netw.tlsid}
        self.prev_ph = ph_init
        self.current_ph = ph_init
        _, self.current_transition = set_next_transition(netw, ph_init, self.current_ph)

        while traci.simulation.getMinExpectedNumber() > 0:
            ########################################
            # simulate one step
            ########################################

            traci.simulationStep()

            ########################################
            # transition of traffic lights
            ########################################
            sec_in_phase = step % self.stepInterval

            phase = "green"
            if not self.nored:
                if sec_in_phase < self.secs_yellow:
                    phase = "yellow"
                elif sec_in_phase < (self.secs_yellow + self.secs_red):
                    phase = "red"
                else:
                    phase = "green"

            if phase == "yellow":
                set_yellow(netw, self.current_transition)
            elif phase == "red":
                set_red(netw, self.current_transition)
            elif phase == "green":
                set_green(netw, self.current_transition)
            else:
                raise ValueError

            ########################################
            # collect statistics and display
            ########################################

            netw_v.reset_xVal()
            netw_v.update_Xvalue()

            if phase == "yellow":
                netw_v.update_Avalue(self.prev_ph)
            elif phase == "red":
                netw_v.update_Avalue(self.prev_ph)
            elif phase == "green":
                netw_v.update_Avalue(self.current_ph)
            else:
                raise ValueError

            self.display_network_values(gcon, netw, netw_v, self.current_ph)

            stat.increase()

            ########################################
            # control traffic signals
            ########################################
            if sec_in_phase == 0:
                ########################################
                # update controller
                ########################################
                gcon.set_parameters(netw_v.a_0, netw_v.a_1, netw_v.o_g_global)

                ########################################
                # set transition states
                ########################################
                # oc = self.controller
                if oc == "1":
                    ph = randomControlParam(netw, self.current_ph, float(self.freq))
                elif oc == "2":
                    ph, self.count = patternControl(
                        netw, self.current_ph, float(self.freq), self.count
                    )
                elif oc == "3":
                    ph = localControl(netw, netw_v.xVal, self.carThreshold)
                elif oc == "4":
                    horizon = int(self.horizon)
                    ph = globalControl(
                        gcon,
                        netw_v,
                        self.current_ph,
                        self.weight,
                        self.weight_mode,
                        horizon,
                    )
                elif oc == "5":
                    ph = logControl(self.df_tls_log, step)

                ph, self.current_transition = set_next_transition(
                    netw, self.current_ph, ph
                )

                ########################################
                # store tls status
                ########################################

                tls = [ph[id] for id in netw.tlsid]

                ########################################
                # collect statistics and output
                ########################################

                with open(self.fname_tls, "a", newline="") as fl:
                    writer = csv.writer(fl)
                    writer.writerow(tls)
                with open(self.fname_tls_csv, "a", newline="") as fl:
                    writer = csv.writer(fl)
                    writer.writerow([step] + tls)

                # hamiltonian, xsquared, sigmasquared = computeHamiltonian(
                #     gcon, netw_v, self.weight, self.current_ph, ph)
                # stat.store(hamiltonian, xsquared, sigmasquared)
                # stat.append_to_file(self.fname_value, step)
                netw_v.reset_xVal()
                # stat.reset()

                ########################################
                # store sigma
                ########################################

                self.prev_ph = self.current_ph
                self.current_ph = ph

                ########################################
                # set transition states
                ########################################
                if self.nored:
                    set_green(netw, self.current_transition)
                else:
                    set_yellow(netw, self.current_transition)

            ########################################
            # increase time step and break
            ########################################

            hamiltonian, xsquared, sigmasquared = computeHamiltonian(
                gcon, netw_v, self.weight, self.prev_ph, self.current_ph
            )
            stat.store(hamiltonian, xsquared, sigmasquared)
            stat.append_to_file(self.fname_value, step)
            stat.reset()
            step += 1
            if step >= self.stepFinish:
                break

        ########################################
        # finalize
        ########################################
        traci.close()
        sys.stdout.flush()
