"""One visible installed-CLI preparation call; no numerical imports/calculations here."""
from pathlib import Path
import argparse
import datetime
import importlib.util
import json
import math
import struct
import subprocess
import sys
import sysconfig
import time

EXAMPLE_ARGS=['--test','t2-indep','--mode','a-priori','--tails','2','--d','0.5',
              '--alpha','0.05','--power','0.95','--ratio','1']
EXPECTED={'n1':105,'n2':105,'n_total':210,'df':208,'ncp':3.6228441865473595,
          'critical_t':1.9714346585183504,'actual_power':0.9501287033889153}

def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def probe(site):
    scipy=site/'scipy'
    pyc=list(scipy.rglob('*.pyc')) if scipy.is_dir() else []
    caches=list(scipy.rglob('__pycache__')) if scipy.is_dir() else []
    samples={}
    for rel in ('__init__.py','stats/__init__.py','stats/_stats_py.py'):
        source=scipy/rel;cached=Path(importlib.util.cache_from_source(str(source)))
        row={'source':str(source),'pyc':str(cached),'exists':cached.is_file()}
        if source.is_file():row.update(source_mtime=int(source.stat().st_mtime),source_bytes=source.stat().st_size)
        if cached.is_file():
            with cached.open('rb') as f:header=f.read(16)
            flags=struct.unpack('<I',header[4:8])[0]
            row.update(header_hex=header.hex(),flags=flags,magic_matches=header[:4]==importlib.util.MAGIC_NUMBER,
                       pyc_mtime_ns=cached.stat().st_mtime_ns,cache_tag=sys.implementation.cache_tag)
            if not flags&1:
                stamp,size=struct.unpack('<II',header[8:16])
                row.update(header_mtime=stamp,header_source_bytes=size,
                           header_matches_source=(stamp==row.get('source_mtime') and size==row.get('source_bytes')))
        samples[rel]=row
    return dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        stage='after --compile-bytecode; before first numerical preparation call',
        site_packages=str(site),scipy=str(scipy),pyc_count=len(pyc),pycache_directory_count=len(caches),
        scipy_imported='scipy' in sys.modules,numpy_imported='numpy' in sys.modules,
        cache_tag=sys.implementation.cache_tag,python=sys.version.split()[0],samples=samples,
        scope='filesystem enumeration and selected header reads only; no import scipy/numpy')

def validate(result):
    errors=[]
    if not isinstance(result,dict):return ['stdout must decode to one JSON object']
    for name,expected in EXPECTED.items():
        value=result.get(name)
        if isinstance(expected,int):
            if type(value) is not int or value!=expected:errors.append(name+' must be exact expected integer')
        elif type(value) not in (int,float) or not math.isfinite(value):errors.append(name+' must be finite numeric')
        elif not (abs(value-expected)<=1e-6 or abs(value-expected)<=1e-6*abs(expected)):
            errors.append(name+' differs from documented example under CONTRACT absolute-or-relative 1e-6')
    return errors

def prepare(command,site,receipt_path,probe_path):
    before=probe(site);write(probe_path,before)
    start=time.perf_counter()
    process_error=None
    try:
        completed=subprocess.run([*command,*EXAMPLE_ARGS],capture_output=True,timeout=180)
        raw_stdout,raw_stderr,exit_code=completed.stdout,completed.stderr,completed.returncode
    except subprocess.TimeoutExpired as exc:
        raw_stdout,raw_stderr,exit_code=exc.stdout or b'',exc.stderr or b'',None
        process_error='Installed CLI preparation exceeded 180-second process timeout'
    except OSError as exc:
        raw_stdout,raw_stderr,exit_code=b'',str(exc).encode('utf-8'),None
        process_error='Installed CLI could not be started: '+type(exc).__name__
    elapsed=time.perf_counter()-start
    stdout=raw_stdout.decode('utf-8',errors='replace')
    stderr=raw_stderr.decode('utf-8',errors='replace')
    try:result=json.loads(stdout);errors=validate(result)
    except (ValueError,TypeError):result=None;errors=['stdout is not a single JSON result']
    if exit_code!=0:errors.insert(0,'installed CLI exit must be 0')
    if process_error:errors.insert(0,process_error)
    receipt=dict(stage='FIRST NUMERICAL CALL in this installation invocation; explicit preparation cost',
       first_numerical_call_in_installation=True,command=[*command,*EXAMPLE_ARGS],
       stdout=stdout,stderr=stderr,exit_code=exit_code,elapsed_seconds=elapsed,process_error=process_error,
       result=result,expected=EXPECTED,validation_errors=errors,success=not errors,
       numeric_validation='exact integers; CONTRACT absolute-or-relative 1e-6 for finite floats',
       timer='perf_counter from before subprocess creation through exit',
       recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
       pycache_before_file=str(probe_path),pycache_before=before,os_disk_cache_cold_claim=False,
       note='Preparation time belongs to installation cost. No <=2s guarantee, no security settings changed.')
    write(receipt_path,receipt)
    return receipt

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cli',type=Path,required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    parser.add_argument('--probe',type=Path,required=True)
    args=parser.parse_args()
    receipt=prepare([str(args.cli)],Path(sysconfig.get_paths()['purelib']),args.receipt,args.probe)
    print('Explicit installed-CLI preparation: '+str(receipt['elapsed_seconds'])+' s; exit='+str(receipt['exit_code']))
    print(receipt['stdout'].strip())
    if not receipt['success']:
        print('Preparation failed: '+'; '.join(receipt['validation_errors']),file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':raise SystemExit(main())
