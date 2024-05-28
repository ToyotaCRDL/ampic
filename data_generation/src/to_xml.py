from absl import app, flags
import xml.etree.ElementTree as ET
import pickle as pk
import yaml
import sys
import networkx as nx
import numpy as np

import contextlib
nax = np.newaxis

FLAGS = flags.FLAGS

flags.DEFINE_string('prefix', "tokyo",
                    'prefix of input and output file names', short_name="o")
flags.DEFINE_float('endtime', 7200,
                   'end time', short_name="e")
flags.DEFINE_float('period', 0.7,
                   'Generate vehicles at regular intervals of a given length', short_name="p")
flags.DEFINE_integer('seed_trips', 0,
                     'random seed for trip generation', short_name="s")

#########################################################
# read xml to build nx.Graph
#########################################################

def parse_xml(filename):
    # ファイルを読み込んでElementTreeを作る
    tree = ET.parse(filename)

    # <map> の処理
    pos_list = []
    if tree.find("map"):
        # グリッドのスケール
        scale = int(tree.find("map").attrib["scale"])

        # 行(<row>)を順に読み込み、各文字を要素に持つnp.ndarrayにする
        arr = []
        for row in tree.find("map").findall("row"):
            arr.append(list(row.attrib["data"]))
        arr = np.array(arr)

        # 上から下、左から右に読み、x がついている場所を順番にpos_listに記録
        H, W = arr.shape
        for i in range(H):
            for j in range(W):
                if arr[i, j] == "x":
                    pos_list.append((j*scale, -i*scale))
    else:
        # map が無い場合、全ノードを仮位置(0,0)とする (offsetX,offsetYで後に調整)
        pos_list = [(0, 0) for _ in tree.find("nodes").findall("node")]

    # pos_list に記録された位置から <node> を生成
    node_pos = {}
    node_weight = {}
    # <node> の現れる順番に pos_list の座標と合わせる
    for t, pos in zip(tree.find("nodes").findall("node"), pos_list):
        # offsetX, offsetY を読み込んで pos を調整
        offsetX, offsetY = 0, 0
        if "offsetX" in t.attrib:
            offsetX = float(t.attrib["offsetX"])
        if "offsetY" in t.attrib:
            offsetY = float(t.attrib["offsetY"])
        x, y = pos
        pos = (x + offsetX, y + offsetY)

        # weight を読み込む、weight のデフォルトは 1
        weight = 1
        if "weight" in t.attrib:
            weight = float(t.attrib["weight"])

        # pos, weight を記録
        n = t.attrib["id"]
        node_pos[n] = pos
        node_weight[n] = weight

    g = nx.Graph()
    for line in tree.find("lines").findall("line"):
        # priority を読み込む、priority のデフォルトは 0
        priority = 0
        if "priority" in line.attrib:
            priority = int(line.attrib["priority"])

        line_name = line.attrib["id"]

        # <line> に現れる <node> の順番に辺を生成
        nodes = [t for t in line.findall("node")]
        for t1, t2 in zip(nodes[:-1], nodes[1:]):
            z1 = t1.attrib["id"]
            z2 = t2.attrib["id"]
            # line 内で line_name と priority は同一
            g.add_edge(z1, z2,
                       road_name=line_name, 
                       priority=priority, 
                       edge_name=z1+"_to_"+z2)

    return node_pos, g, node_weight

#########################################################
# 3-way junctions
#########################################################

# ノード n から無向辺 e でつながる先
def get_other(e, n):
    return e[1] if e[0] == n else e[0]


# ベクトル x1 - x0 の計算
def direction(x0, x1):
    nax = np.newaxis
    d = np.array(x1) - np.array(x0)
    K = len(d.shape)
    assert (d.shape[-1] == 2)
    sli_x = (nax,) * (K-1) + (0,)
    sli_y = (nax,) * (K-1) + (1,)
    th = np.arctan2(d[sli_y], d[sli_x])
    return th


