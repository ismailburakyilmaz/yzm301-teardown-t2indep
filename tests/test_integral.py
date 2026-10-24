"""Additional mathematical checks, separate from unchanged native statsmodels."""
import itertools
import pytest
from scipy import special
from scipy.stats import nct
from independent_t.engine import calculate
from tests.extra_support import EXTRA
from tests.integral_support import compare_integral,integral_power


@pytest.mark.parametrize('case',EXTRA['vectors'],ids=lambda c:c['id'])
def test_conditional_normal_integral_and_separate_continuous_root(case):
    p = case['parameters']
    result = compare_integral(p,calculate(**p))
    assert result['passed'],result


ZERO_CONTROLS = list(itertools.product((1,2,10,38,100,10000,100000000,247276887662),
                                      (1e-7,.05,.5,.75,.9999999),(1,2)))


@pytest.mark.parametrize('df,alpha,tails',ZERO_CONTROLS)
def test_integral_zero_effect_identity_across_tail_boundaries(df,alpha,tails):
    # Mathematical kernel check. Large df here is not a post-hoc CLI claim.
    result = integral_power(tails,0,alpha,1,df+1)
    assert abs(result['power']-alpha)<=1e-10,result
    assert result['estimated_abs_error']<=1e-11,result


def test_integral_has_no_noncentral_t_cdf_or_statsmodels_fallback(monkeypatch):
    def forbidden(*args,**kwargs):
        pytest.fail('integral must not use noncentral-t CDF/SF')
    monkeypatch.setattr(nct,'cdf',forbidden)
    monkeypatch.setattr(nct,'sf',forbidden)
    monkeypatch.setattr(special,'nctdtr',forbidden)
    result = integral_power(2,.7,.025,40,80)
    assert 0<result['power']<1 and result['estimated_abs_error']<=1e-11
