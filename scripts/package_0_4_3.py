"""Package only explicit current inputs, then inspect every real archive member."""
from pathlib import Path
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/release_0_4_3.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
MODULES='__init__ __main__ agent agent_cli agent_identity cli contract engine gemini groq interface mcp_client mcp_proxy mcp_server safe_diagnostics source_guard scalar_distributions'.split()
BASE=['README.md','SPEC.md','pyproject.toml','MANIFEST.in','requirements.lock.txt','.python-version',
      'install.ps1','install.sh','gpower-clone.cmd','gpower-clone','docs/SCIPY_SOURCES.md','docs/mcp_schema.json',
      'src/independent_t/SCIPY_LICENSE.txt']
SCRIPTS=['release_0_4_3.py','measure_release_0_4_3.py','package_0_4_3.py','platform_lock.py',
         'prepare_runtime.py','public_0_4_3.py','measure_once.ps1','cli_vectors_0_4_3.py','check_scalar_0_4_3.py',
         'evaluate_agent.py','agent_eval.py']
TESTS=['tests/'+n for n in ['__init__.py','conftest.py','reference_support.py','extra_support.py','integral_support.py',
       'test_extra.py','test_integral.py','test_agent.py']]
TESTS+=['tests/spec_1_1_0/'+n for n in ['__init__.py','support.py','test_acceptance.py','test_interface.py',
       'test_mathematics.py','test_agent_offline.py','test_startup.py','test_preparation.py']]
TEST_METADATA='reports/agent_runs/20261019_162441_194101/metadata.json'
FIXTURES=['spec_reference.json','provenance.json','acceptance.feature','public_vectors.jsonl','extra_inputs.json']
CURRENT=['current_run.json','current_junit.xml','current_stdout.txt','current_stderr.txt',
         'DIFFERENTIAL_REPORT.md','differential.json','differential_fields.csv','cli_timing.json']
NEW=['vectors_before.json','vectors_after.json','vectors_comparison.json','hashes_before.json','hashes_after.json','changes.json',
     'python_matrix.json','pytest_3_12_summary.json','pytest_3_13_summary.json','pytest_3_14_summary.json',
     'pytest_3_12.xml','pytest_3_13.xml','pytest_3_14.xml','pytest_3_12.stdout.txt','pytest_3_13.stdout.txt','pytest_3_14.stdout.txt',
     'pytest_3_12.stderr.txt','pytest_3_13.stderr.txt','pytest_3_14.stderr.txt',
     'installation.json','installer_receipt.json','preparation.json','pycache_before.json',
     'timing_21.json','timing_interpretation.json','no_path.json','installed_wheel.json','installed_identity.json',
     'public25.json','mcp_tools_list.json','installed_import_proof.json','engine_provenance.json',
     'scalar_boundaries_3.12.15.json','scalar_boundaries_3.13.16.json','scalar_boundaries_3.14.8.json',
     'cli_142_before.json','cli_142_after.json','cli_142_comparison.json','user_supplied_candidate_measurement.json',
     'prior_0_4_2_preservation_before.json','prior_0_4_2_preservation_after.json','RELEASE_REPORT.md']
STAGE=e.OUT/'staging_final'

def forbidden(name):
    parts=name.lower().replace('\\','/').split('/')
    return any(p in {'experiments','history','spec_history','__pycache__','.venv','.cache','.git','.aws','decompile'} for p in parts) or any(
       'spec_questions' in p or 'spec_1_0_3' in p or p.endswith('.exe') or p.endswith('.pyc') or p.startswith('.env') for p in parts)

def build():
    assert not STAGE.exists()
    STAGE.mkdir()
    allowed=BASE+['src/independent_t/'+n+'.py' for n in MODULES]+['scripts/'+n for n in SCRIPTS]
    allowed+=['tests/fixtures/'+n for n in FIXTURES]+TESTS+[TEST_METADATA]
    allowed+=['reports/spec_1_1_0/'+n for n in CURRENT]+['reports/spec_1_1_0/release_0_4_3_20261023/'+n for n in NEW]
    for rel in allowed:
        assert not forbidden(rel),rel
        target=STAGE/rel;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/rel,target)
    raw=e.data()['contract_document']['text'].encode('utf-8')
    assert __import__('hashlib').sha256(raw).hexdigest()=='4cbcc105a31f4b202f3e9a8d2cc0e9d4a8b94933997e47e3e00965f1f67f999f'
    (STAGE/'docs').mkdir(exist_ok=True);(STAGE/'docs/CONTRACT.md').write_bytes(raw);allowed+=['docs/CONTRACT.md']
    e.write('staging_allowlist.json',dict(files={p:e.sha(STAGE/p) for p in sorted(allowed)},
      exclusions='Anything not explicitly listed, all old archives/experiments/questions/recipes, virtualenvs/caches/secrets/binaries/decompile outputs excluded without opening them.',
      test_scope='Complete current 2280-test suite, explicit support files and all required allowed fixtures, including only the expressly allowed safe agent identity metadata; no other agent log/archive.'))
    source_test()
    with zipfile.ZipFile(e.OUT/'independent-t-power-0.4.3-source.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(allowed):
            if rel in ('install.sh','gpower-clone'):
                info=zipfile.ZipInfo(rel);info.create_system=3;info.external_attr=(0o100755<<16)
                info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(STAGE/rel).read_bytes())
            else:z.write(STAGE/rel,rel)
    r=e.command('sdist_build',[sys.executable,'-I','-c','import setuptools.build_meta as b;b.build_sdist('+repr(str(e.OUT))+')'],STAGE)
    assert r['exit_code']==0,r
    # POSIX executable modes must survive the sdist, too; no content change.
    path=e.OUT/'independent_t_power-0.4.3.tar.gz'
    members=[]
    import io
    with tarfile.open(path,'r:gz') as archive:
        for m in archive.getmembers():
            payload=archive.extractfile(m).read() if m.isfile() else None
            if m.name.split('/',1)[-1] in ('install.sh','gpower-clone'):m.mode=0o755
            members.append((m,payload))
    adjusted=e.OUT/'sdist-mode-adjusted.tar.gz'
    with tarfile.open(adjusted,'w:gz') as archive:
        for m,payload in members:archive.addfile(m,io.BytesIO(payload) if payload is not None else None)
    # This newly built sdist is finalized before it is advertised, never an old release.
    os.replace(adjusted,path)
    audit()

