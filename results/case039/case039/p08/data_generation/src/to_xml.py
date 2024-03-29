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



def parse_xml(filename):
    tree = ET.parse(filename)
    pos_list = []
    if tree.find("map"):
        scale = int(tree.find("map").attrib["scale"])
        arr = []
        for row in tree.find("map").findall("row"):
            arr.append(list(row.attrib["data"]))
        arr = np.array(arr)
        H, W = arr.shape
        for i in range(H):
            for j in range(W):
                if arr[i, j] == "x":
                    pos_list.append((j*scale, -i*scale))
    else:
        pos_list = [(0, 0) for _ in tree.find("nodes").findall("node")]

    node_pos = {}
    node_weight = {}
    for t, pos in zip(tree.find("nodes").findall("node"), pos_list):
        offsetX, offsetY = 0, 0
        if "offsetX" in t.attrib:
            offsetX = float(t.attrib["offsetX"])
        if "offsetY" in t.attrib:
            offsetY = float(t.attrib["offsetY"])
        weight = 1
        if "weight" in t.attrib:
            weight = float(t.attrib["weight"])

        x, y = pos
        pos = (x + offsetX, y + offsetY)
        n = t.attrib["id"]
        print(n, offsetX, offsetY)
        node_pos[n] = pos
        node_weight[n] = weight

    g = nx.Graph()
    for line in tree.find("lines").findall("line"):
        line_name = line.attrib["id"]
        priority = 0
        if "priority" in line.attrib:
            priority = int(line.attrib["priority"])
        nodes = [t for t in line.findall("node")]
        for t1, t2 in zip(nodes[:-1], nodes[1:]):
            z1 = t1.attrib["id"]
            z2 = t2.attrib["id"]
            g.add_edge(z1, z2,
                       road_name=line_name, priority=priority, edge_name=z1+"_to_"+z2)
    return node_pos, g, node_weight


def get_other(e, n):
    return e[1] if e[0] == n else e[0]


def direction(x0, x1):
    d = np.array(x1) - np.array(x0)
    K = len(d.shape)
    assert(d.shape[-1] == 2)
    sli_x = (sln,) * (K-1) + (0,)
    sli_y = (sln,) * (K-1) + (1,)
    th = np.arctan2(d[sli_y], d[sli_x])
    return th


def diff_directional(th0, th1_):
    th1 = th1_.copy()
    while np.any(th1 < th0):
        th1[th1 < th0] += np.pi*2
    return th1 - th0


def get_sorted_edges(edges):
    edges = [sorted([s, t]) for s, t in edges]
    return sorted(edges)


def priority_in_3way_junction(g, pos, file=sys.stdout):
    nx.set_edge_attributes(g, 1, name="priority")
    ret = {}
    for n in g.nodes():
        x = pos[n]
        if g.degree(n) == 3:
            ea, eb, ec = get_sorted_edges(g.edges(n))
            a, b, c = [g.edges[e[0], e[1]]["road_name"] for e in [ea, eb, ec]]
            print(n, a, b, c)
            e = ea
            if a != c and b != c and a == b:
                e = ec
            elif a != b and c != b and a == c:
                e = eb
            elif b != a and c != a and b == c:
                e = ea
            if not e:
                ya, yb, yc = map(
                    lambda e_: pos[get_other(e_, n)], [ea, eb, ec])
                y = np.array([ya, yb, yc])
                th = direction(x[nax, :], y)
                idx = np.argsort(th)
                idx0 = idx[[0, 1, 2]]
                idx1 = idx[[1, 2, 0]]
                idx2 = idx[[2, 0, 1]]
                idx = np.stack([idx0, idx1])
                e = [ea, eb, ec][idx2[np.argmax(
                    diff_directional(th[idx0], th[idx1]))]]
            if e:
                g.edges[e[0], e[1]]["priority"] = 0
                ret[n] = get_other(e, n)
    yaml.dump(ret, file)


def generate_nodefile(g, pos, file=sys.stdout):
    print("""<?xml version="1.0" encoding="UTF-8"?>""", file=file)
    print("""<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">""", file=file)

    for n in sorted(list(g.nodes())):
        x, y = pos[n]

        if g.degree(n) <= 2:
            tls_type = "unregulated"
        else:
            tls_type = "traffic_light"

        n = str(n)
        print('    <node id="%s" x="%.2f" y="%.2f" type="%s" tlLayout="opposites"/>' %
              (n, x, y, tls_type), file=file)

    print('</nodes>', file=file)


