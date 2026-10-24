"""Explicit preparation plus the next 20 installed CLI calculations, kept separately."""
from pathlib import Path
import datetime
import importlib.util
import json
import os
import statistics
import sys
import tempfile
import winreg

ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/release_0_4_3.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
RUNTIME=e.OUT/'runtime_final'
VENV=RUNTIME/'.venv';CLI=VENV/'Scripts/gpower-clone.exe';PYTHON=VENV/'Scripts/python.exe'
ARGS=['--test','t2-indep','--mode','a-priori','--tails','2','--d','0.5','--alpha','0.05','--power','0.95','--ratio','1']

def paths():
    result={}
    for name,hive,key in [('user',winreg.HKEY_CURRENT_USER,'Environment'),('machine',winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')]:
        with winreg.OpenKey(hive,key) as h:value,kind=winreg.QueryValueEx(h,'Path')
        result[name]=dict(value=value,kind=kind)
    return result

def summarize(rows):
    times=[r['elapsed_seconds'] for r in rows]
    return dict(count=len(rows),first_seconds=times[0],second_seconds=times[1],
        max_seconds=max(times),median_seconds=statistics.median(times),over_2s=sum(t>2 for t in times))

def run():
    assert not RUNTIME.exists()
    assert (e.REPORT/'pytest_3_14_summary.json').exists(),'Finish heavy tests first'
    before=paths();env=e.clean_env();env.pop('PYTHONDONTWRITEBYTECODE',None)
    uv=ROOT/'deliverables/install_check_python314_retry/runtime/.tools/uv/uv.exe'
    cache=ROOT/'deliverables/install_check_python314_retry/runtime/.cache'
    wheel=e.OUT/'independent_t_power-0.4.3-py3-none-any.whl'
    cwd=Path(tempfile.mkdtemp(prefix='gpower042-prepared-'));assert not cwd.is_relative_to(ROOT)
    installed=e.command('installation',['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'install.ps1',
        '-Destination',RUNTIME,'-Offline','-NoPath','-UvPath',uv,'-PythonExecutable',sys.executable,
        '-WheelPath',wheel,'-CacheDirectory',cache],cwd,env,timeout=600)
    assert installed['exit_code']==0,installed
    prep=json.loads((RUNTIME/'PREPARATION_RECEIPT.json').read_text(encoding='utf-8'))
    probe=json.loads((RUNTIME/'PREPARATION_PYCACHE_BEFORE.json').read_text(encoding='utf-8'))
    assert prep['success'] and prep['exit_code']==0 and prep['first_numerical_call_in_installation']
    assert probe['pyc_count']>0 and probe['pycache_directory_count']>0 and not probe['scipy_imported'] and not probe['numpy_imported']
    e.write('preparation.json',prep);e.write('pycache_before.json',probe)
    e.write('installer_receipt.json',json.loads((RUNTIME/'INSTALLATION_RECEIPT.json').read_text(encoding='utf-8-sig')))
    rows=[]
    # No intervening numerical call or heavy job; these are calls 2..21 of this venv.
    for i in range(1,21):
        r=e.command('after_preparation_'+str(i).zfill(2),[CLI,*ARGS],cwd,env)
        actual=json.loads(r['stdout'])
        assert r['exit_code']==0 and actual==prep['result'],r
        rows.append(r|dict(post_preparation_index=i,installation_numerical_call_index=i+1))
        print('after preparation',i,round(r['elapsed_seconds'],6),flush=True)
    prep_row=dict(prep,installation_numerical_call_index=1)
    all_rows=[prep_row,*rows]
    e.write('timing_21.json',dict(preparation_is_first_numerical_call=True,
       preparation_excluded_from_post_series=True,preparation_is_installation_cost=True,
       after_preparation_20=summarize(rows),including_preparation_first_20=summarize(all_rows[:20]),
       including_preparation_all_21=summarize(all_rows),rows=all_rows,
       gap_after_preparation_note='Installer did only dependency/version/PATH receipt finalization between explicit preparation and series; no further numerical call.',
       execution_context='outside sandbox, after completed full tests; no parallel build/test deliberately launched',
       os_disk_cache_cold_claim=False,cache_or_dll_temperature_guaranteed=False,reboot_tested=False))
    after=paths();assert after==before
    receipt=json.loads((RUNTIME/'INSTALLATION_RECEIPT.json').read_text(encoding='utf-8-sig'))
    assert receipt['no_path'] and receipt['path_registration'] is None and receipt['process_path_before']==receipt['process_path_after']
    e.write('no_path.json',dict(before=before,after=after,registry_unchanged=True,process_path_unchanged=True))
    r=e.command('installed_identity',[PYTHON,'-I','-c',"import sys,json,independent_t,importlib.metadata as m;print(json.dumps(dict(prefix=sys.prefix,module=independent_t.__file__,version=m.version('independent-t-power'))))"],cwd,env)
    identity=json.loads(r['stdout']);assert identity['version']=='0.4.3' and Path(identity['prefix'])==VENV
    e.write('installed_wheel.json',dict(path=str(wheel),sha256=e.sha(wheel),identity=identity))
    print('Preparation',prep['elapsed_seconds'],'post20',summarize(rows),'all21',summarize(all_rows),flush=True)
def same_venv_shells():
    # Supplementary checks after the 21-call series, not first-ever calculations.
    assert (e.REPORT/'timing_21.json').exists()
    current=paths();env=e.clean_env();env.pop('PYTHONDONTWRITEBYTECODE',None)
    env['PATH']=winreg.ExpandEnvironmentStrings(current['machine']['value'])+';'+winreg.ExpandEnvironmentStrings(current['user']['value'])
    cwd=Path(tempfile.mkdtemp(prefix='gpower042-same-venv-shell-'))
    rows=[]
    for shell,prefix in [('powershell',['powershell.exe','-NoProfile','-Command']),('cmd',['cmd.exe','/d','/c'])]:
        for kind,args in [('version',['--version']),('calculation',ARGS)]:
            if shell=='powershell':command="& '"+str(CLI).replace("'","''")+"' "+' '.join(args)
            else:command=str(CLI)+' '+' '.join(args)
            r=e.command('same_venv_new_'+shell+'_'+kind,[*prefix,command],cwd,env)
            assert r['exit_code']==0,r
            rows.append(dict(shell=shell,kind=kind,receipt=r))
    e.write('same_venv_new_shells.json',dict(rows=rows,venv=str(VENV),
       sequence='Supplementary calls after preparation + 20, not first-ever in venv',
       full_executable_path_used=True,registered_bare_command_proof=False,
       note='Test venv remains NoPath. Registered bare-command requirement is separately proved against stable reused .run in new_shells.json.',reboot_tested=False))
    print('Same prepared venv supplementary new-shell calls recorded separately.',flush=True)

if __name__=='__main__':
    same_venv_shells() if sys.argv[1:]==['same-venv-shells'] else run()
