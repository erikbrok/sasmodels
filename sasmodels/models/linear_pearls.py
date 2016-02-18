r"""
This model provides the form factor for $N$ spherical pearls of radius $R$
linearly joined by short strings (or segment length or edge separation)
$l$ $(= A - 2R)$. $A$ is the center-to-center pearl separation distance.
The thickness of each string is assumed to be negligible.

.. figure:: img/linear_pearls_fig1.jpg


Definition
----------

The output of the scattering intensity function for the linear_pearls model
is given by (Dobrynin, 1996)

.. math::

    P(Q) = \frac{scale}{V}\left[ m_{p}^2
    \left(N+2\sum_{n-1}^{N-1}(N-n)\frac{sin(qnl)}{qnl}\right)
    \left( 3\frac{sin(qR)-qRcos(qR)}{(qr)^3}\right)^2\right]

where the mass $m_p$ is $(SLD_{pearl}-SLD_{solvent})*(volume\ of\ N\ pearls)$.
V is the total volume.

The 2D scattering intensity is the same as P(q) above,
regardless of the orientation of the q vector.

.. figure:: img/linear_pearls_1d.jpg

    1D plot using the default values (w/500 data point).

References
----------

A V Dobrynin, M Rubinstein and S P Obukhov, *Macromol.*,
29 (1996) 2974-2979

"""

from numpy import inf

name = "linear_pearls"
title = "Linear pearls model of scattering from spherical pearls."
description = """
    Calculate form factor for Pearl Necklace Model
    [Macromol. 1996, 29, 2974-2979]
    Parameters:

    sld_pearl: the SLD of the pearl spheres
    sld_solv: the SLD of the solvent
    num_pearls: number of the pearls
    radius: the radius of a pearl
    edge_separation: the length of string segment; surface to surface
    """
category = "shape:sphere"

# pylint: disable=bad-whitespace, line-too-long
#            ["name", "units", default, [lower, upper], "type", "description"],
parameters = [
    ["radius",      "Ang",       80.0, [0, inf],     "", "Radius of the pearls"],
    ["edge_sep",    "Ang",      350.0, [0, inf],     "", "Length of the string segment - surface to surface"],
    ["num_pearls",  "",           3.0, [0, inf],     "", "Number of the pearls"],
    ["pearl_sld",   "1e-6/Ang^2", 1.0, [-inf, inf],  "", "SLD of the pearl spheres"],
    ["solvent_sld", "1e-6/Ang^2", 6.3, [-inf, inf],  "", "SLD of the solvent"],
    ]
# pylint: enable=bad-whitespace, line-too-long

source = ["linear_pearls.c"]

demo = dict(scale=1.0, background=0.0,
            radius=80.0,
            edge_sep=350.0,
            num_pearls=3,
            pearl_sld=1.0,
            solvent_sld=6.3)

oldname = "LinearPearlsModel"

oldpars = dict(edge_sep='edge_separation',
               pearl_sld='sld_pearl',
               solvent_sld='sld_solv')

"""
Tests temporarily disabled, until single-double precision accuracy issue solved.

tests = [
    # Accuracy tests based on content in test/utest_model_pearlnecklace.py
    [{'radius':      20.0,
      'num_pearls':   2.0,
      'pearl_sld':    1.0,
      'solvent_sld':  6.3,
      'edge_sep':   400.0,
     }, 0.001, 185.135],

    # Additional tests with larger range of parameters
    [{'radius':     120.0,
      'num_pearls':   5.0,
      'pearl_sld':    2.0,
      'solvent_sld':  2.3,
      'edge_sep':   100.0,
     }, 0.01, 45.4984],

    [{'radius':       7.0,
      'num_pearls':   2.0,
      'pearl_sld':   10.0,
      'solvent_sld': 99.3,
      'edge_sep':    20.0,
     }, 1.0, 0.632811],
    ]
"""