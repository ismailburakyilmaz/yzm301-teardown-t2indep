"""Optional transparent stdio wire recorder for reproducible local evidence."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
import threading


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trace',required=True)
    args = parser.parse_args()
    path = Path(args.trace)
    path.parent.mkdir(parents=True,exist_ok=True)
    lock = threading.Lock()
    with path.open('a',encoding='utf-8') as trace:
        def record(direction,line):
            with lock:
                trace.write(json.dumps(dict(time=datetime.now(timezone.utc).isoformat(),direction=direction,
                                            message=json.loads(line)),ensure_ascii=False)+'\n')
                trace.flush()
        child = subprocess.Popen([sys.executable,'-m','independent_t.mcp_server'],stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,stderr=sys.stderr,
                                 creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        def receive():
            for line in child.stdout:
                record('server_to_client',line)
                sys.stdout.buffer.write(line)
                sys.stdout.buffer.flush()
        reader = threading.Thread(target=receive,daemon=True)
        reader.start()
        try:
            for line in sys.stdin.buffer:
                record('client_to_server',line)
                child.stdin.write(line)
                child.stdin.flush()
        finally:
            child.stdin.close()
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
            reader.join(timeout=10)
    return child.returncode


if __name__ == '__main__':
    raise SystemExit(main())
