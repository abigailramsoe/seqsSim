#!/usr/bin/python
import numpy as np
import random
import copy
sites = 50
founders = 2
geno = [0, 1]
nucs = ["A", "C", "G", "T"]

ploidy = len(geno)
allele_freqs = np.random.uniform(low=0.1, high=0.9, size=(sites,))

def restore():
    return copy.deepcopy(nucs)

def get_ancestral():
    ancestral = random.choices(nucs, k=sites)
    return ancestral

def get_derived(ancestral):
    derived = []
    nucs_der = restore()
    for a in ancestral:
        nucs_der.remove(a)
        derived.append(random.choices(nucs_der)[0])
        nucs_der = restore()
    return derived


def gen_genotypes():
    ind_genotypes = {}
    for ind in range(0, founders):
        ind_genotypes[ind] = []
        for f in range(0, sites):
            freq = allele_freqs[f]
            ind_genotypes[ind].append(sum(random.choices(geno, weights=[freq,1-freq], k=2)))
    return ind_genotypes

def mate(ind1, ind2):
    print("make children")


#this isnt quite right because actually here we dont choose one
# thats sex
# we need both - two haplotypes and sim both

def geno_out(ind):
    for g in range(0, sites):
        geno = ind[g]
        print(geno)
        if geno == 1:
            geno = random.choices([0,2])[0]
            print(geno, "hello")
        if geno == 0:
            print("anc",ancestral[g])
        if geno == 2:
            print("der",derived[g])
        print("")



ind_genotypes = gen_genotypes()
ancestral = get_ancestral()
derived = get_derived(ancestral)

geno_out(ind_genotypes[0])
