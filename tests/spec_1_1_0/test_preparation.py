"""Preparation must execute once, retain evidence, and reject faulty CLI outcomes."""
import json
from pathlib import Path
import py_compile
import sys
import pytest
from scripts.prepare_runtime import EXPECTED,prepare

def fake_cli(tmp_path,payload,code):
    script=tmp_path/'cli_double.py'
    counter=tmp_path/'calls.txt'
    script.write_text('from pathlib import Path\nimport sys\np=Path('+repr(str(counter))+')\np.write_text(p.read_text()+"1" if p.exists() else "1")\nprint('+repr(payload)+')\nsys.exit('+str(code)+')\n',encoding='utf-8')
    return [sys.executable,str(script)],counter

def test_preparation_is_one_call_with_before_cache_evidence(tmp_path):
    site=tmp_path/'site-packages';source=site/'scipy/__init__.py'
    source.parent.mkdir(parents=True);source.write_text('# cache fixture only\n',encoding='utf-8')
    py_compile.compile(str(source),doraise=True)
    command,counter=fake_cli(tmp_path,json.dumps(EXPECTED),0)
    r=prepare(command,site,tmp_path/'receipt.json',tmp_path/'probe.json')
    assert r['success'] and counter.read_text()=='1'
    assert r['pycache_before']['pyc_count']==1
    assert r['pycache_before']['samples']['__init__.py']['header_matches_source']
    assert r['first_numerical_call_in_installation'] and r['exit_code']==0
    assert r['elapsed_seconds']>=0 and json.loads(r['stdout'])==EXPECTED

@pytest.mark.parametrize('payload,exit_code',[
    (json.dumps({**EXPECTED,'n1':104}),0),
    (json.dumps(EXPECTED),1),
    (json.dumps({**EXPECTED,'actual_power':float('nan')}),0),
    ('not JSON',0),
])
def test_bad_preparation_is_failure_and_retains_actual_process_evidence(tmp_path,payload,exit_code):
    command,counter=fake_cli(tmp_path,payload,exit_code)
    r=prepare(command,tmp_path/'site',tmp_path/'receipt.json',tmp_path/'probe.json')
    assert not r['success'] and r['validation_errors'] and counter.read_text()=='1'
    assert r['exit_code']==exit_code and r['stdout'].strip()==payload
    assert json.loads((tmp_path/'receipt.json').read_text(encoding='utf-8'))['success'] is False
