"""BOM-free ASCII JSON: 0 success, 2 invalid input, 1 internal failure."""
import json
import sys
import warnings
from .interface import execute


def run(argv):
    return execute(argv,argv=True)


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('default')  # Python warnings go to stderr.
        code,result = run(sys.argv[1:])
    line=json.dumps(result,ensure_ascii=True,allow_nan=False,separators=(',',':'))+'\n'
    if hasattr(sys.stdout,'buffer'):
        sys.stdout.buffer.write(line.encode('ascii'))
        sys.stdout.buffer.flush()
    else:
        sys.stdout.write(line)
    return code