def generate_edgefile(g, file=sys.stdout):
    print("""<?xml version="1.0" encoding="UTF-8"?>""", file=file)
    print("""<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">""", file=file)
    for i, st in enumerate(get_sorted_edges(g.edges())):
        s, t = sorted(st)
        j = g[s][t]["id"]
        shape = g[s][t]["shape"]
        if shape is not None:
            orig = g[s][t]["orig"]
            if s != orig:
                t = s
                s = orig
        e1 = '    <edge from="%s" id="%d_%sto%s" to="%s" spreadType="roadCenter" numLanes="1" priority="%i"' % \
            (s, j+1, s, t, t, g.edges[s, t]["priority"])
        e2 = '    <edge from="%s" id="%d_%sto%s" to="%s" spreadType="roadCenter" numLanes="1" priority="%i"' % \
            (t, j+1, t, s, s, g.edges[s, t]["priority"])
        if shape is not None:
            orig = g[s][t]["orig"]
            e1 += " shape=\"" + \
                " ".join([f"{x:.2f},{y:.2f}" for x, y in shape]) + "\""
            e2 += " shape=\"" + \
                " ".join([f"{x:.2f},{y:.2f}" for x, y in shape[::-1]]) + "\""

        e1 = e1 + '/>'
        e2 = e2 + '/>'
        print(e1, file=file)
        print(e2, file=file)

    print('</edges>', file=file)



def generate_dst_src_file(g, node_weight, file_src=sys.stdout, file_dst=sys.stdout):
    print("""<edgedata>""", file=file_src)
    print("""<interval begin="0" end="10"/>""", file=file_src)
    print("""<edgedata>""", file=file_dst)
    print("""<interval begin="0" end="10"/>""", file=file_dst)
    # edges = [e for e in g.edges]    
    # w = 1.0 / len(edges)
    w = 1
    for i, st in enumerate(g.edges):
        s, t = st
        j = g[s][t]["id"]
        id = f"{j+1}_{s}to{t}"
        ws = node_weight[s]
        wt = node_weight[t]
        # w = 1
        print(f"""<edge id="{id}" value="{ws}"/>""", file=file_src)
        print(f"""<edge id="{id}" value="{wt}"/>""", file=file_dst)
        id = f"{j+1}_{t}to{s}"
        # w = 1
        print(f"""<edge id="{id}" value="{wt}"/>""", file=file_src)
        print(f"""<edge id="{id}" value="{ws}"/>""", file=file_dst)
        w=0

    print('</interval>', file=file_src)
    print('</edgedata>', file=file_src)
    print('</interval>', file=file_dst)
    print('</edgedata>', file=file_dst)



def contract_edges(node_pos, g):
    nodes_wo_tls = [x for x in g.nodes if g.degree(x) <= 2]
    contracting_paths = []
    for p in nx.connected_components(g.subgraph(nodes_wo_tls)):
        h = g.subgraph(p)
        endpoints = [v for v in h.nodes if h.degree(v) < 2]
        assert(len(endpoints) <= 2)
        if len(endpoints) == 2:
            v1, v2 = endpoints
            q = list(nx.all_simple_paths(h, v1, v2))
            assert(len(q) == 1)
            q = q[0]
            v1, v2 = q[0], q[-1]
            v0 = [v for v in g[v1] if v != q[1]]
            v3 = [v for v in g[v2] if v != q[-2]]
            assert(len(v0) == 1)
            assert(len(v3) == 1)
            v0, v3 = v0[0], v3[0]
            q = [v0] + q + [v3]
        else:
            v1 = endpoints[0]
            v0, v2 = g[v1]
            q = [v0, v1, v2]
        # TODO: handle the case when edges in q has different names
        road_name = g[v0][v1]["road_name"]
        priority = np.max([g[u][v]["priority"] for u, v in zip(q[:-1], q[1:])])

        contracting_paths.append((q, road_name, priority))
    removing_edges = sorted(list(set(sum([
        [(u, v) for u, v in zip(q[:-1], q[1:])]
        for q, _, _ in contracting_paths], []))))
    g.remove_edges_from(removing_edges)
    g.remove_nodes_from(nodes_wo_tls)

    for u, v in g.edges():
        g[u][v]["shape"] = None

    for q, road_name, priority in contracting_paths:
        u, v = q[0], q[-1]
        shape = [node_pos[w] for w in q]
        edge_name = "_".join(q)
        g.add_edge(u, v,
                   road_name=road_name,
                   priority=priority,
                   edge_name=edge_name,
                   shape=shape,
                   orig=u)

    for u, v in g.edges:
        print(g[u][v])
    node_pos = {k: node_pos[k] for k in g.nodes}
    return node_pos, g


