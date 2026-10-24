"""Real installed 0.4.3 CLI/MCP equivalence after the timing series is complete."""
from pathlib import Path
import asyncio
import importlib.util
import json
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('evidence',ROOT/'scripts/release_0_4_3.py')
e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
venv=e.OUT/'runtime_final/.venv';python=venv/'Scripts/python.exe';cli=venv/'Scripts/gpower-clone.exe'
sys.path.insert(0,str(venv/'Lib/site-packages'))
from mcp import Client,StdioServerParameters
async def run():
    env=e.clean_env();env.pop('PYTHONDONTWRITEBYTECODE',None)
    cwd=Path(tempfile.mkdtemp(prefix='gpower042-public-'))
    rows=[]
    params=StdioServerParameters(command=str(python),args=['-I','-m','independent_t.mcp_server'],env={k:env[k] for k in ('SYSTEMROOT','WINDIR','TEMP','TMP') if k in env})
    async with Client(params,read_timeout_seconds=60,mode='legacy') as client:
        tools=await client.list_tools()
        assert len(tools.tools)==1 and tools.tools[0].name=='power_analysis'
        tool=tools.tools[0]
        schema=dict(tool=tool.name,description=tool.description,inputSchema=tool.input_schema,outputSchema=tool.output_schema)
        old_hash=e.sha(ROOT/'docs/mcp_schema.json')
        (ROOT/'docs/mcp_schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        e.write('mcp_tools_list.json',dict(source='Actual installed 0.4.3 tools/list response',schema=schema,
          previous_doc_sha256=old_hash,current_doc_sha256=e.sha(ROOT/'docs/mcp_schema.json'),server_behavior_changed=False))
        for i,case in enumerate(e.data()['public_vector_cli_mcp_cases']):
            p=case['input'];argv=[x for k,v in p.items() for x in ('--'+k,str(v))]
            r=e.command('public_cli_'+str(i+1).zfill(2),[cli,*argv],cwd,env)
            response=await client.call_tool('power_analysis',p);text=json.loads(response.content[0].text)
            assert text==response.structured_content==json.loads(r['stdout'])
            assert response.is_error==(r['exit_code']!=0)
            rows.append(dict(id=case.get('id',i+1),input=p,cli=r,mcp=text,is_error=response.is_error,equal=True))
    assert len(rows)==25 and sum(r['cli']['exit_code']==0 for r in rows)==2
    e.write('public25.json',dict(total=25,equal=25,numeric=2,unsupported=23,rows=rows,scope='Actual installed 0.4.3 executable and separate installed stdio server; after timing series'))
    print('0.4.3 installed CLI-MCP: 25/25 equal.',flush=True)
if __name__=='__main__':asyncio.run(run())
