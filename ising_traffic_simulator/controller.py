import networkx as nx
import numpy as np
import yaml
from scipy.linalg import block_diag

nax = np.newaxis


#########################################################
# interface for dwave solver
#########################################################


def to_dict1(h):
    h_size = np.shape(h)[0]
    h_dict = {}
    for i in range(h_size):
        h_dict[i] = h[i]
    return h_dict


def to_dict2(J):
    J_size = np.shape(J)[0]
    J_dict = {}
    for i in range(J_size):
        for j in range(J_size):
            if i != j:
                J_dict[(i, j)] = J[i][j]
    return J_dict


class global_controller:
    def __init__(self, netw, solver="", numreads=1000):
        #########################################################
        # preparation of solver
        #########################################################
        self.solver = solver
        self.numreads = numreads

        if solver == "dwave_sa":
            print("Using dwave_sa solver.")
            import neal

            self.sampler = neal.SimulatedAnnealingSampler()

        elif solver == "dwave_qa":
            print("Using dwave_qa solver.")

            # with open('dwave.conf') as file:
            #     obj = yaml.safe_load(file)
            #     dwave_token = obj['token']
            # print(dwave_token)

            from dwave.system.composites import EmbeddingComposite
            from dwave.system.samplers import DWaveSampler

            self.sampler = EmbeddingComposite(DWaveSampler())

        elif solver == "dwave_hb":
            print("Using dwave_hybrid solver.")

            from hybrid.reference.kerberos import KerberosSampler

            # self.sampler = KerberosSampler(
            #     max_iter=1000, sa_reads=10, qa_reads=1000)
            self.sampler = KerberosSampler()

        elif solver == "dwave_greedy":
            print("Using dwave_greedy solver.")

            import greedy

            self.sampler = greedy.SteepestDescentSolver()

        elif solver == "amplify_sa":
            print("Using amplify_sa solver.")
            from amplify import Solver
            from amplify.client import FixstarsClient

            client = FixstarsClient()

            with open("amplify.conf") as file:
                obj = yaml.safe_load(file)
                client.url = obj["url"]
                client.token = obj["token"]
                client.proxy = obj["proxy"]

            client.parameters.timeout = 5000  # Timeout [ms]
            client.parameters.outputs.duplicate = True

            self.sampler = Solver(client)

        elif solver == "amplify_gurobi":
            print("Using amplify_gurobi solver.")
            from amplify import Solver
            from amplify.client import GurobiClient

            client = GurobiClient()

            # with open('gurobi.conf') as file:
            #     obj = yaml.safe_load(file)
            #     print(obj['token'])
            #     client.token = obj['token']

            # client.parameters.timelimit = 1  # Timeout [ms]

            self.sampler = Solver(client)

        elif solver == "brute_force":
            self.candidate_spins = None
        elif solver == "ignore_interaction":
            pass
        else:
            print("No solver is selected. Using dwave_sa solver.")
            import neal

            self.sampler = neal.SimulatedAnnealingSampler()

        #########################################################
        # network values
        #########################################################
        self.netw = netw

        Adj = nx.to_numpy_array(self.netw.G, nodelist=self.netw.nodid)

        self.Adj = Adj
        self.L = len(netw.nodid)

    #########################################################
    # build Ising model
    #########################################################
    def set_parameters(self, a_0, a_1, o_g):
        coef_mat = np.zeros((self.L, self.L))  # eta_ij
        state_mat = np.zeros((self.L, self.L))  # s_ij
        for id, jd in self.netw.G.edges:
            i, j = self.netw.G.nodes[id]["id"], self.netw.G.nodes[jd]["id"]
            coef_mat[j, i] = self.netw.G.edges[id, jd]["coef"]
            state_mat[j, i] = self.netw.G.edges[id, jd]["state"]

        a_diff = a_0 - a_1
        a_sum = a_0 + a_1
        o_diff = o_g
        o_sum = o_g

        A_1 = coef_mat * state_mat * a_diff
        A_2 = -np.diag(np.sum(coef_mat * o_diff, axis=1))
        A = A_1 + A_2

        b = np.sum(coef_mat * state_mat * (a_sum - o_sum), axis=1)

        self.A = A
        self.b = b

        Q_ = np.sum(coef_mat * (a_sum), axis=1)
        self.Q = np.size(Q_) * np.diag(Q_ / (np.sum(Q_) + 1e-10))

        Q2_ = np.sum(coef_mat * (a_sum) ** 2, axis=1)
        self.Q2 = np.size(Q2_) * np.diag(Q2_ / (np.sum(Q2_) + 1e-10))

    def build_ising(self, x, sigma, weight, weight_mode):
        # L = (A @ sigma + x + b).T @ (A @ sigma + x + b) - w * sigma_prev.T @ sigma
        # = sigma.T @ (A.T @ A) @ sigma
        #   + 2 * ((x+b).T @ A - w * sigma_prev).T @ sigma
        #   + (x+b).T @ (x+b)
        A, b = self.A, self.b
        if weight_mode == "fixed":
            J = A.T @ A
            h = 2 * (x + b).T @ A - weight * sigma
        elif weight_mode == "linear":
            Q = self.Q
            J = A.T @ Q @ A
            h = 2 * (x + b).T @ Q @ A - weight * sigma
        elif weight_mode == "quad":
            Q2 = self.Q2
            J = A.T @ Q2 @ A
            h = 2 * (x + b).T @ Q2 @ A - weight * sigma
        else:
            print("weight mode is not selected. using fixed weight.")
            J = A.T @ A
            h = 2 * (x + b).T @ A - weight * sigma

        self.ising_J = J
        self.ising_h = h
        return J, h

    #########################################################
    # optimization for control
    #########################################################

    def global_control(self, x, sigma, weight, weight_mode):
        J, h = self.build_ising(x, sigma, weight, weight_mode)

        if (
            self.solver == "dwave_sa"
            or self.solver == "dwave_qa"
            or self.solver == "dwave_hb"
            or self.solver == "dwave_greedy"
        ):
            sigma = self.solve_dwave(J, h, numreads=self.numreads)
        elif self.solver == "amplify_sa" or self.solver == "amplify_gurobi":
            sigma = self.solve_amplify(J, h)
        elif self.solver == "brute_force":
            sigma = self.solve_ising_brute_force(J, h)
        elif self.solver == "ignore_interaction":
            sigma = self.solve_ignore_interaction(self, J, h)
        else:
            print("No solver is selected. Using dwave-sa.")
            sigma = self.solve_dwave(J, h, numreads=self.numreads)

        E = (sigma[nax, :] @ J @ sigma[:, nax])[0, 0] + np.sum(h * sigma)
        print("E:", E)

        return sigma

    def global_control_horizon(self, x, sigma, weight, weight_mode, horizon):
        x_size = np.shape(x)[0]
        I = np.eye(x_size)
        A = self.A
        b = self.b

        II = I
        bb = b

        for i in range(horizon - 1):
            II = np.vstack([II, I])
            bb = np.hstack([bb, (i + 2) * b])

        AA = A
        for i in range(horizon - 1):
            AA = np.vstack([AA, A])

        tmpAA = AA
        for i in range(horizon - 1):
            tmpAA = np.vstack([np.zeros(np.shape(A)), tmpAA])[:-x_size]
            AA = np.hstack([AA, tmpAA])

        if weight_mode == "fixed":
            J_ = AA.T @ AA
            h_ = 2 * (II @ x + bb).T @ AA
        elif weight_mode == "linear":
            Q = self.Q
            QQ = Q
            for i in range(horizon - 1):
                QQ = block_diag(QQ, Q)
            J_ = AA.T @ QQ @ AA
            h_ = 2 * (II @ x + bb).T @ QQ @ AA
        elif weight_mode == "quad":
            Q2 = self.Q2
            QQ2 = Q2
            for i in range(horizon - 1):
                QQ2 = block_diag(QQ2, Q)
            J_ = AA.T @ QQ2 @ AA
            h_ = 2 * (II @ x + bb).T @ QQ2 @ AA
        else:
            print("weight mode is not selected. using fixed weight.")
            J_ = AA.T @ AA
            h_ = 2 * (II @ x + bb).T @ AA

        ww = np.zeros(np.shape(h_))
        WW = np.zeros(np.shape(J_))

        ww[0 : np.shape(sigma)[0]] = weight * sigma

        for i in range(np.shape(sigma)[0] * (horizon - 1)):
            WW[np.shape(sigma)[0] + i, i] = weight

        J = J_ - WW
        h = h_ - ww

        if (
            self.solver == "dwave_sa"
            or self.solver == "dwave_qa"
            or self.solver == "dwave_hb"
            or self.solver == "dwave_greedy"
        ):
            sigma = self.solve_dwave(J, h, numreads=self.numreads)
        elif self.solver == "amplify_sa" or self.solver == "amplify_gurobi":
            sigma = self.solve_amplify(J, h)
        elif self.solver == "brute_force":
            sigma = self.solve_ising_brute_force(J, h)
        elif self.solver == "ignore_interaction":
            sigma = self.solve_ignore_interaction(self, J, h)
        else:
            print("No solver is selected. Using dwave-sa.")
            sigma = self.solve_dwave(J, h, numreads=self.numreads)

        return sigma[:x_size]

    #########################################################
    # call solvers
    #########################################################

    def return_best_result(self, response):
        ene = np.Inf
        for sample, energy in response.data(["sample", "energy"]):
            if energy < ene:
                ene = energy
                best_sample = sample
        return np.array(list(best_sample.values()))

    # dwave_sa and dwave_qa
    def solve_dwave(self, J, h, numreads):
        J_dict = to_dict2(J)
        h_dict = to_dict1(h)
        # seed = np.random.randint(1000000)
        if self.solver == "dwave_hb":
            response = self.sampler.sample_ising(
                h_dict, J_dict, num_reads=1, sa_reads=numreads, qpu_reads=numreads
            )
        else:
            response = self.sampler.sample_ising(h_dict, J_dict, num_reads=numreads)
        sigma = self.return_best_result(response)
        return sigma

    # amplify_sa and amplify_gurobi
    def solve_amplify(self, J, h):
        from amplify import IsingMatrix

        J_size = np.shape(J)[0]
        new_J = np.zeros((J_size, J_size))
        for i in range(0, J_size):
            for j in range(i, J_size):
                if i == j:
                    new_J[i, j] = h[i]
                else:
                    new_J[i, j] = 2 * J[i, j]

        m1 = IsingMatrix(new_J)
        result = self.sampler.solve(m1)
        for solution in result:
            print(f"energy = {solution.energy}")
            print(f"values = {solution.values}")
        sorted_sol = sorted(solution.values.items())
        sigma = np.array([sorted_sol[i][1] for i in range(J_size)])
        return sigma

    # ignore_interaction
    def solve_ignore_interaction(self, J, h):
        sigma = -np.sign(h)
        return sigma

    # brute force
    def solve_ising_brute_force(self, J, h):
        print("solving by brute force solver")
        # minimize xJx+hx
        if self.candidate_spins is None:
            N = h.shape[0]
            assert N <= 25
            L = 1 << N
            self.candidate_spins = np.zeros((L, N))
            for i in np.arange(L):
                self.candidate_spins[i, :] = (
                    np.array([(i >> k) % 2 for k in np.arange(N)]) * 2 - 1
                )

        E = (
            np.einsum("li,ij,lj->l", self.candidate_spins, J, self.candidate_spins)
            + self.candidate_spins @ h
        )
        l_opt = np.argmin(E)
        spins_opt = self.candidate_spins[l_opt, :]
        return spins_opt

    #########################################################
    # compute Hamitonian
    #########################################################

    def get_hamiltonian(self, x, sigma, sigma_p, weight):
        res2 = x.T @ x
        res3 = -sigma.reshape(self.L, 1).T @ sigma_p.reshape(self.L, 1)
        res1 = res2 + weight * res3[0, 0]
        return res1, res2, res3[0, 0]
