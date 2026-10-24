import asyncio,hashlib,json,os,random,subprocess,sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from independent_t.cli import run
from independent_t.interface import execute
from independent_t.engine import NumericalError
from independent_t.mcp_server import invoke,INPUT_SCHEMA,OUTPUT_SCHEMA,TOOL
from independent_t.mcp_client import connect
from .support import DATA,ROOT,parameters,official_match

BASE=parameters(DATA['vectors'][0])
PH=dict(test='t2-indep',mode='post-hoc',tails=2,d=.5,alpha=.05,n1=2,n2=2)
def argv(p):return [x for k,v in p.items() for x in ('--'+k,str(v))]

@pytest.mark.parametrize('patch,code,field',[
    ({'tails':3,'d':0},'OUT_OF_RANGE','tails'),
    ({'d':-1,'alpha':'NaN'},'INVALID_VALUE','alpha'),
    ({'d':0,'power':.03},'OUT_OF_RANGE','d'),
    ({'d':1e-6,'power':.03},'INCONSISTENT','power'),
    ({'ratio':0,'power':.03},'OUT_OF_RANGE','ratio'),
    ({'test':'t-paired','dz':.5},'UNSUPPORTED','test'),
    ({'mode':'sensitivity','n_total':30},'UNSUPPORTED','mode'),
    ({'test':'other','mode':'other','foreign':0},'UNSUPPORTED','test')])
def test_ac104_validation_phases_and_gateway(patch,code,field):
    p={**BASE,**patch};pairs=list(p.items());rng=random.Random(110)
    for _ in range(20):
        rng.shuffle(pairs);rc,out=run(argv(dict(pairs)))
        assert (rc,out['code'],out['field'])==(2,code,field)

@pytest.mark.parametrize('args,code,field',[
    ([], 'MISSING_PARAM','test'),
    (argv({k:v for k,v in BASE.items() if k!='ratio'})+['--n1','2'],'MISSING_PARAM','ratio'),
    (argv(BASE)+['--n2','2','--n1','2'],'UNKNOWN_PARAM','n2'),
    (argv(BASE)+['--n1','2','--n2','2'],'UNKNOWN_PARAM','n1'),
    (argv(BASE)+['--d','.7'],'UNKNOWN_PARAM','d'),
    (['--test','other','--mode','a-priori','--test','t2-indep'],'UNKNOWN_PARAM','test'),
    (['--test','other','--foreign','1'],'UNKNOWN_PARAM','foreign'),
    (['--test','other'],'MISSING_PARAM','mode'),
    (['--test','t2-indep','--mode'],'MISSING_PARAM','mode'),
    (['--version','--d','.5'],'UNKNOWN_PARAM','d'),
    (['--version','--version'],'UNKNOWN_PARAM','version'),
    (['--alpha=.05'],'UNKNOWN_PARAM','alpha=.05')])
def test_ac104_structure(args,code,field):
    rc,out=run(args)
    assert (rc,out['code'],out['field'])==(2,code,field)

@pytest.mark.parametrize('text,code,field',[
    ('-1',2,'n1'),('0',2,'n1'),('1',2,'n1'),('+2',0,None),
    ('2.0',2,'n1'),('2e0',2,'n1'),('NaN',2,'n1'),('Infinity',2,'n1'),('abc',2,'n1'),
    ('-'+'9'*5000,2,'n1'),('+'+'9'*5000,2,'n_total')])
def test_ac104_signed_groups(text,code,field):
    rc,out=run(argv({**PH,'n1':text}));assert rc==code
    if code:
        assert out['field']==field
        expected='INVALID_VALUE' if text in ('2.0','2e0','NaN','Infinity','abc') else 'OUT_OF_RANGE'
        assert out['code']==expected

@pytest.mark.parametrize('negative',[-1,-10**10000],ids=['minus-one','huge-negative'])
def test_later_group_format_precedes_earlier_range(negative):
    rc,out=execute({**PH,'n1':negative,'n2':1.0})
    assert (rc,out['code'],out['field'])==(2,'INVALID_VALUE','n2')
    rc,out=run(argv({**PH,'n1':'-'+'9'*5000,'n2':'2.0'}))
    assert (rc,out['code'],out['field'])==(2,'INVALID_VALUE','n2')

