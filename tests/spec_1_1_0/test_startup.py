"""Fresh-interpreter checks: dependency loading and the injectable lazy surface."""
import json
import os
from pathlib import Path
import subprocess
import sys
import pytest

ROOT=Path(__file__).resolve().parents[2]
BASE=['--test','t2-indep','--mode','a-priori','--tails','2','--d','.5','--alpha','.05','--power','.95','--ratio','1']

@pytest.mark.parametrize('args,expected',[
    (['--version'],0),([],2),(BASE[:-2],2),
    (['--test','other','--mode','a-priori','--foreign','NaN'],2),
    ([*BASE[:7],'NaN',*BASE[8:]],2),
])
def test_cold_noncalculation_does_not_import_scipy(args,expected):
    # Reject an attempted import, not just presence in sys.modules afterwards.
    code='''import importlib.abc,json,sys
class NoNumerics(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in ('scipy','numpy'):
   raise AssertionError('unexpected numerical import: '+fullname)
sys.meta_path.insert(0,NoNumerics())
from independent_t.cli import run
rc,out=run(json.loads(sys.argv[1]))
assert not any(n=='scipy' or n.startswith('scipy.') or n=='independent_t.engine' for n in sys.modules)
print(json.dumps(dict(exit_code=rc,result=out)))
'''
    env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run([sys.executable,'-c',code,json.dumps(args)],env=env,cwd=ROOT,capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    assert json.loads(p.stdout)['exit_code']==expected

def test_cold_calculation_loads_engine_and_keeps_injection_surface():
    code='''import sys,json
from independent_t import interface
assert 'independent_t.engine' not in sys.modules
rc,out=interface.execute(json.loads(sys.argv[1]),argv=True)
assert rc==0 and 'independent_t.engine' in sys.modules and 'scipy' in sys.modules
assert out['n_total']==210
def broken(**kw): raise RuntimeError('test injection')
interface.calculate=broken
rc,out=interface.execute(json.loads(sys.argv[1]),argv=True)
assert rc==1 and out['code']=='NO_SOLUTION' and out['field'] is None
'''
    env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run([sys.executable,'-c',code,json.dumps(BASE)],env=env,cwd=ROOT,capture_output=True,text=True)
    assert p.returncode==0,p.stderr
