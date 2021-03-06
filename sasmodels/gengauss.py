#!/usr/bin/env python
from __future__ import division, print_function

import sys

import numpy as np
from numpy.polynomial.legendre import leggauss

def gengauss(n, path):
    z, w = leggauss(n)

    # Make sure array size is a multiple of 4
    if n%4:
        array_size = n + (4 - n%4)
        z, w = [np.hstack((v, [0.]*(4-n%4))) for v in (z, w)]
    else:
        array_size = n

    with open(path, "w") as fid:
        fid.write("""\
// Generated by sasmodels.gengauss.gengauss(%d)

#ifdef GAUSS_N
# undef GAUSS_N
# undef GAUSS_Z
# undef GAUSS_W
#endif
#define GAUSS_N %d
#define GAUSS_Z Gauss%dZ
#define GAUSS_W Gauss%dWt

"""%(n, n, n, n))

        if array_size != n:
            fid.write("// Note: using array size %d so that it is a multiple of 4\n\n"%array_size)

        fid.write("constant double Gauss%dWt[%d]={\n"%(n, array_size))
        fid.write(",\n".join("\t% .15e"%v for v in w))
        fid.write("\n};\n")

        fid.write("constant double Gauss%dZ[%d]={\n"%(n, array_size))
        fid.write(",\n".join("\t% .15e"%v for v in z))
        fid.write("\n};")