# 向き th0 から th1 まで測った角度
def diff_directional(th0, th1_):
    # 図る向きは同じ
    th1 = th1_.copy()
    while np.any(th1 < th0):
        th1[th1 < th0] += np.pi*2

    return th1 - th0

# 辺 (ノードのペア) を正規化
def get_sorted_edges(edges):
    edges = [sorted([s, t]) for s, t in edges]
    return sorted(edges)


def priority_in_3way_junction(g, pos, file=sys.stdout):
    nx.set_edge_attributes(g, 1, name="priority")
    ret = {}
    for n in g.nodes():
        x = pos[n]
        if g.degree(n) == 3:
            # n につながる辺リストを正規化して取得
            ea, eb, ec = get_sorted_edges(g.edges(n))

            # 非優先道路を e とする
            # road_name が1つだけ違う場合はそれを非優先道路にする、デフォルトは None
            a, b, c = [g.edges[e[0], e[1]]["road_name"] for e in [ea, eb, ec]]
            e = None
            if a != c and b != c and a == b:
                e = ec
            elif a != b and c != b and a == c:
                e = eb
            elif b != a and c != a and b == c:
                e = ea

            # road_name の情報が無い場合は向きで決める
            if not e:
                # 接続先の node
                ya, yb, yc = map(
                    lambda e_: pos[get_other(e_, n)], 
                    [ea, eb, ec]
                )
                # 角度 th を計算してソート
                y = np.array([ya, yb, yc])
                th = direction(x[nax, :], y)
                idx = np.argsort(th)
                # 
                idx0 = idx[[0, 1, 2]] # ソートされた idx
                idx1 = idx[[1, 2, 0]] # idx0 の隣
                idx2 = idx[[2, 0, 1]] # idx0 の隣の隣
                # idx = np.stack([idx0, idx1])
                # 角度の1番大きい辺ペアを直進道路として、それ以外を非優先道路とする
                e = [ea, eb, ec][idx2[
                    np.argmax(diff_directional(th[idx0], th[idx1]))
                ]]

            if e:
                # 非優先道路の priority は 0 にする
                g.edges[e[0], e[1]]["priority"] = 0
                # ret に非優先道路を記録する
                ret[n] = get_other(e, n)

    # 記録された非優先道路のリストをyamlとして出力
    yaml.dump(ret, file)

#########################################################
# generate files for netconvert
#########################################################

# nod.xml の出力
def generate_nodefile(g, pos, file=sys.stdout):
    print("""<?xml version="1.0" encoding="UTF-8"?>""", file=file)
    print("""<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">""", file=file)

    # 頂点の順番は正規化する
    for n in sorted(list(g.nodes())):
        x, y = pos[n]

        # 次数が2以下の辺は信号機を置かない
        if g.degree(n) <= 2:
            tls_type = "unregulated"
        else:
            tls_type = "traffic_light"

        # id は文字列
        n = str(n)

        print('    <node id="%s" x="%.2f" y="%.2f" type="%s" tlLayout="opposites"/>' %
              (n, x, y, tls_type), file=file)

    print('</nodes>', file=file)

# edg.xml の出力
def generate_edgefile(g, file=sys.stdout):
    print("""<?xml version="1.0" encoding="UTF-8"?>""", file=file)
    print("""<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">""", file=file)

    # 辺の順番は正規化する
    for i, st in enumerate(get_sorted_edges(g.edges())):
        # 辺の起終点は正規化して取得
        s, t = sorted(st)
        # "id" は連番
        j = g[s][t]["id"]

        # shape があれば、起点は指定された orig (ノード名)にする
        shape = g[s][t]["shape"]
        if shape is not None:
            orig = g[s][t]["orig"]
            if s != orig:
                t = s
                s = orig

        # <edge> の shape 以外の部分
        e1 = '    <edge from="%s" id="%d_%sto%s" to="%s" spreadType="roadCenter" numLanes="1" priority="%i"' % \
            (s, j+1, s, t, t, g.edges[s, t]["priority"])
        e2 = '    <edge from="%s" id="%d_%sto%s" to="%s" spreadType="roadCenter" numLanes="1" priority="%i"' % \
            (t, j+1, t, s, s, g.edges[s, t]["priority"])

        # shape 部分 (あれば)
        if shape is not None:
            orig = g[s][t]["orig"]
            e1 += " shape=\"" + \
                " ".join([f"{x:.2f},{y:.2f}" for x, y in shape]) + "\""
            e2 += " shape=\"" + \
                " ".join([f"{x:.2f},{y:.2f}" for x, y in shape[::-1]]) + "\""

        # <edge> タグを閉じる
        e1 = e1 + '/>'
        e2 = e2 + '/>'

        # <edge> タグを書き出す
        print(e1, file=file)
        print(e2, file=file)

    print('</edges>', file=file)


