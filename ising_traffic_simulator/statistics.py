import traci  # noqa


#########################################################
# compute statistics
#########################################################


# rate of waiting cars
def computeWaitingCars():
    vIDs = traci.vehicle.getIDList()
    cars = 0
    wcars = 0
    for vid in vIDs:
        sp = traci.vehicle.getSpeed(vid)
        cars += 1
        if sp < 0.1:
            wcars += 1
    rate = float(wcars) / float(cars)
    return rate


# average density of cars
def computeSpeed():
    vm = 0
    edgeID = traci.edge.getIDList()
    for id in edgeID:
        vm += traci.edge.getLastStepMeanSpeed(id)
    return vm / len(edgeID)


# CO2 Emmisions
def computeCO2():
    vIDs = traci.vehicle.getIDList()
    co2 = 0
    for vid in vIDs:
        co2 += traci.vehicle.getCO2Emission(vid)
    return co2


class statistics:
    def __init__(self):
        #########################################################
        # calculate total length of network
        #########################################################
        self.lengthTotal = 0
        for id in traci.edge.getIDList():
            self.lengthTotal += traci.lane.getLength(id + "_0")

        #########################################################
        # reset
        #########################################################
        self.reset()

    #########################################################
    # reset
    #########################################################
    def reset(self):
        self.sum_meanDensity = 0
        self.sum_meanSpeed = 0
        self.sum_meanHamiltonian = 0
        self.sum_rateWcars = 0
        self.sum_rateCO2 = 0
        self.count = 0

    #########################################################
    # increase total of each network statistics
    # and calculate averages in a time window
    #########################################################
    def increase(self):
        self.sum_meanDensity += traci.vehicle.getIDCount() / self.lengthTotal * 1000
        self.sum_meanSpeed += computeSpeed()
        #        self.sum_meanHamiltonian += hamiltonian
        self.sum_rateWcars += computeWaitingCars()
        self.sum_rateCO2 += computeCO2() / 1e6
        self.count += 1

    def get_mean(self):
        if self.count > 0:
            meanDensity = self.sum_meanDensity / self.count
            meanSpeed = self.sum_meanSpeed / self.count
            #            meanHamiltonian = self.sum_meanHamiltonian / self.count
            rateWcars = self.sum_rateWcars / self.count
            rateCO2 = self.sum_rateCO2 / self.count
            #            return meanDensity, meanSpeed, meanHamiltonian, rateWcars, rateCO2
            return meanDensity, meanSpeed, rateWcars, rateCO2
        else:
            return 0, 0, 0, 0

    #########################################################
    # store latest value of Ising model statistics
    #########################################################
    def store(self, h, x, s):
        self.vHamiltonian = h
        self.vXSquared = x
        self.vSigmaSquared = s

    #########################################################
    # output
    #########################################################
    def init_file(self, fname_value, header=None):
        with open(fname_value, "w") as fl:
            if header is not None:
                fl.write(header)
            fl.write(
                "step[s], count, density[car/km], speed[m/s], hamiltonian, xterm, sigmaterm, waiting rate, co2[kg/s]\n"
            )

    def append_to_file(self, fname_value, step):
        #        meanDensity, meanSpeed, meanHamiltonian, rateWcars, rateCO2 = \
        #            self.get_mean()
        meanDensity, meanSpeed, rateWcars, rateCO2 = self.get_mean()

        data = (
            "{:d}, {:d}, {:.5e}, {:.5e}, {:.5e}, {:.5e}, {:.5e}, {:.5e}, {:.5e}".format(
                step,
                traci.vehicle.getIDCount(),
                meanDensity,
                meanSpeed,
                self.vHamiltonian,
                self.vXSquared,
                self.vSigmaSquared,
                rateWcars,
                rateCO2,
            )
        )

        print(data)
        with open(fname_value, "a") as fl:
            fl.write(data + "\n")
