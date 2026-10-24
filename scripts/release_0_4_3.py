"""Local 0.4.3 evidence; inputs are explicit and historical experiments stay closed."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/spec_1_1_0/release_0_4_3_20261023'
OUT = ROOT / 'deliverables/release_0_4_3_20261023'
FIXED = {'SPEC.md':'016233430d0f4337c8d1de36a51747654fea31da2448a0798e17c47217cccdbe',
 'src/independent_t/engine.py':'439e43df7464de82d192c69d87d5e3b0c1230ca953bf0645346675f91d20838c',
 'src/independent_t/contract.py':'efcfc95beab44247e76836591e5dffc74b03cd49f9459e24975cda66de3ba357',
 'requirements.lock.txt':'67a121c8de8c1d69b6599c6bb42c1c0cc6756589a9a1485b7d9fcf54dd7298a8'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name, value):
    (REPORT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def clean_env():
    env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')
    for k in ('PYTHONPATH','PYTHONHOME'): env.pop(k,None)
    return env
def command(label, argv, cwd=None, env=None, timeout=180):
    start=time.perf_counter()
    p=subprocess.run([str(x) for x in argv],cwd=cwd or ROOT,env=env or clean_env(),capture_output=True,timeout=timeout)
    r=dict(argv=[str(x) for x in argv],cwd=str(cwd or ROOT),exit_code=p.returncode,
       stdout=p.stdout.decode('utf-8',errors='replace'),stderr=p.stderr.decode('utf-8',errors='replace'),
       elapsed_seconds=time.perf_counter()-start,recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (REPORT/(label+'.stdout.txt')).write_bytes(p.stdout)
    (REPORT/(label+'.stderr.txt')).write_bytes(p.stderr)
    write(label+'.json',r)
    return r
def data(): return json.loads((ROOT/'tests/fixtures/spec_reference.json').read_text(encoding='utf-8'))
def snapshot():
    sys.path.insert(0,str(ROOT/'src'))
    from independent_t.engine import calculate
    from independent_t.cli import run
    rows=[]
    for v in data()['vectors']:
        p={k[2:]:(val if k in ('--test','--mode') else int(val) if k in ('--tails','--n1','--n2') else float(val))
           for k,val in zip(v['cli_argv'][::2],v['cli_argv'][1::2])}
        raw=calculate(**p)
        rc,cli=run(v['cli_argv'])
        rows.append(dict(id=v['id'],input=p,raw=raw,raw_float_hex={k:x.hex() for k,x in raw.items() if isinstance(x,float)},
                         cli_exit=rc,cli=cli,cli_float_hex={k:x.hex() for k,x in cli.items() if isinstance(x,float)}))
    assert len(rows)==142
    return rows
def inventory():
    result={}
    for name in ('SPEC.md','requirements.lock.txt','README.md','MANIFEST.in','pyproject.toml','install.ps1','install.sh','.python-version'):
        result[name]=sha(ROOT/name)
    for folder in ('src/independent_t','tests'):
        for p in (ROOT/folder).rglob('*'):
            rel=p.relative_to(ROOT).as_posix()
            if p.is_file() and '__pycache__' not in rel and '/spec_history/' not in rel and 'spec_1_0_3' not in rel:
                result[rel]=sha(p)
    return result
def baseline():
    REPORT.mkdir(parents=True,exist_ok=False); OUT.mkdir(parents=True,exist_ok=False)
    inv=inventory()
    for p,h in FIXED.items(): assert inv[p]==h,p
    write('hashes_before.json',inv)
    write('vectors_before.json',snapshot())
    print('Baseline: 142 raw and interface outputs recorded before changes.',flush=True)
def compare():
    current=snapshot(); write('vectors_after.json',current)
    old=json.loads((REPORT/'vectors_before.json').read_text(encoding='utf-8'))
    assert old==current,'142-vector before/after difference'
    write('vectors_comparison.json',dict(total=142,exactly_equal=142,different=0,
        official_numeric_success=sum(r['cli_exit']==0 for r in current),official_rejections=sum(r['cli_exit']==2 for r in current),
        float_hex_equal=True,meaning='Same implementation outputs; no new GPower accuracy claim'))
    print('142/142 exactly equal, including float hex and rejection payloads.',flush=True)
def full_tests():
    env=clean_env(); env['PYTHONPATH']=str(ROOT/'src')
    label=os.environ.get('GPOWER_TEST_LABEL','pytest_full')
    r=command(label,[sys.executable,'-m','pytest','tests/spec_1_1_0','-q','--tb=short',
       '--basetemp='+str(OUT/(label+'-temp')),'--junitxml='+str(REPORT/(label+'.xml'))],env=env,timeout=600)
    import xml.etree.ElementTree as ET
    cases=list(ET.parse(REPORT/(label+'.xml')).getroot().iter('testcase'))
    failed=[e.attrib['classname']+'::'+e.attrib['name'] for e in cases if e.find('failure') is not None]
    errors=[e.attrib['classname']+'::'+e.attrib['name'] for e in cases if e.find('error') is not None]
    skipped=[e.attrib['classname']+'::'+e.attrib['name'] for e in cases if e.find('skipped') is not None]
    prior=json.loads((ROOT/'reports/spec_1_1_0/current_run.json').read_text(encoding='utf-8'))
    summary_name=label+'_summary.json'
    write(summary_name,dict(tests=len(cases),passed=len(cases)-len(failed)-len(errors)-len(skipped),
        failures=len(failed),errors=len(errors),skipped=len(skipped),failed_ids=failed,error_ids=errors,skipped_ids=skipped,
        previous_tests=2280,new_tests=len(cases)-2280,same_failed_ids=set(failed)==set(prior['failed_ids']),
        exit_code=r['exit_code'],python=sys.version,command=r['argv']))
    print(json.dumps(json.loads((REPORT/summary_name).read_text()) | {'failed_ids':'see file'}),flush=True)

def same_shell():
    import tempfile
    cwd=Path(tempfile.mkdtemp(prefix='gpower041-same-shell-'))
    r=command('same_shell_install',['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'scripts/same_shell_0_4_3.ps1'],cwd,timeout=600)
    assert r['exit_code']==0,r
    assert json.loads(r['stdout'].strip().splitlines()[-1])['contract_version']=='1.0.0'
    print('Same-shell installer and bare gpower-clone --version passed.',flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['baseline','compare','full_tests','same_shell'])
    globals()[ap.parse_args().phase]()
