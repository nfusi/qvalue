The only function that needs to be called is 'estimate()'. 
It will accept a numpy array of pvalues and will return a numpy array of qvalues.
For instance, given some uniform p-values:

import numpy as np 
import qvalue

pv = np.random.uniform(0.0, 1.0, size = (1000,))

it's possible to convert them in q-values by calling

qv = qvalue.estimate(pv)

estimate() also includes a memory-efficient (but not CPU-efficient) procedure for the case
when it's not possible to store both the p-values and the q-values in memory at the same time.
In addition it's possible to change the number of hypotheses tested or some parameters of the
procedure (like pi0).

We refer to the documentation (in ipython, 'qvalue.estimate?') for more informations.
