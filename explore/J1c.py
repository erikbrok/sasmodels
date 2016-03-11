r"""
Show numerical precision of $2 J_1(x)/x$.
"""

import numpy as np
from sympy.mpmath import mp
#import matplotlib; matplotlib.use('TkAgg')
import pylab


SHOW_DIFF = True  # True if show diff rather than function value
LINEAR_X = False  # True if q is linearly spaced instead of log spaced

def mp_J1c(vec, bits=500):
    """
    Direct calculation using sympy multiprecision library.
    """
    with mp.workprec(bits):
        return [_mp_J1c(mp.mpf(x)) for x in vec]

def _mp_J1c(x):
    """
    Helper funciton for mp_j1c
    """
    return mp.mpf(2)*mp.j1(x)/x

def np_J1c(x, dtype):
    """
    Direct calculation using scipy.
    """
    from scipy.special import j1 as J1
    x = np.asarray(x, dtype)
    return np.asarray(2, dtype)*J1(x)/x

def cephes_J1c(x, dtype, n):
    """
    Calculation using pade approximant.
    """
    f = np.float64 if np.dtype(dtype) == np.float64 else np.float32
    x = np.asarray(x, dtype)
    ans = np.empty_like(x)
    ax = abs(x)

    # Branch a
    a_idx = ax < f(8.0)
    a_xsq = x[a_idx]**2
    a_coeff1 = list(reversed((72362614232.0, -7895059235.0, 242396853.1, -2972611.439, 15704.48260, -30.16036606)))
    a_coeff2 = list(reversed((144725228442.0, 2300535178.0, 18583304.74, 99447.43394, 376.9991397, 1.0)))
    a_ans1 = np.polyval(np.asarray(a_coeff1[n:], dtype), a_xsq)
    a_ans2 = np.polyval(np.asarray(a_coeff2[n:], dtype), a_xsq)
    ans[a_idx] = f(2.0)*a_ans1/a_ans2

    # Branch b
    b_idx = ~a_idx
    b_ax = ax[b_idx]
    b_x = x[b_idx]

    b_y = f(64.0)/(b_ax**2)
    b_xx = b_ax - f(2.356194491)
    b_coeff1 = list(reversed((1.0, 0.183105e-2, -0.3516396496e-4, 0.2457520174e-5, -0.240337019e-6)))
    b_coeff2 = list(reversed((0.04687499995, -0.2002690873e-3, 0.8449199096e-5, -0.88228987e-6, 0.105787412e-6)))
    b_ans1 = np.polyval(np.asarray(b_coeff1[n:], dtype),b_y)
    b_ans2 = np.polyval(np.asarray(b_coeff2[n:], dtype), b_y)
    b_sn, b_cn = np.sin(b_xx), np.cos(b_xx)
    ans[b_idx] = np.sign(b_x)*np.sqrt(f(0.636619772)/b_ax) * (b_cn*b_ans1 - (f(8.0)/b_ax)*b_sn*b_ans2)*f(2.0)/b_x

    return ans

def div_J1c(x, dtype):
    f = np.float64 if np.dtype(dtype) == np.float64 else np.float32
    x = np.asarray(x, dtype)
    return f(2.0)*np.asarray([_J1(xi, f)/xi for xi in x], dtype)

def _J1(x, f):
    ax = abs(x)
    if ax < f(8.0):
        y = x*x
        ans1 = x*(f(72362614232.0)
                  + y*(f(-7895059235.0)
                  + y*(f(242396853.1)
                  + y*(f(-2972611.439)
                  + y*(f(15704.48260)
                  + y*(f(-30.16036606)))))))
        ans2 = (f(144725228442.0)
                  + y*(f(2300535178.0)
                  + y*(f(18583304.74)
                  + y*(f(99447.43394)
                  + y*(f(376.9991397)
                  + y)))))
        return ans1/ans2
    else:
        y = f(64.0)/(ax*ax)
        xx = ax - f(2.356194491)
        ans1 = (f(1.0)
                  + y*(f(0.183105e-2)
                  + y*(f(-0.3516396496e-4)
                  + y*(f(0.2457520174e-5)
                  + y*f(-0.240337019e-6)))))
        ans2 = (f(0.04687499995)
                  + y*(f(-0.2002690873e-3)
                  + y*(f(0.8449199096e-5)
                  + y*(f(-0.88228987e-6)
                  + y*f(0.105787412e-6)))))
        sn, cn = np.sin(xx), np.cos(xx)
        ans = np.sqrt(f(0.636619772)/ax) * (cn*ans1 - (f(8.0)/ax)*sn*ans2)
        return -ans if (x < f(0.0)) else ans

def plotdiff(x, target, actual, label):
    """
    Plot the computed value.

    Use relative error if SHOW_DIFF, otherwise just plot the value directly.
    """
    if SHOW_DIFF:
        err = np.clip(abs((target-actual)/target), 0, 1)
        pylab.loglog(x, err, '-', label=label)
    else:
        limits = np.min(target), np.max(target)
        pylab.semilogx(x, np.clip(actual,*limits),  '-', label=label)

def compare(x, precision):
    r"""
    Compare the different computation methods using the given precision.
    """
    target = np.asarray(mp_J1c(x), 'double')
    #plotdiff(x, target, mp_J1c(x, 11), 'mp 11 bits')
    plotdiff(x, target, np_J1c(x, precision), 'direct '+precision)
    plotdiff(x, target, cephes_J1c(x, precision, 0), 'cephes '+precision)
    #plotdiff(x, target, cephes_J1c(x, precision, 1), 'cephes '+precision)
    #plotdiff(x, target, div_J1c(x, precision), 'cephes 2 J1(x)/x '+precision)
    pylab.xlabel("qr (1/Ang)")
    if SHOW_DIFF:
        pylab.ylabel("relative error")
    else:
        pylab.ylabel("2 J1(x)/x")
        pylab.semilogx(x, target,  '-', label="true value")
    if LINEAR_X:
        pylab.xscale('linear')

def main():
    r"""
    Compare accuracy of different methods for computing $3 j_1(x)/x$.
    :return:
    """
    if LINEAR_X:
        qr = np.linspace(1,1000,2000)
    else:
        qr = np.logspace(-3,5,400)
    pylab.subplot(121)
    compare(qr, 'single')
    pylab.legend(loc='best')
    pylab.subplot(122)
    compare(qr, 'double')
    pylab.legend(loc='best')
    pylab.suptitle('2 J1(x)/x')

if __name__ == "__main__":
    #print "\n".join(str(x) for x in mp_J1c([1e-6,1e-5,1e-4,1e-3]))
    main()
    pylab.show()