# IsingTrafficSimulator

## Usage


例：
``` 
python main.py --nogui -i sq -p data_generation -c 4
```


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


- `-v`でソルバーを`amplify_sa`にする場合、`amplify.conf`と名前のつけられたファイルをプロジェクト直下に置いてください。
  - 中身は下記のようにしてください
  ```amplify.conf
  url: http://url/
  token: XXXXXXXXXXXXXXXXXXXXXXX
  # proxy: ""
  proxy: http://user:password@proxy:port
  ```


- `random`と`pattern`で指定する切り替え頻度`--freq`は、0:完全に固定して切り替えない、1:毎回切り替える、で頻度を調整するパラメータです。

- `--controller`オプションを整理しました。注意してください。
  - `random`と`random with param`を`random`に統一しました。
  - `global`, `global new`, `global_mpc`を`global`に統一しました。
  - `global`を選んだ場合、`horizon`, `weight`, `weight_mode`を指定できます。
    `weight_mode`で`linear`を選んだ場合、評価関数の$x^2$の項が$x^\top Q x$に変更されます。
    $Q$は、交差点ごとの流量の総和が並べられた対角行列です。   
    流量が多い交差点の流れが優先的に平滑化されると期待されます。
  - `weight_mode`で`quad`を選んだ場合、流量が2乗された量で$Q$を作成します。


## 統計量のプロット

- `plot_case01.ipynb`を動かすためには、下記のようなディレクトリ構成が必要。
  1. `sweep_weight.sh`を実行すると、でweightを変えていった時のシミュレーション結果が得られる。
  2. `plot_case01.ipynb`を順番に実行すると、統計量をプロットできる。

```
.
├── case001
│   ├── ave.sh
│   ├── ave_all.sh
│   └── p_default
│       ├── ave.sh
│       ├── ave_all.sh
│       ├── weight_fixed
│       │   ├── sweep_weight.sh
│       │   ├── w00000
├── plot_case01.ipynb
└── traffic-signal-control
    ├── amplify.conf
    ├── data_generation
    │   ├── hsq.network.xml
    │   ├── hsq.trips.xml
    │   ├── kyoto.network.xml
    │   ├── lad.network.xml
    │   ├── makefile
    │   ├── readme.txt
    │   ├── sq.edg.xml
    │   ├── sq.net.xml
    │   ├── sq.network.xml
    │   ├── sq.nod.xml
    │   ├── sq.priority_3way.yaml
    │   ├── sq.rou.alt.xml
    │   ├── sq.rou.xml
    │   ├── sq.sumocfg
    │   ├── sq.tmp.net.xml
    │   ├── sq.trips.xml
    │   ├── src
    │   │   ├── fix_tlLogic.py
    │   │   ├── generate_route.py
    │   │   ├── make_sumocfg.py
    │   │   ├── parser_HY.py
    │   │   ├── tmp.sumocfg
    │   │   ├── tmp.sumocfg.xml
    │   │   └── to_xml.py
    │   ├── tripinfo.xml
    │   ├── view_HY.xml
    ├── ising_traffic_simulator
    │   ├── controller.py
    │   ├── network.py
    │   ├── network_values.py
    │   ├── parser.py
    │   ├── simulator.py
    │   └── statistics.py
    ├── main.py
    ├── readme.md
```