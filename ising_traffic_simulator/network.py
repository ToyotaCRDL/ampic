from __future__ import absolute_import, print_function

import networkx as nx
import pandas as pd

from .parser import parse_network_xml


#########################################################
# store static network information
#########################################################
class traffic_network:
    def __init__(self, filename):
        #########################################################
        # parse input network file
        #########################################################
        _, data, tlsid, pos = parse_network_xml(filename)

        #########################################################
        # collect edge data
        #########################################################
        tls_list_tmp = []
        edge_data_list_tmp = []
        for _, row in data.iterrows():
            state0 = row["state0"]
            node_from = row["prev"]
            node_here = row["node"]
            edge_id = row["from"]

            if state0 == "g":
                state0 = "G"
            elif state0 == "r":
                state0 = "R"
            edge_data_list_tmp.append((node_from, node_here, edge_id, state0))
            if state0 == "G" or state0 == "R":
                tls_list_tmp.append(node_from)

        self.nodid = sorted(list(set(data["prev"].values) | set(data["node"].values)))
        self.L = len(self.nodid)
        self.tls_list = sorted(list(set(tls_list_tmp)))

        edge_data_list = list(set(edge_data_list_tmp))
        df_edge_data = pd.DataFrame(
            edge_data_list, columns=["from", "to", "id", "state0"]
        )

        # 1 if state0 is green, -1 if state0 is red, 0 otherwise.
        edge_state_dict = {}
        for i, row in df_edge_data.iterrows():
            state0 = row["state0"]
            if state0 == "G":
                edge_state_dict[i] = 1
            elif state0 == "R":
                edge_state_dict[i] = -1
            else:
                edge_state_dict[i] = 0
        df_edge_data["edge_state"] = pd.Series(edge_state_dict)

        #########################################################
        # build networkx digraph
        #########################################################
        G = nx.DiGraph()
        for i, id in enumerate(self.nodid):
            G.add_node(id, id=i)

        for _, row in df_edge_data.iterrows():
            G.add_edge(
                row["from"], row["to"], id=row["id"], state=row["edge_state"], coef=1
            )

        self.G = G
        for id in self.G.nodes:
            ssup = 0
            ssum = 0
            for jd in G.pred[id]:
                state = G.edges[jd, id]["state"]
                if state > 0:
                    ssup += 1
                if state < 0:
                    ssum += 1

            for jd in G.pred[id]:
                state = G.edges[jd, id]["state"]
                if ssup == 1 and state > 0:
                    G.edges[jd, id]["coef"] = 2
                if ssum == 1 and state < 0:
                    G.edges[jd, id]["coef"] = 2

        #########################################################
        # traffic lights
        #########################################################
        self.tlsid = tlsid
        self.pos = pos

        # All nodes must have traffic lights
        assert set(tlsid) == set(self.nodid)