def audit():
    expected=json.loads((e.REPORT/'staging_allowlist.json').read_text(encoding='utf-8'))['files']
    generated={'PKG-INFO','setup.cfg',*('src/independent_t_power.egg-info/'+n for n in ['PKG-INFO','SOURCES.txt','dependency_links.txt','entry_points.txt','requires.txt','top_level.txt'])}
    receipts=[]
    for p in sorted(e.OUT.iterdir()):
        if p.suffix not in ('.zip','.whl','.gz'):continue
        hashes={};modes={}
        if p.suffix in ('.zip','.whl'):
            with zipfile.ZipFile(p) as a:
                names=[n for n in a.namelist() if not n.endswith('/')];assert len(names)==len(set(names))
                for n in names:hashes[n]=__import__('hashlib').sha256(a.read(n)).hexdigest();modes[n]=a.getinfo(n).external_attr>>16
        else:
            with tarfile.open(p,'r:gz') as a:
                members=[m for m in a.getmembers() if m.isfile()];assert len(members)==len({m.name for m in members})
                for m in members:hashes[m.name]=__import__('hashlib').sha256(a.extractfile(m).read()).hexdigest();modes[m.name]=m.mode
        assert not [n for n in hashes if forbidden(n)]
        norm={n:(n.split('/',1)[1] if p.suffix=='.gz' else n) for n in hashes}
        if p.suffix=='.zip':assert set(norm.values())==set(expected)
        elif p.suffix=='.gz':assert set(norm.values())==set(expected)|generated
        else:
            assert set(norm.values())=={'independent_t/'+n+'.py' for n in MODULES}|{'independent_t/SCIPY_LICENSE.txt'}|{
                'independent_t_power-0.4.3.dist-info/'+n for n in ['METADATA','WHEEL','entry_points.txt','top_level.txt','RECORD']}
        for n,rel in norm.items():
            key='src/'+rel if p.suffix=='.whl' and rel.startswith('independent_t/') else rel
            if key in expected:assert hashes[n]==expected[key],n
            if rel in ('install.sh','gpower-clone'):assert modes[n]&0o111
        e.write(p.name+'.files.json',dict(path=str(p),files=hashes,modes=modes,count=len(hashes),forbidden_paths=[],input_hashes_verified=True))
        receipts.append(dict(path=str(p),sha256=e.sha(p),count=len(hashes),file_list_receipt=str(e.REPORT/(p.name+'.files.json'))))
    assert len(receipts)==3
    e.write('packages.json',receipts);print(json.dumps(receipts,indent=2),flush=True)
def source_test():
    env=e.clean_env();env['PYTHONPATH']=str(STAGE/'src')
    code="import pathlib,independent_t,pytest,sys;assert pathlib.Path(independent_t.__file__).is_relative_to(pathlib.Path.cwd()/'src');sys.exit(pytest.main(sys.argv[1:]))"
    result=e.command('source_package_pytest',[sys.executable,'-c',code,'tests/spec_1_1_0','-q','--tb=short',
       '-o','cache_dir='+str(e.OUT/'source-package-pytest-cache'),
       '--basetemp='+str(e.OUT/'source-package-tests'),'--junitxml='+str(e.REPORT/'source_package_pytest.xml')],STAGE,env,timeout=600)
    import xml.etree.ElementTree as ET
    cases=list(ET.parse(e.REPORT/'source_package_pytest.xml').getroot().iter('testcase'))
    failed=[x.attrib['classname']+'::'+x.attrib['name'] for x in cases if x.find('failure') is not None]
    errors=[x.attrib for x in cases if x.find('error') is not None]
    skips=[x.attrib for x in cases if x.find('skipped') is not None]
    reference=json.loads((e.REPORT/'pytest_3_14_summary.json').read_text(encoding='utf-8'))
    e.write('source_package_test_summary.json',dict(tests=len(cases),passed=len(cases)-len(failed)-len(errors)-len(skips),
        failures=len(failed),errors=len(errors),skipped=len(skips),failed_ids=failed,exit_code=result['exit_code'],
        same_failure_ids=set(failed)==set(reference['failed_ids']),module_source='staging/src, explicitly asserted'))
    assert len(cases)==2280 and len(failed)==102 and not errors and not skips
    assert set(failed)==set(reference['failed_ids']) and result['exit_code']==1
    print('Source staging: 2178/2280; same 102 failures; no missing fixture.',flush=True)

if __name__=='__main__':{'build':build,'audit':audit}[sys.argv[1]]()
