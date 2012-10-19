try:
    import rpy2.robjects.numpy2ri
    from rpy2.robjects import r as r
    from rpy2 import rinterface
except ImportError:
    pass

import numpy as np
import scipy as sp
import sys, pickle, pdb
import scipy.stats as st
import scipy.interpolate
from numba import double
from numba.decorators import jit as jit
from numba.decorators import autojit as autojit


def R_qvalues(pv):
    rinterface.set_writeconsole(None)
    r.library("qvalue")
    bench = r("qvalue")
    
    results = bench(pv)
    pi0 = results[1]
    qv = np.array(results[2]) 

    return qv, pi0 


def estimate(pv):
    m = None, verbose = False, lowmem = False, pi0 = None
    assert(pv.min() >= 0 and pv.max() <= 1), "p-values should be between 0 and 1"

    original_shape = pv.shape
    pv = pv.ravel() # flattens the array in place, more efficient than flatten() 

    if m == None:
        m = float(len(pv))
    else:
        # the user has supplied an m
        m *= 1.0

    # if the number of hypotheses is small, just set pi0 to 1
    if len(pv) < 100 and pi0 == None:
        pi0 = 1.0
    elif pi0 != None:
        pi0 = pi0
    else:
        # evaluate pi0 for different lambdas
        pi0 = []
        lam = sp.arange(0, 0.90, 0.01)
        counts = sp.array([(pv > i).sum() for i in sp.arange(0, 0.9, 0.01)])
        
        for l in range(len(lam)):
            pi0.append(counts[l]/(m*(1-lam[l])))

        pi0 = sp.array(pi0)

        # fit natural cubic spline
        tck = sp.interpolate.splrep(lam, pi0, k = 3)
        pi0 = sp.interpolate.splev(lam[-1], tck)
        
        if pi0 > 1:
            if verbose:
                print("got pi0 > 1 (%.3f) while estimating qvalues, setting it to 1" % pi0)
            
            pi0 = 1.0

    assert(pi0 >= 0 and pi0 <= 1), "pi0 is not between 0 and 1: %f" % pi0


    if lowmem:
        # low memory version, only uses 1 pv and 1 qv matrices
        qv = sp.zeros((len(pv),))
        last_pv = pv.argmax()
        qv[last_pv] = (pi0*pv[last_pv]*m)/float(m)
        pv[last_pv] = -sp.inf
        prev_qv = last_pv
        for i in xrange(int(len(pv))-2, -1, -1):
            cur_max = pv.argmax()
            qv_i = (pi0*m*pv[cur_max]/float(i+1))
            pv[cur_max] = -sp.inf
            qv_i1 = prev_qv
            qv[cur_max] = min(qv_i, qv_i1)
            prev_qv = qv[cur_max]

    else:
        p_ordered = sp.argsort(pv)    
        pv = pv[p_ordered]
        qv = pi0 * m/len(pv) * pv
        qv[-1] = min(qv[-1],1.0)

        for i in xrange(len(pv)-2, -1, -1):
            qv[i] = min(pi0*m*pv[i]/(i+1.0), qv[i+1])

        # reorder qvalues
        qv_temp = qv.copy()
        qv = sp.zeros_like(qv)
        qv[p_ordered] = qv_temp

        # reshape qvalues
        qv = qv.reshape(original_shape)
        
    return qv

#fast_estimate = jit(restype=double[:,:], argtypes=[double[:,:]])(estimate)