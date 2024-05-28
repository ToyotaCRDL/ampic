from __future__ import absolute_import, print_function

import optparse

from ising_traffic_simulator import simulator

#########################################################
# get options
#########################################################


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option(
        "--nogui",
        action="store_true",
        default=False,
        help="run the commandline version of sumo",
    )
    optParser.add_option(
        "--input", "-i", default="sq", help="input file prefix (default:square)"
    )
    optParser.add_option(
        "--path", "-p", default=".", help="input data path (default: .)"
    )
    optParser.add_option(
        "--controller",
        "-c",
        default="4",
        help="1:random, 2:pattern, 3:local, 4:global, 5log",
    )
    optParser.add_option(
        "--solver",
        "-v",
        default="dwave_sa",
        help="strings designating sampler dwave_sa, dwave_qa, dwave_hb, dwave_greedy, amplify_sa, amplify_gurobi, brute_force, or ignore_interaction (default=dwave_sa)",
    )
    optParser.add_option(
        "--numreads", default="1000", help="numreads for dwave sampler (default=1000)"
    )
    optParser.add_option(
        "--tls",
        default="traffic_lights_log.csv",
        help="input traffic lights data (default: traffic_lights_log.csv)",
    )
    optParser.add_option(
        "--threshold",
        "-t",
        default="0.1",
        help="threshold for local controller (default=0.1)",
    )
    optParser.add_option(
        "--horizon",
        "-r",
        default="1",
        help="horizon for global_mpc controller (default=1)",
    )
    optParser.add_option(
        "--step-interval",
        "-s",
        default="10",
        help="step interval (in unit s) for traffic signal changes (default=10)",
    )
    optParser.add_option(
        "--nored",
        action="store_true",
        default=False,
        help="use only green for traffic light",
    )
    optParser.add_option(
        "--secs-red",
        default="3",
        help="length (in unit s) for red traffic light (default=3)",
    )
    optParser.add_option(
        "--secs-yellow",
        default="3",
        help="length (in unit s) for yellow traffic light (default=3)",
    )

    optParser.add_option(
        "--step-end",
        "-e",
        default="3600",
        help="total time steps (in unit s) (default=3600)",
    )
    optParser.add_option(
        "--weight", "-w", default="0", help="input weight in hamiltonian (default=0)"
    )
    optParser.add_option(
        "--weight_mode",
        "-q",
        default="fixed",
        help="state weight in hamiltonian fixed, linear, quad (default=fixed)",
    )
    optParser.add_option(
        "--freq",
        default="0.5",
        help="switching frequency in controller 7 and 8 (default=0.5)",
    )
    optParser.add_option("--seed", default="1395", help="random seed (default=1395)")
    options, args = optParser.parse_args()
    return options


#########################################################
# Main
#########################################################
if __name__ == "__main__":
    options = get_options()

    kwargs = {
        "input": options.input,
        "path": options.path + "/",
        "step_interval": int(options.step_interval),
        "step_end": int(options.step_end),
        "threshold": float(options.threshold),
        "weight": float(options.weight),
        "weight_mode": options.weight_mode,
        "seed": int(options.seed),
        "controller": options.controller,
        "solver": options.solver,
        "numreads": int(options.numreads),
        "horizon": int(options.horizon),
        "nogui": options.nogui,
        "freq": options.freq,
        "tls": options.tls,
        "nored": options.nored,
        "secs_yellow": int(options.secs_yellow),
        "secs_red": int(options.secs_red),
    }
    print(kwargs)

    sml = simulator(**kwargs)
    sml.run()
