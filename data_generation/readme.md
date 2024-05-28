# ファイル

`make X.sumocfg` とするとすべての処理が行われ、共通の名前(以下、Xとする)で以下の拡張子を持ったファイルを生成する。

- `X.sumocfg`
    - 最終的に sumo コマンドに引数として渡されるファイルで、net ファイルと rou ファイルを指定する。
    - `src/tmp.sumocfg` からテンプレートを読み込み、`make_sumocfg.py` によって名前の置換を行うことで生成される。

- `X.rou.xml`
    - sumo 用のファイルで、trip のルートと発時刻を指定する。
    - ネットワークファイル (`X.net.xml`) を読み込み、duarouter を用いて生成される。
        - `--weights.random-factor` の値 `RANDOMFACTOR` と、
        - シミュレーション時間 `ETIME` が指定できる。
        - トリップの起終点は `X.trips.xml` で指定される。

- `X.trips.xml`
    - duarouter 用のファイルで、tripの起終点と発時刻を記したファイル。
    - `to_xml.py` で生成される。

- `X.net.xml`
    - sumo 用のネットワークファイルで、信号のパターンを簡略化したもの。
        - パターン0,1
            - 片方青(G)、片方赤(r)
        - パターン2
            - 全赤(r)
        - パターン3
            - 片方黄(y)、片方赤(r)
    - `X.tmp.net.xml` と `X.priority_3way.yaml` を読み込み、`fix_tlLogic.py`で生成される。

- `X.tmp.net.xml`
    - 以下の二つを読み込み、netconvert コマンドによって生成される。
        - `X.nod.xml`
        - `X.edg.xml`
    - sumo が読み込める形式になっているが、信号のパターンが自動生成になっている。

- `X.priority_3way.yaml`
    - 3差路の制御用に辺の優先度を記したファイル
    - to_xml.py で生成される。

- `X.nod.xml`
    - netconvert 用に頂点情報を記したファイル
    - to_xml.py で生成される。
- `X.edg.xml`
    - netconvert 用に辺情報を記したファイル
    - to_xml.py で生成される。

- `X.input.parsed`
    - makefile 用のファイルで、実際には生成されない。

## 不要なファイル

- `tripinfo.xml`
    - sumo に`--tripinfo-output`オプションを付けることで生成される。
    - `The simulation is forced to generate this output using the option --tripinfo-output <FILE> on the command line/within a configuration. This output contains the information about each vehicle's departure time, the time the vehicle wanted to start at (which may be lower than the real departure time) and the time the vehicle has arrived. ` (https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html)

- `X.rou.alt.xml`
    - duarouter で生成される。本実験では使わない。
    - `Additionally a .rou.alt.xml with the same name prefix as the .rou.xml file will be generated. This route alternative file holds a routeDistribution for every vehicle. Such a routeDistribution is used during dynamic user assignment (DUA) but can also be loaded directly into sumo.` (https://sumo.dlr.de/docs/duarouter.html)


# プログラム

- `fix_tlLogic.py`
    - 以下の2つを読み込む。
        - `X.tmp.net.xml` 
        - `X.priority_3way.yaml`
    - 信号のパターンを生成する。
    
- `make_sumocfg.py`
  - `src/tmp.sumocfg` からテンプレートを読み込み、ファイル名をXに置換したものを生成する。

- `to_xml.py`
    - 設定ファイル `X.network.xml` を読み込んで、ネットワークを構築し、以下のファイルを生成する
        - `X.nod.xml`
            - `X.tmp.net.xml` の生成に用いられる
        - `X.edg.xml`
            - `X.tmp.net.xml` の生成に用いられる
        - `X.priority_3way.yaml`
            - `X.net.xml`の生成 に用いられる
        - `X.trips.xml`
            - ルートファイル `X.rou.xml` の生成に用いられる

# X.network.xml のフォーマット

`X.network.xml` の書き方は `kyoto.network.xml` を真似してください。

```
make AAA.sumocfg PERIOD=0.5
```

と実行すると、車が生成される頻度を変えることができます。

----

`<map scale="200">` はグリッドサイズが200mであることを示します。
`<map>` 内の `<row>` がグリッドの各行に対応します。
data の文字列は"."または"x"からなり、"x"があるところに交差点があります。

`<nodes>` 内に、`<map>` に現れる "x"の順番に`<node>`を記述します。
id が交差点名を表します。
offsetX, offsetY を指定することでグリッド上の点から位置をずらせます。

`<lines>`内に路線を記述します。`<line>` が各路線に対応していて、
路線上の交差点を順に`<node>`として記述します。idが交差点名になります。
`<line>` の id が路線名です。路線ごとに別の名前を指定します。

----

三叉路がある場合、同じ路線名の辺が相互に通行できるように信号のstateを生成します。

たとえば 三叉路 y に路線A, Bが 

```
x - A - y - A - z
        |
        B
        |
        w
```

のようにつながっていた場合、
- state 0: x->y:青, z->y:青, w->z:赤
- state 1: x->y:赤, z->y:赤, w->z:青

となります。
