"""Versioned public agent configuration hashes; no credentials or oracle inputs."""
import hashlib
import json
from pathlib import Path
from . import __version__
from .source_guard import POLICY_VERSION


def json_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def agent_identity(provider,model):
    from .agent import INSTRUCTIONS,TOOLS
    sources = {}
    for name in ('__init__.py','agent.py','source_guard.py','agent_identity.py','groq.py','gemini.py',
                 'safe_diagnostics.py','mcp_client.py','mcp_server.py','interface.py','cli.py'):
        sources[name] = hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
    config = dict(provider=provider,requested_model=model,max_output_tokens=1024,
                  automatic_retries=0,guard_policy=POLICY_VERSION,tool_schema_sha256=json_hash(TOOLS),
                  contract_version='1.0.0',mcp_tool='power_analysis',spec_version='1.1.0')
    return dict(agent_version=__version__,policy_version=POLICY_VERSION,
                prompt_sha256=hashlib.sha256(INSTRUCTIONS.encode()).hexdigest(),
                config_sha256=json_hash(config),source_sha256=json_hash(sources),
                tool_schema_sha256=json_hash(TOOLS),source_files=sources,configuration=config)
