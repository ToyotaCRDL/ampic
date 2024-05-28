import xml.etree.ElementTree as ET

import pandas as pd

#########################################################
# read network xml
#########################################################


def _parse_network_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    jct_pos_dict = {}
    for jct in root.findall("junction"):
        id = jct.attrib["id"]
        x = float(jct.attrib["x"])
        y = float(jct.attrib["y"])
        jct_pos_dict[id] = (x, y)

    tlsid_list = []
    tls_state_dict = {}
    tls_pos_dict = {}
    for tl in root.findall("tlLogic"):
        id = tl.attrib["id"]
        state_str_list = [ph.attrib["state"] for ph in tl.findall("phase")]
        tlsid_list.append(id)
        tls_state_dict[id] = state_str_list
        tls_pos_dict[id] = jct_pos_dict[id]

    edge_dict = {}
    for edge in root.findall("edge"):
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
            assert tl_node_1 == tl_node_2

            state_list = []
            if "linkIndex" in conn.attrib:
                lid = int(conn.attrib["linkIndex"])
                tl = conn.attrib["tl"]
                state_list = [state_str[lid] for state_str in tls_state_dict[tl]]
            conn_list.append((fr, to, prev, tl_node_1, next, state_list))

    return tlsid_list, edge_dict, conn_list, tls_state_dict, tls_pos_dict


def parse_network_xml(filename):
    tlsid_list, edge_dict, conn_list, tls_state_dict, tls_pos_dict = _parse_network_xml(
        filename
    )

    conn_df = []
    for x in conn_list:
        fr, to, prev, node, next, states = x
        state_str = "".join(states)
        if state_str == "":
            states = ["", ""]
        conn_df.append([fr, to, prev, node, next] + states)

    edge_df = pd.DataFrame.from_dict(edge_dict, orient="index")
    edge_df.columns = ["from", "to"]

    conn_df = pd.DataFrame(conn_df)
    conn_df.columns = [
        "from",
        "to",
        "prev",
        "node",
        "next",
        "state0",
        "state1",
        "state2",
        "state0y",
        "state1y",
    ]

    return edge_df, conn_df, tlsid_list, tls_pos_dict


#########################################################
# read route xml
#########################################################


def parse_route_xml(filename):
    print(filename)
    tree = ET.parse(filename)
    routes = tree.getroot()
    transition_count = {}
    for vehicle in routes.findall("vehicle"):
        # id = vehicle.attrib["id"]
        # depart = float(vehicle.attrib["depart"])
        route = vehicle.find("route")
        edges = route.attrib["edges"].split(" ")
        if len(edges) >= 2:
            for e1, e2 in zip(edges[:-1], edges[1:]):
                k = (e1, e2)
                transition_count[k] = transition_count.get(k, 0) + 1
    return transition_count
