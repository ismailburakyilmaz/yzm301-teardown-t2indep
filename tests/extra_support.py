import json
import math
import numpy as np
import warnings
from statsmodels.stats.power import TTestIndPower
from tests.reference_support import FIXTURES

EXTRA = json.loads((FIXTURES/'extra_inputs.json').read_text())
SM = TTestIndPower()


def sm_power(p,n1,n2):
    # statsmodels documents positive effect_size. SPEC power is sign invariant;
    # normalize direction by abs(d), use 'larger' for one tail, never feed a
    # negative d into statsmodels' fixed 'larger' rejection region.
    return float(SM.power(abs(p['d']),n1,p['alpha'],ratio=n2/n1,
                          alternative='larger' if p['tails']==1 else 'two-sided'))


def compare_extra(p, result):
    if p['mode']=='a-priori':
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            raw_n1 = SM.solve_power(effect_size=abs(p['d']),alpha=p['alpha'],
                         power=p['power'],ratio=p['ratio'],
                         alternative='larger' if p['tails']==1 else 'two-sided')
        warning_messages = [str(w.message) for w in caught]
        failed_convergence = any('ConvergenceWarning' in w.category.__name__ for w in caught)
        n1_cont = float(np.asarray(raw_n1).item())
        total_cont = n1_cont*(1+p['ratio'])
        if not math.isfinite(total_cont):
            pw = sm_power(p,result['n1'],result['n2'])
            return dict(continuous_n1=n1_cont,continuous_total=total_cont,
                        projected_even_total=None,projected_n1=None,n_matches=False,
                        engine_power=result['actual_power'],statsmodels_power=pw,
                        power_abs_difference=abs(result['actual_power']-pw),
                        library_root_power=float('nan'),library_root_residual=float('nan'),
                        library_warnings=warning_messages,library_convergence_failed=failed_convergence)
        total_even = max(4,2*math.ceil(total_cont/2))
        expected_n1 = math.floor(total_even/(1+p['ratio'])+0.5)
        pw = sm_power(p,result['n1'],result['n2'])
        root_power = sm_power(p,n1_cont,n1_cont*p['ratio'])
        return dict(continuous_n1=n1_cont,continuous_total=total_cont,
                    projected_even_total=total_even,projected_n1=expected_n1,
                    n_matches=result['n_total']==total_even and result['n1']==expected_n1,
                    engine_power=result['actual_power'],statsmodels_power=pw,
                    power_abs_difference=abs(result['actual_power']-pw),
                    library_root_power=root_power,
                    library_root_residual=abs(root_power-p['power']),
                    library_warnings=warning_messages,library_convergence_failed=failed_convergence)
    pw = sm_power(p,p['n1'],p['n2'])
    return dict(engine_power=result['power'],statsmodels_power=pw,
                power_abs_difference=abs(result['power']-pw))


def comparison_passes(x):
    """SPEC 1.0.1 section 10: finite values, root residual and convergence."""
    finite = all(math.isfinite(v) for v in x.values() if isinstance(v,(int,float)))
    return (finite and not x.get('library_convergence_failed',False)
            and x['power_abs_difference'] <= 1e-10 and x.get('n_matches',True)
            and x.get('library_root_residual',0) <= 1e-6)