def relabel_nodes(node_pos, g, node_weight):
    node_pos_ret = {}
    node_weight_ret = {}
    node_relabel = {}
    for n1 in g.nodes():
        n2 = n1
        assert(g.degree(n1) == 3 or g.degree(n1) == 4)
        if g.degree(n1) == 3:
            n2 = "3way_" + n1
        elif g.degree(n1) == 4:
            n2 = "4way_" + n1
        node_pos_ret[n2] = node_pos[n1]
        node_weight_ret[n2] = node_weight[n1]
        node_relabel[n1] = n2

    nx.relabel_nodes(g, node_relabel, copy=False)

    for u, v in g.edges():
        if "orig" in g[u][v]:
            orig = g[u][v]["orig"]
            if orig in node_relabel:
                g[u][v]["orig"] = node_relabel[orig]

    return node_pos_ret, g, node_weight_ret


@contextlib.contextmanager
def fixedseed(seed):
    state = np.random.get_state()
    try:
        np.random.seed(seed)
        yield
    finally:
        np.random.set_state(state)

def draw_trips(node_weights, L, seed=0):
    nodes = list(node_weights.keys())
    weights = np.array([node_weights[v] for v in nodes]).astype("f")
    weights /= np.sum(weights)
    N = len(nodes)
    trips = []
    with fixedseed(seed):
        for i in range(L):
            t = None
            f = None
            while t == f:                  
                t = np.random.choice(N, p=weights)
                f = np.random.choice(N, p=weights)
            trips.append((nodes[f], nodes[t]))
    return trips
            
def generate_tripfile(g, node_weight, f_trip, period = 0.7, endtime=7200, seed=0):
    print(f"generate trips at fixed interval rate of {period}. The end time is {endtime}.")
    N = int(endtime / period)
    print("""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">""", file=f_trip)
    trips = draw_trips(node_weight, N, seed=seed)
    for i, trip in enumerate(trips):
        depart = i * period
        f, t = trip
        print(f"""<trip id="{i}" depart="{depart}" fromJunction="{f}" toJunction="{t}"/>""", file=f_trip)
    print("""</routes>""", file=f_trip)
    

def to_xml(prefix="tokyo", period=0.7, endtime=7200, seed_trips = 0):
    pos, g, node_weight = parse_xml(prefix+".network.xml")
    pos, g = contract_edges(pos, g)
    pos, g, node_weight = relabel_nodes(pos, g, node_weight)
    print(node_weight)

    with open(prefix + ".priority_3way.yaml", "w") as f:
        priority_in_3way_junction(g, pos, f)
    
    for i,e in enumerate(get_sorted_edges(g.edges())):
        s, t = e
        g[s][t]["id"] = i

    with open(prefix + ".nod.xml", "w") as f:
        generate_nodefile(g, pos, file=f)
    with open(prefix + ".edg.xml", "w") as f:
        generate_edgefile(g, file=f)
    # with open(prefix + ".src.xml", "w") as f_src:
    #     with open(prefix + ".dst.xml", "w") as f_dst:
    #         generate_dst_src_file(g, node_weight, file_src=f_src, file_dst=f_dst)
    with open(prefix + ".trips.xml", "w") as f:
        generate_tripfile(g, node_weight, f, period=period, endtime = endtime, seed=seed_trips)


def main(argv):
    to_xml(prefix=FLAGS.prefix, period=FLAGS.period, endtime=FLAGS.endtime, seed_trips=FLAGS.seed_trips)


if __name__ == '__main__':
    app.run(main)
