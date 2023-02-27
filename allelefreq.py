#!/usr/bin/python
import numpy as np
import random

sites = 50
founders = 10
allele_freqs = np.random.uniform(low=0.1, high=0.9, size=(sites,))
geno = [0, 1]
ploidy = 2

ind_genotypes = {}

for ind in range(0, founders):
    ind_genotypes[ind] = np.zeros(shape=(sites, ploidy))
    for f in range(0, len(allele_freqs)):
        freq = allele_freqs[f]
        for p in range(0, ploidy):
            ind_genotypes[ind][f][p] = random.choices(geno, weights=[freq,1-freq], k=1)[0]

# Print
if False:
    for i in range(0, sites):
        print(allele_freqs[i], end=" ")
        for k in ind_genotypes:
            print(ind_genotypes[k][i], end=" "),
        print("")

ind_summed = {}
for ind in range(0, founders):
    ind_summed[ind] = []
    for f in range(0, len(allele_freqs)):
        ind_summed[ind].append(sum(ind_genotypes[ind][f]))

for i in range(0, sites):
    print(allele_freqs[i], end=" ")
    for k in ind_summed:
        print(ind_summed[k][i], end=" "),
    print("")
