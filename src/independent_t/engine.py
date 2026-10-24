"""RULE-006..013: distributions only from SciPy; integer search is local.

No terminal, oracle fixtures, reference IDs, MCP, or LLM dependency.
"""
import math
from .scalar_distributions import nct, t
from .contract import validate_values


class NumericalError(ArithmeticError):
    pass


def _cdf(x,df,delta):
    value = float(nct.cdf(x,df,delta))
    if not math.isfinite(value):
        # SF = 1-CDF (SciPy API). Some Boost extreme lower-tail calls produce
        # NaN while the complementary SF is finite; use the same distribution.
        value = 1-float(nct.sf(x,df,delta))
    return value


def _sf(x,df,delta):
    value = float(nct.sf(x,df,delta))
    if not math.isfinite(value):
        value = 1-float(nct.cdf(x,df,delta))
    return value


def distribution_result(tails, d, alpha, n1, n2):
    """Also accepts continuous allocations privately for RULE-010 search."""
    total = n1+n2
    df = total-2
    delta = d*math.sqrt(n1*n2/total)
    sign = -1 if d < 0 else 1
    critical = sign*float(t.ppf(1-alpha/tails,df))
    if tails == 1 and alpha == 0.5:
        # RULE-008: the numerical median residual is displayed positively,
        # including negative d. No reference values or fitted coefficients.
        critical = abs(critical)
    if delta == 0:
        achieved = alpha
    elif tails == 1:
        achieved = (_sf(critical,df,delta) if sign == 1
                    else _cdf(critical,df,delta))
    else:
        threshold = abs(critical)
        achieved = _sf(threshold,df,delta) + _cdf(-threshold,df,delta)
    if not all(math.isfinite(x) for x in (critical,delta,achieved)):
        raise NumericalError('non-finite distribution result')
    return {'power':achieved,'critical':critical,'df':df,'ncp':delta}


def continuous_power(total, tails, d, alpha, ratio):
    n1 = total/(1+ratio)
    n2 = total*ratio/(1+ratio)
    return distribution_result(tails,d,alpha,n1,n2)['power']


def required_total(tails, d, alpha, power, ratio):
    """Bracket and bisect pair count; smallest qualifying even N >= 4.

    Integer endpoints terminate exactly, without a relative N tolerance.
    RULE-010 is an observed generalization, not a claim about G*Power internals.
    """
    def reaches(pairs):
        return continuous_power(2*pairs,tails,d,alpha,ratio) >= power
    if power == alpha or reaches(2):
        return 4
    low, high = 2,4
    for _ in range(128):
        if reaches(high):
            break
        low,high = high,2*high
    else:
        raise NumericalError('sample-size bracket not found')
    while high-low > 1:
        mid = (high+low)//2
        if reaches(mid):
            high = mid
        else:
            low = mid
    return 2*high


def calculate(**parameters):
    validate_values(parameters)
    p = parameters
    if p['mode'] == 'post-hoc':
        return distribution_result(p['tails'],p['d'],p['alpha'],p['n1'],p['n2'])
    total = required_total(p['tails'],p['d'],p['alpha'],p['power'],p['ratio'])
    n1 = math.floor(total/(1+p['ratio'])+0.5)
    n2 = total-n1
    r = distribution_result(p['tails'],p['d'],p['alpha'],n1,n2)
    return {'n1':n1,'n2':n2,'n_total':total,'actual_power':r['power'],
            'critical':r['critical'],'df':total-2,'ncp':r['ncp']}
