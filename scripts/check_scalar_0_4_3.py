"""Direct scalar boundary comparison to the same pinned scipy.stats, not an oracle."""
from pathlib import Path
import importlib.util
import itertools
import json
import math
import sys
import warnings
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('e',ROOT/'scripts/release_0_4_3.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
sys.path.insert(0,str(ROOT/'src'))
from independent_t.scalar_distributions import nct,t
from scipy.stats import nct as reference_nct,t as reference_t
import numpy as np
import scipy

def equal(a,b):
    return (math.isnan(a) and math.isnan(b)) or a.hex()==b.hex()

def run():
    dfs=[-math.inf,-1,0,np.nextafter(0.,1.),.5,1,2,10,208,1e12,math.inf,math.nan]
    ncs=[-math.inf,-100,-1,-0.,0,.5,20,100,math.inf,math.nan]
    xs=[-math.inf,-1e300,-100,-1,-0.,0,.5,1,100,1e300,math.inf,math.nan]
    qs=[math.nan,-math.inf,-1,-np.finfo(float).eps,-0.,0,np.nextafter(0.,1.),1e-7,.5,.95,1-np.finfo(float).eps,1,1+np.finfo(float).eps,math.inf]
    rows=[]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for method in ('cdf','sf'):
            for x,df,nc in itertools.product(xs,dfs,ncs):
                a=float(getattr(nct,method)(x,df,nc));b=float(getattr(reference_nct,method)(x,df,nc))
                rows.append(dict(method=method,input_hex=[float(v).hex() for v in (x,df,nc)],actual_hex=a.hex(),reference_hex=b.hex(),equal=equal(a,b)))
        for q,df in itertools.product(qs,dfs):
            a=float(t.ppf(q,df));b=float(reference_t.ppf(q,df))
            rows.append(dict(method='ppf',input_hex=[float(v).hex() for v in (q,df)],actual_hex=a.hex(),reference_hex=b.hex(),equal=equal(a,b)))
    failures=[r for r in rows if not r['equal']]
    # Match the pinned overflow context even when the caller asks NumPy to raise.
    with np.errstate(over='raise'):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            a=float(nct.sf(1e300,208,20));b=float(reference_nct.sf(1e300,208,20))
    assert equal(a,b)
    e.write('scalar_boundaries_'+sys.version.split()[0]+'.json',dict(python=sys.version,scipy=scipy.__version__,total=len(rows),
      equal=len(rows)-len(failures),failures=failures,rows=rows,comparison='exact float.hex or both NaN',
      no_numeric_test_expectation_changed=True,overflow_context_verified=True))
    print('Boundary comparison',sys.version.split()[0],len(rows),'cases; mismatches',len(failures),flush=True)
    assert not failures,failures[:5]
if __name__=='__main__':run()
