
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd

from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_string('prefix', "square",
                    'input XML file prefix', short_name="i")
flags.DEFINE_string('fig', "map.png",
                    'output map image file', short_name="f")


def parse_network_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    jct_pos_dict = {}
    for jct in root.findall('junction'):
        id = jct.attrib["id"]
        x = float(jct.attrib["x"])
        y = float(jct.attrib["y"])
        jct_pos_dict[id] = (x, y)

    tlsid = []
    tls_state_dict = {}
    tls_pos_dict = {}
    for tl in root.findall('tlLogic'):
        id = tl.attrib["id"]
        state_str_list = [ph.attrib["state"] for ph in tl.findall("phase")]
        tlsid.append(id)
        tls_state_dict[id] = state_str_list
        tls_pos_dict[id] = jct_pos_dict[id]

    edge_dict = {}
    for edge in root.findall('edge'):
        id = edge.attrib["id"]
        if not edge.attrib.get("function", None) == "internal":
            fr = edge.attrib["from"]
            to = edge.attrib["to"]
            edge_dict[id] = (fr, to)

    conn_list = []
    for conn in root.findall("connection"):
        fr = conn.attrib["from"]
        to = conn.attrib["to"]
        if (fr in edge_dict) and (to in edge_dict):
            prev, tl_node_1 = edge_dict[fr]
            tl_node_2, next = edge_dict[to]
            assert(tl_node_1 == tl_node_2)

            state_list = []
            if "linkIndex" in conn.attrib:
                lid = int(conn.attrib["linkIndex"])
                tl = conn.attrib["tl"]
                state_list = [state_str[lid]
                              for state_str in tls_state_dict[tl]]
            conn_list.append((fr, to, prev, tl_node_1, next, state_list))

    return tlsid, edge_dict, conn_list, tls_state_dict, tls_pos_dict


def main(argv):
    filename = FLAGS.prefix+'.net.xml'
    fig_filename = FLAGS.fig
    edge_filename = FLAGS.prefix+'.edge.csv'
    conn_filename = FLAGS.prefix+'.conn.csv'
    tls_filename = FLAGS.prefix+'.tls.csv'

    tlsid_list, edge_dict, conn_list, tls_state_dict, tls_pos_dict = \
        parse_network_xml(filename)

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    for tlsid in tls_pos_dict:
        x, y = tls_pos_dict[tlsid]
        plt.scatter([x], [y], marker="o")
        plt.annotate(tlsid, xy=(x, y))
    plt.savefig(fig_filename)

    conn_df = []
    for x in conn_list:
        fr, to, prev, node, next, states = x
        state_str = "".join(states)
        if state_str == "":
            states = ["", ""]
        conn_df.append([fr, to, prev, node, next]+states)

    edge_df = pd.DataFrame.from_dict(edge_dict, orient='index')
    edge_df.columns = ["from", "to"]
    edge_df.to_csv(edge_filename)

    conn_df = pd.DataFrame(conn_df)
    conn_df.columns = ["from", "to", "prev",
                       "node", "next", "state0", "state1"]
    conn_df.to_csv(conn_filename)

    pd.DataFrame({"tls": tlsid_list},
                 index=list(range(len(tlsid_list)))).to_csv(tls_filename)


if __name__ == '__main__':
    app.run(main)
