"""Scalar-only SciPy 1.16.3 distribution adapter; no scipy.stats import.

Mappings and scalar boundary policy follow the published SciPy 1.16.3 sources
_continuous_distns.py and _distn_infrastructure.py. See docs/SCIPY_SOURCES.md
and SCIPY_LICENSE.txt. Private _nct_sf is intentionally tied to the pinned
version; this module is not a general replacement for scipy.stats.
"""
import math
import numpy as np
import scipy
from scipy import special
from scipy.special._ufuncs import _nct_sf

if scipy.__version__ != '1.16.3':
    raise RuntimeError('Scalar distribution adapter requires scipy==1.16.3')


class _NoncentralT:
    @staticmethod
    def cdf(x, df, nc):
        x, df, nc = float(x), float(df), float(nc)
        if not df > 0 or math.isnan(nc) or math.isnan(x):
            return math.nan
        if x == -math.inf:
            return 0.0
        if x == math.inf:
            return 1.0
        return float(special.nctdtr(df, nc, x))

    @staticmethod
    def sf(x, df, nc):
        x, df, nc = float(x), float(df), float(nc)
        if not df > 0 or math.isnan(nc) or math.isnan(x):
            return math.nan
        if x == -math.inf:
            return 1.0
        if x == math.inf:
            return 0.0
        with np.errstate(over='ignore'):
            return float(np.clip(_nct_sf(x, df, nc), 0, 1))


class _StudentT:
    @staticmethod
    def ppf(q, df):
        q, df = float(q), float(df)
        if not df > 0 or math.isnan(q) or not 0 <= q <= 1:
            return math.nan
        if q == 0:
            return -math.inf
        if q == 1:
            return math.inf
        return float(special.stdtrit(df, q))


nct = _NoncentralT()
t = _StudentT()
