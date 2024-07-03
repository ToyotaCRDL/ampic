# AMPIC: Adaptive Model Predictive Ising Controller

This repository implements AMPIC, a method for controlling traffic signals by solving Ising problems, on the traffic simulator SUMO (Simulation of Urban MObility).

## Usage

Run `main.py.`
```
python main.py
```

### Option

| command                 | default                | description                                                                                                                            |
| ----------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `--nogui`               | False                  | run the commandline version of sumo                                                                                                    |
| `--input`, `-i`         | sq                     | input file prefix                                                                                                                      |
| `--path`, `-p`          | `.`                    | input data path                                                                                                                        |
| `--controller`, `-c`    | 4                      | 1:random, 2:pattern, 3:local, 4:global, 5:log                                                                                          |
| `--solver`, `-v`        | dwave_sa               | strings designating sampler dwave_sa, dwave_qa, dwave_hb, dwave_greedy, amplify_sa, amplify_gurobi, brute_force, or ignore_interaction |
| `--numreads`            | 1000                   | numreads parameter for d-wave sampler                                                                                                  |
| `--tls`                 | traffic_lights_log.csv | input traffic lights data                                                                                                              |
| `--threshold`, `-t`     | 0.1                    | threshold for local controller                                                                                                         |
| `--horizon`, `-r`       | 1                      | horizon for global_mpc controller                                                                                                      |
| `--step-interval`, `-s` | 10                     | step interval (in unit s) for traffic signal changes                                                                                   |
| `--nored`               | False                  | use only green for traffic light                                                                                                       |
| `--secs-red`            | 3                      | length (in unit s) for red traffic light                                                                                               |
| `--secs-yellow`         | 3                      | length (in unit s) for yellow traffic light                                                                                            |
| `--step-end`, `-e`      | 3600                   | total time steps                                                                                                                       |
| `--weight`, `-w`        | 0                      | input weight in hamiltonian                                                                                                            |
| `--weight_mode`, `-q`   | fixed                  | state weight in hamiltonian. (fixed / linear / quad)                                                                                   |
| `--freq`,               | 0.5                    | switching frequency in rondom & pattern controller                                                                                     |
| `--seed`                | 1395                   | random seed                                                                                                                            |


## Citation

If you find our paper or this code useful or relevant to your work please consider citing us.

```
D. Inoue, H. Yamashita, K. Aihara, and H. Yoshida, “AMPIC: Adaptive Model Predictive Ising Controller for large-scale urban traffic signals.” arXiv, Jun. 05, 2024. doi: 10.48550/arXiv.2406.03690.
```

In bibtex format:

```
@misc{ampic,
Author = {Daisuke Inoue and Hiroshi Yamashita and Kazuyuki Aihara and Hiroaki Yoshida},
Title = {AMPIC: Adaptive Model Predictive Ising Controller for large-scale urban traffic signals},
Year = {2024},
Eprint = {arXiv:2406.03690},
}
```

## License


This project is licensed under the [GPL2](https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html).