#########################################################
# edit and simpligy graph
#########################################################

# drop nodes that do not have traffic lights
def contract_edges(node_pos, g):
    ########
    # 不要な辺の削除
    ########

    # 信号機のない(次数2以下)ノードを削除したい
    nodes_wo_tls = [x for x in g.nodes if g.degree(x) <= 2]

    # 削除予定の頂点からなる連結成分をパスとして contracting_paths に記録する
    contracting_paths = []
    for p in nx.connected_components(g.subgraph(nodes_wo_tls)):
        h = g.subgraph(p)
        # subgraph で次数が 1 のものは端点
        endpoints = [v for v in h.nodes if h.degree(v) < 2]
        assert (len(endpoints) <= 2)

        if len(endpoints) == 2:
            # v1-...-v2 の頂点リストをqとする
            v1, v2 = endpoints
            q = list(nx.all_simple_paths(h, v1, v2))
            assert (len(q) == 1) # v1,v2間のパスは1つしか無いはず
            q = q[0]
            v1, v2 = q[0], q[-1]

            # v1, v2 につながる頂点をv0, v3 とし、 v0-v1-...-v2-v3 とする
            v0 = [v for v in g[v1] if v != q[1]]
            v3 = [v for v in g[v2] if v != q[-2]]
            assert (len(v0) == 1)
            assert (len(v3) == 1)
            v0, v3 = v0[0], v3[0]
            q = [v0] + q + [v3]
        else:
            # 端点が1つの場合、それは v0-v1-v2 の形
            v1 = endpoints[0]
            v0, v2 = g[v1]
            q = [v0, v1, v2]

        # 新しい辺の road_name を決める
        # TODO: handle the case when edges in q has different names
        road_name = g[v0][v1]["road_name"]
        # 新しい辺の priority をパスのうちで最大の優先度とする
        priority = np.max([g[u][v]["priority"] for u, v in zip(q[:-1], q[1:])])

        # contracting_paths に記録する
        contracting_paths.append((q, road_name, priority))

    # 削除される辺を列挙する
    removing_edges = sorted(list(set(sum([
        [(u, v) for u, v in zip(q[:-1], q[1:])]
        for q, _, _ in contracting_paths], []))))

    # 列挙された辺を実際に削除し、
    g.remove_edges_from(removing_edges)
    # 信号機のない頂点を実際に削除する
    g.remove_nodes_from(nodes_wo_tls)

    # 元からある辺は shape なし
    for u, v in g.edges():
        g[u][v]["shape"] = None

    # 削除されたパスの代わりの辺を追加
    for q, road_name, priority in contracting_paths:
        u, v = q[0], q[-1]

        # パスに沿って shape をつくり edge_name をつける
        shape = [node_pos[w] for w in q]
        edge_name = "_".join(q)

        # 辺を実際に追加する
        # shape の起点情報を orig に記録する
        g.add_edge(u, v,
                   road_name=road_name,
                   priority=priority,
                   edge_name=edge_name,
                   shape=shape,
                   orig=u)

    # 残っている頂点だけ位置情報をとってくる
    node_pos = {k: node_pos[k] for k in g.nodes}
    return node_pos, g


