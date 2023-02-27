#!/usr/bin/python
import numpy as np
import random
import copy
import time
import os
import glob

sites = 100000
invariable_sites = 1000
founders = 4
geno = [0, 1]
nucs = ["A", "C", "G", "T"]
ploidy = len(geno)
last_time = time.time()
def restore():
    return copy.deepcopy(nucs)

def msg(m):
    global last_time
    this_time = time.time()
    elapsed = this_time - last_time
    print("%s - took %.5f secs" % (m, elapsed))
    last_time = this_time

def get_ancestral():
    ancestral = random.choices(nucs, k=sites)
    save_genome(ancestral, "ancestral")
    return ancestral

def get_derived(ancestral):
    derived = []
    nucs_der = restore()
    for a in ancestral:
        nucs_der.remove(a)
        derived.append(random.choices(nucs_der)[0])
        nucs_der = restore()
    save_genome(derived, "derived")
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
    child_geno = []
    for g in range(0, sites):
        this_child_geno = 0
        for ind in [ind1, ind2]:
            geno = ind[g]
            if geno == 1:
                r = np.random.randint(0,1)
                this_child_geno += r
            if geno == 0:
                this_child_geno += 0
            if geno == 2:
                this_child_geno += 1
        child_geno.append(this_child_geno)
    return child_geno


def geno_out(ind):
    f1, f2 = [], []
    for g in range(0, sites):
        geno = ind[g]
        anc = ancestral[g]
        der = derived[g]
        if geno == 0:
            f1.append(anc)
            f2.append(anc)
        if geno == 1:
            f1.append(anc)
            f2.append(der)
        if geno == 2:
            f1.append(der)
            f2.append(der)
    return f1, f2

def save_sites(f, outname):
    out = "variable_sites/" + outname + ".txt"
    with open (out, 'w') as file:
        for i in f:
            o = i + "\n"
            file.write(o)

def make_ref():
    ref = []
    for i in range(0,sites):
        random_sites = random.choices(nucs, k=invariable_sites)
        for s in random_sites:
            ref.append(s)
        ref.append("N")
    save_genome(ref, "reference_genome")

def mating_pairs(ind_genotypes):
    pairs = []
    keys = list(ind_genotypes.keys())
    while len(keys) > 1:
        r1 = random.choices(keys)[0]
        keys.remove(r1)
        r2 = random.choices(keys)[0]
        keys.remove(r2)
        pairs.append([r1,r2])

    children = {}
    for p in pairs:
        i1, i2 = p
        id = "%s_%s" % (i1, i2)
        children[id] = mate(ind_genotypes[i1], ind_genotypes[i2])
    return children

def print_sites(f, id):
    f1, f2 = geno_out(f)
    save_sites(f1, (id + ".h1"))
    save_sites(f2, (id + ".h2"))

def save_genome(fa, outname):
    out = "fasta/" + outname + ".fa"
    with open (out, 'w') as file:
        header = ">" + outname + "\n"
        file.write(header)
        file.write("".join(fa))
        file.write("\n")

def save_freq(allele_freqs):
    out = "af.txt"
    with open (out, 'w') as file:
        for i in allele_freqs:
            o = str(i) + "\n"
            file.write(o)

def remove_old():
    files = glob.glob('variable_sites/*')
    for f in files:
        os.remove(f)

allele_freqs = np.random.uniform(low=0.1, high=0.9, size=(sites,))
msg("Generated allele frequencies")

save_freq(allele_freqs)
msg("Saved frequencies")

founders = gen_genotypes()
msg("Created founders")

ancestral = get_ancestral()
msg("Generated ancestral")

derived = get_derived(ancestral)
msg("Generated derived")

children = mating_pairs(founders)
msg("Made children")

make_ref()
msg("Made invariable reference")

remove_old()
msg("Removed old stuff in site dir")

for f in founders:
    msg("Saving founder " + str(f))
    id = "founder-%i" % f
    print_sites(founders[f], id)
for c in children:
    msg("Saving child " + str(c))
    id = "child-%s" % c
    print_sites(children[c], id)
