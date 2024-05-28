import traci  # noqa
import numpy as np
from .parser import parse_route_xml


# sigma[i] = +1 when tls[id] = 0 (state0), i<-j for s_{ij}=+1 is is green
# sigma[i] = -1 when tls[id] = 1 (state1), i<-j for s_{ij}=-1 is is green

# 1 if state0 is green, -1 if state0 is red, 0 otherwise.


def is_straight(edge_state, tls):
    return (edge_state > 0 and tls == 0) or (edge_state < 0 and tls == 1) or tls < 0


#########################################################
# observe traffic information to calculate input parameters for controller
#########################################################
class network_values:
    def __init__(self, netw, L, stepInterval, numRef, lenRef, filename_route):
        self.netw = netw
        self.stepInterval = stepInterval
        self.numRef = numRef
        self.lenRef = lenRef

        #########################################################
        # calculate transition probability by all input routes in advance
        #########################################################
        self.transition_count = parse_route_xml(filename_route)
        self.transition_prob = self.transition_probability()

        #########################################################
        # reset
        #########################################################
        self.reset(L)

    #########################################################
    # calculate transition probability by all input routes in advance
    #########################################################
    def transition_probability(self):
        # L = self.netw.L
        transition_prob = {}
        transition_sum = {}
        for k, v in self.transition_count.items():
            eid1, eid2 = k
            transition_sum[eid1] = transition_sum.get(eid1, 0) + v

        for jd, id in self.netw.G.edges:
            eid1 = self.netw.G.edges[jd, id]["id"]
            for kd in self.netw.G.succ[id]:
                eid2 = self.netw.G.edges[id, kd]["id"]
                transition = (eid1, eid2)
                if transition in self.transition_count:
                    transition_prob[transition] = (
                        self.transition_count[transition] / transition_sum[eid1]
                    )
                else:
                    transition_prob[transition] = 0
        return transition_prob

    #########################################################
    # reset
    #########################################################
    def reset_xVal(self):
        self.xVal = {}
        for id in self.netw.nodid:
            self.xVal[id] = 0

    def reset(self, L):
        self.reset_xVal()
        self.a_s = np.zeros((L, L))
        self.a_t = np.zeros((L, L))
        self.an_s = np.zeros((L, L))
        self.an_t = np.zeros((L, L))
        self.o_g = np.zeros((L, L))
        self.on_g = np.zeros((L, L))

        ### new statistics ###
        self.sum_exit = 0
        self.green_count = 0
        self.prev_routeid = {}
        self.current_transition_count = {}
        self.exit_count = {}

    #########################################################
    # normalize car counts
    #########################################################

    def get_edge_density(self, edge):
        lane = edge + "_0"
        l = traci.lane.getLength(lane)
        cars = traci.edge.getLastStepVehicleNumber(edge)
        return (cars / self.numRef) * (self.lenRef / l)

    def get_edge_flow(self, edge):
        lane = edge + "_0"
        l = traci.lane.getLength(lane)
        cars = traci.edge.getLastStepVehicleNumber(edge)
        vm = traci.lane.getLastStepMeanSpeed(lane)
        return (cars / self.numRef) / (l / self.lenRef) * (vm / l)

    #########################################################
    # update X value at tls of id
    # and store it to xVal
    #########################################################

    def update_Xvalue(self):
        for jd, id in self.netw.G.edges:
            edge = self.netw.G.edges[jd, id]["id"]
            coef = self.netw.G.edges[jd, id]["coef"]
            state = self.netw.G.edges[jd, id]["state"]
            self.xVal[id] += coef * state * self.get_edge_density(edge)
            # / self.stepInterval

    #########################################################
    # update A value at tls of id
    # and store them to a_0, a_1, o_g_global
    #########################################################

    def update_Avalue(self, tls_current):
        self.collect_vehicle_positions(tls_current)
        self.distribute()

    def distribute(self):
        L = self.netw.L
        a_0 = np.zeros((L, L))
        a_1 = np.zeros((L, L))
        o_g = np.zeros((L, L))

        for id1, id2 in self.netw.G.edges:
            eid2 = self.netw.G.edges[id1, id2]["id"]
            i1, i2 = self.netw.G.nodes[id1]["id"], self.netw.G.nodes[id2]["id"]
            lane = eid2 + "_0"
            l = traci.lane.getLength(lane)
            w = 1.0 / self.numRef / (l / self.lenRef) * self.stepInterval
            for id0 in self.netw.G.pred[id1]:
                eid1 = self.netw.G.edges[id0, id1]["id"]
                state = self.netw.G.edges[id0, id1]["state"]
                transition = (eid1, eid2)
                prob = self.transition_prob[transition]
                a = self.rate_global * prob  # rate[i1, i0] == rate_global
                if state > 0:
                    a_0[i2, i1] += a * w
                elif state < 0:
                    a_1[i2, i1] += a * w
                assert state != 0
            o_g[i2, i1] = self.rate_global * w  # rate[i2, i1] == rate_global

        self.a_0 = a_0
        self.a_1 = a_1
        self.o_g_global = o_g

    def collect_vehicle_positions(self, tls_current):
        vehicle_list = traci.vehicle.getIDList()
        routeid = {}
        for vid in vehicle_list:
            routeid[vid] = traci.vehicle.getRouteIndex(vid)

        if self.prev_routeid:
            for vid in vehicle_list:
                if vid in self.prev_routeid:
                    p_rid = self.prev_routeid[vid]
                    rid = routeid[vid]
                    if p_rid != rid:
                        route = traci.vehicle.getRoute(vid)
                        p_eid = route[p_rid]
                        eid = route[rid]
                        self.current_transition_count[(p_eid, eid)] = (
                            self.current_transition_count.get((p_eid, eid), 0) + 1
                        )
                        self.exit_count[p_eid] = self.exit_count.get(p_eid, 0) + 1
                        self.sum_exit += 1
        self.prev_routeid = routeid

        for id in self.netw.G.nodes:
            tlsi = tls_current[id]
            for jd in self.netw.G.pred[id]:
                state = self.netw.G.edges[jd, id]["state"]
                if is_straight(state, tlsi):
                    self.green_count += 1

        self.rate_global = self.sum_exit / self.green_count