# rename traffic lights (nodes)
def relabel_nodes(node_pos, g, node_weight):
    node_pos_ret = {}
    node_weight_ret = {}
    node_relabel = {}
    for n1 in g.nodes():
        # 新しい名前を n2 とする
        # 3差路か4差路かで頭に"3way_"または"4way_"をつける
        n2 = n1
        assert (g.degree(n1) == 3 or g.degree(n1) == 4)
        if g.degree(n1) == 3:
            n2 = "3way_" + n1
        elif g.degree(n1) == 4:
            n2 = "4way_" + n1

        # 位置とweightの辞書をリネームする
        node_pos_ret[n2] = node_pos[n1]
        node_weight_ret[n2] = node_weight[n1]
        node_relabel[n1] = n2

    # nx.Graph の頂点をリネームする
    nx.relabel_nodes(g, node_relabel, copy=False)

    # orig もリネームする
    for u, v in g.edges():
        if "orig" in g[u][v]:
            orig = g[u][v]["orig"]
            if orig in node_relabel:
                g[u][v]["orig"] = node_relabel[orig]

    return node_pos_ret, g, node_weight_ret


#########################################################
# trip generation
#########################################################

@contextlib.contextmanager
def fixedseed(seed):
    state = np.random.get_state()
    try:
        np.random.seed(seed)
        yield
    finally:
        np.random.set_state(state)

# trip の起終点をサンプリングする
def draw_trips(node_weights, L, seed=0):
    nodes = list(node_weights.keys())
    N = len(nodes)

    # weight の辞書を np.array に変換し、正規化する
    weights = np.array([node_weights[v] for v in nodes]).astype("f")
    weights /= np.sum(weights)

    # weight に従って起終点をL個サンプリング
    trips = []
    with fixedseed(seed):
        for i in range(L):
            t = None
            f = None
            while t == f: # 起終点は違う必要がある
                t = np.random.choice(N, p=weights)
                f = np.random.choice(N, p=weights)
            trips.append((nodes[f], nodes[t]))

    return trips

# trips.xml の出力
def generate_tripfile(g, node_weight, f_trip, period=0.7, endtime=7200, seed=0):
    print(
        f"generate trips at fixed interval rate of {period}. The end time is {endtime}.")

    # 発時刻は period ごとなので、trip の数が決まる
    N = int(endtime / period)
    # trip の起終点をサンプリングする
    trips = draw_trips(node_weight, N, seed=seed)

    print("""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">""", file=f_trip)
    for i, trip in enumerate(trips):
        depart = i * period # 発時刻は period ごと
        f, t = trip
        print(
            f"""<trip id="{i}" depart="{depart}" fromJunction="{f}" toJunction="{t}"/>""", file=f_trip)
    print("""</routes>""", file=f_trip)

#########################################################
# main routine
#########################################################

def to_xml(prefix="tokyo", period=0.7, endtime=7200, seed_trips=0):
    # xml to build nx.Graph
    pos, g, node_weight = parse_xml(prefix+".network.xml")
    # edit and simpligy graph
    pos, g = contract_edges(pos, g)
    pos, g, node_weight = relabel_nodes(pos, g, node_weight)
    print(node_weight)

    # process 3-way junctions
    with open(prefix + ".priority_3way.yaml", "w") as f:
        priority_in_3way_junction(g, pos, f)

    # set edge indices
    for i, e in enumerate(get_sorted_edges(g.edges())):
        s, t = e
        g[s][t]["id"] = i

    # output node and edge files for netconvert
    with open(prefix + ".nod.xml", "w") as f:
        generate_nodefile(g, pos, file=f)
    with open(prefix + ".edg.xml", "w") as f:
        generate_edgefile(g, file=f)

    # generate and output trip information for duarouter
    with open(prefix + ".trips.xml", "w") as f:
        generate_tripfile(g, node_weight, f, period=period,
                          endtime=endtime, seed=seed_trips)


def main(argv):
    to_xml(prefix=FLAGS.prefix, period=FLAGS.period,
           endtime=FLAGS.endtime, seed_trips=FLAGS.seed_trips)


if __name__ == '__main__':
    app.run(main)
