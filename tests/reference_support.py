"""Oracle expectations live only in tests, never in the production engine."""
import hashlib
import json
from pathlib import Path
import re
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests' / 'fixtures'
DATA = json.loads((FIXTURES / 'spec_reference.json').read_text(encoding='utf-8'))


def parameters(v):
    a = dict(zip(v['cli_argv'][::2], v['cli_argv'][1::2]))
    return {k[2:]: (value if k in ('--test', '--mode') else
                    int(value) if k in ('--tails', '--n1', '--n2') else float(value))
            for k, value in a.items()}


def matches(value, expected, rule):
    if rule['rule'] in ('exact_integer', 'exact_zero'):
        return value == expected
    # Decimal avoids cancellation in subtraction against the printed decimal.
    return abs(Decimal(str(value)) - Decimal(str(expected))) <= Decimal(str(rule['abs_tol']))


def validate_fixture():
    provenance = json.loads((FIXTURES / 'provenance.json').read_text())
    raw = (ROOT / 'SPEC.md').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == provenance['spec_sha256'], 'SPEC changed: explicit re-extraction required'
    assert hashlib.sha256((FIXTURES / 'spec_reference.json').read_bytes()).hexdigest() == provenance['reference_sha256']
    assert hashlib.sha256((FIXTURES / 'acceptance.feature').read_bytes()).hexdigest() == provenance['gherkin_sha256']
    assert DATA['schema_version'] in (2,3) and DATA['template_only'] is False
    vectors = DATA['vectors']
    assert len(vectors) >= 30
    if DATA['schema_version']==3:
        total,ap,ph=(DATA['counts'][k] for k in ('gui_vectors','gui_ap','gui_ph'))
        assert (total,ap,ph)==(142,97,45)
        assert {v['id'] for v in vectors[:87]}==({f'GP-AP-{i:03}' for i in range(1,52)}|{f'GP-PH-{i:03}' for i in range(1,37)})
    else:
        section9=raw.decode('utf-8-sig').split('## 9. Gömülü referans veri',1)[1]
        declared=re.search(r'\*\*(\d+) geçerli vektörü\*\* \((\d+) a-priori, (\d+) post-hoc',section9)
        total,ap,ph=map(int,declared.groups())
        assert {v['id'] for v in vectors} == ({f'GP-AP-{i:03}' for i in range(1,ap+1)} | {f'GP-PH-{i:03}' for i in range(1,ph+1)})
    assert len(vectors) == len({v['id'] for v in vectors}) == total == ap+ph
    assert sum(v['mode'] == 'a-priori' for v in vectors) == ap
    assert sum(v['mode'] == 'post-hoc' for v in vectors) == ph
    for v in vectors:
        assert v['test'] == 't2-indep' and v['counts_in_success_rate'] is True
        fields = ({'n1','n2','n_total','actual_power','critical','df','ncp'} if v['mode'] == 'a-priori'
                  else {'power','critical','df','ncp'})
        assert set(v['expected']) == set(v['displayed']) == set(v['comparison']) == fields
        p = parameters(v)
        assert p['test'] == v['test'] and p['mode'] == v['mode'] and p['tails'] in (1,2)
        for field, comp in v['comparison'].items():
            shown = v['displayed'][field]
            assert Decimal(shown) == Decimal(str(v['expected'][field]))
            if field in ('n1','n2','n_total','df'):
                assert comp['rule'] == 'exact_integer'
            elif shown == '0':
                assert comp['rule'] == 'exact_zero'
            else:
                assert comp['rule'] in ('displayed_decimals', 'displayed_significant_scientific')
                unit = Decimal(10) ** Decimal(shown).as_tuple().exponent
                assert Decimal(str(comp['abs_tol'])) == unit / 2
    invalid_count=25 if DATA['schema_version']==3 else 22
    assert len(DATA['invalid']) == invalid_count
    assert len({x['id'] for x in DATA['invalid']}) == invalid_count
    for x in DATA['invalid']:
        assert x['cli_argv'] and x['expected_cli']['exit_code'] == 2
    assert len(DATA['agent_cases']) == 14
    lookup = {v['id']:v for v in vectors}
    for a in DATA['agent_cases']:
        if a['kind'] == 'core':
            v = lookup[a['reference_vector_id']]
            for f in ('n1','n2','n_total'):
                assert a['expected_'+f] == v['expected'][f]
    return {'vectors':total,'a_priori':ap,'post_hoc':ph,'invalid':invalid_count,'agent_cases':14,**provenance}


def measurement_source(metadata):
    """Validate a frozen measurement at its original fixture, never relabel it."""
    current=validate_fixture()
    if metadata['spec_sha256']==current['spec_sha256']:
        assert metadata['reference_sha256']==current['reference_sha256']
        return current
    sha=metadata['spec_sha256']
    assert re.fullmatch('[a-f0-9]{64}',sha)
    histories=list((FIXTURES/'spec_history').glob('*_'+sha))
    assert len(histories)==1, 'measurement source fixture must be preserved explicitly'
    history=histories[0]
    p=json.loads((history/'provenance.json').read_text())
    assert p['spec_sha256']==sha and p['reference_sha256']==metadata['reference_sha256']
    for name,key in [('spec_reference.json','reference_sha256'),('acceptance.feature','gherkin_sha256')]:
        assert hashlib.sha256((history/name).read_bytes()).hexdigest()==p[key]
    old=json.loads((history/'spec_reference.json').read_text(encoding='utf-8'))
    lookup={v['id']:v for v in DATA['vectors']}
    if DATA['schema_version']==3:
        # Preserve every old observation field; only official interface metadata
        # was added. Invalid expected_cli belongs to its original fixture.
        for v in old['vectors']:
            assert all(lookup[v['id']][k]==value for k,value in v.items())
        invalid={v['id']:v for v in DATA['invalid']}
        for v in old['invalid']:
            assert all(invalid[v['id']][k]==value for k,value in v.items() if k!='expected_cli')
        assert old['agent_cases']==DATA['agent_cases']
    else:
        assert all(lookup[v['id']]==v for v in old['vectors'])
        assert old['invalid']==DATA['invalid'] and old['agent_cases']==DATA['agent_cases']
    return dict(vectors=len(old['vectors']),a_priori=sum(v['mode']=='a-priori' for v in old['vectors']),
                post_hoc=sum(v['mode']=='post-hoc' for v in old['vectors']),invalid=len(old['invalid']),agent_cases=len(old['agent_cases']),**p)
