"""Compare actual stdout/stderr/exit for all 142 CLI vectors, separate from timing."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('e',ROOT/'scripts/release_0_4_3.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)

def run(phase):
    if phase=='before':venv=ROOT/'deliverables/release_0_4_2_20261023/runtime_prepared/.venv'
    else:venv=e.OUT/'runtime_final/.venv'
    cli=venv/'Scripts/gpower-clone.exe'
    assert cli.is_file()
    cwd=Path(tempfile.mkdtemp(prefix='gpower043-cli-vectors-'))
    env=e.clean_env()
    def one(pair):
        i,v=pair
        p=subprocess.run([str(cli),*v['cli_argv']],cwd=cwd,env=env,capture_output=True,timeout=120)
        return dict(id=v['id'],argv=v['cli_argv'],exit_code=p.returncode,
          stdout=p.stdout.decode('ascii'),stderr=p.stderr.decode('utf-8',errors='replace'),
          stdout_hex=p.stdout.hex(),stderr_hex=p.stderr.hex())
    # Throughput check, not a performance benchmark. Every call is a real process.
    with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(one,enumerate(e.data()['vectors'])))
    assert len(rows)==142
    e.write('cli_142_'+phase+'.json',dict(launcher=str(cli),engine_sha256=e.sha(venv/'Lib/site-packages/independent_t/engine.py'),
       scope='142 actual executable processes, four workers; not timing evidence',rows=rows))
    if phase=='after':
        old=json.loads((e.REPORT/'cli_142_before.json').read_text(encoding='utf-8'))['rows']
        changed=[a['id'] for a,b in zip(old,rows) if a!=b]
        e.write('cli_142_comparison.json',dict(total=142,exact_stdout_stderr_exit_equal=142-len(changed),changed_ids=changed,
           byte_hex_compared=True,official_success=120,official_rejections=22,no_accuracy_gain_claim=True))
        assert not changed,changed
    print(phase,': 142 actual CLI outputs recorded.',flush=True)
if __name__=='__main__':run(sys.argv[1])
