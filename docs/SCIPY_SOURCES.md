# SciPy scalar adapter — source and license record

0.4.3 uses the existing SciPy 1.16.3 dependency through a scalar-only adapter.
Source of behavior is the public tagged SciPy source, not binary inspection,
Ghidra, an earlier candidate implementation, or a 1.0.3 recipe.

- [SciPy 1.16.3 _continuous_distns.py](https://github.com/scipy/scipy/blob/v1.16.3/scipy/stats/_continuous_distns.py):
  nct_gen._argcheck, _cdf, _sf and t_gen._ppf.
- [SciPy 1.16.3 _distn_infrastructure.py](https://github.com/scipy/scipy/blob/v1.16.3/scipy/stats/_distn_infrastructure.py):
  scalar validity, NaN/support endpoints and quantile endpoints in cdf/sf/ppf.
- [SciPy 1.16.3 license](https://github.com/scipy/scipy/blob/v1.16.3/LICENSE.txt):
  BSD-3-Clause, copyright Enthought/SciPy Developers; full notice is retained
  in src/independent_t/SCIPY_LICENSE.txt and packaged in the wheel.

The implementation calls special.nctdtr(df,nc,x), special.stdtrit(df,q),
and special._ufuncs._nct_sf(x,df,nc). The SF path keeps NumPy over='ignore'
and clipping to [0,1]; it does not substitute 1-CDF. For df>0 and non-NaN nc,
infinite x uses the same support endpoints; invalid arguments return NaN.
The adapter is scalar-only, loc=0/scale=1; it is not a replacement for the
array/loc/scale API of scipy.stats.

_nct_sf is a **private API**. Only scipy==1.16.3 is supported; a module guard
rejects another version. Upgrading SciPy requires new source review and
boundary/142-vector/full-suite checks. Pinning alone is not a promise that a
private symbol will exist in future versions. Production calculations do not
import scipy.stats; tests may import it as the comparison reference.

The distribution backend is the same installed SciPy implementation. No new
N solver, allocation, rounding, numerical tuning, reference table or oracle
branch is introduced. Existing engine NaN-complement fallbacks remain unchanged.
BSD notice retention is a source-license requirement, not a G*Power license
or an endorsement by SciPy/G*Power authors. No SciPy binary is vendored here.
