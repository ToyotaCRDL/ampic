from hybrid.reference.kerberos import KerberosSampler
import numpy as np

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

from dimod.generators import and_gate
bqm = and_gate('in1', 'in2', 'out')

sampler = EmbeddingComposite(DWaveSampler())
sampleset = sampler.sample(bqm, num_reads=1000)
print(sampleset.first.energy)


solution = KerberosSampler().sample(bqm, max_iter=10, convergence=3)
print(solution.first.energy)


def return_best_result(response):
    ene = np.Inf
    for sample, energy in response.data(['sample', 'energy']):
        if energy < ene:
            ene = energy
            best_sample = sample
    return np.array(list(best_sample.values()))


print(return_best_result(sampleset))
print(return_best_result(solution))
