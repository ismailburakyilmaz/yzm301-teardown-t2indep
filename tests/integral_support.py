"""Test-only conditional-normal/chi-square integral, no nct or statsmodels.

X=(Z+delta)/sqrt(V/df). Transform sqrt(V)=sqrt(df)+offset and normalize
its unscaled density over central chi-square mass 1-2e-14. Missing mass is
bounded by 2e-14. Shared dependencies: SciPy central t, chi2 quantiles,
normal ndtr, QUADPACK and (test-only) continuous brentq, not an independent
software stack and not a G*Power oracle.
"""
from functools import lru_cache
import math
import warnings
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import chi2,t

TAIL_MASS = 1e-14
QUAD_TOL = 2e-13


def log1pmx(z):
    if abs(z)<0.01:
        return math.fsum((-1 if k%2==0 else 1)*z**k/k for k in range(2,10))
    return math.log1p(z)-z


def integrate(function,lo,hi,points=()):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        output = quad(function,lo,hi,points=sorted(set(x for x in points if lo<x<hi)),
                      epsabs=QUAD_TOL,epsrel=QUAD_TOL,limit=300,full_output=1)
    if caught or len(output)!=3:
        raise ArithmeticError('integral convergence warning: '+str([str(w.message) for w in caught])+str(output[3:]))
    value,error,_ = output
    if not math.isfinite(value) or not math.isfinite(error):
        raise ArithmeticError('non-finite integral')
    return float(value),float(error)


@lru_cache(maxsize=8192)
def density_band(df):
    center = math.sqrt(df)
    lo = math.sqrt(float(chi2.ppf(TAIL_MASS,df)))-center
    hi = math.sqrt(float(chi2.isf(TAIL_MASS,df)))-center
    def shape(x):
        z = x/center
        return math.exp((df-1)*log1pmx(z)-z-0.5*df*z*z)
    mass,error = integrate(shape,lo,hi,(0,))
    return center,lo,hi,mass,error


def integral_power(tails,d,alpha,n1,n2):
    total = n1+n2
    df = total-2
    delta = abs(d)*math.sqrt(n1*n2/total)
    critical = float(t.ppf(1-alpha/tails,df))
    center,lo,hi,mass,mass_error = density_band(df)
    def weighted(x):
        z = x/center
        density = math.exp((df-1)*log1pmx(z)-z-0.5*df*z*z)
        threshold = critical*(1+z)
        conditional = float(ndtr(delta-threshold))
        if tails==2:
            conditional += float(ndtr(-delta-threshold))
        return conditional*density
    points = [0.0]
    if critical!=0:
        for sign in (-1,1):
            for width in (-8,0,8):
                points.append(center*((sign*delta+width)/critical-1))
    value,error = integrate(weighted,lo,hi,points)
    retained_mass = 1-2*TAIL_MASS
    power = retained_mass*value/mass
    estimated = retained_mass*(error/mass+abs(value)*mass_error/(mass*mass))+2*TAIL_MASS
    return dict(power=power,estimated_abs_error=estimated,truncated_tail_mass_bound=2*TAIL_MASS)


def compare_integral(p,result):
    highest_error = 0.0
    def power_at(n1,n2):
        nonlocal highest_error
        r = integral_power(p['tails'],p['d'],p['alpha'],n1,n2)
        highest_error = max(highest_error,r['estimated_abs_error'])
        return r['power']
    row = {}
    if p['mode']=='a-priori':
        def continuous(total):
            return power_at(total/(1+p['ratio']),total*p['ratio']/(1+p['ratio']))
        minimum_power = continuous(4)
        if p['power']==p['alpha'] or minimum_power>=p['power']:
            root = 4.0
            row.update(root_status='minimum_N4_policy_boundary',root_converged=None,
                       root_power=minimum_power,root_residual=None,minimum_power_margin=minimum_power-p['power'])
        else:
            high = 8.0
            while continuous(high)<p['power']:
                high *= 2
                if high>1e18:
                    raise ArithmeticError('independent bracket unresolved')
            root,info = brentq(lambda n:continuous(n)-p['power'],4,high,xtol=1e-8,rtol=1e-15,full_output=True)
            root = float(root)
            root_power = continuous(root)
            row.update(root_status='continuous_root',root_converged=bool(info.converged),
                       root_power=root_power,root_residual=abs(root_power-p['power']))
        even = max(4,2*math.ceil(root/2))
        projected_n1 = math.floor(even/(1+p['ratio'])+0.5)
        row.update(continuous_total=root,projected_even_total=even,projected_n1=projected_n1,
                   projected_n2=even-projected_n1,
                   n_matches=(even,projected_n1,even-projected_n1)==(result['n_total'],result['n1'],result['n2']))
        check = power_at(result['n1'],result['n2'])
        engine = result['actual_power']
    else:
        check = power_at(p['n1'],p['n2'])
        engine = result['power']
    row.update(integral_power=check,engine_power=engine,power_abs_difference=abs(check-engine),
               maximum_estimated_abs_error=highest_error,convergence_warnings=[],
               passed=(abs(check-engine)<=1e-10 and row.get('n_matches',True) and highest_error<=1e-11
                       and row.get('root_converged') is not False
                       and (row.get('root_residual') is None or math.isfinite(row['root_residual']) and row['root_residual']<=1e-6)))
    return row
