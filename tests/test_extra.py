import pytest
from independent_t.engine import calculate, continuous_power, distribution_result
from independent_t.contract import InputError
from tests.reference_support import DATA, parameters
from tests.extra_support import EXTRA, compare_extra, comparison_passes


@pytest.mark.parametrize('v',EXTRA['vectors'],ids=lambda v:v['id'])
def test_statsmodels_crosscheck(v):
    p = v['parameters']
    comparison = compare_extra(p,calculate(**p))
    # This is a separate library cross-check criterion, never an oracle tolerance.
    assert comparison_passes(comparison), comparison


@pytest.mark.parametrize('v',[v for v in DATA['vectors'] if v['mode']=='a-priori'],ids=lambda v:v['id'])
def test_ap_posthoc_consistency_and_even_minimality(v):
    p = parameters(v)
    result = calculate(**p)
    n1,n2,total = result['n1'],result['n2'],result['n_total']
    ph = dict(test='t2-indep',mode='post-hoc',tails=p['tails'],d=p['d'],alpha=p['alpha'],n1=n1,n2=n2)
    if n1 >= 1 and n2 >= 1 and total <= 2147483646:
        again = calculate(**ph)
        assert again['power'] == result['actual_power']
        for field in ('df','critical','ncp'):
            assert result[field] == again[field]
    else:
        # SPEC allows AP outputs outside the post-hoc input domain; explicit error
        # is the correct adapter behavior. Internal shared distribution still agrees.
        with pytest.raises(InputError):
            calculate(**ph)
        assert distribution_result(p['tails'],p['d'],p['alpha'],n1,n2)['power'] == result['actual_power']
    assert total >= 4 and total%2 == 0
    assert continuous_power(total,p['tails'],p['d'],p['alpha'],p['ratio']) >= p['power']
    if total > 4:
        assert continuous_power(total-2,p['tails'],p['d'],p['alpha'],p['ratio']) < p['power']


@pytest.mark.parametrize('v',[v for v in EXTRA['vectors'] if v['parameters']['mode']=='post-hoc'],ids=lambda v:v['id'])
def test_posthoc_swap_and_sign(v):
    p = v['parameters']
    a = calculate(**p)
    b = calculate(**{**p,'n1':p['n2'],'n2':p['n1']})
    c = calculate(**{**p,'d':-p['d']})
    assert a == b
    assert abs(a['power']-c['power']) <= 1e-14
    assert a['ncp'] == -c['ncp']
