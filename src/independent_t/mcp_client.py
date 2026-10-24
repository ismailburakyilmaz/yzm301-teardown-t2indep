"""Real SDK client: starts a distinct server process over stdio."""
from contextlib import asynccontextmanager
from pathlib import Path
import os
import sys
from mcp import Client, StdioServerParameters


@asynccontextmanager
async def connect(python=None,trace_path=None):
    # Forward only what the local server needs, never credentials.
    source = str(Path(__file__).resolve().parents[1])
    env = {'PYTHONPATH':source,'PYTHONIOENCODING':'utf-8'}
    for name in ('SYSTEMROOT','WINDIR','TEMP','TMP'):
        if os.environ.get(name):
            env[name] = os.environ[name]
    args = (['-m','independent_t.mcp_proxy','--trace',str(trace_path)] if trace_path
            else ['-m','independent_t.mcp_server'])
    params = StdioServerParameters(command=python or sys.executable,args=args,env=env)
    async with Client(params,read_timeout_seconds=60,mode='legacy') as client:
        yield client
