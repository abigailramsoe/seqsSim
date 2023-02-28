#!/usr/bin/python
import sys

invariable = 1000
variable = 100000

c = 1001
for v in range(0,variable):
    print("reference_genome\t", c+v)
    c += 1000