@pytest.mark.parametrize('n1,n2,field',[(1,1,'n1'),(2,1,'n2'),(-1,2,'n1'),(1073741824,1073741823,'n_total')])
def test_group_field_projection(n1,n2,field):
    code,out=execute({**PH,'n1':n1,'n2':n2})
    assert (code,out['code'],out['field'])==(2,'OUT_OF_RANGE',field)

def test_ac110_gateway_never_calls_motor(monkeypatch):
    def forbidden(**kw):raise AssertionError('unsupported invoked motor')
    monkeypatch.setattr('independent_t.interface.calculate',forbidden)
    for case in DATA['public_vector_cli_mcp_cases'][2:]:
        p=case['input'];code,out=run(argv(p))
        assert code==2 and out['code']=='UNSUPPORTED'
        assert invoke(p)==(True,out)

def test_ac111_injected_internal_failure(monkeypatch,capsys):
    def broken(**kw):raise NumericalError('synthetic injection')
    monkeypatch.setattr('independent_t.interface.calculate',broken)
    code,out=run(argv(BASE));assert code==1 and out['code']=='NO_SOLUTION' and out['field'] is None
    assert invoke(BASE)==(True,out)
    assert 'NumericalError' in capsys.readouterr().err

@pytest.mark.parametrize('encoding',['cp1254','cp1252','utf-16'])
@pytest.mark.parametrize('args',[['--version'],argv(BASE),argv({**BASE,'d':0})],ids=['version','success','turkish-error'])
def test_ac105_real_ascii_transport(encoding,args):
    env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),PYTHONIOENCODING=encoding,PYTHONUTF8='0')
    result=subprocess.run([sys.executable,'-m','independent_t',*args],env=env,capture_output=True)
    text=result.stdout.decode('ascii');out=json.loads(text)
    assert text.count('\n')==1 and not result.stdout.startswith(b'\xef\xbb\xbf')
    assert (result.returncode,out)==run(args)
    if 'error' in out:assert any(ord(c)>127 for c in out['error']) and '\\u' in text

def test_ac108_original_scientific_units():
    lookup={v['id']:v for v in DATA['vectors']}
    for vid,tol in [('R7-P03',5e-13),('R7-I04',5e-14),('R8-B06',5e-14),('R8-B07',5e-24),('R8-B08',5e-14)]:
        assert tol in [c.get('abs_tol') for c in lookup[vid]['comparison'].values()]

def test_ac106_ap_degenerate_groups():
    lookup={v['id']:v for v in DATA['vectors']}
    for vid in ('GP-AP-024','R6-R01','R6-R02','R8-B01','R8-B02','R8-B03','R7-T06','R7-T07'):
        v=lookup[vid];code,out=run(v['cli_argv']);assert code==0
        assert all(out[k]==v['expected'][k] for k in ('n1','n2','n_total'))

def test_ac110_112_real_public_mcp(tmp_path):
    async def check():
        async with connect(trace_path=tmp_path/'public_wire.jsonl') as client:
            tools=await client.list_tools();assert [t.name for t in tools.tools]==['power_analysis']
            Draft202012Validator.check_schema(INPUT_SCHEMA);Draft202012Validator.check_schema(OUTPUT_SCHEMA)
            for case in DATA['public_vector_cli_mcp_cases']:
                p=case['input'];code,expected=run(argv(p))
                response=await client.call_tool('power_analysis',p)
                assert response.structured_content==json.loads(response.content[0].text)==expected
                assert response.content[0].text.isascii() and response.is_error==(code!=0)
                Draft202012Validator(OUTPUT_SCHEMA).validate(expected)
                exp=case['expected_cli'];assert code==exp['exit_code']
                if code:assert (expected['code'],expected['field'])==(exp['code'],exp['field'])
                else:assert all(official_match(expected[k],e,k) for k,e in exp['expected'].items())
    asyncio.run(check())
