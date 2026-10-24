import hashlib,json,os,subprocess,sys
import pytest
from independent_t.cli import run
from independent_t.engine import calculate
from .support import DATA,ROOT,parameters,matches,renamed,official_match

@pytest.mark.parametrize('v',DATA['vectors'],ids=lambda v:v['id'])
def test_ac107_strict_raw_oracle(v):
    actual=calculate(**parameters(v))
    delta={k:{'expected':e,'actual':actual.get(k),'rule':v['comparison'][k]} for k,e in v['expected'].items() if not matches(actual[k],e,v['comparison'][k])}
    assert not delta,delta

@pytest.mark.parametrize('v',DATA['vectors'],ids=lambda v:v['id'])
def test_ac101_102_official_gui_expectation(v):
    code,actual=run(v['cli_argv']);exp=v['cli_expectation']
    assert code==exp['exit_code'],actual
    assert set(exp['required_keys'])<=set(actual)
    if exp['outcome']=='success':
        expected=renamed(v['expected'])
        delta={k:{'expected':e,'actual':actual.get(k)} for k,e in expected.items() if not official_match(actual[k],e,k)}
        assert not delta,delta
    else:
        assert (actual['code'],actual['field'])==(exp['code'],exp['field'])
        assert actual['error']

@pytest.mark.parametrize('v',DATA['invalid'],ids=lambda v:v['id'])
def test_ac103_invalid(v):
    code,actual=run(v['cli_argv']);exp=v['expected_cli']
    assert code==2 and (actual.get('code'),actual.get('field'))==(exp['code'],exp['field'])
    assert actual['error']

@pytest.mark.parametrize('v',[v for v in DATA['vectors'] if v['cli_expectation']['outcome']=='success'],ids=lambda v:v['id'])
def test_ac109_alias_and_unrounded_transport(v):
    code,out=run(v['cli_argv'])
    assert code==0 and out==renamed(calculate(**parameters(v)))
    assert json.loads(json.dumps(out,allow_nan=False))==out

def test_ac105_version():
    assert run(['--version'])==(0,dict(contract_version='1.0.0',name='Takim 20 - Ismail Burak Yilmaz',engine='Python '+sys.version.split()[0]))

def test_ac115_embedded_bytes_and_engine_identity():
    for key in ('contract_document','public_vectors_document'):
        doc=DATA[key];raw=(ROOT/doc['repository_destination']).read_bytes()
        assert raw==doc['text'].encode('utf-8')
        assert hashlib.sha256(raw).hexdigest()==doc['sha256']
    # Historical 0.4.2 engine: 439e43df7464de82d192c69d87d5e3b0c1230ca953bf0645346675f91d20838c.
    # User-approved 0.4.3 change is the scalar SciPy distribution import only.
    assert hashlib.sha256((ROOT/'src/independent_t/engine.py').read_bytes()).hexdigest()=='60d856fefe398633a4561adfa6d6ec48d04cc21cb04655be6cfce2170f52bd48'
